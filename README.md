# 书籍翻译系统

## 主要功能

主要功能是将pdf类的书籍进行翻译，现可以将pdf翻译成pdf和markdown格式。后续可以扩展word版本



## 核心技术栈

openai、pdfplumber、ReprotLab

- ​	翻译功能是通过调用openai的接口进行翻译。以后也可以扩展为GLM model
- ​	pdf的读取是通过pdfplumber库中的接口，具体例子可以参考pdftest文件夹。
- ​	pdf写入是通过ReportLab 库的接口，涉及到文件字体和排版。
- ​	markdown的写入是直接通过文件读取进行的，只要按照markdown的标签格式写入就能保证排版。

## 核心难点

​		难点主要是对pdf数据读取按照什么格式传给openai，和openai传输出来的数据格式必须得要求清楚。

以及表格的处理和排版，需要逐步调整。



