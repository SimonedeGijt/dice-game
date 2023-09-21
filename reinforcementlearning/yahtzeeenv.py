from collections import Counter
from typing import Optional

import gym
import numpy as np
from gym import spaces
from gym.core import ObsType

from model.excpetion import AlreadyPlayedError
from model.game import Yahtzee
from service.randomdecisionservice import RandomDecisionService


class YahtzeeEnv(gym.Env):
    def __init__(self):
        super(YahtzeeEnv, self).__init__()

        # Define action and observation spaces
        self.action_space = spaces.Discrete(13)  # 13 different scoring categories
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0, 0] + [0] * 13),
                                            high=np.array([5, 5, 5, 5, 5, 5] + [1] * 13),
                                            dtype=int)
        self.reward_range = (-500, 50)

        # Initialize game-specific variables
        self.game = None
        self.decision_service = RandomDecisionService()
        self.dice = None

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        # Reset the game state
        self.game = Yahtzee(1)
        self.dice = self.game.recognition_service.dice_rols(None)
        info = {'reset_info': 'Environment reset successfully', 'options_used': options}
        return self._get_state(), info

    def step(self, action: int):
        # Store the total score before the action
        prev_score = self.game.players[0].get_total()  # one player is assumed
        reward = 0
        try:
            # play the action in the round
            self.decision_service.decision_to_action(action, self.dice, self.game.players[0].score_card)
        except AlreadyPlayedError:
            # a move was tried that is not allowed
            reward = -500

        if reward == 0:
            # Calculate the reward as the difference in score
            reward = self.game.players[0].get_total() - prev_score

        self.dice = self.game.recognition_service.dice_rols(None)
        state = self._get_state()

        # Check if the game is over
        done = self.game.is_finished()
        info = {'reset_info': 'Environment reset successfully'}

        return state, reward, done, {}, info

    def _get_state(self, ):
        counts = Counter(self.dice)
        dice_state = [counts[i] for i in range(1, 7)]

        # Get the scorecard state
        scorecard = self.game.players[0].score_card
        scorecard_state = [
            scorecard.upper_section.aces,
            scorecard.upper_section.twos,
            scorecard.upper_section.threes,
            scorecard.upper_section.fours,
            scorecard.upper_section.fives,
            scorecard.upper_section.sixes,
            scorecard.lower_section.three_of_a_kind,
            scorecard.lower_section.four_of_a_kind,
            scorecard.lower_section.full_house,
            scorecard.lower_section.small_straight,
            scorecard.lower_section.large_straight,
            scorecard.lower_section.yahtzee,
            scorecard.lower_section.chance
        ]

        # Replace None with -1
        scorecard_state = [0 if x is None else 1 for x in scorecard_state]

        return np.array(dice_state + scorecard_state)

# Example usage:
