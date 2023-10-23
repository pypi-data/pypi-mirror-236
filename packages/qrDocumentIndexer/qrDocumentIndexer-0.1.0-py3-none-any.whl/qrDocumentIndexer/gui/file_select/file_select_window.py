from typing import Type

import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from .file_list import FileListFrame
from .action_handler import ActionHandler

class FileSelectWindow(ctk.CTkToplevel):
    def __init__(self, master, title: str, 
                    action_button_text: str, 
                    options_frame: Type[ctk.CTkFrame],
                    action_handler: Type[ActionHandler],
                    default_extension: str = '.pdf',
                    filetypes: list = [['PDF Files','*.pdf']],
                    *args, **kwargs):
        ctk.CTkToplevel.__init__(self, master, *args, **kwargs)
        self.geometry("1200x800")
        self.title(title)
        self.button_frame = ctk.CTkFrame(self)
        self.select_files = ctk.CTkButton(self.button_frame, text='Select Files',
                                        command=self._select_files_clicked)
        self.action_button = ctk.CTkButton(self.button_frame, text=action_button_text,
                                                command=self._action_button_clicked)
        
        self.button_frame.pack(side=tk.TOP, fill=tk.X)
        self.select_files.pack(side=tk.LEFT, fill=tk.X)
        self.action_button.pack(side=tk.RIGHT, fill=tk.X)

        if options_frame:
            self.options_frame = options_frame(self)
            self.options_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.file_list = FileListFrame(self, height=2000)
        self.file_list.pack(fill=tk.BOTH)

        self.action_handler = action_handler

        self._file_types = filetypes
        self._default_extension = default_extension

    def _select_files_clicked(self):
        files = filedialog.askopenfilenames(defaultextension= self._default_extension,
                                        filetypes=self._file_types,
                                        title= 'Select Files to Stamp with PDF')
        for file in files:
            self.file_list.add_file(file)

    def _action_button_clicked(self):
        options = None
        try:
            options = self.options_frame.options
            print(f"Loaded options: {options}")
        except:
            print("No options found")

        handler = self.action_handler()
        handler.process_files(self.file_list, options)
        pass