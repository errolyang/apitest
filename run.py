import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11")
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages")

import os
import pytest
import traceback
from utils.allure_tool.allure_report_data import AllureFileClean
from utils.other_tool.send_email import SendEmail


def run():
    try:
        pytest.main(['-vs', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                     '--alluredir', './report/tmp', '--clean-alluredir'])
        os.system(r"allure generate ./report/tmp -c -o ./report/html")
        os.system(f"allure serve ./report/tmp -h 127.0.0.1 -p 9999")
        allure_data = AllureFileClean.get_case_count()
        SendEmail(allure_data).send_main()

    except Exception:
        e = traceback.format_exc()
        send_mail = SendEmail(AllureFileClean.get_case_count())
        send_mail.error_email(e)
        raise


if __name__ == "__main__":
    run()
