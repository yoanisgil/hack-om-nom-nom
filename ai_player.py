import random
import tensorflow as tf

EMBED_DIM = 10

class Evaluator:
    def __init__(self):
    
        print("Evaluator init")
    
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



class AiPlayer(object):
    def __init__(self):
    
        self.eval = Evaluator()
        pass

    def init(self, index, total_players):
        self.my_index = index
        pass

    def play(self, state, cards_to_play):
        card = random.choice(cards_to_play)

        print("Payouts are {}".format(state.payouts))
        print("State.cards is {}".format(state.cards))
        print("Playing {}".format(card))
        return card

    def turn_ended(self, moves):
        pass

    def round_ended(self):
        pass
