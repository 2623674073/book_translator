# ReportLab 库（一个用于生成 PDF 的 Python 第三方库
import os
from datetime import datetime
from io import BytesIO

import pandas as pd
from reportlab.lib import pagesizes, colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, PageBreak, Image as PdfImage

from book.content import ContentType
from utils.log_utils import log


class FileWriter:

    def __init__(self,book):
        self.book = book

    def save_book(self,out_file_path:str=None,file_format:str="PDF"):
        """
        负责将翻译之后的数据写入一个文件
        :param out_file_path:
        :param file_format:
        :return:
        """

        if file_format.lower() == 'pdf':
            self.save_book_pdf(out_file_path)
        elif file_format.lower() == 'md':
            self.save_book_makrdown(out_file_path)
        elif file_format.lower() == 'doc' or file_format.lower() == 'docx':
            pass
        else:
            log.warning('当前的文件格式不支持，项目仅仅支持：PDF，Word，Markdown这三种！')
            return

    def save_book_pdf(self,out_file_path:str=None):
        """
        把数据写入PDF文件中
        :param out_file_path:
        :return:
        """
        if not out_file_path:
            subfix = self.book.file_path[self.book.file_path.rindex('.'):]  # 找到右边第一个‘.’的索引位置再进行切分
            out_file_path = self.book.file_path.replace(subfix,'_translated.pdf')

            # 写入日志
            log.debug(f"pdf文件的原路径是：{self.book.file_path} , 翻译之后的路径是：{out_file_path}")

            # 1. 先注册中文字体    ：将系统中的宋体（SimSun）字体文件注册到 ReportLab 中，以便在生成 PDF 时可以使用该字体显示中文或其他字符。
            pdfmetrics.registerFont(TTFont('SimSun','../fonts/simsun.ttc'))

            # 2. 创建一个pdf的文字段落样式
            style  = ParagraphStyle('SimSun',fontName='SimSun',fontSize=12,leading=14)

            # 3. 创建一个pdf的文档
            doc  = SimpleDocTemplate(out_file_path,pagesize = pagesizes.letter)     # 文件页面的大小

            pdf_data = []   # 临时存放写入pdf文件的数据

            for page in self.book.pages:    # 遍历book的每一页
                for content in page.contents:        # 遍历每一页中的内容
                    if content.status:
                        # 如果是文本内容，则添加文本
                        if content.content_type == ContentType.TEXT:
                            paragraph  = Paragraph(text=content.translation, style=style)
                            pdf_data.append(paragraph)

                        # 如果是表格内容，则添加表格
                        elif content.content_type == ContentType.TABLE:
                            table_style  = TableStyle(  # 表格的样式 注意(0, 0)代表一组，每组坐标为（列，行）
                                [
                                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),   # 相当于第一行的背景色
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),  # 更改表头字体为 "SimSun"
                                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),  # 更改表格中的字体为 "SimSun"
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                                ]
                            )
                            # 把DataFrame转换成列表，并创建一个表格对象
                            table = Table(data=content.translation.values.tolist(),colWidths=1.5*inch,rowHeights=0.5*inch)
                            table.setStyle(table_style) # 设置样式
                            pdf_data.append(table)
                        # 如果是图片内容，
                        elif content.content_type == ContentType.IMAGE:
                            img_data = content.original
                            img_bytes = img_data.get("bytes")
                            if not img_bytes:
                                log.warning("图像为空，跳过")
                                continue

                            # 使用 BytesIO 把字节流包装成“虚拟文件”
                            img_stream = BytesIO(img_bytes)

                            try:
                                img = PdfImage(img_stream, width=4 * inch, height=3 * inch)
                                pdf_data.append(img)
                            except Exception as e:
                                log.error(f"插入图像失败：{e}")


                # 当前这一页的内容都处理了， 紧跟着接一条分页符
                # 分页符不能加在最后一页
                if page != self.book.pages[-1]:
                    pdf_data.append(PageBreak())    # 加分页符

            doc.build(pdf_data)
            log.info('pdf写入成功！')

    def save_book_makrdown(self,out_file_path:str=None):
        """
                把数据写入makrdown文件中
                :param out_file_path:
                :return:
                """
        if not out_file_path:
            subfix = self.book.file_path[self.book.file_path.rindex('.'):]  # 找到右边第一个‘.’的索引位置再进行切分
            out_file_path = self.book.file_path.replace(subfix, '_translated.md')

            # 写入日志
            log.debug(f"pdf文件的原路径是：{self.book.file_path} , 翻译之后的路径是：{out_file_path}")

            # 创建一个专门存放图像的临时目录
            image_dir_name = f"images_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(image_dir_name, exist_ok=True)
            log.info(f"正在将图像写入临时目录：{image_dir_name}")

            with open(out_file_path,'w',encoding='UTF-8') as md_file:
                for page_index,page in enumerate(self.book.pages):
                    for content in page.contents:
                        if content.status:
                            # 如果是文本内容，则添加文本
                            if content.content_type == ContentType.TEXT:
                                # 写入一个段落
                                md_file.write(content.translation + '\n\n')

                            # 如果是表格内容，则添加表格
                            elif content.content_type == ContentType.TABLE:
                                # 写入一个表格
                                df:pd.DataFrame = content.translation   # 翻译之后的表格数据     赋值给变量 df，它是一个 Pandas 的 DataFrame 对象

                                first_row = df.values.tolist()[0]   # 获取 DataFrame 的第一行数据
                                df.columns = first_row              # 把第一行设为列名
                                df.drop([0],inplace=True)     # 删除原来的第 0 行 因为这一行已经被用作列名了
                                # 炫第一是按照markdown中的标签格式来写的
                                # 构建 Markdown 表格的头部
                                header = '| ' + ' | '.join(
                                    [str(column_name) for column_name in df.columns]) + ' |' + '\n'

                                # 构建表格分隔符 来区分表头和表格内容
                                tr = '| '+ ' | '.join(['---']*len(df.columns)) + ' |' + '\n'

                                # 构建表格主题内容
                                t_body= '\n' .join(['| ' + ' | '.join(str(cell)  for cell in row)  +' |' for row in df.values.tolist()]) + '\n\n'

                                md_file.write(header + tr + t_body)

                            elif content.content_type == ContentType.IMAGE:
                                img_bytes = content.original.get("bytes", b"")
                                img_ext = content.original.get("ext", "png")

                                if not img_bytes:
                                    log.warning("图像内容为空，跳过写入")
                                    continue

                                # 构建图像文件名
                                image_filename = f"image_page{page_index}_{content.original.get('index', 0)}.{img_ext}"
                                image_path = os.path.join(image_dir_name, image_filename)

                                try:
                                    # 保存图像到文件
                                    with open(image_path, "wb") as img_file:
                                        img_file.write(img_bytes)
                                    # 写入 Markdown 图像语法
                                    md_file.write(
                                        f"![Image]({os.path.relpath(image_path, start=os.path.dirname(out_file_path))})\n\n")
                                except Exception as e:
                                    log.error(f"无法保存图像 {image_filename}: {e}")

                    # 当前这一页的内容都处理了， 紧跟着接一条分页符
                    # 分页符不能加在最后一页
                    if page != self.book.pages[-1]:
                        md_file.write('\n -----\n\n')  # 除了最后一页，每页的后面都加上一个分页符

            log.info('MarkDown文件写入完成！')