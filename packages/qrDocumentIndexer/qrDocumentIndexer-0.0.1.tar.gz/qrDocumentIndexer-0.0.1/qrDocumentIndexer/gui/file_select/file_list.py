import tkinter as tk
import customtkinter as ctk

class FileRowFrame(ctk.CTkFrame):
    def __init__(self, parent, file_path: str, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)

        self._path = file_path

        self.file_label = ctk.CTkLabel(self, text=file_path)
        self.file_label.pack(side=tk.LEFT, fill=tk.X)

    @property
    def path(self):
        return self._path
    
class FileListFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkScrollableFrame.__init__(self, parent, *args, **kwargs)
        self.files: list[FileRowFrame] = []

    def add_file(self, file_path: str):
        file_row = FileRowFrame(self, file_path)
        file_row.pack(side=tk.BOTTOM, fill=tk.X)
        # file_row.grid(row=len(self.files), column=0)
        self.files.append(file_row)