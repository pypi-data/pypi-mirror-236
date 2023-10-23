import os

from PIL import Image
from qrDocumentIndexer.page_info import PageInfo
from qrDocumentIndexer.scanned_page import ScannedPage
from fitz import Document

EXPECTED_PAGEINFO = PageInfo('test_ingest.pdf', 1, ["Bookmark 1"])

THIS_DIR, _ = os.path.split(__file__)

NO_INFO_IMAGES = ['invalid_qr.jpg', 'page_without_qr.jpg']
INFO_IMAGES = ['page_with_qr.jpg']

NO_INFO_PDFS = ['invalid_qr.pdf', 'page_without_qr.pdf']
INFO_PDFS = ['page_with_qr.pdf']

def get_path(filename: str) -> str:
    return os.path.join(THIS_DIR, 'test_docs', 'test_scan_docs', filename)

def test_page_images_no_valid_qr():
    for image in NO_INFO_IMAGES:
        path = get_path(image)
        loaded_image = Image.open(path)
        page = ScannedPage(loaded_image)
        
        assert page.page_info is None

def test_page_images_valid_qr():
    for image in INFO_IMAGES:
        path = get_path(image)
        loaded_image = Image.open(path)
        page = ScannedPage(loaded_image)
        
        assert page.page_info == EXPECTED_PAGEINFO

def test_page_pdf_no_valid_qr():
    for pdf in NO_INFO_PDFS:
        path = get_path(pdf)
        doc = Document(path)
        pdf_page = doc.load_page(0)
        page = ScannedPage(pdf_page)

        assert page.page_info is None

def test_page_pdf_valid_qr():
    for pdf in INFO_PDFS:
        path = get_path(pdf)
        doc = Document(path)
        pdf_page = doc.load_page(0)
        page = ScannedPage(pdf_page)

        assert page.page_info == EXPECTED_PAGEINFO