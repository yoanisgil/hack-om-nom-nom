import random
import copy
import tensorflow as tf
from game_logic import State, next_state
import itertools

EMBED_DIM = 10
SAMPLES = 2

class Evaluator:
    def __init__(self):

        learning_rate = 0.1

        self.payouts = tf.placeholder(tf.int32, [None, 6]) # the payouts
        self.cards = tf.placeholder("float", [None, 6]) # whether I still have the card

        self.weights = {
            'h1': tf.Variable(tf.random_normal([12, EMBED_DIM])),
            'h2': tf.Variable(tf.random_normal([EMBED_DIM, 6])),
            }
        self.biases = {
            'b1': tf.Variable(tf.random_normal([12])),
            'b2': tf.Variable(tf.random_normal([6])),
            }

    def evaluate(self):
        return([1/6.0, 1/6.0, 1/6.0, 1/6.0, 1/6.0, 1/6.0])


class AiPlayer(object):
    def __init__(self):
        pass

    # init the AI player
    def init(self, index, total_players):
        self.my_index = index
        self.total_players = total_players

        self.evals = [Evaluator() for x in xrange(self.total_players)]

    def valueFromScore(self, score):
        if max(score) == score[self.my_index]:
            ret = 1.0
        else:
            ret = 0.0

        return ret

    # internal function to sample a strategy and evaluate the score
    def sample(self, state, strategy):

        # play my moves in sequence
        for x in strategy:

            moves = [random.choice(y) for y in state.cards] # pick a random card, in each player possible cards. TODO : samples
            moves[self.my_index] = x

            state = next_state(state, moves)

        return state

    # API call to play a move
    def play(self, state, cards_to_play):

        strategies = itertools.permutations(cards_to_play)

        strategy_value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        strategy_value_count = [0, 0, 0, 0, 0, 0]

        for strategy in strategies:
            for i in xrange(SAMPLES):
                next_state = copy.copy(state)
                next_state = self.sample(next_state, strategy)

            # the value of the strategy starting by each move is a function of the score
            strategy_value[strategy[0]] = strategy_value[strategy[0]] + self.valueFromScore(next_state.score)
            strategy_value_count[strategy[0]] = strategy_value_count[strategy[0]] + 1

        bestValue = 0.0
        bestCard = cards_to_play[0]

        for x in xrange(6):
            if strategy_value_count[x] > 0:
                strategy_value[x] = strategy_value[x] / strategy_value_count[x]
            if strategy_value[x] > bestValue:
                bestValue = strategy_value[x]
                bestCard = x

        print("playing card {}".format(bestCard))

        return bestCard

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass
