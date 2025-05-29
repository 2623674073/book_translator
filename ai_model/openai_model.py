import time
from ai_model.model import Model
from utils.log_utils import log
from openai import OpenAI
import openai



class OpenAIModel(Model):

    def __init__(self, model: str, api_key: str,base_url:str):
        self.model = model
        self.client = OpenAI(api_key=api_key,base_url=base_url)

    def request_model(self, prompt):
        """
        请求模型的API接口
        返回两个值： 1、翻译之后的文本，2、True或者False。翻译是否成功
        设计思路：我们总共可以调用三次API
        """

        count = 0   # 调用aip的次数
        while count < 3:
            try:
                resp = self.client.chat.completions.create(
                    model= self.model,
                    messages=[
                        {'role': 'user',
                         'content': prompt}
                    ]
                )

                tranlation = resp.choices[0].message.content.strip()
                return tranlation,True

            except openai.RateLimitError as s:
                count+=1
                if count < 3:
                    # 输出一个警告提示，并且休眠30秒，然后继续调用API接口
                    log.warning('调用API连接失败，30秒后自动重新调用......')
                    time.sleep(30)
                else:
                    raise Exception('已经连续调用API接口3次了，不能再继续，请检查网络')
            except Exception as e:
                log.exception(e)

                return '',False
        return '', False