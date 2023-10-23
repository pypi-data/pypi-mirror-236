from PIL.Image import Image
from fitz.fitz import Page, Pixmap, Document, Matrix
from qreader import QReader
import numpy as np

from qrDocumentIndexer.page_info import PageInfo

class ScannedPage:
    def __init__(self, page: Image | Page, 
                 src_doc: Document = None, 
                 src_image: str = None) -> None:
        if isinstance(page, Image):
            self._image = page
            self._src_image = src_image
        elif isinstance(page, Page):
            self._pdf_page = page
            self._src_doc = src_doc
        else:
            raise TypeError('Page type is not valid')
    
    def _scan_page_info(self):
        qreader = QReader()
        results = ()
        if hasattr(self, '_image') and self._image:
            pix_array = np.array(self._image.convert("RGB"))
            results = qreader.detect_and_decode(pix_array)
        elif hasattr(self, '_pdf_page') and self._pdf_page:
            mat = Matrix(5, 5)
            image: Pixmap = self._pdf_page.get_pixmap(matrix = mat)
            pix_array = np.frombuffer(buffer=image.samples, dtype=np.uint8).reshape((image.height, image.width, -1))
            results = qreader.detect_and_decode(pix_array)

        for code in results:
            try:
                decoded: PageInfo = PageInfo.fromJson(code)
            except:
                continue

            self._page_info: PageInfo = decoded
            return

        self._page_info: PageInfo = None

    @property
    def page_info(self) -> PageInfo:
        if not hasattr(self, '_page_info'):
            self._scan_page_info()

        return self._page_info
    
    def add_to_document(self, doc: Document):
        if hasattr(self, '_image'):
            im_doc = Document(self._src_image)
            im_doc_pdf = Document("pdf", im_doc.convert_to_pdf())
            doc.insert_pdf(im_doc_pdf, 0, 0)
        elif hasattr(self, '_pdf_page'):
            doc.insert_pdf(self._src_doc, self._pdf_page.number, self._pdf_page.number)