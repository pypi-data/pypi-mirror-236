import tkinter as tk
import customtkinter as ctk

from ..pdf_ingest import QR_POSITION
from .file_select.options_frame import Options

class StampOptions(Options):
    def __init__(self,
                 position: QR_POSITION,
                 size: int,
                 offset: int):
        self._position = position
        self._size = size
        self._offset = offset

    @property
    def position(self):
        return self._position
    
    @property
    def size(self):
        return self._size
    
    @property
    def offset(self):
        return self._offset
    
    def __str__(self):
        return f'Position: {self.position.value}, Size: {self.size}, Offset: {self.offset}'

class StampOptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Position selection

        self.position_frame = ctk.CTkFrame(self)
        self.position_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.position_label = ctk.CTkLabel(self.position_frame, text="QR Code Position: ")
        self.position_label.pack(side=tk.LEFT, fill=tk.BOTH)

        self.position_combo = ctk.CTkComboBox(self.position_frame, 
                                              values=[QR_POSITION.TOP_LEFT.value,
                                                      QR_POSITION.TOP_RIGHT.value,
                                                      QR_POSITION.BOTTOM_LEFT.value,
                                                      QR_POSITION.TOP_RIGHT.value])
        self.position_combo.set(QR_POSITION.TOP_LEFT.value)
        self.position_combo.pack(side=tk.LEFT, fill=tk.BOTH)

        # Size selection

        self.size_frame = ctk.CTkFrame(self)
        self.size_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.size_label = ctk.CTkLabel(self.size_frame, text="QR Code Size (percent of page width): 5%")
        self.size_label.pack(side=tk.TOP, fill=tk.BOTH)

        self.size_slider = ctk.CTkSlider(self.size_frame, 
                                        from_ = 2,
                                        to = 20,
                                        number_of_steps = 18,
                                        command = self.update_width_slider_command)
        self.size_slider.set(5)
        self.size_slider.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Offset selection

        self.offset_frame = ctk.CTkFrame(self)
        self.offset_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.offset_label = ctk.CTkLabel(self.offset_frame, text="QR Code offset from edge of page in mm: 5mm")
        self.offset_label.pack(side=tk.TOP, fill=tk.BOTH)

        self.offset_slider = ctk.CTkSlider(self.offset_frame, 
                                        from_ = 0,
                                        to = 100,
                                        number_of_steps = 100,
                                        command = self.update_offset_slider_command)
        self.offset_slider.set(5)
        self.offset_slider.pack(side=tk.BOTTOM, fill=tk.BOTH)

    @property
    def options(self) -> StampOptions:
        position_value = self.position_combo.get()
        position = QR_POSITION(position_value)
        
        size = int(self.size_slider.get())

        offset = int(self.offset_slider.get())

        return StampOptions(position, size, offset)
    
    def update_width_slider_command(self, value):
        self.size_label.configure(text=f"QR Code Size (percent of page width): {int(value)}%")

    def update_offset_slider_command(self, value):
        self.offset_label.configure(text=f"QR Code offset from edge of page: {int(value)}mm")