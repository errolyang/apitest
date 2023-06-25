import requests
import os
from jsonpath import jsonpath
from utils.cache_tool.regular_control import RegularControl
from utils.cache_tool.cache_control import CacheHandler
from common.conf_control import get_data_path
from common import yaml_control
from utils.request_tool.request_control import RequestControl


class DependentCase:
    """处理依赖相关的业务"""
    def __init__(self, dependent_yaml_case):
        self.__yaml_case = dependent_yaml_case

    @classmethod
    def jsonpath_data(cls, obj, expr):
        _jsonpath_data = jsonpath(obj, expr)
        if _jsonpath_data is False:
            raise ValueError(f"jsonpath提取失败\n 提取的数据：{obj}\n jsonpath规则：{expr}")
        return _jsonpath_data

    def dependent_request(self, name, path):
        base_path = get_data_path()
        dependent_case_path = base_path + os.sep + path
        dependent_case = yaml_control.YamlReader(dependent_case_path)
        dependent_case_data = dependent_case.yamldata_all()
        for i in dependent_case_data:
            if i["case_name"] == name:
                res = RequestControl(i).request_control()
                return res

    def set_dependent_cache(self, _jsonpath, set_value, data):
        jsonpath_data = jsonpath(eval(data), _jsonpath)
        if len(jsonpath_data) > 1:
            CacheHandler.update_cache(cache_name=set_value, value=jsonpath_data)
        else:
            CacheHandler.update_cache(cache_name=set_value, value=jsonpath_data[0])

    def dependent_handler(self):
        dependent_type = self.__yaml_case["dependence_case"]
        dependent_case_datas = self.__yaml_case["dependence_case_data"]
        if dependent_type is True:
            for dependent_case_data in dependent_case_datas:
                _case_name = dependent_case_data["case_name"]
                _case_path = dependent_case_data["case_path"]
                _dependent_datas = dependent_case_data["dependent_data"]
                if _case_name == "self":
                    pass
                else:
                    for _dependent_data in _dependent_datas:
                        _dependent_type = _dependent_data["dependent_type"]
                        _jsonpath = _dependent_data["jsonpath"]
                        cache_name = _dependent_data["set_cache"]
                        res = self.dependent_request(name=_case_name, path=_case_path)
                        if _dependent_type == "response":
                            data = res.response_data
                            self.set_dependent_cache(_jsonpath=_jsonpath, set_value=cache_name, data=data)
                        elif _dependent_type == "request":
                            data = res.request_body
                            self.set_dependent_cache(_jsonpath=_jsonpath, set_value=cache_name, data=data)
                        else:
                            pass

















