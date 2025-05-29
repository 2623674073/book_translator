from book.content import Content



class Page:
    """
    代表书里面的一页内容
    """

    def __init__(self):
        self.contents = []

    def add_content(self,content:Content):
        self.contents.append(content)