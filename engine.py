from random_player import Player


class State(object):
    def __init__(self, num_players):
        self.payouts = 9 * [0]
        self.cards = [[1] * 6] * num_players

        # TODO: Throw the dice


class Engine(object):
    def __init__():
        pass

    def start(self, players):
        state = State(len(players))

        for player in players:
            player.play(state)


if __name__ == '__main__':
    player1 = Player()
    player2 = Player()

    engine = Engine()
    engine.start([player1, player2])
