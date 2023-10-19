"""优化策略
    Author: github@luochang212
    Date: 2023-10-18
"""

import random


def jaccard_sim(lst1: list, lst2: list):
    intersection = len(set(lst1).intersection(lst2))
    return intersection / (len(lst1) + len(lst2) - intersection)

def hit_sim(lst1: list, lst2: list):
    lst1 = [(i, e) for i, e in enumerate(lst1)]
    lst2 = [(i, e) for i, e in enumerate(lst2)]
    return jaccard_sim(lst1, lst2)

def blow_sim(lst1: list, lst2: list):
    return jaccard_sim(lst1, lst2)


class Strategy:

    def __init__(self, possible_result, hist_attempt, strategy):
        self.possible_result = possible_result
        self.hist_attempt = hist_attempt
        self.strategy = strategy

    def jaccard_similarity(self, reverse=False):
        scores = list()
        pr = self.possible_result
        for i, e1 in enumerate(pr):
            score = 0
            for e2 in pr[:i] + pr[i+1:]:
                score += (hit_sim(e1, e2) + blow_sim(e1, e2))
            scores.append(round(score, 5))

        extreme_score = min(scores) if reverse else max(scores)
        return random.choice([r for s, r in zip(scores, pr) if s == extreme_score])

    def random(self):
        return random.choice([e for e in self.possible_result if e not in self.hist_attempt])

    def apply(self):
        if self.strategy == 'jaccard':
            return self.jaccard_similarity(reverse=False)
        elif self.strategy == 'jaccard:reverse':
            return self.jaccard_similarity(reverse=True)

        return self.random()


if __name__ == '__main__':
    s = Strategy([[3,2,3]],1,2)
