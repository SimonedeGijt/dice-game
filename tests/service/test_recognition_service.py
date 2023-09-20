from service.recognition import RecognitionService


def test_predict_valid_response():
    service = RecognitionService()
    result = service.dice_rols(None)
    assert len(result) == 5
