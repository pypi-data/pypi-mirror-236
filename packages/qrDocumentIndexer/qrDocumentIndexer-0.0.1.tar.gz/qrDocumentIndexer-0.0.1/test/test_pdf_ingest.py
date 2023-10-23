import os
import pathlib
import shutil
import io

import fitz
import numpy
from qreader import QReader
from PIL import Image

from qrDocumentIndexer.pdf_ingest import PDFIngest, QR_POSITION
from qrDocumentIndexer.page_info import PageInfo

THIS_DIR, _ = os.path.split(__file__)
INGEST_FILENAME = 'test_ingest.pdf'
INGEST_DOC_PATH = os.path.join(THIS_DIR, 'test_docs', INGEST_FILENAME)

EXPECTED_PAGES_FOR_INGEST_DOC = [
        PageInfo(INGEST_FILENAME, 1, ['Bookmark 1']),
        PageInfo(INGEST_FILENAME, 2, ['Bookmark 2']),
        PageInfo(INGEST_FILENAME, 3, []),
        PageInfo(INGEST_FILENAME, 4, ['Bookmark 3']),
        PageInfo(INGEST_FILENAME, 5, ['Bookmark 3', 'Bookmark 3 Sub Bookmark 1']),
        PageInfo(INGEST_FILENAME, 6, [])
    ]

def test_extracted_pageinfos_match_document():
    ingest = PDFIngest(INGEST_DOC_PATH)

    assert ingest.page_metadata == EXPECTED_PAGES_FOR_INGEST_DOC

def test_pdf_qr_insert_has_expected_values(tmp_path : pathlib.Path):
    temp_filepath = (tmp_path / INGEST_FILENAME).as_posix()

    shutil.copyfile(INGEST_DOC_PATH, temp_filepath)

    ingest = PDFIngest(temp_filepath)
    for _ in ingest.insert_qr_codes(QR_POSITION.TOP_LEFT):
        pass

    doc = fitz.Document(temp_filepath)

    found_qrs = []

    qreader = QReader()

    for page in doc:
        pix: fitz.Pixmap = page.get_pixmap(dpi=300)
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        temp_image = tmp_path / 'image.png'
        img.save(temp_image)
        result = qreader.detect_and_decode(numpy.array(img))
        str_data :str = result[0]
        found_page_info = PageInfo.fromJson(str_data)
        found_qrs.append(found_page_info)

    assert found_qrs == EXPECTED_PAGES_FOR_INGEST_DOC

