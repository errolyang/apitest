import os
from common import yaml_control
'''读取各路经，配置信息'''

current = os.path.abspath(__file__)
BASE_path = os.path.dirname(os.path.dirname(current))
config_path = BASE_path + os.sep + "config"
print(config_path)
data_path = BASE_path + os.sep + "data"
default_path = config_path + os.sep + "default.yml"


def get_base_path():
    return BASE_path


def get_config_path():
    return config_path


def get_data_path():
    return data_path


def get_default_path():
    return default_path


class Confdefault():
    def __init__(self, config):
        self.config = config
        # config = yaml_control.YamlReader(get_default_path()).yamldata()

    def get_baseurl(self):
        return self.config["base"]["url"]

    def get_project_name(self):
        return self.config["project_name"]

    def get_email_send_user(self):
        return self.config["email"]["send_user"]

    def get_email_host(self):
        return self.config["email"]["email_host"]

    def get_email_stamp_key(self):
        return self.config["email"]["stamp_key"]

    def get_email_send_list(self):
        return self.config["email"]["send_list"]


if __name__ == '__main__':
    conf = Confdefault()
    baseurl = conf.get_baseurl()
    print(baseurl)