# 断言封装

import json
import jsonpath


class AssertUtil:

    def __init__(self, assert_data, response_data, status_code):
        self.assert_data = assert_data
        self.response_data = response_data
        self.status_code = status_code

    def assert_code(self, check_value, excepted_value):
        try:
            assert int(check_value) == int(excepted_value)
            return True
        except:
            raise AssertionError("check_value error,check_value is %s,excepted_value is %s"
                                 % (check_value, excepted_value))

    def assert_body(self, check_value, excepted_value):
        try:
            assert check_value == excepted_value
            return True
        except:
            raise AssertionError("check_value error,check_value is %s,excepted_value is %s"
                                 % (check_value, excepted_value))

    def assert_in_body(self, check_value, excepted_value):
        try:
            check_value = json.dumps(check_value)
            assert excepted_value in check_value
            return True
        except:
            raise AssertionError("不包含或者check_value错误，check_value is %s,excepted_value is %s"
                                 % (check_value, excepted_value))

    @property
    def get_assert_data(self):
        assert self.assert_data is not None, ("'%s' should either include a 'assert_data' attribute"
                                              % self.__class__.__name__)
        return self.assert_data

    @property
    def get_type(self):
        assert 'type' in self.get_assert_data.keys(), ("断言数据：'%s' 中缺少 'type' 属性" % self.get_assert_data)
        name = self.get_assert_data.get("type")
        if name == 'code':
            assert_type = 'assert_code'
        elif name == 'body':
            assert_type = 'assert_body'
        else:
            assert_type = 'assert_in_body'
        return assert_type

    @property
    def get_value(self):
        assert 'value' in self.get_assert_data.keys(), ("断言数据：'%s' 中缺少 'value' 属性" % self.get_assert_data)
        return self.get_assert_data.get("value")

    @property
    def get_jsonpath(self):
        assert 'jsonpath' in self.get_assert_data.keys(), ("断言数据：'%s' 中缺少 'jsonpath' 属性" % self.get_assert_data)
        return self.get_assert_data.get("jsonpath")

    @property
    def get_asserttype(self):
        assert 'AssertType' in self.get_assert_data.keys(), ("断言数据：'%s' 中缺少 'AssertType' 属性" % self.get_assert_data)
        return self.get_assert_data.get("AssertType")

    @property
    def get_response_data(self):
        return json.loads(self.response_data)

    def _assert(self, check_value, excepted_value):
        assert_type = self.get_type
        if assert_type == 'assert_code':
            return self.assert_code(check_value, excepted_value)
        elif assert_type == 'assert_body':
            return self.assert_body(check_value, excepted_value)
        else:
            return self.assert_in_body(check_value, excepted_value)

    @property
    def _assert_resp_data(self):
        resp_data = jsonpath.jsonpath(self.get_response_data, self.get_jsonpath)
        assert resp_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.get_response_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(resp_data) > 1:
            return resp_data
        return resp_data[0]

    def assert_type_handle(self):
        return self._assert(self._assert_resp_data, self.get_value)


class Assert(AssertUtil):

    def assert_data_list(self):
        assert_list = []
        for k, v in self.assert_data.items():
            if k == "status_code":
                assert self.status_code == v, "响应状态码断言失败"
            else:
                assert_list.append(v)
        return assert_list

    def assert_type_handle(self):
        for i in self.assert_data_list():
            self.assert_data = i
            result = super().assert_type_handle()
            return result
