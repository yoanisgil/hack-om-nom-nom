from game_logic import State, new_state
from random_player import Player


class Engine(object):
    def __init__(self):
        pass

    def start(self, players):
        state = State(len(players))

        for player_index, player in enumerate(players):
            player.init(player_index, len(players))

        for i in range(0, 6):
            moves = []

            for idx, player in enumerate(players):
                player_cards = state.cards[idx]
                card = player.play(state, state.cards[idx])

                if card not in player_cards:
                    continue  # Shit happens

                moves.append(card)

            for player in players:
                player.turn_ended(moves)

            state = new_state(state, moves)

        for player in players:
            player.round_ended()


if __name__ == '__main__':
    player1 = Player()
    player2 = Player()

    engine = Engine()
    engine.start([player1, player2])
    #    State(2)
