import random


class Player(object):
    def __init__(self):
        pass

    def init(self, index, total_players):
        self.my_index = index

    def play(self, state, cards_to_play):
        card = random.choice(cards_to_play)

        print("Random playing {}".format(card))
        return card

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass
