from abc import ABC, abstractmethod

from .file_list import FileListFrame
from .options_frame import Options

class ActionHandler(ABC):
    @abstractmethod
    def process_files(self, file_list: FileListFrame, options: Options):
        pass