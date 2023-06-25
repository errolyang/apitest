"""
日志装饰器，控制日志输入，默认为True
设置为Flase，则程序不会打印日志
"""
from functools import wraps
from utils.logging_tool.log_control import INFO, ERROR


def log_decorator(switch: bool):
    """
    封装日志装饰器，打印请求和响应信息
    :param switch: 日志开关
    :return:
    """

    def decorator(func):
        @wraps(func)
        def swapper(*args, **kwargs):
            res = func(*args, **kwargs)
            # 判断日志为开启，才打印日志
            if switch:
                _log_msg = f"\n===================================================\n" \
                               f"用例标题：{res.detail}\n" \
                               f"请求路径：{res.url}\n" \
                               f"请求方法：{res.method}\n" \
                               f"请求头：{res.headers}\n" \
                               f"请求内容：{res.request_body}\n" \
                               f"响应内容：{res.response_data}\n" \
                               f"接口响应时长：{res.res_time} ms\n" \
                               f"Http状态码：{res.status_code}\n" \
                               "==================================================="
                # 判断正常的用例，日志打印为绿色
                if res.status_code == 200:
                    INFO.logger.info(_log_msg)
                # 失败的用例，日志打印为红色
                else:
                    ERROR.logger.error(_log_msg)
            return res
        return swapper
    return decorator







