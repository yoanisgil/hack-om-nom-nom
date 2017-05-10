import random


class Player(object):
    def __init__(self):
        pass

    def init(self, index):
        self.my_index = index
        pass
    
    def play(self, state, cards_to_play):
        card = random.choice(cards_to_play)

        print("Payouts are {}".format(state.payouts))
        print("Playing {}".format(card))
        return card

    def was_played(self):
        pass

    def round_ended(self):
        pass

