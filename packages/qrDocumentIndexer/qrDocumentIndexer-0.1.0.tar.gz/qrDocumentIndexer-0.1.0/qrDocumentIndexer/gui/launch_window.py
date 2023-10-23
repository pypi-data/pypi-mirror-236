import customtkinter as ctk

from .file_select.file_select_window import FileSelectWindow

from .stamp_options_frame import StampOptionsFrame
from .stamp_action_handler import StampActionHandler

from .sort_actions_handler import SortActionHandler
from .sort_options_frame import SortOptionsFrame

ADD_PDF_TITLE = 'Add QR Codes to PDFs'
SORT_SCANNED_DOCS_TITLE = 'Sort Scanned Documents'


class LaunchWindow(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.add_qrs_to_pdf_button = ctk.CTkButton(master=self, text=ADD_PDF_TITLE, command=self.click_stamp_docs)
        self.add_qrs_to_pdf_button.pack(fill='both', side='top', expand=True)
        self.sort_scanned_docs_button = ctk.CTkButton(master=self, text=SORT_SCANNED_DOCS_TITLE, command=self.click_sort_button)
        self.sort_scanned_docs_button.pack(fill='both', side='bottom', expand=True)

        self.pack(side='top', fill='both', expand=True)

    def click_stamp_docs(self):
        FileSelectWindow(self, ADD_PDF_TITLE, ADD_PDF_TITLE, StampOptionsFrame, StampActionHandler)

    def click_sort_button(self):
        FileSelectWindow(self, SORT_SCANNED_DOCS_TITLE, SORT_SCANNED_DOCS_TITLE, SortOptionsFrame, SortActionHandler,
                         '.pdf', 
                         [['PDF Files','*.pdf'], ['Image Files', ['*.jpg','*.jpeg','*.png','*.tiff','*.tif']],['All Files', '*.*']])