from game_logic import State, next_state
from random_player import Player
from ai_player import AiPlayer


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

            state = next_state(state, moves)

        for player in players:
            player.round_ended()

        return state


if __name__ == '__main__':

    totals = [0,0]
    wins = [0,0]
    
    for i in xrange(1000):
        player1 = Player()
        player2 = AiPlayer()

        engine = Engine()
        ret = engine.start([player1, player2])

        for x in xrange(2):
            totals[x] = totals[x] + ret.score[x]
            if ret.score[x] == max(ret.score):
                wins[x] = wins[x] + 1

        print "Totals: {}, wins: {}".format(totals, wins)


    #    State(2)
