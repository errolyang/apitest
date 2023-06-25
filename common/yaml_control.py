import os
import yaml
'''yaml文件内容读取'''


class YamlReader:

    def __init__(self, yamlpath):
        if os.path.exists(yamlpath):
            self.path = yamlpath
        else:
            raise FileNotFoundError("文件不存在")
        self.data = None

    def yamldata(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
        return self.data

    def yamldata_all(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data = list(yaml.safe_load_all(f))
        return self.data





