from tabulate import tabulate

class Stichansagen:

    def __init__(self, rounds = [1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1,"K"]) -> None:
        self.rounds = rounds
        self.players = []
        self.reset()

    def reset(self):
        self.inputs = []
        self.plays = {}
        self.calling = 0
        self.roundIndex = 0
        self.player_round = PlayerRound(self.calling_player(), self.roundIndex) #tbd unused

    def add_player(self, name):
        self.players.append(name)

    def next(self):
        if(self.roundIndex == None):
            self.roundIndex = 0
        elif (len(self.rounds) > self.roundIndex + 1):
            self.roundIndex += 1
        next = self.calling_player()
        self.player_round = PlayerRound(next, self.roundIndex)
        

    def input(self, number):
        self.inputs.append(number)
        calling_player = self.calling_player()
        player_round = PlayerRound(calling_player, self.roundIndex)
        if(not self.has_called(player_round)):
            self.call(player_round, number)
        else:
            self.record_actual(player_round, number)    

    def undo(self):
        self.again = self.inputs[:-1]
        self.reset()
        for input in self.again:
            self.input(input)
        
    def call(self, player_round, stiche):
        self.plays[player_round] = Play(stiche)
        self.set_calling_to_next()
        self.player_round = PlayerRound(self.calling_player(), self.roundIndex)

    def record_actual(self, player_round, stiche):
        self.plays[player_round] = Play(self.plays[player_round].called, stiche)
        self.set_calling_to_next()
        if(self.all_actuals_given()):
            self.next()

    def set_calling_to_next(self):
        self.calling = (self.calling + 1) % len(self.players)
            
    def is_player_to_record_actuals_from(self, player):
        return self.player_to_record_actuals() == player

    def player_to_record_actuals(self):
        for player in self.players:
            player_round = PlayerRound(player, self.roundIndex)
            if(player_round not in self.plays or self.plays[player_round].actual is None):
                return player        

    def rounds_played(self):
        if(self.roundIndex == None or self.roundIndex == 0):
            return [0]
        return range(0, self.roundIndex + 1)
    
    def __str__(self):
        return self.table() + "\n" + self.info()

    def table(self):
        return tabulate(self.body(), self.headers())
    
    def headers(self):
        return ["", *self.players]
    
    def body(self):
        if self.roundIndex is None:
            return []
        
        body = []
        for round in self.rounds_played():
            row = []
            row.append(str(self.rounds[round]))
            for player in self.players:
                row.append(self.cell_output(PlayerRound(player, round)))
            body.append(row)

        totals = [""]
        for player in self.players:
            total = 0
            for round in self.rounds_played():
                total += self.points(PlayerRound(player, round))
            totals.append(str(total))
        body.append(totals)

        return body
    
    def gibt(self):
        return self.players[self.roundIndex % len(self.players)]
    
    def info(self):
        gibt = ""
        if(self.players and self.roundIndex != None):
            gibt = self.gibt() + " gibt " + str(self.rounds[self.roundIndex])
        return gibt

    def cell_output(self, player_round):
        if(not self.has_called(player_round)):
            if(player_round.player is self.calling_player()): 
                return "?"
            else:
                return ""
        if(self.everybody_called(player_round.round)):
            if(self.actuals_given(player_round)):
                return self.called_vs_actual(player_round) + ":" + str(self.points(player_round)) 
            else:
                return self.called_vs_actual(player_round)      
        return str(self.call_of(player_round))

    def everybody_called(self, round):
        for player in self.players:
            if(not self.has_called(PlayerRound(player, round))):
                return False
        return True
    
    def has_called(self, player_round):
        return player_round in self.plays and self.plays[player_round].is_called()
    
    def all_actuals_given(self):
        for player in self.players:
            if(not self.actuals_given(PlayerRound(player, self.roundIndex))):
                return False
        return True

    def points(self, player_round):
        potential_points = self.potential_points(player_round)
        if(self.correct(player_round)):
            return potential_points
        if(self.wrong(player_round)):
            return potential_points * -1
        return 0;
        
    def potential_points(self, player_round):
        return self.get_play(player_round).potential_points()
        
    def get_play(self, player_round):
        if (player_round in self.plays): 
            return self.plays[player_round]
        return NotPlayed()

    def called_vs_actual(self, player_round):
        call_value = str(self.call_of(player_round))
        actual_value = self.actual_output(player_round)
        if(actual_value == ""):
            return call_value
        return "/".join([call_value, actual_value])

    def correct(self, player_round):
        return player_round in self.plays and self.plays[player_round].correct()
        
    def wrong(self, player_round):
        return player_round in self.plays and self.plays[player_round].wrong()
        
    def actual_output(self, player_round):
        if(self.actuals_given(player_round)):
            return str(self.actual_of(player_round))
        if(self.is_player_to_record_actuals_from(player_round.player)):
            return "?"
        return ""

    def call_of(self, player_round):
        return self.get_play(player_round).called
        
    def actual_of(self, player_round):
        return self.get_play(player_round).actual
        
    def actuals_given(self, player_round):
        return player_round in self.plays and self.plays[player_round].is_played()

    def calling_player(self):
        if self.calling < len(self.players):
            return self.players[self.calling]
        else:
            return ""


class PlayerRound:

    def __init__(self, player, round):
        self.player = player
        self.round = round
    
    def __hash__(self):
        return hash((self.player, self.round))
    
    def __eq__(self, value: object) -> bool:
        return self.player == value.player and self.round == value.round
    
    def __str__(self):
        return str(self.player) + "(" + str(self.round) + ")"


class Play:

    def __init__(self, called=None, actual=None):
        self.called = called
        self.actual = actual

    def is_called(self):
        return self.called is not None
    
    def is_played(self):
        return self.actual is not None
    
    def potential_points(self):
        if(not self.is_called()):
            return 0
        return 5 + self.called
    
    def correct(self):
        return self.is_called() and self.is_played() and self.called == self.actual

    def wrong(self):
        return self.is_called() and self.is_played() and self.called != self.actual
    
class NotPlayed(Play):
    pass

    
# wer beginnt zu rufen ist falsch