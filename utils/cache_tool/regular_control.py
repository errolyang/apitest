"""
正则读取缓存
"""
from utils.cache_tool.cache_control import CacheHandler
import re
from typing import Dict


class RegularControl:
    """通过正则的方式，读取缓存中的内容"""

    def __init__(self, regular_value):
        self.regular_value = regular_value

    def cache_regular(self):
        regular_datas = re.findall(r"\$cache\{(.*?)\}", str(self.regular_value))

        def value_handler(i: int) -> Dict:
            regular_data = CacheHandler.get_cache(regular_datas[i])
            _pattern = re.compile(r'\$cache\{' + str(regular_datas[i]) + r'\}')
            if i == 0:
                _value = re.sub(_pattern, str(regular_data), str(self.regular_value))
                return _value
            else:
                _value = re.sub(_pattern, str(regular_data), str(value_handler(i - 1)))
                return _value

        if len(regular_datas) == 1:
            cache_data = CacheHandler.get_cache(regular_datas[0])
            pattern = re.compile(r'\$cache\{' + regular_datas[0] + r'\}')
            value = re.sub(pattern, cache_data, str(self.regular_value))
            return eval(value)
        elif len(regular_datas) > 1:
            i = len(regular_datas)
            value = value_handler(i-1)
            return eval(value)
        elif len(regular_datas) == 0:
            return self.regular_value

















"""def cache_regular(value):
    
    regular_datas = re.findall(r"\$cache\{(.*?)\}", value)

    def value_handler(i):
        regular_data = CacheHandler.get_cache(regular_datas[i])
        pattern = re.compile(r'\$cache\{' + str(regular_datas[i]) + r'\}')
        if i == 0:
            value = re.sub(pattern, str(regular_data), str(value))
            return value
        else:
            value = re.sub(pattern, str(cache_data), value_handler(i - 1))
            return value


    if len(regular_datas) == 1:
        cache_data = CacheHandler.get_cache(regular_datas[0])
        pattern = re.compile(r'\$cache\{' + regular_datas[0] + r'\}')
        value = re.sub(pattern, str(cache_data), value)
        return value
    else:"""





