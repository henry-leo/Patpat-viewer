"""数据导入和分页处理器
"""
import uuid

import utility
import checker


class SourceFinisher:
    """导入并检查数据"""

    def __init__(self, task: str):
        try:
            uuid.UUID(task)
        except ValueError:
            print('Please check uuid.')
        else:
            self.task = task
            self.data_origin = dict()
            self.data_checked = dict()
            self.source = []
            self._load_source()
            self._check_source()

    def _load_source(self):
        """从Patpat搜索结果的json文件中导入数据"""
        try:
            self.data_origin = utility.get_result_from_file(self.task)
        except FileNotFoundError:
            print('Please check task uuid.')

    def _check_source(self):
        """确定Patpat搜索结果对应的数据库"""
        if self.data_origin:
            pass
        else:
            raise ValueError('Please check task uuid.')

        for s in self.data_origin.keys():
            if self.data_origin[s]:
                self.source.extend([s])

    def run(self, checkers: list = None):
        """运行并检查 **BETA**
        默认根据数据选择对应的检查器（Checker），但用户也可自定义Checker
        """
        data_checked = dict()

        if not checkers:
            checkers = [c() for c in checker.Checker.__subclasses__()]
        else:
            pass

        for checker_ in checkers:
            if checker_.source in self.source:
                checker_.load(self.data_origin)
                checker_.check()
                data_checked.update(checker_.get())
            else:
                continue

        # 添加Patpat识别符
        for n, d in enumerate(data_checked.values()):
            self.data_checked.update({f'PAT{str(n).zfill(4)}': d})
        return self.data_checked
