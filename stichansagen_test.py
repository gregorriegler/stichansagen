from stichansagen import Stichansagen
from stichansagen import PlayerRound
from textwrap import dedent


def test_starts_empty():
    game = Stichansagen()
    assert game.players == []
    assert game.headers() == [""]
    assert game.body() == [['1'],['']]

def test_add_player():
    game = Stichansagen()
    game.add_player("Gregor")
    assert game.players == ["Gregor"]
    assert game.headers() == ["", "Gregor"]

def test_add_another_player():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    assert game.players == ["Gregor", "Christina"]
    assert game.headers() == ["", "Gregor", "Christina"]
    
def test_body():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    assert game.body() == [
        ["1", "", "?"],
        ["", "0", "0"]
    ]
    assert game.gibt() == "Gregor"

def test_call_1():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    
    game.input(1)

    assert game.body() == [
        ["1", "?", "1"],
        ["", "0", "0"]
    ]

def test_call_2():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    
    game.input(1)
    game.input(0)
    
    assert game.body() == [
        ["1", "0", "1/?"],
        ["", "0", "0"]
    ]

def test_correct_6():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
   
    game.input(1)
    game.input(0)
    game.input(1)
    
    assert game.body() == [
        ["1", "0/?", "1/1:6"],
        ["", "0", "6"]
    ]
    
def test_correct_5():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    
    game.input(0)
    game.input(0)
    game.input(0)
    
    assert game.body() == [
        ["1", "0/?", "0/0:5"],
        ["", "0", "5"]
    ]

def test_wrong_5():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    
    game.input(0)
    game.input(0)
    game.input(1)
    
    assert game.body() == [
        ["1", "0/?", "0/1:-5"],
        ["", "0", "-5"]
    ]

def test_wrong_6():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    
    game.input(1)
    game.input(0)
    game.input(0)
    
    assert game.body() == [
        ["1", "0/?", "1/0:-6"],
        ["", "0", "-6"]
    ]

def test_play_with_inputs():
    game = Stichansagen()
    game.add_player("Gregor")
    game.add_player("Christina")
    
    game.input(0)
    game.input(1)
    game.input(2)
    game.input(1)
    game.input(3)
    
    assert game.body() == [
        ["1", "1/1:6", "0/2:-5"],
        ["2", "3", "?"],
        ["", "6", "-5"]
    ]

def test_reset():
    game = Stichansagen(rounds = [1, 1])
    game.add_player("Gregor")
    game.add_player("Christina")

    game.reset()

    assert game.body() == [
        ["1", "", "?"],
        ["", "0", "0"]
    ]

def test_undo():
    game = Stichansagen(rounds = [1, 2])
    game.add_player("Gregor")
    game.add_player("Christina")
    game.input(1)

    game.undo()
    
    assert game.body() == [
        ["1", "", "?"],
        ["", "0", "0"]
    ]

def test_undo2():
    game = Stichansagen(rounds = [1, 2])
    game.add_player("Gregor")
    game.add_player("Christina")
    game.input(1)
    game.input(1)

    game.undo()
    
    assert game.body() == [
        ["1", "?", "1"],
        ["", "0", "0"]
    ]

def test_play_til_end():
    game = Stichansagen(rounds = [1])
    game.add_player("Gregor")
    game.add_player("Christina")
    
    game.input(1)
    game.input(0)
    game.input(1)
    game.input(0)

    assert game.body() == [
        ["1", "0/0:5", "1/1:6"],
        ["", "5", "6"]
    ]


def test_ignore_too_many_inputs():
    game = Stichansagen(rounds = [1])
    game.add_player("Gregor")
    game.input(1)
    game.input(1)
    game.input(1)

    assert game.inputs == [1, 1]