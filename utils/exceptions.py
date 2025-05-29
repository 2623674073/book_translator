

class PageOutOfRangeException(Exception):

    def __init__(self, book_total, translator_pages):
        self.book_total = book_total
        self.translator_pages = translator_pages
        super().__init__(f'页号的范围越界：这本书的总页数为:{self.book_total}, 但是你输入的页数为: {self.translator_pages}')