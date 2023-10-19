"""命令行游戏
    Author: github@luochang212
    Date: 2023-10-18
    Usage: python game.py
"""

from .base import Base


class Game(Base):

    def __init__(self, n=4, replacement=False, max_guess_times=8):
        Base.__init__(self, n=n, replacement=False)
        self.max_guess_times = max_guess_times

    @staticmethod
    def show_prompt(balls):
        num = 34
        print('{} PROMPT {}\n- Valid balls: {}\n- Notice: Your inputs should be separated by blank space\n- An example of your input: r y b w\n{}'.format(
            '=' * num,
            '=' * num,
            ', '.join([k + ' (' + v + ')' for k, v in balls.items()]).strip(),
            '=' * (2 * num + 8)
        ))

    @staticmethod
    def show_err_prompt(err_code):
        head = 'Warning:'
        if err_code == 1:
            print(f'{head} The number of balls is not right.')
        elif err_code == 2:
            print(f'{head} Invalid balls.')
        else:
            raise Exception('Unknown error code')

    def main(self):
        # 游戏开始，打印提示语
        self.show_prompt(self.balls)

        # 生成游戏答案
        res = self.generate_result(self.valid_balls, self.n, self.replacement)

        i, flag = 0, True
        while i < self.max_guess_times:
            # 接收输入
            print(f'\nPlease give your answer ({self.max_guess_times - i} chances left):')
            attempt = input().strip().split(' ')

            # 校验输入是否合法
            chk, err_code = self.check_attempt(attempt, self.n, self.valid_balls)
            if not chk:
                self.show_err_prompt(err_code)
                continue

            # 反馈本轮是否猜中
            x, y = self.feedback(attempt, res)
            hit_num, blow_num = x, y - x

            if hit_num == self.n:
                print('\nWinner!!!')
                print('✧\(>o<)ﾉ✧ ✧\(>o<)ﾉ✧ ✧\(>o<)ﾉ✧')
                flag = False
                break

            print(f'{hit_num} Hits! {blow_num} Blows!')
            i += 1

        if flag:
            print('\nToo bad...')
            print('(´;ω;`) (´;ω;`) (´;ω;`)')
            print('Correct answer: {}'.format(' '.join(res)))


if __name__ == '__main__':
    g = Game()
    g.main()
