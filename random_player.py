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

class GreedyPlayer(object):
    def __init__(self):
        pass

    def init(self, index, total_players):
        self.my_index = index

    def play(self, state, cards_to_play):
        best = cards_to_play[0]
        best_score = 0

        for i in cards_to_play:
            value = state.dices_distribution[i + 3]
            if i>2:
                value = value * 2
            if value > best_score:
                best_score = value
                best = i

        print("Random playing {}".format(best))
        return best

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass
