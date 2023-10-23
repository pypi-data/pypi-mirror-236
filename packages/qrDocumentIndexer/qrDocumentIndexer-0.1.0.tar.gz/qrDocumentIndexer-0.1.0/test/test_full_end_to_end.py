import os
from pathlib import Path

from fitz import Document

from qrDocumentIndexer.scanned_page import ScannedPage
from qrDocumentIndexer.scanned_documents import ScannedDocuments
from qrDocumentIndexer.reconstituted_document import ReconstitutedDocument, BLANK_PAGE

from .test_pdf_ingest import EXPECTED_PAGES_FOR_INGEST_DOC

THIS_DIR, _ = os.path.split(__file__)
INGEST_DOC_PATH = os.path.join(THIS_DIR, 'test_docs', 'test_reco_docs')
ORIGINAL_DOC_PATH = os.path.join(THIS_DIR, 'test_docs', 'test_ingest.pdf')


def test_end_to_end_scan(tmp_path):
    '''
        This test checks that separated page can be successfully
        scanned and reconstituted into a single file
    '''
    docs = ScannedDocuments()
    for file in os.listdir(INGEST_DOC_PATH):
        docs.add_document(os.path.join(INGEST_DOC_PATH, file))

    reco_docs: list[ReconstitutedDocument] = []

    for filename, pages in docs.pages_by_output_doc.items():
        reco_docs.append(ReconstitutedDocument(pages, filename))

    assert len(reco_docs) == 1

    tmp_path.mkdir(exist_ok=True)
    output = tmp_path / 'output.pdf'
    reco = reco_docs[0]

    reco.save_document(output.as_posix())

    out_doc = Document(output.as_posix())
    original_doc = Document(ORIGINAL_DOC_PATH)

    assert out_doc.page_count == original_doc.page_count

    as_scanned_doc = ScannedDocuments()
    as_scanned_doc.add_document(output.as_posix())

    for i, page in enumerate(as_scanned_doc.pages):
        assert page.page_info == EXPECTED_PAGES_FOR_INGEST_DOC[i]

    assert out_doc.get_toc(True) == original_doc.get_toc(True)