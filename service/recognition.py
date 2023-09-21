import os
from random import Random

from service.recognizeDice import recognize_dice_in_image


class DiceService:
    def __init__(self, ):
        pass

    def dice_rols(self, image, dice_needed: int = 5) -> [int]:
        env = os.getenv('ENV')
        if env == 'dev':
            random = Random()
            return [random.randint(1, 6) for _ in range(dice_needed)]
        else:
            dice_results = recognize_dice_in_image()
            return dice_results[0:dice_needed]
