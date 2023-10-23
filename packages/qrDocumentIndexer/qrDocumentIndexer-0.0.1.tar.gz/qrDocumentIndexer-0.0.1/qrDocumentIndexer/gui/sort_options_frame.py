from os import PathLike

import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from .file_select.options_frame import Options

class SortOptions(Options):
    def __init__(self,
                 output_directory: str | PathLike):
        self._save_directory = output_directory

    @property
    def output_directory(self):
        return self._save_directory
    
    def __str__(self):
        return f'Save directory: {self._save_directory}'

class SortOptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Position selection

        self.save_loc_frame = ctk.CTkFrame(self)
        self.save_loc_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.save_loc_button = ctk.CTkButton(self.save_loc_frame, text="Select Save Location", command=self.select_save_location)
        self.save_loc_button.pack(side=tk.LEFT, fill=tk.BOTH)

        self.save_loc_textbox = ctk.CTkEntry(self.save_loc_frame, placeholder_text="Save Location")
        self.save_loc_textbox.pack(side=tk.LEFT, fill=tk.X, expand=True)

    @property
    def options(self) -> SortOptions:
        directory = self.save_loc_textbox.get()

        return SortOptions(directory)
    
    def select_save_location(self):
        directory = filedialog.askdirectory(title="Select output location for sorted PDFs")
        self.save_loc_textbox.delete(1.0, tk.END)
        self.save_loc_textbox.insert(1.0, directory)