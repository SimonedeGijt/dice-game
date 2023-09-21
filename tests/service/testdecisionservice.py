from model.game import Yahtzee
from model.player import Player
from service.decisionservice import SmartDecisionService
from service.recognition import DiceService


def test_good_decisions_also_if_its_taken(mocker):
    service = SmartDecisionService()
    player = Player('smartBoy', service)
    game = Yahtzee(1, [player])

    mocker.patch.object(DiceService, 'dice_rols', return_value=[5, 5, 5, 5, 5])

    _, action = service.decide(game, player)
    assert action == 12

    # now what is the action if yahtzee is already taken
    player.score_card.lower_section.yahtzee = 50
    _, action = service.decide(game, player)
    assert action == 8
