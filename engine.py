from random_player import Player


class State(object):
    def __init__(self, num_players):
        self.payouts = 9 * [0]
        self.cards = [range(0, 6)] * num_players
        self.score = [0] * num_players

        # TODO: Throw the dice

    @staticmethod
    def new_state(old_state, moves):
        return []


class Engine(object):
    def __init__(self):
        pass

    def start(self, players):
        state = State(len(players))

        for i in range(0, 6):
            moves = []

            for idx, player in enumerate(players):
                player_cards = state.cards[idx]
                card = player.play(state, state.cards[idx])

                if card not in player_cards:
                    continue  # Shit happens

                moves.append(card)

            state = State.new_state(state, moves)



if __name__ == '__main__':
    player1 = Player()
    player2 = Player()

    engine = Engine()
    engine.start([player1, player2])
