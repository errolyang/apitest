"""
缓存内容处理
"""

_cache_config = {}


class CacheHandler:

    @staticmethod
    def get_cache(cache_data):
        try:
            return _cache_config[cache_data]
        except KeyError:
            raise KeyError(f"{cache_data}的缓存数据未找到，请检查是否将该数据存入缓存中")

    @staticmethod
    def update_cache(cache_name, value):
        _cache_config[cache_name] = value




