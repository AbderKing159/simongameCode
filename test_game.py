import pytest
from game import SimonGame

@pytest.fixture
def simon_game():
    return SimonGame()

def test_button_highlight(simon_game):
    button = simon_game.buttons[0]
    button.highlight()
    assert button.highlighted == True

def test_button_reset_highlight(simon_game):
    button = simon_game.buttons[0]
    button.highlight()
    button.reset_highlight()
    assert button.highlighted == False

def test_generate_pattern(simon_game):
    simon_game.generate_pattern(4)
    assert len(simon_game.pattern) == 4

def test_save_high_score(simon_game):
    high_score_file = "C:\\Users\\Abderrahmane\\Desktop\\pygamex\\high_score.txt"
    simon_game.save_high_score(30)
    with open(high_score_file, "r") as file:
        assert int(file.read()) == 30
