from model.yahtzeescorecard import YahtzeeScoreCard
from service.decisionservice import RandomDecisionService


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.score_card: YahtzeeScoreCard = YahtzeeScoreCard()
        self.decision_model: RandomDecisionService = RandomDecisionService()

    def get_total(self):
        total = self.score_card.card_points()
        return total

    def start_game(self):
        self.score_card = YahtzeeScoreCard()

    def play_round(self, game):
        self.score_card = self.decision_model.play_optimal_play(game, self)
