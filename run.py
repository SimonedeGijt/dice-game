import logging

from colorlog import ColoredFormatter

from model.game import Yahtzee


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

    logging.info('starting game')
    game = Yahtzee(4)
    logging.info('game started')
