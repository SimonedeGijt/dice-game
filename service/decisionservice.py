import itertools
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
        best_option, best_score = self.find_best_action(dice, player)

        best_option, best_score, dice = self.do_potential_re_roll(best_option, best_score, dice, game, player)
        best_option, best_score, dice = self.do_potential_re_roll(best_option, best_score, dice, game, player)

        logging.debug(f'{player.name} chose {best_option} for {dice} with {best_score} points')

        return dice, best_option

    def do_potential_re_roll(self, best_option, best_score, dice, game, player):
        # try re-rolls and find if we want to do that just do that a couple of times and average what the best is
        # get all combinations with the current dice
        # for each combination simulate a 20 dice rolls with the remaining dice and see what the best option is
        # store for all found scores for the combination
        # find the combination with the best average score and compare that to the best option we already have, if it's better use that
        # TODO decide if we want a margin here
        combinations = self.get_dice_combinations(dice)

        results_per_combination = {}
        for combination in combinations:
            best_result = self.simulate_re_rolls(game, player, combination)
            results_per_combination[combination] = best_result

        best_combination = max(results_per_combination, key=lambda k: results_per_combination[k])
        best_combination_score = results_per_combination[best_combination]

        if best_combination_score > best_score:
            # start doing a real re-roll with the best combination
            re_roll_dice = game.get_dice_roll(player, False, 5 - len(best_combination))
            re_roll_dice.extend(best_combination)
            logging.debug(f'went from {dice} to {re_roll_dice}')

            dice = re_roll_dice
            best_option, best_score = self.find_best_action(re_roll_dice, player)

        return best_option, best_score, dice

    def simulate_re_rolls(self, game, player, combination) -> (int, int):
        results = {}

        for _ in range(15):
            new_dice = game.get_dice_roll(player, False, 5 - len(combination))
            new_dice.extend(combination)

            best_option, best_score = self.find_best_action(new_dice, player)

            if best_option not in results:
                results[best_option] = []
            results[best_option].append(best_score)

        # find the option that has the most results and return it with the average score
        combined_values = [value for sublist in results.values() for value in sublist]
        score = sum(combined_values) / len(combined_values)

        return score

    @staticmethod
    def get_dice_combinations(dice):
        all_combinations = []
        # Generate all combinations of all lengths from 1 to len(dice) so we only get 4 dice max since we never want to re-roll 0 dice
        for r in range(1, len(dice)):
            combinations_object = itertools.combinations(dice, r)
            combinations_list = list(combinations_object)
            all_combinations.extend(combinations_list)

        return all_combinations

    def find_best_action(self, dice, player):
        # for these dice check all options and see which one will give the most points
        best_option = 1
        best_score = 0

        for action in range(1, 13):
            try:
                points = self.decision_to_action(action, dice, player.score_card, True)
                if points >= best_score:  # its better to fill one of the higher options since we roll it less often
                    best_score = points
                    best_option = action
            except AlreadyPlayedError:
                pass

        # only try chance if the best score is way lower than the sum of the points, so that we can save chance for later
        if best_score <= sum(dice) - 10:
            try:
                points = self.decision_to_action(0, dice, player.score_card, True)
                if points >= best_score:  # its better to fill one of the higher options since we roll it less often
                    best_score = points
                    best_option = 0
            except AlreadyPlayedError:
                pass

        logging.debug(f'{player.name} chose {best_option} for {dice} with {best_score} points')

        return best_option, best_score
