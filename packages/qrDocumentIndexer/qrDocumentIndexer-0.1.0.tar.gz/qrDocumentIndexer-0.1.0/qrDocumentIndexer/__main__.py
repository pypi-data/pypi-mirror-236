import customtkinter as ctk

from .gui.launch_window import LaunchWindow

from qrDocumentIndexer.pdf_ingest import QR_POSITION, PDFIngest

def main():
    print("launched")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk(className="qrImageIndexerGUI")
    LaunchWindow(app)
    app.title('QR Image Indexer GUI')
    app.geometry("300x75")
    app.resizable(width=False, height=False)
    app.mainloop()


if __name__ == '__main__':
    main()