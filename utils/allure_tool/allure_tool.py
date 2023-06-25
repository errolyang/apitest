import json
import allure


def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    :return:
    """
    with allure.step(step):
        allure.attach(
            step,
            json.dumps(str(var), ensure_ascii=False, indent=4),
            allure.attachment_type.JSON
        )


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step:
    :return:
    """
    with allure.step(step):
        pass
