"""用于数据准入
只有通过 checker，原始数据才能进入patpat-viewer

    Typical usage example:
    典型用法示例：

    import patpat-viewer.checker as checker
    import patpat-viewer.finisher as finisher

    uuid = '3d5b4e1d-937c-4661-83a2-b6ed7c19f060'

    data = finisher.SourceFinisher(uuid)
    data.run([checker.PRIDEChecker()])
"""

import time


class Checker:
    """基类
    self.source 是必要的变量
    """
    def load(self, data):
        """"""
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PRIDEChecker(Checker):
    """"""

    def __init__(self):
        self.source = 'PRIDE'
        self.data_origin = None
        self.data_checked = None

    def load(self, data):
        """"""
        self.data_origin = data[self.source]

    def check(self):
        """"""
        data_checked = dict()
        data_origin = self._precheck()

        for idr in data_origin.keys():
            data_checked[idr] = {
                # database ref
                'title': data_origin[idr]['title'],
                'database': 'PRIDE',
                'identifier': data_origin[idr]['accession'],
                'time': data_origin[idr]['submissionDate'],
                'authors': set(
                    [n['name'].upper().capitalize() for n in data_origin[idr]['submitters']] +
                    [n['name'].upper().capitalize() for n in data_origin[idr]['labPIs']]
                ),

                'keywords': data_origin[idr]['keywords'],
                # patpat ref
                'summary': data_origin[idr]['summary'],
                'website': data_origin[idr]['website'],
                'protein': data_origin[idr]['protein'],
                'peptides': data_origin[idr]['peptides'],
            }
        self.data_checked = data_checked

    def get(self):
        if self.data_checked:
            return self.data_checked

    def _precheck(self):
        if self.data_origin:
            data_origin = self.data_origin.copy()
        else:
            raise FileExistsError('No data. Please call PRIDEChecker.load().')

        for data in data_origin.values():
            self._check_title(data)
            self._check_time(data)
            self._check_authors(data)

        return data_origin

    def _check_title(self, data: dict):
        d = data.copy()
        if d['title']:
            pass
        else:
            print(f"{d['accession']} no title")
        if isinstance(d['title'], str):
            pass
        else:
            print(f"{d['accession']} title has some issues. show: {d['title']}")

    def _check_time(self, data: dict):
        d = data.copy()
        t = d['submissionDate']
        if t:
            pass
        else:
            print(f"{d['accession']} no submissionDate")

        if time.strftime('%Y-%m-%d', time.strptime(t, '%Y-%m-%d')) == t:
            pass
        else:
            print(f"{d['accession']} submissionDate has some issues. show: {t}")

    def _check_authors(self, data: dict):
        d = data.copy()
        try:
            a1 = [n['name'] for n in d['submitters']]
            a2 = [n['name'] for n in d['labPIs']]
        except KeyError:
            print(f"{d['accession']} title has some issues. show: {d['submitters']}, d['labPIs']")
        else:
            if a1 or a2:
                pass
            else:
                print(f"{d['accession']} no authors")


class IPROXChecker(Checker):
    """"""
    pass
