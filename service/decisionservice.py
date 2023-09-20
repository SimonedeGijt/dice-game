from model.scorecard import ScoreCard


class DecisionService:
    def __init__(self):
        pass

    def decide_optimal_play(self, dice_rolls: [int], score_card: ScoreCard) -> ScoreCard:
        # find first thing that is not filled in
        # if nothing is filled in, find the thing that is most likely to be filled in

        score_card.fill_first_none(sum(dice_rolls))

        return score_card
