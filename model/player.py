import logging

from model.scorecard import ScoreCard


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.score_card: [ScoreCard] = []

    def get_total(self):
        total = 0
        for score_card in self.score_card:
            total += score_card.get_total()

        logging.info(f'{self.name} has a total of {total} points')
        return total

    def start_game(self):
        self.score_card.append(ScoreCard())
