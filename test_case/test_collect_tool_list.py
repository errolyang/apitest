import os
from common.assert_control import Assert
from common import conf_control
from common import yaml_control
import pytest
import allure
from utils.request_tool.request_control import RequestControl
# from utils.cache_tool.cache_control import _cache_config

collectlist_path = conf_control.get_data_path() + os.sep + "collect_tool_list.yml"
collectlist_case = yaml_control.YamlReader(collectlist_path)
collectlist_data = collectlist_case.yamldata_all()
# print(collectlist_data)


@allure.epic("开发平台接口")
@allure.feature("收藏模块")
class TestCollectToolList:
    @allure.story("收藏网址列表接口")
    @pytest.mark.parametrize("collect_list", collectlist_data, ids=[i["detail"] for i in collectlist_data])
    def test_collect_tool_list(self, collect_list):
        res = RequestControl(collect_list).request_control()
        assert_data = collect_list["assert"]
        response_data = res.response_data
        status_code = res.status_code
        Assert(assert_data=assert_data, response_data=response_data, status_code=status_code).assert_type_handle()

        """headers = collectlist_data["headers"]
        print(headers)
        regular_datas = re.findall(r"\$cache\{(.*?)\}", headers["cookies"])
        print(regular_datas)
        print(type(regular_datas))
        cache_data = CacheHandler.get_cache(regular_datas[0])
        print(cache_data)"""


if __name__ == "__main__":
    pytest.main(['-vs', 'test_collect_tool_list.py'])






