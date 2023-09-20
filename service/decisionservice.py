import random

from model.excpetion import AlreadyPlayedError
from model.yathzeescorecard import YathzeeScoreCard


class DecisionService:
    def __init__(self):
        pass

    def decide_optimal_play(self, dice_rolls: [int], score_card: YathzeeScoreCard) -> int:
        # find first thing that is not filled in
        # if nothing is filled in, find the thing that is most likely to be filled in

        return random.Random().randint(1, 13)

    def decision_to_action(self, decision: int, dice_rolls: [int], score_card: YathzeeScoreCard) -> int:
        try:
            if decision == 1:
                score_card.play_ones(dice_rolls)
            elif decision == 2:
                score_card.play_twos(dice_rolls)
            elif decision == 3:
                score_card.play_threes(dice_rolls)
            elif decision == 4:
                score_card.play_fours(dice_rolls)
            elif decision == 5:
                score_card.play_fives(dice_rolls)
            elif decision == 6:
                score_card.play_sixes(dice_rolls)
            elif decision == 7:
                score_card.play_three_of_a_kind(dice_rolls)
            elif decision == 8:
                score_card.play_four_of_a_kind(dice_rolls)
            elif decision == 9:
                score_card.play_full_house(dice_rolls)
            elif decision == 10:
                score_card.play_small_straight(dice_rolls)
            elif decision == 11:
                score_card.play_large_straight(dice_rolls)
            elif decision == 12:
                score_card.play_yahtzee(dice_rolls)
            elif decision == 13:
                score_card.play_chance(dice_rolls)

        except AlreadyPlayedError:
            # a move was tried that is not allowed
            return -500
