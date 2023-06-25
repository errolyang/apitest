import smtplib
from email.mime.text import MIMEText
from utils.other_tool.model import TestMetrics
from utils.allure_tool.allure_report_data import AllureFileClean
from common.conf_control import Confdefault, get_default_path
from common.yaml_control import YamlReader


class SendEmail:
    """发送邮件"""
    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics
        self.allure_data = AllureFileClean()
        self.casedetail = self.allure_data.get_failed_case_detail()

    @classmethod
    def send_email(cls, user_list: list, sub, content: str) -> None:
        config = YamlReader(get_default_path()).yamldata()
        user = "ymc" + "<" + Confdefault(config=config).get_email_send_user() + ">"
        message = MIMEText(content, _subtype="plain", _charset="utf-8")
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)
        server = smtplib.SMTP()
        server.connect(Confdefault(config=config).get_email_host())
        server.login(Confdefault(config=config).get_email_send_user(), Confdefault(config=config).get_email_stamp_key())
        server.sendmail(user, user_list, message.as_string())
        server.close()

    def error_email(self, error_message: str) -> None:
        """异常通知邮件"""
        config = YamlReader(get_default_path()).yamldata()
        email = Confdefault(config=config).get_email_send_list()
        user_list = email.split(",")
        sub = Confdefault(config=config).get_project_name() + "接口自动化执行异常通知"
        content = f"接口自动化执行完毕，程序出现异常，报错信息如下：\n{error_message}"
        self.send_email(user_list, sub, content)

    def send_main(self):
        config = YamlReader(get_default_path()).yamldata()
        email = Confdefault(config=config).get_email_send_list()
        user_list = email.split(",")
        sub = Confdefault(config=config).get_project_name() + "接口自动化执行报告"
        content = f"""
        各位同事，大家好：
           接口自动化用例执行完成，结果如下：
           用例运行总数：{self.metrics.total}
           通过用例个数：{self.metrics.passed}
           失败用例个数：{self.metrics.failed}
           异常用例个数：{self.metrics.broken}
           跳过用例个数：{self.metrics.skipped}
           成功率：{self.metrics.pass_rate}
           
           
        dear xuan：
            ppt你就不要想了，除非你先给我写
            以下是我的日常，你不要太羡慕了哦
            {self.metrics.oneday}
            怎么样，我还是很听话的吧
            那么我忽悠过你的过去，咱们就一笔勾销了吧！
           
        {self.casedetail}
        """
        self.send_email(user_list, sub, content)


if __name__ == "__main__":
    SendEmail(AllureFileClean.get_case_count()).send_main()






