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
        self.num_players = num_players
        self.dices_distribution = 9 * [0]
        self.cards = [range(0, 6)] * num_players
        self.score = [0] * num_players

        dices_count = DiceRoller.roll_dices(15)

        for i in range(3, 9):
            self.dices_distribution[i] = dices_count[i - 3]

    @staticmethod
    def from__config(num_players, dices_distribution, cards=None, score=None):
        state = State(num_players)
        state.dices_distribution = dices_distribution

        if cards:
            state.cards = cards

        if score:
            state.score = score

        return state


def remove_cards(cards, moves):
    new_cards = []

    for player_index, card_index in enumerate(moves):
        new_cards.append(filter(lambda e: e != card_index, cards[player_index]))

    return new_cards


def next_state(old_state, moves):
    cards_distribution = [0] * 9

    new_dices_distribution = old_state.dices_distribution[:]
    new_score = old_state.score[:]

    # Calculate how many cards are in each cell in the first 6 rows so that we can later calculate the scores
    for i in range(0, 6):
        cards_distribution[i] = len(filter(lambda e: e == i, moves))

    # Loop over each cell

    for i in range(0, 6):
        score = 0
        dices_to_remove = 0

        if cards_distribution[i] == 0:
            continue

        if 0 <= i <= 2:
            points_per_player = (cards_distribution[i + 3] + old_state.dices_distribution[i + 3]) / cards_distribution[
                i]

            if points_per_player > 0:
                score = points_per_player + 1

            dices_to_remove = points_per_player * cards_distribution[i] - cards_distribution[i + 3]
            cards_distribution[i + 3] = 0
        else:
            number_of_dices = old_state.dices_distribution[i + 3] / cards_distribution[i]
            if number_of_dices > 0:
                score = 2 * number_of_dices + 1

            dices_to_remove = number_of_dices

        new_dices_distribution[i + 3] -= dices_to_remove

        for player_index, cell_index in enumerate(moves):
            if cell_index == i:
                new_score[player_index] += score

    new_cards = remove_cards(old_state.cards, moves)

    return State.from__config(old_state.num_players, new_dices_distribution, cards=new_cards, score=new_score)
