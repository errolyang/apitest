import json
import os
from typing import List, Text
from common.conf_control import get_base_path
from utils.other_tool.get_all_files_path import get_all_files_path
from utils.other_tool.model import TestMetrics


class AllureFileClean:
    """allure报告清洗，提取业务需要的数据"""

    @classmethod
    def get_testcases(cls) -> List:
        """获取所有allure报告中用例执行情况"""
        # 将所有数据收集到files中
        files = []
        path = get_base_path() + os.sep + "report/html/data/test-cases"
        for i in get_all_files_path(path):
            with open(i, "r", encoding="utf-8") as file:
                data = json.load(file)
                files.append(data)
        return files

    def get_failed_case(self) -> List:
        """获取失败的用例标题和代码路径"""
        error_case = []
        for i in self.get_testcases():
            if i["status"] == "failed" or i["status"] == "broken":
                error_case.append((i["name"], i["fullname"]))
        return error_case

    def get_failed_case_detail(self) -> Text:
        """获取失败用例的相关内容"""
        data = self.get_failed_case()
        values = ""
        if len(data) >= 1:
            values = "失败的用例:\n"
            values += "         ************************\n"
            for i in data:
                values = "        " + i[0] + ":" + i[1] + "\n"
        return values

    @classmethod
    def get_case_count(cls) -> "TestMetrics":
        """统计用例数量"""
        try:
            file_name = get_base_path() + os.sep + "report/html/widgets/summary.json"
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                _case_count = data["statistic"]
                _time = data["time"]
                keep_keys = {"passed", "failed", "skipped", "broken", "total"}
                run_case_data = {k: v for k, v in data["statistic"].items() if k in keep_keys}
                # 判断运行用例总数大于0
                if _case_count["total"] > 0:
                    # 计算用例成功率
                    run_case_data["pass_rate"] = round(_case_count["passed"]/_case_count["total"] * 100, 2)
                else:
                    run_case_data["pass_rate"] = 0.0
                run_case_data["time"] = _time if _case_count["total"] == 0 else round(_time["duration"]/1000, 2)
                run_case_data["oneday"] = """
                                          8:00 起床吃饭
                                          9:00 睡回笼觉
                                          11:00 学习
                                          2:00 做饭吃饭
                                          3:00 躺着看电影
                                          4:00 学习
                                          一直一直学习学习
                                          """
                return TestMetrics(**run_case_data)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "程序中检查到您未生成allure报告，"
                "通常可能导致的原因是allure环境未配置正确，"
                "详情可查看如下博客内容："
                "https://blog.csdn.net/weixin_43865008/article/details/124332793"
            ) from exc


if __name__ == "__main__":
    AllureFileClean.get_case_count()











