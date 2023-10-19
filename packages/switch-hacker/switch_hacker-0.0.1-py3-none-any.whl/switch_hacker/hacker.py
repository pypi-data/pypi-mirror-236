"""作弊器
    Author: github@luochang212
    Date: 2023-10-18
    Usage: python auto_play.py
"""

from .auto_play import AutoPlay


class Hacker(AutoPlay):

    def __init__(self, n=4, max_guess_times=15, strategy='random'):
        AutoPlay.__init__(self, n=n, max_guess_times=max_guess_times, strategy=strategy)

    @staticmethod
    def show_hacker_prompt(balls):
        num = 34
        print('{} PROMPT {}\n- Valid balls: {}\n- Feedback: X Hits! Y Blows! (X and Y should be separated by blank space)\n- An example of your input: 2 1\n{}'.format(
            '=' * num,
            '=' * num,
            ', '.join([k + ' (' + v + ')' for k, v in balls.items()]).strip(),
            '=' * (2 * num + 8)
        ))
    
    @staticmethod
    def show_feedback_prompt():
        print('\nPlease enter the feedback:')

    @staticmethod
    def check_feedback(feedback, n):
        vals = [e for e in range(0, n+1)]
        if len(feedback) != 2:
            return False, 1
        elif not feedback[0].isdigit():
            return False, 2
        elif not feedback[1].isdigit():
            return False, 3
        elif int(feedback[0]) not in vals:
            return False, 2
        elif int(feedback[1]) not in vals:
            return False, 3
        elif int(feedback[0]) + int(feedback[1]) not in vals:
            return False, 4
        return True, 0

    def main(self):
        self.show_hacker_prompt(self.balls)

        hist_attempt = list()
        possible_result = list()

        i, t = 0, 0
        max_tries = 3
        while i < self.max_guess_times:
            # 猜答案
            if i == 0:
                attempt = self.gen_first_attempt(self.valid_balls, self.n)
            else:
                attempt = self.gen_next_attempt(possible_result, hist_attempt, strategy=self.strategy)
            print(f'\n=> attempt {i+1}: {attempt}')

            # 检测小球是否合法
            chk, err_code = self.check_attempt(attempt, self.n, self.valid_balls)
            if not chk:
                raise Exception(f'ball err_code: {err_code}')

            # 获取反馈
            self.show_feedback_prompt()
            feedback = input().strip().split(' ')

            # 检测反馈是否合法
            chk, err_code = self.check_feedback(feedback, self.n)
            while not chk and t < max_tries:
                print(f'feedback err_code: {err_code}')
                print('Please Re-enter the feedback:')
                feedback = input().strip().split(' ')
                chk, err_code = self.check_feedback(feedback, self.n)
                t += 1
            t = 0

            # 检测是否猜中
            hit_num, blow_num = feedback
            hit_num, blow_num = int(hit_num), int(blow_num)
            print(f'{hit_num} Hits! {blow_num} Blows!')
            if hit_num == self.n:
                print('\nWinner!!!')
                print('✧\(>o<)ﾉ✧ ✧\(>o<)ﾉ✧ ✧\(>o<)ﾉ✧')
                break

            hist_attempt.append(attempt)
            
            # 计算答案概率空间
            x, y = hit_num, hit_num + blow_num
            if i == 0:
                possible_result = self.get_possible_result(attempt, (x, y), self.valid_balls, self.n)
            else:
                tmp_result = self.get_possible_result(attempt, (x, y), self.valid_balls, self.n)
                possible_result = self.merge_possible_results(tmp_result, possible_result)

            i += 1
        print('Too bad...')


if __name__ == '__main__':
    h = Hacker()
    h.main()
