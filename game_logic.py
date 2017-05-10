import random


class DiceRoller(object):
    @staticmethod
    def roll_dices(number):
        dices_count = [0] * 6

        for i in range(0, number):
            dices_count[random.randint(0, 5)] += 1

        return dices_count


class State(object):
    def __init__(self, num_players):
        self.payouts = 9 * [0]
        self.cards = [range(0, 6)] * num_players
        self.score = [0] * num_players

        dices_count = DiceRoller.roll_dices(15)

        for i in range(3, 9):
            self.payouts[i] = dices_count[i - 3]


def new_state(old_state, moves):
    cards_distribution = [0] * 6

    for i in range(0, 6):
        cards_distribution[i] = len(filter(lambda e: e == i, moves))

    return old_state