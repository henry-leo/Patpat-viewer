"""用于分发符合条件的数据条目

筛选、排序
"""


class YearFilter:
    """根据上传年份进行对数据集筛选"""
    def __init__(self, data: dict, acc: list):
        self.data = data.copy()

        if acc:
            self.acc = acc
        else:
            self.acc = []

    def __call__(self, *args, **kwargs):
        pass
