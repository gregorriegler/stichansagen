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

def test_start():
    game = Stichansagen()
    game.add_player("Gregor")

    game.start()

    assert str(game) == dedent("""\
                        Gregor
                        ===
                        ?

                        Gregor gibt 1
                        Gregor sagt:
                        """)

def test_cannot_call_without_start():
    game = Stichansagen()
    game.add_player("Gregor")
    
    game.call("Gregor", 1)

    assert str(game) == dedent("""\
                        Gregor
                        ===
                        """)

def test_call1():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()

    game.call("Gregor", 1)

    assert str(game) == dedent("""\
                        Gregor Christina
                        ===
                        1 ?

                        Gregor gibt 1
                        Christina sagt:
                        """)

def test_call2():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call("Gregor", 1)

    game.call("Christina", 0)

    assert str(game) == dedent("""\
                        Gregor Christina
                        ===
                        1/? 0/
                        """)

def test_correct_6():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call("Gregor", 1)
    game.call("Christina", 0)

    game.record_actual("Gregor", 1)

    assert str(game) == dedent("""\
                        Gregor Christina
                        ===
                        6(1/1) 0/?
                        """)

def test_correct_5():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call("Gregor", 0)
    game.call("Christina", 0)

    game.record_actual("Gregor", 0)

    assert str(game) == dedent("""\
                        Gregor Christina
                        ===
                        5(0/0) 0/?
                        """)

def test_wrong_5():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call("Gregor", 0)
    game.call("Christina", 0)

    game.record_actual("Gregor", 1)

    assert str(game) == dedent("""\
                        Gregor Christina
                        ===
                        -5(0/1) 0/?
                        """)


def test_wrong_6():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call("Gregor", 1)
    game.call("Christina", 0)

    game.record_actual("Gregor", 0)

    assert str(game) == dedent("""\
                        Gregor Christina
                        ===
                        -6(1/0) 0/?
                        """)


