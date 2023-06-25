import json
import requests
import allure
from utils.logging_tool.log_decorator import log_decorator
from utils.logging_tool.run_time_decorator import execution_time
from utils.other_tool.model import ResponseData
from typing import Dict, Text
from utils.cache_tool.regular_control import RegularControl
from utils.allure_tool.allure_tool import allure_step, allure_step_no
from utils.request_tool.set_current_request_cache import SetCurrentRequestCache
# from utils.request_tool.dependent_case import DependentCase


class RequestControl:
    """ 封装请求 """
    def __init__(self, case_data):
        self.case_data = case_data

    @classmethod
    def check_headers_str_null(cls, headers: Dict) -> Dict:
        """
        兼容用户未填写headers或者header值为int
        :param headers:
        :return:
        """
        if headers is None:
            headers = {"headers": None}
        else:
            headers = RegularControl(str(headers)).cache_regular()
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
        return headers

    def check_data_int(self, data):
        """处理请求数据值应该为int，但从cache中获取到的是str的情况"""

        if self.case_data["dependence_case"] == "True":
            for key, value in data.items():
                if isinstance(eval(value), int):
                    data[key] = eval(value)
        return data

    def request_type_for_json(self, **kwargs):
        _url = self.case_data["host"] + self.case_data["url"]
        _data = self.case_data["data"]
        _headers = self.check_headers_str_null(self.case_data["headers"])
        _method = self.case_data["method"]
        res = requests.request(
            method=_method,
            url=_url,
            headers=_headers,
            json=json.dumps(_data),
            verify=False,
            **kwargs
        )
        return res

    def request_type_for_data(self, regular_case_data, **kwargs):
        # _url = self.case_data["host"] + self.case_data["url"]
        _url = regular_case_data["host"] + regular_case_data["url"]
        # _data = self.case_data["data"]
        data = regular_case_data["data"]
        _data = self.check_data_int(data)
        _headers = self.check_headers_str_null(self.case_data["headers"])
        _method = self.case_data["method"]
        res = requests.request(
            method=_method,
            url=_url,
            headers=_headers,
            data=_data,
            verify=True,
            **kwargs
        )
        return res

    def request_type_for_params(self, **kwargs):
        _url = self.case_data["host"] + self.case_data["url"]
        _data = self.case_data["data"]
        _headers = self.check_headers_str_null(self.case_data["headers"])
        _method = self.case_data["method"]
        res = requests.request(
            method=_method,
            url=_url,
            headers=_headers,
            params=_data,
            verify=False,
            **kwargs
        )
        return res

    def request_type_for_none(self, regular_case_data, **kwargs):
        # _url = self.case_data["host"] + self.case_data["url"]
        _url = regular_case_data["host"] + regular_case_data["url"]
        _headers = self.check_headers_str_null(self.case_data["headers"])
        _method = self.case_data["method"]
        res = requests.request(
            method=_method,
            url=_url,
            headers=_headers,
            data=None,
            verify=True,
            **kwargs
        )
        return res

    @classmethod
    def response_elapsed_total_seconds(cls, res):
        """获取接口响应时长"""
        try:
            return round(res.elapsed.total_seconds() * 1000, 2)
        except AttributeError:
            return 0.00

    @classmethod
    def api_allure_step(
            cls,
            *,
            url: Text,
            headers: Text,
            method: Text,
            data: Text,
            assert_data: Text,
            res_time: Text,
            res: Text
    ) -> None:
        """在allure中记录请求数据"""
        allure_step_no(f"请求URL:{url}")
        allure_step_no(f"请求方式:{method}")
        allure_step("请求头", headers)
        allure_step("请求数据", data)
        allure_step("预期数据", assert_data)
        allure_step_no(f"请求耗时(ms):{str(res_time)}")
        allure_step("响应内容", res)

    def _check_params(self, res, yaml_data):
        _data = {
            "url": res.url,
            "detail": yaml_data["detail"],
            "response_data": res.text,
            "request_body": res.request.body, # yaml_data["data"]
            "method": yaml_data["method"],
            "headers": res.request.headers,
            "cookie": res.cookies,
            "assert_data": yaml_data["assert"],
            "res_time": self.response_elapsed_total_seconds(res),
            "status_code": res.status_code
        }
        return ResponseData(**_data)

    @log_decorator(True)
    @execution_time(3000)
    def request_control(self):
        from utils.request_tool.dependent_case import DependentCase

        request_type_mapping = {
            'json': self.request_type_for_json,
            'data': self.request_type_for_data,
            'params': self.request_type_for_params,
            'none': self.request_type_for_none
        }
        DependentCase(dependent_yaml_case=self.case_data).dependent_handler()
        case_data = RegularControl(self.case_data).cache_regular()
        # res = request_type_mapping.get(self.case_data["requestType"])()
        res = request_type_mapping.get(self.case_data["requestType"])(case_data)
        _res_data = self._check_params(res=res, yaml_data=case_data)
        self.api_allure_step(
            url=_res_data.url,
            headers=_res_data.headers,
            method=_res_data.method,
            data=_res_data.request_body,
            assert_data=str(_res_data.assert_data),
            res_time=str(_res_data.res_time),
            res=_res_data.response_data
        )
        SetCurrentRequestCache(
            current_request_set_cache=self.case_data["current_request_set_cache"],
            request_data=self.case_data["data"],
            response_data=res
        ).set_caches_main()
        return _res_data









