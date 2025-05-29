from book.page import Page

class Book:
    """
    代表你需要翻译的一本书
    """
    def __init__(self,file_path):
        self.file_path = file_path
        self.pages:[Page] = []  # # 这本所有的内容页   self.pages是Page类型的列表

    def add_page(self,page:Page):
        self.pages.append(page)
