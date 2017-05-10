import random


class Player(object):
    def play(self, state, cards_to_play):
        return random.choice(cards_to_play)
