from collections import Counter
from typing import Optional

from model.excpetion import AlreadyPlayedError


class YahtzeeScoreCard:
    def __init__(self):
        self.upper_section = UpperSection()
        self.lower_section = LowerSection()

    def is_full(self) -> bool:
        return all([val is not None for attr, val in vars(self.upper_section).items()]) and \
            all([val is not None for attr, val in vars(self.lower_section).items()])

    def card_points(self):
        return self.upper_section.get_total_no_bonus() + self.lower_section.get_total()

    def play_ones(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.upper_section.aces is not None:
            raise AlreadyPlayedError('Already played ones')
        points = sum([dice for dice in dice_rolls if dice == 1])

        if not trial:
            self.upper_section.aces = points

        return points

    def play_twos(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.upper_section.twos is not None:
            raise AlreadyPlayedError('Already played twos')
        points = sum([dice for dice in dice_rolls if dice == 2])

        if not trial:
            self.upper_section.twos = points

        return points

    def play_threes(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.upper_section.threes is not None:
            raise AlreadyPlayedError('Already played threes')
        points = sum([dice for dice in dice_rolls if dice == 3])

        if not trial:
            self.upper_section.threes = points

        return points

    def play_fours(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.upper_section.fours is not None:
            raise AlreadyPlayedError('Already played fours')
        points = sum([dice for dice in dice_rolls if dice == 4])

        if not trial:
            self.upper_section.fours = points

        return points

    def play_fives(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.upper_section.fives is not None:
            raise AlreadyPlayedError('Already played fives')
        points = sum([dice for dice in dice_rolls if dice == 5])

        if not trial:
            self.upper_section.fives = points

        return points

    def play_sixes(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.upper_section.sixes is not None:
            raise AlreadyPlayedError('Already played sixes')
        points = sum([dice for dice in dice_rolls if dice == 6])

        if not trial:
            self.upper_section.sixes = points

        return points

    def play_three_of_a_kind(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.lower_section.three_of_a_kind is not None:
            raise AlreadyPlayedError('Already played three of a kind')

        # get number where there are 3 from and sum all dice if the 3 of a kind is there
        count = Counter(dice_rolls)
        three_of_a_kind = [key for key, val in count.items() if val >= 3]
        if len(three_of_a_kind) > 0:
            points = sum(dice_rolls)
        else:
            points = 0

        if not trial:
            self.lower_section.three_of_a_kind = points

        return points

    def play_four_of_a_kind(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.lower_section.four_of_a_kind is not None:
            raise AlreadyPlayedError('Already played four of a kind')

        # get number where there are 4 from and sum all dice if the 4 of a kind is there
        count = Counter(dice_rolls)
        four_of_a_kind = [key for key, val in count.items() if val >= 4]
        if len(four_of_a_kind) > 0:
            points = sum(dice_rolls)
        else:
            points = 0

        if not trial:
            self.lower_section.four_of_a_kind = points

        return points

    def play_full_house(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.lower_section.full_house is not None:
            raise AlreadyPlayedError('Already played full house')

        # get number where there are 3 from and 2 from and sum all dice if the full house is there
        count = Counter(dice_rolls)
        three_of_a_kind = [key for key, val in count.items() if val >= 3]
        two_of_a_kind = [key for key, val in count.items() if val >= 2]
        if len(three_of_a_kind) > 0 and len(two_of_a_kind) > 1:  # they can't both be 1, they are the same pair
            points = 25
        else:
            points = 0

        if not trial:
            self.lower_section.full_house = points

        return points

    def play_small_straight(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.lower_section.small_straight is not None:
            raise AlreadyPlayedError('Already played small straight')

        arr = sorted(set(dice_rolls))  # Sort and remove duplicates

        # Check for the possible straights
        points = None
        for seq in [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]:
            if all(num in arr for num in seq):
                points = 30
                break

        if points is None:
            points = 0

        if not trial:
            self.lower_section.small_straight = points

        return points

    def play_large_straight(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.lower_section.large_straight is not None:
            raise AlreadyPlayedError('Already played large straight')

        arr = sorted(set(dice_rolls))
        if arr in [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]:
            points = 40
        else:
            points = 0

        if not trial:
            self.lower_section.large_straight = points

        return points

    def play_yahtzee(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.lower_section.yahtzee is not None:
            raise AlreadyPlayedError('Already played yahtzee')

        count = Counter(dice_rolls)
        yahtzee = [key for key, val in count.items() if val >= 5]
        if len(yahtzee) > 0:
            points = 50
        else:
            points = 0

        if not trial:
            self.lower_section.yahtzee = points

        return points

    def play_chance(self, dice_rolls: [int], trial: bool = False) -> int:
        if self.lower_section.chance is not None:
            raise AlreadyPlayedError('Already played chance')

        points = sum(dice_rolls)

        if not trial:
            self.lower_section.chance = points

        return points


class UpperSection:
    def __init__(self):
        self.aces: Optional[int] = None
        self.twos: Optional[int] = None
        self.threes: Optional[int] = None
        self.fours: Optional[int] = None
        self.fives: Optional[int] = None
        self.sixes: Optional[int] = None

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

    def get_total(self):
        total = 0

        for attr, val in vars(self).items():
            if val is not None:
                total += val

        return total

    def get_yahtzee_bonus(self):
        return self.yahtzee * 100
