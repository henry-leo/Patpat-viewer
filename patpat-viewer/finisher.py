"""数据导入、排序和分页处理器
"""

import uuid

import checker
import filter
import sorter
import utility


class ImportFinisher:
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
            d['accession'] = f'PAT{str(n).zfill(4)}'
            self.data_checked.update({f'PAT{str(n).zfill(4)}': d})
        return self.data_checked


class FiltrateFinisher:
    """"""

    def __init__(self, datasets: dict, condition: dict):
        self.accession_filtered = set()
        self.datasets = datasets
        self.condition = condition
        self._given = {'datasets': self.datasets, 'condition': self.condition}
        self._detect()

    def _detect(self):
        """检查condition是否完整"""
        if 'start' not in self._given['condition']:
            raise ValueError(f"please check the input {self._given['condition']}")
        if 'end' not in self._given['condition']:
            raise ValueError(f"please check the input {self._given['condition']}")
        if 'databases' not in self._given['condition']:
            raise ValueError(f"please check the input {self._given['condition']}")
        if 'keywords' not in self._given['condition']:
            raise ValueError(f"please check the input {self._given['condition']}")

    def run(self):
        """"""
        filters = [f() for f in filter.Filter.__subclasses__()]

        filter_ = dict()
        for i in range(0, len(filters)):
            if i == 0:
                filter_ = filters[i](given=self._given)
            else:
                filter_ = filters[i](given=filter_)

        self.accession_filtered = filter_['accession']
        return self.accession_filtered


class SortFinisher:
    """"""

    def __init__(self, datasets, accession, mode: str, key: {str, int}):
        self.accession = []
        self.datasets_sorted = []
        if mode == 'submit':
            self._sorter = sorter.SubmitSorter(datasets=datasets,
                                               accession=accession,
                                               mode=key)
        elif mode == 'randomize':
            self._sorter = sorter.RandomizeSorter(datasets=datasets,
                                                  accession=accession,
                                                  num=key)

    def run(self):
        self._sorter.run()
        self.accession = self._sorter.accession
        datasets_sorted = [self._sorter.datasets[acc] for acc in self._sorter.accession]
        self.datasets_sorted = datasets_sorted
        return self.accession


class PaginateFinisher:
    """"""

    def __init__(self, data: {list, dict}=None, run_per_page=5):
        self.pagination = None
        self.groups = list()
        self.run_per_page = run_per_page

        self._data = data

    def run(self):
        if self._data:
            if isinstance(self._data, dict):
                self._data = [i for i in self._data.values()]
        elif self._data is None:
            self._data = utility.config_process()

        groups = utility.group_list(self._data, self.run_per_page)
        pagination = range(1, len(groups) + 1)

        self.groups = groups
        self.pagination = pagination

        return self.groups
