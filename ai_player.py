import random
import copy
import tensorflow as tf
from game_logic import State, next_state
import itertools
import numpy as np

EMBED_DIM = 30
SAMPLES = 20

class Evaluator:
    def __init__(self):

        learning_rate = 0.1

        self.payouts = tf.placeholder("float", [None, 6]) # the payouts
        self.cards = tf.placeholder("float", [None, 6]) # whether I still have the card

        self.weights = {
            'h1': tf.Variable(tf.random_uniform([12, EMBED_DIM],-0.1,0.1, dtype = "float")),
            'h2': tf.Variable(tf.random_uniform([EMBED_DIM, 6],-0.1,0.1, dtype = "float"))
            }
        self.biases = {
            'b1': tf.Variable(tf.random_uniform([EMBED_DIM],-0.1,0.1, dtype = "float")),
            'b2': tf.Variable(tf.random_uniform([6],-0.1,0.1, dtype = "float")),
            }

        self.inputs = tf.concat([self.payouts, self.cards], axis=1)

        self.play_prob = self.prediction()

        self.actual_play_prob = tf.placeholder("float", [None, 6])

        # Define loss and optimizer
#        self.cost = tf.reduce_mean(tf.square(tf.subtract(self.play_prob, self.actual_play_prob)))
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.play_prob, labels=self.actual_play_prob))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)

        # Initializing the variables
        self.init = tf.global_variables_initializer()

    def prediction(self):
        # Hidden layer with RELU activation
        layer_1 = tf.add(tf.matmul(self.inputs, self.weights['h1']), self.biases['b1'])
        layer_1 = tf.nn.relu(layer_1)

        # Hidden layer with RELU activation
        layer_2 = tf.add(tf.matmul(layer_1, self.weights['h2']), self.biases['b2'])

        # Output layer with linear activation
        out_layer = tf.nn.softmax(layer_2)

        return out_layer

    def evaluate(self):
        return([1/6.0, 1/6.0, 1/6.0, 1/6.0, 1/6.0, 1/6.0])

class AiPlayer(object):
    def __init__(self):
        pass

    # init the AI player
    def init(self, index, total_players):
        print("Init")
        self.learn_strat = False
        self.my_index = index
        self.total_players = total_players

        self.evals = [Evaluator() for x in xrange(self.total_players)]

        self.sess = tf.Session()
        self.last_inputs = [None for i in xrange(self.total_players)]

        for x in self.evals:
            self.sess.run(x.init)

        # tensorflow state saver
        self.saver = tf.train.Saver()
        self.count = 0

#        self.saver.restore(self.sess, "model1.ckpt")
        print("Model restored.")

    def value_from_score(self, score):
        return score[self.my_index]
#        if max(score) == score[self.my_index]:
#            ret = 1.0
#        else:
#            ret = 0.0
#        return ret

    def get_input_from_state(self, player_index, state):
        inputs = [0.0 for i in xrange(12)]
        for i in state.cards[player_index]:
            inputs[i] = 1.0
        for i in xrange(6):
            inputs[i + 6] = state.dices_distribution[i + 3]

        return inputs

    def get_play_probability(self, player_index, state):

        inputs = self.get_input_from_state(player_index, state)
        inputs = np.asarray(inputs).reshape(1,12)

        if self.learn_strat:
            eval = self.evals[player_index]

            p0 = self.sess.run([eval.play_prob], feed_dict={eval.inputs:inputs})
            prob = (p0[0].tolist()[0])
        else:
        
            payouts = [0.,0.,0.,0.,0.,0.]
            for i in xrange(6):
                payouts[i] = inputs[0, i + 6] * inputs[0, i]
            
            payouts[3] = payouts[3] * 2
            payouts[4] = payouts[4] * 2
            payouts[5] = payouts[5] * 2
            
            if player_index == 1: #TODO HACK HACK HACK
                prob = [(1. if payouts[i] == max(payouts) else 0.) for i in xrange(6)]
            else:
                prob = [1.,1.,1.,1.,1.,1.]
            

        sum = 0.0

        # normalize over the legal inputs
        for i in xrange(6):
            if inputs[0][i]:
                sum = sum + prob[i]
            else:
                prob[i] = 0.0

        if sum == 0.0:
            # something went way weird. Normalize over all the legal moves
            for i in xrange(6):
                if inputs[0][i]:
                    sum = sum + 1.0
                    prob[i] = 1.0
                else:
                    prob[i] = 0.0

        for i in xrange(6):
            prob[i] = prob[i] / sum

        return prob

    # internal function to sample a strategy and evaluate the score
    def sample(self, state, strategy):

        # play my moves in sequence
        for x in strategy:
            moves = [0 for y in xrange(self.total_players)]

            # for each opponent
            for player in xrange(self.total_players):
                if player != self.my_index:

                    # play a move sample from what we think they will play
                    play_probability = self.get_play_probability(player, state)
                    moves[player] = np.random.choice(xrange(6), 1, p = play_probability)[0]

            moves[self.my_index] = x
            state = next_state(state, moves)

        return state

    # API call to play a move
    def play(self, state, cards_to_play):

        #save the input to the NN
        for i in xrange(self.total_players):
            self.last_inputs[i] = self.get_input_from_state(i, state)

        strategies = itertools.permutations(cards_to_play, 3) # TODO 3 is depth. test

        strategy_value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        strategy_value_count = [0, 0, 0, 0, 0, 0]

        for strategy in strategies:
            for i in xrange(SAMPLES):
                next_state = copy.copy(state)
                next_state = self.sample(next_state, strategy)

            # the value of the strategy starting by each move is a function of the score
            strategy_value[strategy[0]] = strategy_value[strategy[0]] + self.value_from_score(next_state.score)
            strategy_value_count[strategy[0]] = strategy_value_count[strategy[0]] + 1

        bestValue = 0.0
        bestCard = cards_to_play[0]

        sum = 0.0
        for x in xrange(6):
            if strategy_value_count[x] > 0:
                strategy_value[x] = strategy_value[x] / strategy_value_count[x]
                sum += strategy_value[x]
        
        if (sum != 0.0):
            for x in xrange(6):
                strategy_value[x] = strategy_value[x] / sum
        else:
            for x in xrange(6):
                strategy_value[x] = 1.0/len(cards_to_play) if x in cards_to_play else 0.0
                
        bestCard = np.random.choice(6, 1, p=strategy_value)[0]


        print("state {}".format(state))
        for i in xrange(self.total_players):
            if i != self.my_index:
                print("AI believes player {} would play with distribution {}".format(i, self.get_play_probability(i, state)))
        print("AI playing card {}".format(bestCard))

        return bestCard

    def turn_ended(self, moves):
        for i in xrange(self.total_players):
            if i != self.my_index:

                eval = self.evals[i]

                play_prob = [0.0 for j in xrange(6)]
                play_prob[moves[i]] = 1.0

                play_prob = np.asarray(play_prob).reshape(1,6)
                inputs = np.asarray(self.last_inputs[i]).reshape(1,len(self.last_inputs[i]))
                
                if self.learn_strat:
                    self.sess.run([eval.optimizer, eval.cost], feed_dict={eval.inputs:inputs, eval.actual_play_prob:play_prob})
                    print("Trained with {} {}".format(inputs,play_prob))

    def round_ended(self):

        if self.count % 100 == 0:
            save_path = self.saver.save(self.sess, "model" + str(self.count/100) + ".ckpt")
            print("Model saved in file: %s" % save_path)
        self.count = self.count + 1
