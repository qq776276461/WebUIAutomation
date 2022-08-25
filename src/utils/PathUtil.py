import os
from pathlib import Path
import sys


def __get_project_abspath():
    current_file_path = os.getcwd()
    project_root_path = None
    for path in sys.path:
        if current_file_path == path:
            continue
        if current_file_path.__contains__(path):
            project_root_path = path
            break
    if not project_root_path:
        project_root_path = current_file_path
    return project_root_path


def path_join(*path, is_mkdir=True) -> str:
    """
    基于项目根目录开始的目录拼接
    :param path: 要拼接的目录名,可以传多个目录名
    :param is_mkdir: 如果拼接完成的路径不存在,是否需要创建该目录
    :return: 拼接后的完整路径
    """
    ab_path = Path(PROJECT_ROOT_PATH).joinpath(*path)
    if not ab_path.exists() and is_mkdir:
        ab_path.mkdir(parents=True, exist_ok=True)
    return str(ab_path)


PROJECT_ROOT_PATH = __get_project_abspath()
