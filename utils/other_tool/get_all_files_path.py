import os
# from common.conf_control import get_base_path


def get_all_files_path(file_path) -> list:
    """获取文件路径"""
    filename = []
    for path, dirs, files in os.walk(file_path):
        for _file_path in files:
            _path = os.path.join(path, _file_path)
            filename.append(_path)
    return filename
