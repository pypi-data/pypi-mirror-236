"""自动解算器
    Author: github@luochang212
    Date: 2023-10-18
    Usage: python auto_play.py
"""

import random
from .base import Base
from .strategy import Strategy


class AutoPlay(Base):

    def __init__(self, n=4, max_guess_times=100, strategy='random'):
        Base.__init__(self, n=n, replacement=False)
        self.max_guess_times = max_guess_times
        self.strategy = strategy
        print(f'mode: {strategy}')

    @staticmethod
    def gen_first_attempt(balls, n):
        random.shuffle(balls)
        return balls[:n]

    @staticmethod
    def gen_next_attempt(possible_result, hist_attempt, strategy='random'):
        return Strategy(possible_result, hist_attempt, strategy).apply()

    def single_test_stat(self, res):
        hist_attempt = list()
        possible_result = list()

        i = 0
        while i < self.max_guess_times:
            # 猜答案
            if i == 0:
                attempt = self.gen_first_attempt(self.valid_balls, self.n)
            else:
                attempt = self.gen_next_attempt(possible_result, hist_attempt, strategy=self.strategy)

            # 检测输入是否合法
            chk, err_code = self.check_attempt(attempt, self.n, self.valid_balls)
            if not chk:
                raise Exception(f'err_code: {err_code}')

            # 验证答案是否正确
            x, y = self.feedback(attempt, res)
            if x == self.n:
                return 1, i + 1

            hist_attempt.append(attempt)

            # 计算答案概率空间
            if i == 0:
                possible_result = self.get_possible_result(attempt, (x, y), self.valid_balls, self.n)
            else:
                tmp_result = self.get_possible_result(attempt, (x, y), self.valid_balls, self.n)
                possible_result = self.merge_possible_results(tmp_result, possible_result)

            i += 1

        return 0, self.max_guess_times

    def single_test_debug(self, res):
        print(f'Answer: {res}')

        hist_attempt = list()
        possible_result = list()

        i = 0
        while i < self.max_guess_times:
            # 猜答案
            if i == 0:
                attempt = self.gen_first_attempt(self.valid_balls, self.n)
            else:
                attempt = self.gen_next_attempt(possible_result, hist_attempt, strategy=self.strategy)
            print(f'attempt {i+1}: {attempt}')

            # 检测输入是否合法
            chk, err_code = self.check_attempt(attempt, self.n, self.valid_balls)
            if not chk:
                raise Exception(f'err_code: {err_code}')

            # 验证答案是否正确
            x, y = self.feedback(attempt, res)
            if x == self.n:
                print(f'Winner!')
                return 1, i + 1

            hist_attempt.append(attempt)

            # 计算答案概率空间
            if i == 0:
                possible_result = self.get_possible_result(attempt, (x, y), self.valid_balls, self.n)
            else:
                tmp_result = self.get_possible_result(attempt, (x, y), self.valid_balls, self.n)
                possible_result = self.merge_possible_results(tmp_result, possible_result)

            i += 1
        print('Too bad...')
        return 0, self.max_guess_times


if __name__ == '__main__':
    ap = AutoPlay(strategy='similarity')
    ap.single_test_debug(['r', 'g', 'w', 'b'])
    # print(ap.single_test_stat(['r', 'g', 'w', 'b']))
