from random import Random


class DiceService:
    def __init__(self, ):
        pass

    def dice_rols(self, image, dice_needed: int = 5) -> [int]:
        random = Random()

        return [random.randint(1, 6) for _ in range(dice_needed)]
