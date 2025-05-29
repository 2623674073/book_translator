from typing import Optional

import fitz

from book.content import Content, ContentType, TableContent, ImageContent
from utils.exceptions import PageOutOfRangeException

import pdfplumber

from book.book import Book
from book.page import Page
from utils.log_utils import log


def parse_pdf(pdf_filf_path:str, pages:Optional[int] = None)->Book :
    """
    接卸pdf文件的函数，返回解析后的文本对象
    :param pdf_filf_path:   pdf文件路径
    :param pages:           可选的，需要翻译的前n页，默认是整个pdf文件
    :return:                返回一个Book对象
    """
    book = Book(pdf_filf_path)  # 一个pdf对应一本书，就是一个book对象

    with pdfplumber.open(pdf_filf_path) as pdf:

        # pages不能超过pdf文件中的总页数
        if pages and pages > len(pdf.pages):
            raise PageOutOfRangeException(len(pdf.pages),pages)

        if pages is None:   # 如果没有传这个值，默认为整本书
            page_arr = pdf.pages
        else:
            page_arr = pdf.pages[:pages]    # 切片进行截取需要页数

        # 同时用 fitz 打开 PDF 来提取图像
        doc = fitz.open(pdf_filf_path)

        for index,pdf_page in enumerate(page_arr):   # 遍历每一页

            page = Page()   # 每一页就是一个page对象

            # 从pdf的page中提取文本内容
            raw_text = pdf_page.extract_text()      # 这里也会提取表格中的内容，所以要删除掉重复内容
            tables = pdf_page.extract_tables()

            # 出现重复的文本提取
            for table in tables:
                for row in table:
                    for cell in row:
                        raw_text = raw_text.replace(cell, '', 1)

            # 处理文本内容
            if raw_text:
                # 数据清洗 ： 删除空行，和首位空白字符
                lines = raw_text.splitlines()
                cleaned_lines = [line.strip() for line in lines if line.strip()]  # if line.strip()为非空才能保存
                cleaner_text = '\n'.join(cleaned_lines)     # 把每一个列表元素通过"\n"再次连接起来

                # 文本内容对应一个Content对象
                text_content = Content(content_type=ContentType.TEXT,original=cleaner_text)
                page.add_content(text_content)      # 把文本内容添加到 page中去
                log.debug(f"[pdf解析之后的文本内容]： \n{cleaner_text}")

            # 处理表格内容
            if tables:
                tables_content = TableContent(content_type=ContentType.TABLE,original=tables)
                page.add_content(tables_content)    # 把表格内容添加到 page中去
                log.debug(f"[pdf解析之后的表格内容]： \n{tables}")

            # 图片不需要翻译
            # ---- 提取图像内容（使用 fitz） ----
            # ---- 图像处理开始 ----
            fitz_page = doc.load_page(index)  # 加载对应页码
            image_list = fitz_page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]  # 图像二进制数据
                image_ext = base_image["ext"]  # 格式：png / jpeg 等

                # 构造图像原始数据
                img_data = {
                    "index": img_index,
                    "ext": image_ext,
                    "bytes": image_bytes,
                    "width": base_image.get("width"),
                    "height": base_image.get("height"),
                    "colorspace": base_image.get("colorspace"),
                }

                # 创建 ImageContent 对象
                image_content = ImageContent(
                    content_type=ContentType.IMAGE,
                    original=img_data
                )
                page.add_content(image_content)


            book.add_page(page)
        doc.close()

    return book


# python-docx 处理word的包
# openpyxl 处理excel的包
