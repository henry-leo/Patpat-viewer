"""用于排序"""
import time
import random


class Sorter:
    def __init__(self):
        pass


class SubmitSorter(Sorter):
    def __init__(self, datasets: dict, accession: set, mode='recently'):
        super().__init__()
        self.name = 'submit'
        self.datasets = datasets
        self.accession = accession
        self._mode = mode

    def run(self):
        target = dict()
        for acc in self.accession:
            target[acc] = time.strptime(self.datasets[acc]['time'], '%Y-%m-%d')

        m = True
        if self._mode == 'recently':
            m = True
        elif self._mode == 'previously':
            m = False
        acc_sorted = [i[0] for i in sorted(target.items(), key=lambda d: d[1], reverse=m)]
        self.accession = acc_sorted


class RandomizeSorter(Sorter):
    def __init__(self, datasets: dict, accession: {set, list}, num: int = 5):
        super().__init__()
        self.name = 'randomize'
        self.datasets = datasets
        self.accession = accession
        self._num = num

    def run(self):
        try:
            accession = random.sample(self.accession, k=self._num)
        except ValueError(f'The number of datasets are smaller than the number of samples:'
                          f' {len(self.accession)} < {self._num}'):
            accession = self.accession

        self.accession = accession
        return self.accession
