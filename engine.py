from random_player import Player


class State(object):
    def __init__(self, num_players):
        self.payouts = 9 * [0]
        self.cards = [range(0, 6)] * num_players

        # TODO: Throw the dice


class Engine(object):
    def __init__():
        pass

    def start(self, players):
        state = State(len(players))

        for idx, player in enumerate(players):
            player_cards = state.cards[idx]
            card = player.play(state, state.cards[idx])

            if card not in player_cards:
                continue # Shit happens

            player_cards.remove(card)


if __name__ == '__main__':
    player1 = Player()
    player2 = Player()

    engine = Engine()
    engine.start([player1, player2])
