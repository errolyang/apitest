import types
from typing import Text, Dict, Callable, Union, Optional, List, Any
from pydantic import BaseModel
from dataclasses import dataclass


class ResponseData(BaseModel):
    url: Text
    detail: Text
    response_data: Text
    request_body: Any
    method: Text
    # sql_data: Dict
    # yaml_data: Dict
    headers: Any
    cookie: Dict
    assert_data: Dict
    res_time: Union[int, float]
    status_code: int
    # teardown: List["TearDown"] = None
    # teardown_sql: Union[None, List]


@dataclass
class TestMetrics:
    """用例执行数据"""
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text
    oneday: Text

