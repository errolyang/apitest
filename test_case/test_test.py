import os
import requests
import jsonpath
from common.assert_control import Assert
from common import conf_control
from common import yaml_control
import re
from utils.cache_tool.cache_control import CacheHandler, _cache_config
import pytest
from utils.request_tool.request_control import RequestControl
from utils.cache_tool.regular_control import RegularControl
from utils.request_tool.dependent_case import DependentCase


class Testcase:

    def test_case(self):
        """delete_path = conf_control.get_data_path() + os.sep + "collect_delete_tool.yml"
        delete_case = yaml_control.YamlReader(delete_path)
        delete_data = delete_case.yamldata()
        print(delete_data)
        delete_url = delete_data["host"] + delete_data["url"]
        headers = RegularControl(str(delete_data["headers"])).cache_regular()
        # print(headers)
        # case_data = cache_regular(str(delete_data))
        # print(case_data)
        # res = requests.get(url=delete_url, headers=headers)
        # print(res.text)

        DependentCase(dependent_yaml_case=delete_data).dependent_handler()
        print(_cache_config)
        value = RegularControl(delete_data).cache_regular()
        print(value)"""

        case_path = conf_control.get_base_path() + os.sep + "report/html/data/test-cases"
        a = os.listdir(case_path)
        print(a)
        b = os.walk(case_path)
        for path, dirs, files in b:
            print(path)
            print(dirs)
            print(files)
            print("\n")

        print("测试git回退版本")



if __name__ == "__main__":
    pytest.main(['-vs', 'test_test.py'])

