"""
分页
"""
import uuid

import utility


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
        try:
            self.data_origin = utility.get_result_from_file(self.task)
        except FileNotFoundError:
            print('Please check task uuid.')

    def _check_source(self):
        if self.data_origin:
            pass
        else:
            raise ValueError('Please check task uuid.')

        for s in self.data_origin.keys():
            if self.data_origin[s]:
                self.source.extend([s])

    def run(self, checkers: list):
        """运行检查"""
        data_checked = dict()
        for checker in checkers:
            if checker.source in self.source:
                checker.load(self.data_origin)
                checker.check()
                data_checked.update(checker.get())
            else:
                continue

        # 添加识别符
        for n, d in enumerate(data_checked.values()):
            self.data_checked.update({f'PAT{str(n).zfill(4)}': d})
        return self.data_checked

