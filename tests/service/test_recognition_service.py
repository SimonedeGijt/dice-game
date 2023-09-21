from service.recognition import DiceService


def test_predict_valid_response():
    service = DiceService()
    result = service.dice_rols(None)
    assert len(result) == 5
