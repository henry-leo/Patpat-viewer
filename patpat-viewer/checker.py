"""用于数据准入
只有通过 checker，原始数据才能进入patpat-viewer
"""
import utility


class Checker:
    """基类"""
    def get_data(self):
        raise NotImplementedError


class PRIDEChecker(Checker):
    def __init__(self, task):
        self.task = task

    def get_data(self):
        try:
            utility.get_result_from_file(self.task)
        except FileNotFoundError:
            print('Please check task uuid')


class IPROXChecker(Checker):
    pass
