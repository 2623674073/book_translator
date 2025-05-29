from translator.book_translator import PDFTranslator
from utils.argument_utils import ArgumentUtils
from utils.loader_config import LoaderConfig

from ai_model.openai_model import OpenAIModel
from ai_model.glm_model import ChatGLMModel




if __name__ == '__main__':
    print('项目启动！！！')


    # 启动命令中的参数解析和验证,并返回所有参数
    arg_utils = ArgumentUtils()
    args = arg_utils.parser_arg()

    # 读取配置文件（YAML）
    loader_config = LoaderConfig(args.config)
    config = loader_config.load_config()

    # 模型的名字： 先从命令行参数中获取，否则 从配置文件中获取
    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    # api_key
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    # base_url
    base_url = args.openai_base_url if args.openai_base_url else config['OpenAIModel']['base_url']

    # 初始化模型对象
    if args.model_type == 'OpenAIModel':
        model = OpenAIModel(model_name,api_key,base_url)
    else:
        model = ChatGLMModel()


    # 初始化一个翻译器
    file_path = args.file_path if args.file_path else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    if file_path[file_path.rindex('.'):] == '.pdf' or file_path[file_path.rindex('.'):] == '.PDF':
        translator = PDFTranslator(model=model)
    else:
        print("暂只支持PDF格式,word等版本需要自己扩展word类")


    # 开始翻译
    translator.book_tranlattion(file_path=file_path, out_file_format=file_format)
    