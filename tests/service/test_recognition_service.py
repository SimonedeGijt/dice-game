from service.recognition import DiceService
from service.recognizeDice import recognize_dice_in_image
import pytest
import os

@pytest.mark.parametrize("file_name, expected_response", [
    ("../resources/pictures2/test0.jpg", [2, 3, 4, 4, 5]),
    ("../resources/pictures2/test1.jpg", [1, 3, 3, 4, 6]),
    ("../resources/pictures2/test2.jpg", [1, 3, 4, 5, 6]),
    ("../resources/pictures2/test3.jpg", [1, 2, 4, 4, 5]),
    ("../resources/pictures2/test4.jpg", [1, 2, 4, 6, 6]),
    ("../resources/pictures2/test5.jpg", [3, 4, 4, 6, 6]),
    ("../resources/pictures2/test6.jpg", [1, 1, 4, 4, 5]),
    ("../resources/pictures2/test7.jpg", [2, 3, 4, 6, 6]),
    ("../resources/pictures2/test8.jpg", [1, 2, 3, 6, 6]),
    ("../resources/pictures2/test9.jpg", [1, 1, 2, 3, 4]),
    ("../resources/pictures2/test10.jpg", [1, 3, 5, 5, 6]),
    ("../resources/pictures2/test11.jpg", [1, 2, 4, 5, 6]),
    ("../resources/pictures2/test12.jpg", [1, 2, 2, 2, 2]),
    ("../resources/pictures2/test13.jpg", [2, 3, 4, 5, 5]),
    ("../resources/pictures2/test14.jpg", [2, 3, 3, 4, 5]),
    ("../resources/pictures2/test15.jpg", [4, 4, 4, 5, 6]),
    ("../resources/pictures2/test16.jpg", [2, 5, 5, 5, 6]),
    ("../resources/pictures2/test17.jpg", [1, 1, 2, 2, 5]),
    ("../resources/pictures2/test18.jpg", [1, 2, 3, 3, 4]),
    ("../resources/pictures2/test19.jpg", [1, 1, 2, 3, 3])

])
def test_image_recogniton(file_name, expected_response):
    os.putenv("ENV", "dev")
    dice_result = recognize_dice_in_image(file_name)
    dice_result.sort()
    print(dice_result)
    assert dice_result == expected_response

