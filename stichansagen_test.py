from stichansagen import Stichansagen
from textwrap import dedent


def test_starts_empty():
    game = Stichansagen()
    assert game.headers() == []
    assert game.body() == []

def test_add_player():
    game = Stichansagen()
    game.add_player("Gregor")
    assert game.headers() == ["Gregor"]
    assert game.body() == []

def test_add_another_player():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    assert(game.headers() == ["Gregor", "Christina"])

def test_cannot_call_without_start():
    game = Stichansagen()
    game.add_player("Gregor")
    
    game.call("Gregor", 1)

    assert game.body() == []
    assert game.info() == ""
    
def test_start():
    game = Stichansagen()
    game.add_player("Gregor")

    game.start()

    assert game.headers() == ["Gregor"]
    assert game.body() == [["?"]]
    assert game.info() == "Gregor gibt 1"

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


# TBD mehr als 1 zeile
# TBD totals
# TBD playable