"""用于数据准入
只有通过 checker，原始数据才能进入patpat-viewer

    Typical usage example:
    典型用法示例：

    import patpat_viewer.checker as checker
    import patpat_viewer.finisher as finisher

    uuid = '3d5b4e1d-937c-4661-83a2-b6ed7c19f060'

    data = finisher.SourceFinisher(uuid)
    data.run([checker.PRIDEChecker()])
"""

import re
import time


class Checker:
    """基类
    self.source 是必要的变量
    """

    def __init__(self):
        self.source = None
        self.data_origin = None
        self.data_checked = None

    def load(self, data):
        """"""
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PRIDEChecker(Checker):
    """PRIDE数据库搜索结果检查器

    """

    def __init__(self):
        super().__init__()
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

    @staticmethod
    def _check_title(data: dict):
        d = data.copy()
        if d['title']:
            pass
        else:
            print(f"{d['accession']} no title")
        if isinstance(d['title'], str):
            pass
        else:
            print(f"{d['accession']} title has some issues. show: {d['title']}")

    @staticmethod
    def _check_time(data: dict):
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

    @staticmethod
    def _check_authors(data: dict):
        d = data.copy()
        try:
            a1 = [n['name'] for n in d['submitters']]
            a2 = [n['name'] for n in d['labPIs']]
        except KeyError:
            print(f"{d['accession']} has some issues. show: {d['submitters'], d['labPIs']}")
        else:
            if a1 or a2:
                pass
            else:
                print(f"{d['accession']} no authors")


class IPROXChecker(Checker):
    """iProX数据库搜索结果检查器

    """

    def __init__(self):
        super().__init__()
        self.source = 'iProX'
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
                'database': 'iProX',
                'identifier': data_origin[idr]['accession']['value'],
                'time': None,
                'authors': set([j['contactProperties'][1]['value'] for j in
                                [i for i in data_origin[idr]['contacts']]
                                if j['contactProperties'][1]['name'] == 'contact name']),
                'keywords': re.split('[,;]', data_origin[idr]['keywords'][0]['value']),
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
            # self._check_time(data)
            self._check_authors(data)

        return data_origin

    @staticmethod
    def _check_title(data: dict):
        d = data.copy()
        if d['title']:
            pass
        else:
            print(f"{d['accession']} no title")
        if isinstance(d['title'], str):
            pass
        else:
            print(f"{d['accession']} title has some issues. show: {d['title']}")

    @staticmethod
    def _check_time(data: dict):
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

    @staticmethod
    def _check_authors(data: dict):
        d = data.copy()
        try:
            a1 = [n['contactProperties'] for n in d['contacts']]
            authors = []
            for n in a1:
                authors.extend([n[1]['value']])
        except KeyError:
            print(f"{d['accession']['value']} title has some issues. show: {d['contacts']}")
        else:
            if authors:
                pass
            else:
                print(f"{d['accession']['value']} no authors")


class MASSIVEChecker(Checker):
    # MassIVE数据库搜索结果检查器 **BETA**

    def __init__(self):
        super().__init__()
        self.source = 'MassIVE'
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
                'database': 'MassIVE',
                'identifier': f"{data_origin[idr]['MASSIVE']['dataset_name']}/"
                              f"{data_origin[idr]['MASSIVE']['origin_identifier']}",
                'time': self.refine_time(data_origin[idr]['MASSIVE']['create_time']),
                'authors': set([i[1]['value'] for i in data_origin[idr]['PROXI']['contacts']
                                if i[1]['name']
                                ]),
                'keywords': re.split('[,;]', data_origin[idr]['MASSIVE']['keywords']),
                # patpat ref
                'summary': data_origin[idr]['summary'],
                'website': data_origin[idr]['website'],
                'protein': self.find_targets(data_origin[idr]['MASSIVE']['target'], 'protein'),
                'peptides': self.find_targets(data_origin[idr]['MASSIVE']['target'], 'peptides'),
            }
        self.data_checked = data_checked

    def get(self):
        if self.data_checked:
            return self.data_checked

    def _precheck(self):
        """"""
        if self.data_origin:
            data_origin = self.data_origin.copy()
        else:
            raise FileExistsError('No data. Please call PRIDEChecker.load().')

        for data in data_origin.values():
            self._check_title(data)
            self._check_time(data)
            self._check_authors(data)
        return data_origin

    @staticmethod
    def _check_title(data):
        d = data.copy()
        if d['title']:
            pass
        else:
            print(f"{d['MASSIVE']['dataset_name']} no title")
        if isinstance(d['title'], str):
            pass
        else:
            print(f"{d['MASSIVE']['dataset_name']} title has some issues. show: {d['title']}")

    def _check_time(self, data: dict):
        d = data.copy()
        time_ = d['MASSIVE']['create_time']
        title = d['MASSIVE']['dataset_name']

        if time_:
            pass
        else:
            print(f"{title} no submissionDate")

        try:
            self.refine_time(time_)
        except ValueError:
            print(f"{title} submissionDate has some issues. show: {time_}")

    @staticmethod
    def _check_authors(data: dict):
        d = data.copy()
        title = d['MASSIVE']['dataset_name']
        try:
            set([i[1]['value'] for i in d['PROXI']['contacts']
                 if i[1]['name']
                 ]),
        except KeyError:
            print(f"{title}  has some issues. show: {d['PROXI']['contacts']}")
        else:
            pass

    @staticmethod
    def refine_time(input_time):
        """

        Args:
            input_time: str, origin MassIVE create_time (%Y-%m-%d %H:%M:%S.0)

        Returns:
            refined: str, refined MassIVE create_time (%Y-%m-%d)

        """
        formated = time.strptime(input_time, '%Y-%m-%d %H:%M:%S.0')
        refined = time.strftime('%Y-%m-%d', formated)
        return refined

    @staticmethod
    def find_targets(input_target: dict, mode: str):
        """"""
        if mode == 'protein':
            try:
                return input_target['protein']
            except KeyError:
                return []
        if mode == 'peptides':
            try:
                return input_target['peptides']
            except KeyError:
                return []
