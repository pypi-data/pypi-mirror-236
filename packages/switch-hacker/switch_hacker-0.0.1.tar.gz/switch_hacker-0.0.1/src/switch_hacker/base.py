"""通用函数集合
    Author: github@luochang212
    Date: 2023-10-18
"""

import random
from itertools import permutations, combinations


class Base:

    def __init__(self, n=4, replacement=False):
        """◌ ○ ● ◉ ◍ ◎"""
        self.balls = {
            'b': 'blue',
            'r': 'red',
            'y': 'yellow',
            'p': 'pink',
            'g': 'green',
            'w': 'white'
        }
        self.valid_balls = list(self.balls.keys())
        if n > len(self.balls):
            raise Exception("n <= len(self.balls)")
        self.n = n
        self.replacement = replacement

    @staticmethod
    def generate_result(balls, n, replacement=False):
        """生成答案"""
        if replacement:
            return [random.choice(balls) for _ in range(n)]
        else:
            random.shuffle(balls)
            return balls[:n]

    @staticmethod
    def check_attempt(attempt, n, valid_balls):
        """检查输入是否合法"""
        if len(attempt) != n:
            return False, 1
        if not all([e in valid_balls for e in attempt]):
            return False, 2
        return True, 0

    @staticmethod
    def feedback(attempt, res):
        """返回全对的个数、全对+半对的个数"""
        return (
            len([i for i in range(len(res)) if attempt[i] == res[i]]),
            sum([min(len([e1 for e1 in res if e1 == c]), len([e2 for e2 in attempt if e2 == c])) for c in set(res)])
        )

    @staticmethod
    def get_possible_result(attempt, feedback, valid_balls, n):
        """根据当前attempt计算答案的概率空间"""
        res = []
        for e in permutations(attempt, feedback[1]):
            remaining_balls = [b for b in valid_balls if b not in attempt]
            for r in permutations(remaining_balls, n - feedback[1]):
                # allocate position
                for indexs in combinations(range(n), len(e)):
                    inner = zip(indexs, e)
                    outer = zip([i for i in range(n) if i not in list(indexs)], r)
                    lst = [t[1] for t in sorted(list(inner) + list(outer), key=lambda e: e[0])]
                    assume_hit = [lst[i] for i in range(n) if attempt[i] in e and attempt[i] == lst[i]]
                    if len(assume_hit) == feedback[0]:
                        res.append(lst)
        return res

    @staticmethod
    def merge_possible_results(res1, res2):
        """结合历史概率空间计算新概率空间"""
        return [e for e in res1 if e in res2]


if __name__ == '__main__':
    b = Base()
    res = b.generate_result(b.valid_balls, b.n)
    attempt = ['r', 'b', 'g', 'y']
    flag, err_code = b.check_attempt(attempt, b.n, b.valid_balls)
    if not flag:
        raise Exception(f'err_code: {err_code}')
    x, y = b.feedback(attempt, res)
    hit_num, blow_num = x, y - x
    if hit_num == b.n:
        print('Winner!')

    print(f'attempt: {attempt}')
    print(f'res: {res}')
    print(f'hit_num: {hit_num}')
    print(f'blow_num: {blow_num}')

    possible_result = b.get_possible_result(attempt, (x, y), b.valid_balls, b.n)
    print("possible_result:")
    for i, e in enumerate(possible_result):
        print(e, end='\t')
        if i%3 == 2:
            print()
