import logging

from colorlog import ColoredFormatter

from model.game import Yahtzee
from model.player import Player
from service.decisionservice import SmartDecisionService


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)


if __name__ == '__main__':
    setup_logger()

    players = [
        # Player('random1', RandomDecisionService()),
        # Player('random2', RandomDecisionService()),
        Player('smart1', SmartDecisionService()),
        # Player('smart2', SmartDecisionService())
    ]

    winners_averages = {}
    for i in range(10):
        logging.info(f'starting game {i}')
        game = Yahtzee(2, players)
        logging.info('finished game')

        winner = game.play_game()
        if winner.name not in winners_averages:
            winners_averages[winner.name] = []

        winners_averages[winner.name].append(winner.get_total())

    logging.info(f'averages: {winners_averages}, \n'
                 f'average: {sum(winners_averages["smart1"]) / len(winners_averages["smart1"])} \n '
                 f'max: {max(winners_averages["smart1"])} \n '
                 f'min: {min(winners_averages["smart1"])}'
                 )
