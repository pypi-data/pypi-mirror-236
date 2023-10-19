import switch_hacker


if __name__ == '__main__':
    # e = switch_hacker.game.Game()
    # e.main()

    # e = switch_hacker.auto_play.AutoPlay()
    # e.single_test_debug(['r', 'g', 'w', 'b'])

    # e = switch_hacker.experiment.Experiment(iter_num=1000, strategy='random')
    # e.main()

    e = switch_hacker.hacker.Hacker()
    e.main()
