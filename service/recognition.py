from random import Random
import os
import recognizeDice

class RecognitionService:
    def __init__(self, ):
        pass

    def dice_rols(self, image, dice_needed: int = 5) -> [int]:
        env = os.getenv('ENV')
        if (env == 'dev'):
            random = Random()
            return [random.randint(1, 6) for _ in range(dice_needed)]
        else:
            diceResults = recognizeDice.recognizeDiceInImage("")
            return diceResults[0:dice_needed]
