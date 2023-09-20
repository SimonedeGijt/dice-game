from typing import Optional


class ScoreCard:
    def __init__(self):
        self.upper_section = UpperSection()
        self.lower_section = LowerSection()

    def get_total(self):
        return self.upper_section.get_total() + self.lower_section.get_total()


class UpperSection:
    def __init__(self):
        self.aces: Optional[int] = None
        self.twos: Optional[int] = None
        self.threes: Optional[int] = None
        self.fours: Optional[int] = None
        self.fives: Optional[int] = None
        self.sixes: Optional[int] = None

    def get_total(self):
        return self.get_upper_total() + self.get_bonus()

    def get_bonus(self):
        if self.get_upper_total() >= 63:
            return 35
        else:
            return 0

    def get_upper_total(self):
        return self.aces + self.twos + self.threes + self.fours + self.fives + self.sixes


class LowerSection:
    def __init__(self):
        self.three_of_a_kind: Optional[int] = None
        self.four_of_a_kind: Optional[int] = None
        self.full_house: Optional[int] = None
        self.small_straight: Optional[int] = None
        self.large_straight: Optional[int] = None
        self.yahtzee: Optional[int] = None
        self.chance: Optional[int] = None

    def get_total(self):
        return self.three_of_a_kind + self.four_of_a_kind + self.full_house + self.small_straight + self.large_straight + self.yahtzee + self.chance + self.get_yahtzee_bonus()

    def get_yahtzee_bonus(self):
        return self.yahtzee * 100
