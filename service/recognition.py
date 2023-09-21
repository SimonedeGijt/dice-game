import os
from random import Random

from service.recognizeDice import recognizeDiceInImage


class DiceService:
    def __init__(self, ):
        pass

    def dice_rols(self, image, dice_needed: int = 5) -> [int]:
        env = os.getenv('ENV', 'dev')
        if env == 'dev':
            random = Random()
            return [random.randint(1, 6) for _ in range(dice_needed)]
        else:
            dice_results = recognizeDiceInImage()
            return dice_results[0:dice_needed]
