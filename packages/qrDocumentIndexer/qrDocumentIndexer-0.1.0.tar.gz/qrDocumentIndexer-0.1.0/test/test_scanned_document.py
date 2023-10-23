from PIL import Image

from qrDocumentIndexer.page_info import PageInfo
from qrDocumentIndexer.scanned_documents import ScannedDocuments
from qrDocumentIndexer.scanned_page import ScannedPage

from .test_scanned_page import get_path

EXPECTED_IMAGE_PAGEINFO = PageInfo('test_ingest.pdf', 1, ["Bookmark 1"])

EXPECTED_PDF_PAGEINFO = [
        PageInfo('test_ingest.pdf', 1, ['Bookmark 1']),
        PageInfo('test_ingest.pdf', 3, []),
        PageInfo('test_ingest.pdf', 5, ['Bookmark 3', 'Bookmark 3 Sub Bookmark 1'])
    ]

INFO_IMAGE = 'page_with_qr.jpg'

INCOMPLETE_PDF = 'incomplete_doc.pdf'

def test_scanned_document_produces_correct_pageinfo_for_image_with_single_page():
    doc = ScannedDocuments()
    doc.add_document(get_path(INFO_IMAGE))

    assert len(doc.pages) == 1
    assert doc.pages[0].page_info == EXPECTED_IMAGE_PAGEINFO

def test_scanned_document_produces_correct_pageinfo_for_pdf_with_multiple_pages():
    doc = ScannedDocuments()
    doc.add_document(get_path(INCOMPLETE_PDF))

    assert len(doc.pages) == 3

    for i in range(3):
        assert doc.pages[i].page_info == EXPECTED_PDF_PAGEINFO[i]

def test_adding_multiple_documents_adds_pages():
    doc = ScannedDocuments()
    doc.add_document(get_path(INCOMPLETE_PDF))
    doc.add_document(get_path(INFO_IMAGE))

    assert len(doc.pages) == 4

    for i in range(3):
        assert doc.pages[i].page_info == EXPECTED_PDF_PAGEINFO[i]
    assert doc.pages[3].page_info == EXPECTED_IMAGE_PAGEINFO

def test_pages_by_output_doc_sorts_correctly_by_filename():
    doc = ScannedDocuments()
    
    file1 = 'doc_1.pdf'
    file2 = 'doc_2.pdf'

    target_pageinfo = [
        PageInfo(file1, 1, ['Bookmark 1']),
        PageInfo(file2, 3, []),
        PageInfo(file1, 5, ['Bookmark 3', 'Bookmark 3 Sub Bookmark 1'])
    ]

    blank_image = Image.new("RGB", (100, 100))

    for pageinfo in target_pageinfo:
        page = ScannedPage(blank_image)
        page._page_info = pageinfo
        doc._pages.append(page)

    page = ScannedPage(blank_image)
    page._page_info = None
    doc._pages.append(page)

    sorted = doc.pages_by_output_doc

    assert file1 in sorted
    assert file2 in sorted
    assert None in sorted

    file1_pages = list(filter(lambda x: x.file_name == file1, target_pageinfo))
    file2_pages = list(filter(lambda x: x.file_name == file2, target_pageinfo))
    none_pages = [None]

    assert [p.page_info for p in sorted[file1]] == file1_pages
    assert [p.page_info for p in sorted[file2]] == file2_pages
    assert [p.page_info for p in sorted[None]] == none_pages





