import pytest

from model.yahtzeescorecard import YahtzeeScoreCard


@pytest.mark.parametrize("dice_rolls, expected_score", [
    ([1, 2, 3, 4, 5], 30),
    ([3, 2, 3, 4, 5], 30),
    ([3, 1, 2, 2, 4], 30),
    ([1, 2, 3, 4, 1], 30),
    ([1, 2, 3, 2, 3], 0),
    ([6, 3, 4, 2, 5], 30),
    ([3, 4, 1, 5, 1], 0),
])
def test_small_straight(dice_rolls, expected_score):
    score_card = YahtzeeScoreCard()
    score_card.play_small_straight(dice_rolls)
    assert score_card.lower_section.small_straight == expected_score


def test_small_straight_already_played():
    score_card = YahtzeeScoreCard()
    score_card.play_small_straight([1, 2, 3, 4, 5])
    with pytest.raises(Exception):
        score_card.play_small_straight([1, 2, 3, 4, 5])


@pytest.mark.parametrize("dice_rolls, expected_score", [
    ([2, 3, 4, 5, 6], 40),
    ([3, 2, 3, 4, 5], 0),
    ([3, 1, 2, 2, 4], 0),
    ([1, 2, 3, 4, 1], 0),
    ([1, 2, 3, 2, 3], 0),
    ([6, 3, 4, 2, 5], 40),
])
def test_large_straight(dice_rolls, expected_score):
    score_card = YahtzeeScoreCard()
    score_card.play_large_straight(dice_rolls)
    assert score_card.lower_section.large_straight == expected_score


@pytest.mark.parametrize("dice_rolls, expected_score", [
    ([1, 1, 1, 1, 1], 50),
    ([3, 2, 3, 4, 5], 0),
    ([3, 1, 2, 2, 4], 0),
    ([3, 3, 3, 3, 3], 50),
])
def test_yahtzee(dice_rolls, expected_score):
    score_card = YahtzeeScoreCard()
    score_card.play_yahtzee(dice_rolls)
    assert score_card.lower_section.yahtzee == expected_score


@pytest.mark.parametrize("dice_rolls, expected_score", [
    ([1, 1, 1, 1, 1], 5),
    ([1, 1, 5, 6, 6], 2),
])
def test_one(dice_rolls, expected_score):
    score_card = YahtzeeScoreCard()
    score_card.play_ones(dice_rolls)
    assert score_card.upper_section.aces == expected_score


@pytest.mark.parametrize("dice_rolls, expected_score", [
    ([2, 2, 2, 2, 2], 0),
    ([1, 1, 5, 6, 6], 0),
    ([1, 1, 1, 6, 6], 25),
])
def test_full_house(dice_rolls, expected_score):
    score_card = YahtzeeScoreCard()
    score_card.play_full_house(dice_rolls)
    assert score_card.lower_section.full_house == expected_score


@pytest.mark.parametrize("dice_rolls, expected_score", [
    ([2, 2, 2, 2, 2], 10),
    ([1, 1, 5, 6, 6], 0),
    ([1, 1, 1, 6, 6], 15),
    ([1, 1, 1, 1, 6], 10),
])
def test_three_of_a_kind(dice_rolls, expected_score):
    score_card = YahtzeeScoreCard()
    score_card.play_three_of_a_kind(dice_rolls)
    assert score_card.lower_section.three_of_a_kind == expected_score
