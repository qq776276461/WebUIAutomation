import yaml

from src.utils.PathUtil import PROJECT_ROOT_PATH


class ConfigRead:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        config_path = f'{PROJECT_ROOT_PATH}/config/config.yaml'
        with open(config_path, 'r', encoding='utf-8') as yaml_file:
            self.__config = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)

    @property
    def chrome_config(self) -> dict:
        return self.__config['ChromeOptions']

    @property
    def selenium_config(self) -> dict:
        return self.__config['SeleniumConfig']


CONFIG = ConfigRead()

if __name__ == '__main__':
    print(CONFIG.chrome_config)
