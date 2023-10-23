from os import path

from CTkMessagebox import ctkmessagebox

from .file_select.action_handler import ActionHandler
from .file_select.file_list import FileListFrame
from .sort_options_frame import SortOptions

from ..scanned_documents import ScannedDocuments
from ..reconstituted_document import ReconstitutedDocument

class SortActionHandler(ActionHandler):
    def process_files(self, file_list: FileListFrame, options: SortOptions):
        scanned_docs = ScannedDocuments()
        
        for file in file_list.files:
            file_path = file.path
            scanned_docs.add_document(file_path)
        
        output_docs = [ReconstitutedDocument(pages, filename) for filename, pages in scanned_docs.pages_by_output_doc.items()]

        for doc in output_docs:
            file_path = path.join(options.output_directory, doc.filename)
            doc.save_document(file_path)

        ctkmessagebox.CTkMessagebox(title="Done", message="Processing done.")