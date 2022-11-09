"""
分页
"""
import uuid

import utility


class SourceFinisher:
    def __init__(self, task: str):
        try:
            uuid.UUID(task)
        except ValueError:
            print('Please _check_source uuid.')
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
            print('Please _check_source task uuid.')

    def _check_source(self):
        if self.data_origin:
            pass
        else:
            raise ValueError('Please call GenericChecker()._load_source() first.')

        for s in self.data_origin.keys():
            if self.data_origin[s]:
                self.source.extend([s])

    def run(self, checkers: list):
        """"""
        data_checked = dict()
        for checker in checkers:
            if checker.source in self.source:
                checker.load(self.data_origin)
                checker.check()
                data_checked.update(checker.get())
            else:
                continue

        for n, d in enumerate(data_checked.values()):
            self.data_checked.update({f'PAT{str(n).zfill(4)}': d})
        return self.data_checked

