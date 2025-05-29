import yaml

class LoaderConfig:

    def __init__(self,config_file_path):
        self.config_file_path = config_file_path

    def load_config(self):
        """
        加载配置文件中的内容
        :return:
        """
        with open(self.config_file_path,'r') as f:
            config = yaml.safe_load(f)

        return config