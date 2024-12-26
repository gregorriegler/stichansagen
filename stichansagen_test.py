from stichansagen import Stichansagen


def test_starts_empty():
    game = Stichansagen()
    assert str(game) == ""

def test_add_player():
    game = Stichansagen()
    game.add_player("Gregor")
    assert str(game) == "Gregor"

def test_add_another_player():
    game = Stichansagen()
    game.add_player("Gregor")

    game.add_player("Christina")

    assert str(game) == "Gregor Christina"