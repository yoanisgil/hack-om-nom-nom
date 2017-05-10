import uuid
import logging
from game_logic import State, next_state
from random_player import Player


class WebGameSession(object):
    def __init__(self, number_of_players):
        self.session_id = str(uuid.uuid4())

        # Last player is always the human player
        self.state = State(number_of_players + 1)
        self.players = [Player()] * number_of_players
        self.player_moves = []

    def to_json(self):
        return {
            'session_id': self.session_id,
            'num_players': self.state.num_players,
            'dices_distribution': self.state.dices_distribution,
            'cards': self.state.cards,
            'score': self.state.score,
            'player_moves': self.player_moves
        }

    def add_player_move(self, card_index):
        self.player_moves.append(card_index)


class WebGameEngine(object):
    def __init__(self):
        self.sessions = {}

    def new_session(self, number_of_players):
        session = WebGameSession(number_of_players)

        self.sessions[session.session_id] = session

        logging.debug('Created session for {} players with ID {}'.format(number_of_players, session.session_id))

        return session

    def __get_session(self, session_id):
        if session_id not in self.sessions:
            raise Exception('No session with ID {}'.format(session_id))

        return self.sessions[session_id]

    def next_move(self, session_id, card_index):
        session = self.__get_session(session_id)

        moves = []

        for idx, player in enumerate(session.players):
            player_cards = session.state.cards[idx]
            card = player.play(session.state, session.state.cards[idx])

            if card not in player_cards:
                continue  # Shit happens

            moves.append(card)

        moves.append(card_index)

        session.state = next_state(session.state, moves)
        session.add_player_move(card_index)

        return session

    def has_next_move(self, session_id):
        session = self.__get_session(session_id)

        return len(session.player_moves) < 6
