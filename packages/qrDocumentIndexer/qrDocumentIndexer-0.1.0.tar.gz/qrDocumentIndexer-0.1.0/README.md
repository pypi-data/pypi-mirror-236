# qrDocumentIndexer
A python library for tagging PDF documents with QR codes so that they can be rebuilt into the same document structure after being printed and scanned back.

## Purpose

This library is intended to be used where documents may be printed and then subsequently scanned back to digital format. Normally
this process would result in the loss of any format structure. The documents may even be scanned back in different orders. This
can be particularly common in the cases where documents being printed are technical drawings and they may be re-ordered for
review or other purposes before being scanned again.

This library is intended to store the following information about each page of a PDF in a QR code:
- Filename
- Page number
- Bookmarks (including nesting)

This information can then be used to restructure the documents after scanning. This should even be possible if documents
are scanned into multiple PDFs or image files.

Additional metadata that could be included in future could include:
- Pagesizes
- Paper orientation

## Current State

The tool in it's current state should be fully functional. It can:

- Insert QR codes into each page of provided PDFs to allow later sorting;
- Scan PDFs or image files for QR codes to determine their appropriate order in a document;
- Reconstitute PDF files based on the order dictated by detected QR codes, recreating the original filenames and orders of the documents.

What is missing:

- There is currently no progress indication. It will finish when it finishes;
- Currently the QR scanning process is single threaded so it may take some time to complete;
- There is no preview for the documents so you will have to run the tool for everything to see what you get.

## How to install

Install with the following command:
```
pip install qrDocumentIndexer
```

### ZBar

This package relies on the ZBar library. Please see the below guides for ensuring this library is properly installed:

On **Windows**:  

No installation is required as it is packaged with the python libraries, but it does have dependancies which if not present can cause errors:

If you see an ugly ImportError related with `lizbar-64.dll`, install the [vcredist_x64.exe](https://www.microsoft.com/en-gb/download/details.aspx?id=40784) from the _Visual C++ Redistributable Packages for Visual Studio 2013_

On **Linux**:  
```bash
sudo apt-get install libzbar0
```

On **Mac OS X**: 
```bash
brew install zbar
```
