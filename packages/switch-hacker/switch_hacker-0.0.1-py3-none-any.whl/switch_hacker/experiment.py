"""实验统计
    Author: github@luochang212
    Date: 2023-10-18
    Usage: python experiment.py
"""

import time
from collections import Counter
import numpy as np
from multiprocessing import Pool
from .auto_play import AutoPlay


def timer(func):
    def f(*args, **kwargs):
        start = time.perf_counter()
        rv = func(*args, **kwargs)
        print(f'time taken: {(time.perf_counter() - start):.2f} seconds')
        return rv
    return f


class Experiment(AutoPlay):

    def __init__(self, n=4, max_guess_times=100, strategy='random', iter_num=1000):
        AutoPlay.__init__(self, n=n, max_guess_times=max_guess_times, strategy=strategy)
        self.iter_num = iter_num

    @staticmethod
    def repo(lst):
        print(f'avg: {np.mean(lst):.3f}')
        print(f'var: {np.var(lst):.3f}')
        print(f'mdn: {np.median(lst)}')
        print(f'max: {max(lst)}')
        print(f'min: {min(lst)}')
        print(f'distribution: {dict(sorted(Counter(lst).items(), key=lambda e: e[0]))}')

    @timer
    def main(self):
        # print(self.single_test_stat(self.generate_result(self.valid_balls, self.n)))
        with Pool(processes=4) as pool:
            tasks = [self.generate_result(self.valid_balls, self.n) for _ in range(self.iter_num)]
            res = pool.map(self.single_test_stat, tasks)

            success_times = sum([k for k, _ in res])
            guess_num_list = [v for k, v in res if k == 1]

            print(f'success_times: {success_times}')
            self.repo(guess_num_list)


if __name__ == '__main__':
    e1 = Experiment(iter_num=1000, strategy='random')
    e1.main()

    print()

    e2 = Experiment(iter_num=1000, strategy='jaccard')
    e2.main()
