from stichansagen import Stichansagen
from textwrap import dedent


def test_starts_empty():
    game = Stichansagen()
    assert str(game) == ""

def test_add_player():
    game = Stichansagen()
    game.add_player("Gregor")
    assert str(game) == dedent("""\
                        Gregor
                        ===
                        """)

def test_add_another_player():
    game = Stichansagen()
    game.add_player("Gregor")

    game.add_player("Christina")

    assert str(game) == dedent("""\
                        Gregor Christina
                        ===
                        """)

def test_next():
    game = Stichansagen()
    game.add_player("Gregor")

    game.next()

    assert str(game) == dedent("""\
                        Gregor
                        ===

                        Gregor gibt 1
                        """)