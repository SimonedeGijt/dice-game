from service.recognition import RecognitionService


def test_predict_valid_response():
    service = RecognitionService()
    result = service.predict(None)
    assert result == [1, 2, 3, 4, 5, 6]
