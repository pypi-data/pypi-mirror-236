from fitz import Document

from qrDocumentIndexer.page_info import PageInfo
from qrDocumentIndexer.scanned_page import ScannedPage

class BlankPage(ScannedPage):
    def __init__(self):
        pass

    @property
    def page_info(self) -> PageInfo:
        return PageInfo(None, 0, [])
    
    def add_to_document(self, doc: Document):
        doc.new_page(-1, # insertion point: end of document
            width = 595, # page dimension: A4 portrait
            height = 842)

BLANK_PAGE = BlankPage()

class ReconstitutedDocument():
    def __init__(self, pages: list[ScannedPage], filename: str):
        self._unordered_pages = pages
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @property
    def sorted_pages(self) -> list[ScannedPage]:
        if not hasattr(self, '_ordered_pages'):
            self._sort_pages()

        return self._ordered_pages
        

    def _sort_pages(self):
        sorted_pages: list[ScannedPage] = sorted(self._unordered_pages, key = lambda x: x.page_info.page_no)
        page_nos = [x.page_info.page_no for x in sorted_pages]
        max_page_no = max(page_nos)
        for i in range(1, max_page_no):
            if i in page_nos:
                continue
            if i == 1:
                # If we are missing first page will be no page to insert after
                sorted_pages.insert(0, BLANK_PAGE)
            else:
                last_index = len(page_nos) - page_nos[::-1].index(i - 1)
                sorted_pages.insert(last_index, BLANK_PAGE)
            page_nos = [x.page_info.page_no for x in sorted_pages]

        self._ordered_pages = sorted_pages

    @property
    def _sorted_toc(self):
        toc = []
        for i, page in enumerate(self.sorted_pages):
            for j, bookmark in enumerate(page.page_info.bookmarks):
                last_at_level = ReconstitutedDocument.__get_last_toc_at_level(toc, j + 1)
                if last_at_level != bookmark:
                    toc.append([j + 1, bookmark, i + 1]) # TOC is [level, title, page number]
        
        return toc

    def __get_last_toc_at_level(toc: list, level: int) -> str:
        toc_rev = toc[::-1]
        for entry in toc_rev:
            if entry[0] < level:
                return None # We have alredy hit a higher level bookmark
            elif entry[0] == level:
                return entry[1]
        return None


    def save_document(self, filepath: str):
        doc = Document()
        for page in self.sorted_pages:
            page.add_to_document(doc)
        doc.set_toc(self._sorted_toc)
        doc.save(filepath)