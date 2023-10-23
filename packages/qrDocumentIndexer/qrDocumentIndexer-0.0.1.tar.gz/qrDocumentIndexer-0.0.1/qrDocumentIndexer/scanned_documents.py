from os.path import splitext, isfile, join

import fitz
from PIL import Image

from qrDocumentIndexer.scanned_page import ScannedPage

class ScannedDocuments:
    def __init__(self) -> None:
        self._pages = []
        self._loaded_files = {}

    def add_document(self, document_path: str) -> None:
        if not isfile(document_path):
            raise FileNotFoundError(f'Could not find file {document_path}')
        
        if document_path in self._loaded_files:
            raise FileExistsError(f'Already loaded file {document_path}')
        
        _, ext = splitext(document_path)

        if ext.lower() == '.pdf':
            pdf = fitz.Document(document_path)
            for page in pdf:
                self._pages.append(ScannedPage(page, src_doc=pdf))
            self._loaded_files[document_path] = pdf
        else:
            image = Image.open(document_path)
            self._pages.append(ScannedPage(image, src_image=document_path))
            self._loaded_files[document_path] = image

    @property
    def pages(self) -> list[ScannedPage]:
        '''
            Return all scanned pages
        '''
        return self._pages
    
    @property
    def filepath(self) -> str:
        '''
            Filepath of scanned document
        '''
        return self._filepath
    
    @property
    def pages_by_output_doc(self) -> dict[str, list[ScannedPage]]:
        '''
            Group all scanned pages by the file they will be sorted to
            when reconstituted
        '''
        result = {}

        for page in self.pages:
            filename = None

            if page.page_info is not None:
                filename = page.page_info.file_name

            if filename not in result:
                result[filename] = []
            
            result[filename].append(page)

        return result



    


