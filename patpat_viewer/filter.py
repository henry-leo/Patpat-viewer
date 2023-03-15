"""用于分发符合条件的数据条目"""

import time

from patpat_viewer import checker


class Filter:
    """"""

    def __init__(self):
        self.given = {'datasets': dict(),
                      'accession': set(),
                      'condition': dict()}

    def __call__(self, given: dict):
        raise NotImplementedError

    def _loading(self,
                 given: dict,
                 ):
        """
        Args:
            given:
                ['datasets']: dict，完整的Patpat-viewer准入数据
                ['accession']: 可选，set，需要筛选的数据集的Patpat编号，默认为 None，意味着全部需要筛选，如：{"PAT0000","PAT0007"}
                ['condition']: 可选，dict，筛选条件
        """
        self.given['datasets'] = given['datasets']

        try:
            if given['accession']:
                self.given['accession'] = given['accession']
            elif given['accession'] is None:
                self.given['accession'] = set(given['datasets'].keys())
            elif not given['accession']:
                self.given['accession'] = set()
        except KeyError:
            self.given['accession'] = set(given['datasets'].keys())

        if given['condition']:
            self.given['condition'] = given['condition']
        else:
            self.given['condition'] = dict()

    def _comment_check(self):
        # 如果self.accession为空列表，说明无候选数据集
        if not self.given['accession']:
            return self.given

        # 如果self.condition为空，说明无筛选条件
        elif not self.given['condition']:
            return self.given

        # 如果输入的条件不是字典
        elif not isinstance(self.given['condition'], dict):
            print(f"Inputted conditions are mistake: {self.given['condition']}")
            return self.given
        else:
            return True

    def _condition_check(self):
        raise NotImplementedError


class YearFilter(Filter):
    """根据上传年份对数据集进行筛选"""

    def __init__(self):
        super().__init__()

    def __call__(self, given: dict):
        """

        Args:
            given: 由其他 Filter生成的筛选结果
                ['datasets']: dict，完整的Patpat-viewer准入数据
                ['accession']: 可选，set，需要筛选的数据集的Patpat编号，默认为 None，意味着全部需要筛选，如：{"PAT0000","PAT0007"}
                ['condition']: 可选，dict，筛选条件，如：{"start": "2006", "end": "2008"}

        Returns:
            given: 筛选结果

        """
        self._loading(given=given)

        check = self._comment_check()
        if check is True:
            check = self._condition_check()

        if check is True:
            start = time.strptime(self.given['condition']['start'], '%Y')
            end = time.strptime(str(int(self.given['condition']['end']) + 1), '%Y')

            accession = self.given['accession'].copy()
            for acc in accession:
                target = self.given['datasets'][acc]['time']
                if target:
                    target = time.strptime(target, '%Y-%m-%d')
                    if sorted([target, start, end])[1] != target:
                        self.given['accession'].remove(acc)
                else:
                    # iProX数据库没有时间信息，则不筛选
                    pass

            return self.given

        else:
            return check

    def _condition_check(self):
        """如果输入的字典格式不符合要求"""
        if 'start' or 'end' not in self.given['condition']:
            print(f"Filter condition are mistake: {self.given['condition']}")
            return self.given

        elif not self.given['condition']['start'] and not self.given['condition']['end']:
            # 空筛选
            return self.given
        else:
            # 表明可以进行筛选
            return True


class DatabaseFilter(Filter):
    """根据所属数据库对数据集进行筛选"""

    def __init__(self):
        super().__init__()

    def __call__(self, given: dict):
        """

        Args:
            given: 由其他 Filter生成的筛选结果
                ['datasets']: dict，完整的Patpat-viewer准入数据
                ['accession']: 可选，set，需要筛选的数据集的Patpat编号，默认为 None，意味着全部需要筛选，如：{"PAT0000","PAT0007"}
                ['condition']: 可选，dict，筛选条件，如：{"databases": ["PRIDE", "iProX"]}

        Returns:
            given: 筛选结果

        """
        self._loading(given=given)

        check = self._comment_check()
        if check is True:
            check = self._condition_check()

        if check is True:
            databases = self.given['condition']["databases"]

            accession = self.given['accession'].copy()
            for acc in accession:
                target = self.given['datasets'][acc]['database']
                if target not in databases:
                    self.given['accession'].remove(acc)

            return self.given

        else:
            return check

    def _condition_check(self):
        """如果输入的字典格式不符合要求"""
        databases = []
        for d in checker.Checker.__subclasses__():
            databases.extend([d().source])

        if "databases" not in self.given['condition']:
            print(f"Filter condition are mistake: {self.given['condition']}")
            return self.given

        for d in self.given['condition']["databases"]:
            if d not in databases:
                print(f"Filter condition are mistake: {self.given['condition']}")
                return self.given

        if not self.given['condition']["databases"]:
            # 空筛选
            return self.given

        return True


class KeywordFilter(Filter):
    def __init__(self):
        super().__init__()

    def __call__(self, given: dict):
        """

        Args:
            given: 由其他 Filter生成的筛选结果
                ['datasets']: dict，完整的Patpat-viewer准入数据
                ['accession']: 可选，set，需要筛选的数据集的Patpat编号，默认为 None，意味着全部需要筛选，如：{"PAT0000","PAT0007"}
                ['condition']: 可选，dict，筛选条件，如：{'keywords': ['proteomics', 'Hela Cell']}

        Returns:
            given: 筛选结果

        """
        self._loading(given=given)

        check = self._comment_check()
        if check is True:
            check = self._condition_check()

        if check is True:
            keywords = self.given['condition']['keywords']

            accession = self.given['accession'].copy()
            for acc in accession:
                target = self.given['datasets'][acc]['keywords']
                if not [i for i in target if i in keywords]:
                    self.given['accession'].remove(acc)

            return self.given

        else:
            return check

    def _condition_check(self):
        """如果输入的字典格式不符合要求"""
        if not isinstance(self.given['condition']['keywords'], list) or\
                'keywords' not in self.given['condition']:
            print(f"Filter condition are mistake: {self.given['condition']}")
            return self.given
        elif not self.given['condition']['keywords']:
            # 空筛选
            return self.given
        else:
            # 表明可以进行筛选
            return True
