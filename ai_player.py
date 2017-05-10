import random
import copy
import tensorflow as tf
from game_logic import State, new_state
import itertools

EMBED_DIM = 10

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

    def init(self, index, total_players):
        self.my_index = index
        self.total_players = total_players

        self.evals = [Evaluator() for x in xrange(self.total_players)]

    def play(self, state, cards_to_play):
    
        strategies = itertools.permutations(cards_to_play)

        card = random.choice(cards_to_play)
        return card

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass
