import pytest
import requests
from utils.cache_tool.cache_control import CacheHandler


@pytest.fixture(scope="session", autouse=True)
def login_cookie():
    """
    获取登陆cookie
    :return:
    """
    url = "https://www.wanandroid.com/user/login"
    data = {
        "username": 13816653014,
        "password": 123456
    }
    res = requests.post(url=url, data=data, verify=True)
    response_cookie = res.cookies
    cookies = ''
    for k, v in response_cookie.items():
        _cookie = k + "=" + v + ";"
        # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
        cookies += _cookie
        # 将登录接口中的cookie写入缓存中，其中login_cookie是缓存名称
    CacheHandler.update_cache(cache_name="login_cookie", value=cookies)

