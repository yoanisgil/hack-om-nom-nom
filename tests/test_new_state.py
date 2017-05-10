from game_logic import State, next_state


def test_one():
    # All dices are in the last cell
    dices_distribution = [0] * 9
    dices_distribution[-1] = 15

    state = State.from__config(2, dices_distribution)

    new_state = next_state(state, [0, 3])

    assert new_state.score == [2, 0]
    assert new_state.cards[0] == [1, 2, 3, 4, 5]
    assert new_state.cards[1] == [0, 1, 2, 4, 5]
