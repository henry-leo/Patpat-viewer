"""用于分发符合条件的数据条目

筛选、排序
"""


class YearFilter:
    """根据上传年份进行对数据集筛选"""
    def __init__(self, data: dict,
                 accession: list = None,
                 condition: dict = None,
                 ):
        """
        Args:
            data: 完整的Patpat-viewer准入数据
            accession: 可选，需要筛选的数据集的Patpat编号，默认为None，意味着全部需要筛选。
            condition: 可选，筛选条件
        """
        self.data = data.copy()

        if accession:
            self.accession = accession
        elif accession is None:
            self.accession = list(data.keys())
        elif not accession:
            self.accession = None

        if condition:
            self.condition = condition
        else:
            self.condition = None

    def __call__(self, *args, **kwargs):
        # 如果self.accession为空列表，说明无候选数据集
        if not self.accession:
            return self.data, []

        # 如果self.condition为空，说明无筛选条件
        elif not self.condition:
            return self.data, self.accession

        # 如果self.accession和self.condition均不为空，进行筛选
        elif self.condition:
            pass
