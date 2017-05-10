import random


class Player(object):
    def __init__(self):
        pass

    def init(self):
        pass
    
    def play(self, state, cards_to_play):
        card = random.choice(cards_to_play)
        print("Playing {}".format(card))
        return card

    def wasPlayed(self):
        pass

    def roundEnded(self):
        pass

