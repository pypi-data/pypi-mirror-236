from CTkMessagebox import ctkmessagebox

from .file_select.action_handler import ActionHandler
from .file_select.file_list import FileListFrame
from .stamp_options_frame import StampOptions

from ..pdf_ingest import PDFIngest

class StampActionHandler(ActionHandler):
    def process_files(self, file_list: FileListFrame, options: StampOptions):
        for file in file_list.files:
            file_path = file.path
            ingester = PDFIngest(file_path)
            for _ in ingester.insert_qr_codes(location=options.position,
                                     qr_pos_offset=options.offset,
                                     qr_size_multi=float(options.size)/100.0):
                pass
        ctkmessagebox.CTkMessagebox(title="Done", message="Processing done.")