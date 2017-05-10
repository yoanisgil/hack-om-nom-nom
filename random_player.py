import random
import tensorflow


class Player(object):
    def __init__(self):
        pass

    def init(self, index, total_players):
        self.my_index = index

    def play(self, state, cards_to_play):
        card = random.choice(cards_to_play)

        print("Payouts are {}".format(state.payouts))
        print("Playing {}".format(card))
        return card

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass
