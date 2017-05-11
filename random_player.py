import random


class Player(object):
    def __init__(self):
        pass

    def init(self, index, total_players):
        self.my_index = index

    def play(self, state, cards_to_play):
        card = random.choice(cards_to_play)

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

        return best

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass

class GreedyBastardPlayer(object):
    def __init__(self):
        pass

    def init(self, index, total_players):
        self.my_index = index

    def play(self, state, cards_to_play):
        best = cards_to_play[0]
        best_score = 0

        values = [0.0 for i in xrange(6)]
        for i in cards_to_play:
            values[i] = state.dices_distribution[i + 3]
            if i>2:
                values[i] = values[i] * 2
        
        for i in cards_to_play:
            if values[i] > best_score:
                best_score = values[i]
                best = i
                values[i] = 0
                
        if random.randrange(2) == 0:
            best_score = 0
            for i in cards_to_play:
                if values[i] > best_score:
                    best_score = values[i]
                    best = i
                    values[i] = 0

        return best

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass
