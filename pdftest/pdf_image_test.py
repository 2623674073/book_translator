import pdfplumber

# 加载一个pdf文件

# pdf = pdfplumber.open('./test.pdf')
pdf = pdfplumber.open('./test.pdf')




# pdf中每一页都对应一个Page对象
page1 = pdf.pages[0]  # 第一个Page对象
page2 = pdf.pages[1]  # 第二个Page对象

# 提取内容

# 提取图片
print(page1.images)
print(page2.images)

# 直接提取某一页的图片
img = page2.images[0]
ppoint = (img['x0'],img['top'],img['x1'],img['bottom'])
    # 打印和保存图片
# page2.crop(ppoint).to_image(antialias=True, resolution=1080).show()     # # antialias=True抗锯齿, resolution=1080高清
# page2.crop(ppoint).to_image(antialias=True, resolution=1080).save('./image/test1.png')


# 整个页面全部提取为图片
page1.to_image(antialias=True).show()  # antialias=True抗锯齿, resolution=1080高清
# page1.to_image(antialias=True).save('./image/test2.png')



