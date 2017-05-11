from game_logic import State, next_state
from random_player import Player, GreedyPlayer
from ai_player import AiPlayer


class Engine(object):
    def __init__(self):
        pass

    def start(self, players):

        totals = [0 for p in players]
        wins = [0 for p in players]

        for player_index, player in enumerate(players):
            player.init(player_index, len(players))

        for i in xrange(1000):
            state = State(len(players))

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

                state = next_state(state, moves)

            for player in players:
                player.round_ended()

            for x in xrange(len(players)):
                totals[x] = totals[x] + state.score[x]
                if state.score[x] == max(state.score):
                    wins[x] = wins[x] + 1

            print "Totals: {}, wins: {}".format(totals, wins)

        return state


if __name__ == '__main__':
    
    player1 = Player()
    player2 = GreedyPlayer()
    player3 = AiPlayer()

    engine = Engine()
    ret = engine.start([player2, player3])

    #    State(2)
