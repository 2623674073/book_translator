import pdfplumber

# 加载一个pdf文件

# pdf = pdfplumber.open('./test.pdf')
pdf = pdfplumber.open('./test.pdf')

# 得到pdf的元数据和页数
print(pdf.metadata)
print(pdf.pages)


# pdf中每一页都对应一个Page对象
page1 = pdf.pages[0]  # 第一个Page对象
page2 = pdf.pages[1]  # 第二个Page对象
# 获得page对象中各种属性
print(page1.page_number)    # 页号
print(page1.width)
print(page1.height)


# 提取内容
# 1、提取文本内容
print(page1.extract_text())
print('-'*20)
print(page1.extract_text(layout=True))  # 按照原来的布局提取文本内容

# 2、提取图片
# print(page2.images)

# 3、提取表格
print(page1.extract_tables())