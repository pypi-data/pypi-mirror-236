import io
import os
from enum import Enum

import fitz
import qrcode

from qrDocumentIndexer.page_info import PageInfo

class _PDFBookmark:
    def __init__(self, bookmark: list):
        self.lvl: int = bookmark[0]
        self.title: str = bookmark[1]
        self.page: int = bookmark[2]
        self.heirarchy: list(str) = [self.title]

class QR_POSITION(Enum):
    TOP_LEFT = "Top Left"
    TOP_RIGHT = "Top Right"
    BOTTOM_LEFT = "Bottom Left"
    BOTTOM_RIGHT = "Bottom Right"

    def __str__(self):
        return self.value

class PDFIngest:
    def __init__(self, filepath: str):
        self.page_metadata = []

        self.doc = fitz.Document(filepath)
        self.filepath = filepath

        _, filename = os.path.split(filepath)

        # Get all bookmarks. Remove bookmarks that don't point to a page
        bookmarks = [_PDFBookmark(bookmark) for bookmark in self.doc.get_toc(True)]
        bookmarks = [bookmark for bookmark in bookmarks if bookmark.page > 0]


        # Build up bookmark heirarchy for each page
        for i in range(len(bookmarks) - 1, -1, -1):
            current_bookmark = bookmarks[i]
            if current_bookmark.lvl == 1 or i == 0:
                continue
            for j in range(i - 1, -1, -1):
                previous_bookmark = bookmarks[j]
                if previous_bookmark.lvl == current_bookmark.lvl -1:
                    current_bookmark.heirarchy.insert(0, previous_bookmark.title)
                if previous_bookmark.lvl == 1:
                    break

        for no, page in enumerate(self.doc, 1):
            page: fitz.Page
            bookmark = next((bookmark.heirarchy for bookmark in bookmarks if bookmark.page == no), [])
            page_info = PageInfo(filename, no, bookmark)
            self.page_metadata.append(page_info)

    def insert_qr_codes(self, 
                        location: QR_POSITION, 
                        verbose: bool = False, 
                        qr_pos_offset: int = 5, 
                        qr_size_multi: float = 0.1):
        for i, page in enumerate(self.doc):
            page_info: PageInfo = self.page_metadata[i]
            page: fitz.Page

            qr = qrcode.QRCode(version=None,
                               error_correction=qrcode.constants.ERROR_CORRECT_H,
                               box_size=10,
                               border=4)
            
            qr.add_data(page_info.toJson())
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color='black', back_color='white')

            if not page.is_wrapped:
                page.wrap_contents()

            page_size: fitz.Rect = page.rect
            qr_size = int(page_size.width * qr_size_multi)

            if location == QR_POSITION.TOP_LEFT:
                qr_rect = fitz.Rect(qr_pos_offset, 
                                    qr_pos_offset, 
                                    qr_size + qr_pos_offset, 
                                    qr_size + qr_pos_offset)
            elif location == QR_POSITION.TOP_RIGHT:
                qr_rect = fitz.Rect(page_size.x1 - qr_size - qr_pos_offset, 
                                    qr_pos_offset, 
                                    page_size.x1 - qr_pos_offset, 
                                    qr_size + qr_pos_offset)
            elif location == QR_POSITION.BOTTOM_LEFT:
                qr_rect = fitz.Rect(qr_pos_offset, 
                                    page_size.y1 - qr_size - qr_pos_offset, 
                                    qr_size + qr_pos_offset, 
                                    page_size.y1 - qr_pos_offset)
            elif location == QR_POSITION.BOTTOM_RIGHT:
                qr_rect = fitz.Rect(page_size.x1 - qr_size - qr_pos_offset, 
                                    page_size.y1 - qr_size - qr_pos_offset, 
                                    page_size.x1 - qr_pos_offset, 
                                    page_size.y1 - qr_pos_offset)

            with io.BytesIO() as output:
                qr_image.save(output, format="PNG")
                page.insert_image(qr_rect, stream=output)

            yield

        self.doc.save(self.filepath, incremental=True, encryption=0)