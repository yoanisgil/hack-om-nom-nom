from game_logic import State, next_state


def test_one_predator_one_prey():
    # All dices are in the last cell
    dices_distribution = [0] * 9
    dices_distribution[-1] = 15

    state = State.from__config(2, dices_distribution)

    new_state = next_state(state, [0, 3])

    assert new_state.score == [2, 0]
    assert new_state.dices_distribution[-1] == 15
    assert new_state.cards[0] == [1, 2, 3, 4, 5]
    assert new_state.cards[1] == [0, 1, 2, 4, 5]


def test_two_predators_one_prey():
    # All dices are in the last cell
    dices_distribution = [0] * 9
    dices_distribution[-1] = 15

    state = State.from__config(3, dices_distribution)

    new_state = next_state(state, [0, 3, 0])

    assert new_state.score == [0, 0, 0]
    assert new_state.dices_distribution[-1] == 15
    assert new_state.cards[0] == [1, 2, 3, 4, 5]
    assert new_state.cards[1] == [0, 1, 2, 4, 5]
    assert new_state.cards[2] == [1, 2, 3, 4, 5]


def test_two_predators_two_preys():
    # All dices are in the last cell
    dices_distribution = [0] * 9
    dices_distribution[-1] = 15

    state = State.from__config(4, dices_distribution)

    new_state = next_state(state, [0, 3, 0, 3])

    assert new_state.score == [2, 0, 2, 0]
    assert new_state.dices_distribution[-1] == 15
    assert new_state.cards[0] == [1, 2, 3, 4, 5]
    assert new_state.cards[1] == [0, 1, 2, 4, 5]
    assert new_state.cards[2] == [1, 2, 3, 4, 5]
    assert new_state.cards[3] == [0, 1, 2, 4, 5]


def test_one_predator_one_dice():
    dices_distribution = [0] * 9
    dices_distribution[3] = 1
    dices_distribution[-1] = 14

    state = State.from__config(2, dices_distribution)

    new_state = next_state(state, [0, 1])

    assert new_state.score == [2, 0]
    assert new_state.dices_distribution[3] == 0
    assert new_state.dices_distribution[-1] == 14
    assert new_state.cards[0] == [1, 2, 3, 4, 5]
    assert new_state.cards[1] == [0, 2, 3, 4, 5]

def test_one_prey_one_dice():
    dices_distribution = [0] * 9
    dices_distribution[6] = 1
    dices_distribution[-1] = 14

    state = State.from__config(2, dices_distribution)

    new_state = next_state(state, [3, 1])

    assert new_state.score == [3, 0]
    assert new_state.dices_distribution[6] == 0
    assert new_state.dices_distribution[-1] == 14
    assert new_state.cards[0] == [0, 1, 2, 4, 5]
    assert new_state.cards[1] == [0, 2, 3, 4, 5]

def test_two_preys_one_dice():
    dices_distribution = [0] * 9
    dices_distribution[6] = 1
    dices_distribution[-1] = 14

    state = State.from__config(2, dices_distribution)

    new_state = next_state(state, [3, 3])

    assert new_state.score == [0, 0]
    assert new_state.dices_distribution[6] == 1
    assert new_state.dices_distribution[-1] == 14
    assert new_state.cards[0] == [0, 1, 2, 4, 5]
    assert new_state.cards[1] == [0, 1, 2, 4, 5]


def test_one_predator_one_prey_one_dice():
    dices_distribution = [0] * 9
    dices_distribution[6] = 1
    dices_distribution[-1] = 14

    state = State.from__config(2, dices_distribution)

    new_state = next_state(state, [0, 3])

    assert new_state.score == [2, 0]
    assert new_state.dices_distribution[6] == 1
    assert new_state.dices_distribution[-1] == 14
    assert new_state.cards[0] == [1, 2, 3, 4, 5]
    assert new_state.cards[1] == [0, 1, 2, 4, 5]