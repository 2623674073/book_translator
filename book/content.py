import re
from enum import Enum,auto
from typing import Optional

import pandas as pd

from utils.log_utils import log


class ContentType(Enum):
    """内容的类型 枚举"""
    TEXT  = auto()  # 自动为枚举成员分配值（默认从 1 开始递增）。
    TABLE = auto()
    IMAGE = auto()


class Content:
    def __init__(self,content_type:ContentType,original,translation=None):
        """
        内容初始化
        :param content_type:    内容类型
        :param original:        原文
        :param translation:     翻译之后的内容
        """
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False # 翻译完成的状态

    def set_translation(self,translation,status):
        """ 设置翻译之后的文本， 并设置翻译状态 """

        if self.content_type == ContentType.TEXT and isinstance(translation,str) and status:
            self.translation = translation
            self.status = status
        else:
            log.warning('当前翻译之后的文本内容不是字符串，请检查！')

    def set_status(self, status: bool):
        self.status = status

    def get_original_to_string(self):
        """ 把对象变成一个字符串 """
        return self.original


class TableContent:
    """ 书中表格内容 """
    def __init__(self,content_type:ContentType, original, translation=None):
        """
        内容初始化
        :param content_type:    内容类型
        :param original:        原文
        :param translation:     翻译之后的内容
        """
        df = pd.DataFrame(original)
        self.content_type = content_type
        self.original = df
        self.translation = translation
        self.status = False     # 翻译完成的状态

    @log.catch
    def set_translation(self, translation, status):
        """
        设置翻译之后的文本，并设置翻译状态
        1、判断数据的合法性
        2、把translation文本数据，变成二维的数组
        3、把二维数组变成DataFrame
        """
        if self.content_type == ContentType.TABLE and isinstance(translation, str) and status:
            # 得到的二维数组
            # re.split(',|，',row.strip()) 将一行文本按照英文逗号或中文逗号进行分割，返回一个由各个单元格组成的列表
            table_data = [ re.split(',|，',row.strip())  for row in translation.strip().split('\n')]
            log.debug(table_data)

            # 得到dataframe数据，表头单独处理
            translation_df = pd.DataFrame(table_data[0:])

            log.debug(f"处理成DataFrame数据: \n{translation_df}")
            self.translation = translation_df
            self.status = status
    def get_original_to_string(self):
        """把dataframe对象变成一个字符串"""
        return self.original.to_string(header=False, index=False)

class ImageContent(Content):
    """
    图像内容类，继承自 Content。
    用于统一管理从 PDF 中提取出的图像信息。
    """

    def __init__(self, original: dict, content_type: ContentType = ContentType.IMAGE, translation: Optional[str] = None):
        """
        :param original: 包含图像信息的字典，例如：
                         {
                             "index": 0,
                             "ext": "png",
                             "bytes": b'\x89PNG\r\n\x1a\n...'  # 图像二进制数据
                         }
        :param content_type: 内容类型，默认为 ContentType.IMAGE
        :param translation: 可选翻译结果（例如图像描述文字）
        """
        super().__init__(content_type=content_type, original=original, translation=translation)

    def get_image_bytes(self) -> bytes:
        """获取图像的原始二进制数据"""
        return self.original.get("bytes", b"")

    def get_image_extension(self) -> str:
        """获取图像的扩展名（如 png, jpeg）"""
        return self.original.get("ext", "bin")

    def get_image_index(self) -> int:
        """获取图像在页面中的序号"""
        return self.original.get("index", -1)

    def save_to_file(self, file_path: str):
        """将图像保存到指定路径"""
        try:
            with open(file_path, "wb") as f:
                f.write(self.get_image_bytes())
            print(f"图像已保存至: {file_path}")
        except Exception as e:
            print(f"保存图像失败: {e}")

    def get_original_to_string(self) -> str:
        """返回图像的基本信息字符串"""
        return f"[Image] index={self.get_image_index()}, ext={self.get_image_extension()}, size={len(self.get_image_bytes())} bytes"


if __name__ == '__main__':
    pass
