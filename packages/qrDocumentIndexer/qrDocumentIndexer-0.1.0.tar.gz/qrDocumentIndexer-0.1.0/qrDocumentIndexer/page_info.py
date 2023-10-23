from __future__ import annotations
import json

class PageInfo:
    def __init__(self, file_name: str, page_no: int, bookmarks: list[str]= []):
        self.file_name = file_name
        self.page_no = page_no
        self.bookmarks = bookmarks

    def toJson(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def fromJson(j_str: str):
        def hook(dict):
            return PageInfo(dict['file_name'],
                            dict['page_no'], 
                            dict.get('bookmarks') if dict.get('bookmarks') else [])
        return json.loads(j_str, object_hook=hook)

    def __eq__(self, other: PageInfo):
        if not isinstance(self, other.__class__):
            return False
        return (
            self.bookmarks == other.bookmarks and
            self.file_name == other.file_name and
            self.page_no == other.page_no
        )