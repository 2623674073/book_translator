import argparse

class ArgumentUtils:
    """
    命令行参数解析对象
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="书籍自动翻译器")
        self.parser.add_argument('--config',type=str,default='config.yaml',help="项目的整体配置文件")
        self.parser.add_argument('--model_type', type=str, default='OpenAIModel', choices=['GLMModel', 'OpenAIModel'],
                                 help='选择OpenAI还是GLM的模型')
        self.parser.add_argument('--glm_model_url', type=str, help='ChatGLM的模型访问路径')
        self.parser.add_argument('--timeout', type=int, help='API接口请求的超时时间')
        self.parser.add_argument('--openai_model', type=str, help='OpenAI中所使用的模型名字')
        self.parser.add_argument('--openai_api_key', type=str, help='OpenAI中的api_key')
        self.parser.add_argument('--openai_base_url', type=str, help='OpenAI中的base_url')
        self.parser.add_argument('--file_path', type=str, help='需要翻译的书籍所属的文件路径')
        self.parser.add_argument('--file_format', type=str, help='翻译之后生成的文件格式')

    def parser_arg(self):
        """
        解析和验证命令行中的参数
        :return:
        """

        args = self.parser.parse_args()
        # 参数的验证，可以有更多
        # if args.model_type == 'OpenAIModel' and not args.openai_model and not args.openai_api_key:
        #     self.parser.error('当选择OpenAI后，--openai_model和--openai_api_key参数，必须要传！')
        return args
