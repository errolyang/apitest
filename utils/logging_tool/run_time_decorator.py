"""
统计请求运行时长装饰器，如时长超时，会输出红色日志，
提示http请求超时，默认时长为 3000ms
"""
from utils.logging_tool.log_control import ERROR


def execution_time(number: int):
    """
    封装统计函数运行时长装饰器
    :param number: 函数运行时长默认值
    :return:
    """

    def decorator(func):
        def swapper(*args, **kwargs):
            res = func(*args, **kwargs)
            run_time = res.res_time
            if run_time > number:
                ERROR.logger.error(
                    "\n===================================\n"
                    "测试用例执行时间较长，请关注。\n"
                    "用例执行时长：%s ms\n"
                    "测试用例相关数据：%s\n"
                    "===================================="
                    , run_time, res)
            return res
        return swapper
    return decorator
