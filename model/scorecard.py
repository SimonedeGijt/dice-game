from typing import Optional


class ScoreCard:
    def __init__(self):
        self.upper_section = UpperSection()
        self.lower_section = LowerSection()

    def card_points(self):
        return self.upper_section.get_total_no_bonus() + self.lower_section.get_total()

    def fill_first_none(self, value: int):
        if not self.upper_section.set_first_none(value):
            self.lower_section.set_first_none(value)


class UpperSection:
    def __init__(self):
        self.aces: Optional[int] = None
        self.twos: Optional[int] = None
        self.threes: Optional[int] = None
        self.fours: Optional[int] = None
        self.fives: Optional[int] = None
        self.sixes: Optional[int] = None

    def set_first_none(self, value: int):
        for attr, val in vars(self).items():
            if val is None:
                setattr(self, attr, value)
                return True  # Property was set
        return False  # No property was set

    def get_total_no_bonus(self):
        return self.get_total() + self.get_bonus()

    def get_bonus(self):
        if self.get_total() >= 63:
            return 35
        else:
            return 0

    def get_total(self):
        total = 0

        for attr, val in vars(self).items():
            if val is not None:
                total += val

        return total


class LowerSection:
    def __init__(self):
        self.three_of_a_kind: Optional[int] = None
        self.four_of_a_kind: Optional[int] = None
        self.full_house: Optional[int] = None
        self.small_straight: Optional[int] = None
        self.large_straight: Optional[int] = None
        self.yahtzee: Optional[int] = None
        self.chance: Optional[int] = None

    def set_first_none(self, value: int):
        for attr, val in vars(self).items():
            if val is None:
                setattr(self, attr, value)
                return True  # Property was set
        return False  # No property was set

    def get_total(self):
        total = 0

        for attr, val in vars(self).items():
            if val is not None:
                total += val

        return total

    def get_yahtzee_bonus(self):
        return self.yahtzee * 100
