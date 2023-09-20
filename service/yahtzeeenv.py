from collections import Counter
from typing import Optional

import gym
import numpy as np
from gym import spaces

from model.excpetion import AlreadyPlayedError
from model.game import Yahtzee
from service.decisionservice import DecisionService


class YahtzeeEnv(gym.Env):
    def __init__(self):
        super(YahtzeeEnv, self).__init__()

        # Define action and observation spaces
        self.action_space = spaces.Discrete(13)  # 13 different scoring categories
        self.observation_space = spaces.Box(low=np.array([1, 1, 1, 1, 1, 1] + [-1] * 13),
                                            high=np.array([6, 6, 6, 6, 6, 6] + [50] * 13),
                                            dtype=np.int)

        # Initialize game-specific variables
        self.game = Yahtzee(1)
        self.decision_service = DecisionService()
        self.dice = self.game.recognition_service.dice_rols(None)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        # Reset the game state
        self.game = Yahtzee(1)
        return self._get_state()

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

        return state, reward, done, {}

    def _get_state(self, ):
        # Convert the dice rolls to the frequency count representation
        counts = Counter(self.dice)
        state = [counts[i] for i in range(1, 7)]
        return np.array(state)

# Example usage:
