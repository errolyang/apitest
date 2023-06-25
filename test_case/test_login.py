import pytest
import allure
import os
from common.assert_control import Assert
from common import conf_control
from common import yaml_control
from utils.request_tool.request_control import RequestControl
# from utils.cache_tool.cache_control import _cache_config

login_path = conf_control.get_data_path() + os.sep + "login.yml"
login_case = yaml_control.YamlReader(login_path)
login_data = login_case.yamldata_all()
# print(login_data)


@allure.epic("开发平台接口")
@allure.feature("登录模块")
class TestLogin:

    @allure.story("登录")
    @pytest.mark.parametrize("login", login_data, ids=[i["detail"] for i in login_data])
    def test_login(self, login):
        # res_url = login["host"] + login["url"]
        # data = login["data"]
        # res = requests.post(url=res_url, data=data)
        res = RequestControl(login).request_control()
        assert_data = login["assert"]
        response_data = res.response_data
        status_code = res.status_code
        Assert(assert_data=assert_data, response_data=response_data, status_code=status_code).assert_type_handle()

# print(res_url)
# print(data)
# print(res.json())
# print(res.headers)
# print(res.cookies)

"""
code_json = login_data["assert"]["errorCode"]["jsonpath"]
#print(code_json)
errorcode = jsonpath.jsonpath(res.json(),code_json)
#print(errorcode[0])
excepted_code = login_data["assert"]["errorCode"]["value"]
assert_res = AssertControl()
assert_re01 = assert_res.assert_code(errorcode[0],excepted_code)
#print(assert_re01)
username_json = login_data["login_01"]["assert"]["username"]["jsonpath"]
username = jsonpath.jsonpath(res.json(),username_json)
excepted_username = login_data["login_01"]["assert"]["username"]["value"]
assert_re02 = assert_res.assert_body(username[0],excepted_username)
#print(assert_re02)
"""

if __name__ == "__main__":
    pytest.main(['-vs', 'test_login.py'])

