from typing import Text
import jsonpath
import json
from utils.cache_tool.cache_control import CacheHandler


class SetCurrentRequestCache:
    """将用例中的请求或响应内容存入缓存"""
    def __init__(
            self,
            current_request_set_cache,
            request_data,
            response_data
    ):
        self.current_request_set_cache = current_request_set_cache
        self.request_data = {"data": request_data}
        self.response_data = response_data.text

    def set_request_cache(
            self,
            jsonpath_value: Text,
            cache_name: Text) -> None:
        """将接口的请求参数传入缓存"""
        _request_data = jsonpath.jsonpath(self.request_data, jsonpath_value)
        if _request_data is not False:
            CacheHandler.update_cache(cache_name=cache_name, value=_request_data[0])
        else:
            raise ValueError(
                "缓存设置失败，未检测到需要缓存的数据"
                f"请求参数：{self.request_data}"
                f"提取的jsonpath内容：{jsonpath_value}"
            )

    def set_response_cache(
            self,
            jsonpath_value: Text,
            cache_name: Text) -> None:
        _response_data = jsonpath.jsonpath(json.loads(self.response_data), jsonpath_value)
        if _response_data is not False:
            CacheHandler.update_cache(cache_name=cache_name, value=_response_data[0])
        else:
            raise ValueError(
                "缓存设置失败，未检测到需要缓存的数据"
                f"响应数据：{self.response_data}"
                f"提取的jsonpath内容：{jsonpath_value}"
            )

    def set_caches_main(self):
        if self.current_request_set_cache is not None:
            for i in self.current_request_set_cache:
                _type = i["type"]
                _jsonpath_value = i["jsonpath"]
                _cache_name = i["name"]
                if _type == "request":
                    self.set_request_cache(jsonpath_value=_jsonpath_value, cache_name=_cache_name)
                elif _type == "response":
                    self.set_response_cache(jsonpath_value=_jsonpath_value, cache_name=_cache_name)





