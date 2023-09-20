import logging

from model.scorecard import ScoreCard
from service.decisionservice import DecisionService


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.score_card: [ScoreCard] = []
        self.decision_model: DecisionService = DecisionService()

    def get_total(self):
        total = self.score_card[-1].get_total()

        logging.info(f'{self.name} has a total of {total} points')
        return total

    def start_game(self):
        self.score_card.append(ScoreCard())

    def play_round(self, dice_rolls: [int]):
        self.score_card = self.decision_model.decide_optimal_play(dice_rolls, self.score_card[-1])
