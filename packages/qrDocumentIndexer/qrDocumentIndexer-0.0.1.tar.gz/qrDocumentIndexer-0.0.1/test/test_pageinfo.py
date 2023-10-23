from qrDocumentIndexer.page_info import PageInfo

def test_pageinfo_comparison_true_for_like_objects():
    filename = "my_filename.pdf"
    pageno = 57
    bookmarks = ["bookmark1", "bookmark2"]
    
    pageinfo1 = PageInfo(filename, pageno, bookmarks)
    pageinfo2 = PageInfo(filename, pageno, bookmarks)

    assert pageinfo1 == pageinfo2

def test_pageinfo_comparison_false_for_disimilar_objects():
    filename = "my_filename.pdf"
    pageno = 57
    bookmarks = ["bookmark1", "bookmark2"]
    
    pageinfo1 = PageInfo(filename, pageno, bookmarks)
    pageinfo2 = PageInfo(filename, 65, bookmarks)

    assert pageinfo1 != pageinfo2

def test_pageinfo_serialization():
    filename = "my_filename.pdf"
    pageno = 57
    bookmarks = ["bookmark1", "bookmark2"]

    info_to_serialize = PageInfo(filename, pageno, bookmarks)

    json = info_to_serialize.toJson()

    quoted_bookmarks = ", ".join([f"\"{bookmark}\"" for bookmark in bookmarks])

    assert json == f'{{"file_name": "{filename}", "page_no": {pageno}, "bookmarks": [{quoted_bookmarks}]}}'

def test_pageinfo_serialization_no_bookmarks():
    filename = "my_filename.pdf"
    pageno = 57

    info_to_serialize = PageInfo(filename, pageno)

    json = info_to_serialize.toJson()

    assert json == f'{{"file_name": "{filename}", "page_no": {pageno}, "bookmarks": []}}'

def test_pageinfo_deserialization():
    filename = "my_filename.pdf"
    pageno = 57
    bookmarks = ["bookmark1", "bookmark2"]
    quoted_bookmarks = ", ".join([f"\"{bookmark}\"" for bookmark in bookmarks])

    j_str = f"""{{
        "file_name": "{filename}",
        "page_no": {pageno},
        "bookmarks": [{quoted_bookmarks}]
    }}"""

    decoded: PageInfo = PageInfo.fromJson(j_str)

    assert isinstance(decoded, PageInfo)
    assert decoded.file_name == filename
    assert decoded.bookmarks == bookmarks
    assert decoded.page_no == pageno

def test_pageinfo_deserialization_no_bookmarks():
    filename = "my_filename.pdf"
    pageno = 57

    j_str = f"""{{
        "file_name": "{filename}",
        "page_no": {pageno}
    }}"""

    decoded: PageInfo = PageInfo.fromJson(j_str)

    assert isinstance(decoded, PageInfo)
    assert decoded.file_name == filename
    assert decoded.bookmarks == []
    assert decoded.page_no == pageno