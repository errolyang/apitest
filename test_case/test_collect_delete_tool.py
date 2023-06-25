import os
from common.assert_control import Assert
from common import conf_control
from common import yaml_control
import pytest
import allure
from utils.request_tool.request_control import RequestControl
# from utils.cache_tool.cache_control import _cache_config

deletetool_path = conf_control.get_data_path() + os.sep + "collect_delete_tool.yml"
deletetool_case = yaml_control.YamlReader(deletetool_path)
deletetool_data = deletetool_case.yamldata_all()


@allure.epic("开发平台接口")
@allure.feature("收藏模块")
class TestCollectToolList:
    @allure.story("删除收藏网址接口")
    @pytest.mark.parametrize("collect_deletetool", deletetool_data, ids=[i["detail"] for i in deletetool_data])
    def test_collect_tool_list(self, collect_deletetool):
        res = RequestControl(collect_deletetool).request_control()
        assert_data = collect_deletetool["assert"]
        response_data = res.response_data
        status_code = res.status_code
        Assert(assert_data=assert_data, response_data=response_data, status_code=status_code).assert_type_handle()


if __name__ == "__main__":
    pytest.main(['-vs', 'test_collect_delete_tool.py'])
