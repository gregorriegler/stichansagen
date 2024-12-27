from stichansagen import Stichansagen
from stichansagen import PlayerRound
from textwrap import dedent


def test_starts_empty():
    game = Stichansagen()
    assert game.players == []
    assert game.headers() == [""]
    assert game.body() == []

def test_add_player():
    game = Stichansagen()
    game.add_player("Gregor")
    assert game.players == ["Gregor"]
    assert game.headers() == ["", "Gregor"]
    assert game.body() == []

def test_add_another_player():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    assert game.players == ["Gregor", "Christina"]
    assert game.headers() == ["", "Gregor", "Christina"]

def test_cannot_call_without_start():
    game = Stichansagen()
    game.add_player("Gregor")
    
    game.call(PlayerRound("Gregor", 0), 1)

    assert game.body() == []
    assert game.info() == ""
    
def test_start():
    game = Stichansagen()
    game.add_player("Gregor")

    game.start()

    assert game.body() == [
        ["1", "?"],
        ["", "0"]
    ]
    assert game.info() == "Gregor gibt 1"

def test_call_1():
    game = Stichansagen()
    game.add_player("Gregor")
    game.start()

    game.call(PlayerRound("Gregor", 0), 1)

    assert game.body() == [
        ["1", "1/?"],
        ["", "0"]
    ]

def test_correct_6():
    game = Stichansagen()
    game.add_player("Gregor")
    game.start()
    game.call(PlayerRound("Gregor", 0), 1)
    game.record_actual(PlayerRound("Gregor", 0), 1)

    assert game.body() == [
        ["1", "6(1/1)"],
        ["2", "?"],
        ["", "6"]
    ]

def test_two_rounds():
    game = Stichansagen()
    game.add_player("Gregor")
    game.start()
    game.call(PlayerRound("Gregor", 0), 1)
    game.record_actual(PlayerRound("Gregor", 0), 1)
    
    game.call(PlayerRound("Gregor", 1), 2)
    game.record_actual(PlayerRound("Gregor", 1), 2)


    assert game.body() == [
        ["1", "6(1/1)"],
        ["2", "7(2/2)"],
        ["3", "?"],
        ["", "13"]
    ]

def test_call_1_with_second_player():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()

    game.call(PlayerRound("Gregor", 0), 1)

    assert game.body() == [
        ["1", "1", "?"],
        ["", "0", "0"]
    ]

def test_call_2():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call(PlayerRound("Gregor", 0), 1)

    game.call(PlayerRound("Christina", 0), 0)

    assert game.body() == [
        ["1", "1/?", "0/"],
        ["", "0", "0"]
    ]

def test_correct_6_against_christina():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call(PlayerRound("Gregor", 0), 1)
    game.call(PlayerRound("Christina", 0), 0)

    game.record_actual(PlayerRound("Gregor", 0), 1)

    assert game.body() == [
        ["1", "6(1/1)", "0/?"],
        ["", "6", "0"]
    ]
    
def test_correct_5():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call(PlayerRound("Gregor", 0), 0)
    game.call(PlayerRound("Christina", 0), 0)

    game.record_actual(PlayerRound("Gregor", 0), 0)

    assert game.body() == [
        ["1", "5(0/0)", "0/?"],
        ["", "5", "0"]
    ]

def test_wrong_5():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call(PlayerRound("Gregor", 0), 0)
    game.call(PlayerRound("Christina", 0), 0)

    game.record_actual(PlayerRound("Gregor", 0), 1)

    assert game.body() == [
        ["1", "-5(0/1)", "0/?"],
        ["", "-5", "0"]
    ]

def test_wrong_6():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()
    game.call(PlayerRound("Gregor", 0), 1)
    game.call(PlayerRound("Christina", 0), 0)

    game.record_actual(PlayerRound("Gregor", 0), 0)

    assert game.body() == [
        ["1", "-6(1/0)", "0/?"],
        ["", "-6", "0"]
    ]

def test_play_til_end():
    game = Stichansagen(rounds = [1])
    game.add_player("Gregor")
    game.start()
    game.call(PlayerRound("Gregor", 0), 1)
    game.record_actual(PlayerRound("Gregor", 0), 1)

    assert game.body() == [
        ["1", "6(1/1)"],
        ["", "6"]
    ]

def test_play_with_inputs():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    game.start()

    game.input(0)
    game.input(1)
    game.input(2)
    game.input(1)
    game.input(3)
    
    assert game.body() == [
        ["1", "-5(0/2)", "6(1/1)"],
        ["2", "3", "?"],
        ["", "-5", "6"]
    ]

def test_duplicate_rounds():
    game = Stichansagen(rounds = [1, 1])
    game.add_player("Gregor")
    game.start()
    game.input(1)
    game.input(1)
    game.input(1)
    game.input(1)
    
    assert game.body() == [
        ["1", "6(1/1)"],
        ["1", "6(1/1)"],
        ["", "12"]
    ]