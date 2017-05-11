import random
import copy
from game_logic import State, next_state
import itertools
import numpy as np

EMBED_DIM = 30
SAMPLES = 20

class AiPlayer(object):
    def __init__(self):
        pass

    # init the AI player
    def init(self, index, total_players):
        self.learn_strat = False
        self.maximize_score = False

        self.my_index = index
        self.total_players = total_players

        self.last_inputs = [None for i in xrange(self.total_players)]

        self.count = 0

#        self.saver.restore(self.sess, "model1.ckpt")

    def value_from_score(self, score):
        if self.maximize_score:
            return score[self.my_index]
        else:
            if max(score) == score[self.my_index]:
                ret = 1.0
            else:
                ret = 0.0
            return ret

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
        
            prob = [0.,0.,0.,0.,0.,0.]
            for i in xrange(6):
                prob[i] = inputs[0, i + 6] * inputs[0, i]

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

        return bestCard

    def turn_ended(self, moves):
        pass

    def round_ended(self):

        if self.learn_strat and self.count % 100 == 0:
            save_path = self.saver.save(self.sess, "model" + str(self.count/100) + ".ckpt")
            print("Model saved in file: %s" % save_path)
        self.count = self.count + 1
