import logging
import random

from model.excpetion import AlreadyPlayedError
from model.yahtzeescorecard import YahtzeeScoreCard


class RandomDecisionService:
    def play_optimal_play(self, game, player) -> YahtzeeScoreCard:
        valid_choice = -1
        while valid_choice == -1:
            rolls, decision = self.decide(game, player)
            try:
                self.decision_to_action(decision, rolls, player.score_card)
                valid_choice = decision
            except AlreadyPlayedError:
                logging.debug(f'{player.name} tried to play {decision} but it was already played')
                # keep on retrying till we have played a valid move
                pass

        return player.score_card

    def decide(self, game, player) -> ([int], int):
        dice = game.get_dice_roll(player, False)
        return dice, random.Random().randint(0, 12)

    @staticmethod
    def decision_to_action(decision: int, dice_rolls: [int], score_card: YahtzeeScoreCard, trial: bool = False) -> int:
        if decision == 1:
            return score_card.play_ones(dice_rolls, trial)
        elif decision == 2:
            return score_card.play_twos(dice_rolls, trial)
        elif decision == 3:
            return score_card.play_threes(dice_rolls, trial)
        elif decision == 4:
            return score_card.play_fours(dice_rolls, trial)
        elif decision == 5:
            return score_card.play_fives(dice_rolls, trial)
        elif decision == 6:
            return score_card.play_sixes(dice_rolls, trial)
        elif decision == 7:
            return score_card.play_three_of_a_kind(dice_rolls, trial)
        elif decision == 8:
            return score_card.play_four_of_a_kind(dice_rolls, trial)
        elif decision == 9:
            return score_card.play_full_house(dice_rolls, trial)
        elif decision == 10:
            return score_card.play_small_straight(dice_rolls, trial)
        elif decision == 11:
            return score_card.play_large_straight(dice_rolls, trial)
        elif decision == 12:
            return score_card.play_yahtzee(dice_rolls, trial)

        # we only want to use chance as a last resort
        elif decision == 0:
            return score_card.play_chance(dice_rolls, trial)


class SmartDecisionService(RandomDecisionService):
    def decide(self, game, player) -> ([int], int):
        dice = game.get_dice_roll(player)

        # for these dice check all options and see which one will give the most points
        best_option = 1
        best_score = 0

        for action in range(0, 13):
            try:
                points = self.decision_to_action(action, dice, player.score_card, True)
                if points >= best_score:  # its better to fill one of the higher options since we roll it less often
                    best_score = points
                    best_option = action
            except AlreadyPlayedError:
                pass

        logging.debug(f'{player.name} chose {best_option} for {dice} with {best_score} points')

        return dice, best_option
