class Stichansagen:

    def __init__(self, rounds = [1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1,"K"], players = None):
        self.rounds = rounds
        if players is None:
            players = []
        self.players = players
        self.reset()

    def reset(self):
        self.inputs = []
        self.plays = {}
        self.roundIndex = 0
        self.player_round = PlayerRound(1, self.roundIndex)

    def add_player(self, name):
        self.players.append(name)
        
    def undo(self):
        without_last = self.inputs[:-1]
        self.reset()
        self.load(without_last)
        
    def load(self, inputs):
        if isinstance(inputs, str):
            self.load([int(char) for char in inputs if char.isdigit()])
        else:
            for input in inputs:
                self.input(input)

    def save(self):
        return "".join(str(i) for i in self.inputs)

    def input(self, number):
        if(self.is_over()):
            return
        self.inputs.append(number)
        self.set_current_play(self.get_current_play().input(number))
        self.next()

    def is_over(self):
        return len(self.inputs) > 0 and len(self.inputs) == len(self.rounds) * len(self.players) * 2

    def next(self):
        if(self.round_finished()):
            self.next_round()
        else:
            self.next_player()

    def round_finished(self):
        for player_idx, _ in enumerate(self.players):
            if(not self.get_play(PlayerRound(player_idx, self.roundIndex)).is_played()):
                return False
        return True

    def next_round(self):
        if(self.roundIndex == None):
            self.roundIndex = 0
        elif (len(self.rounds) > self.roundIndex + 1):
            self.roundIndex += 1
        player = (self.roundIndex + 1) % len(self.players)
        self.player_round = PlayerRound(player, self.roundIndex)
    
    def next_player(self):
        player = (self.player_round.player + 1) % len(self.players)
        self.player_round = PlayerRound(player, self.roundIndex)

    def rounds_played(self):
        if(self.roundIndex == None or self.roundIndex == 0):
            return [0]
        return range(0, self.roundIndex + 1)
    
    def headers(self):
        return ["", *self.players]
    
    def body(self):
        if self.roundIndex is None:
            return []
        
        body = []
        for round in self.rounds_played():
            row = []
            row.append(str(self.rounds[round]))
            for player_idx, _ in enumerate(self.players):
                row.append(self.cell_output(PlayerRound(player_idx, round)))
            body.append(row)

        totals = [""]
        for player_idx, _ in enumerate(self.players):
            total = self.player_total(player_idx)
            totals.append(str(total))
        body.append(totals)

        return body
    
    def player_total(self, player_idx):
        total = 0
        for round in self.rounds_played():
            total += self.get_play(PlayerRound(player_idx, round)).points()
        return total

    def gibt(self):
        return self.players[self.gibt_index()]
    
    def gibt_index(self):
        return self.roundIndex % len(self.players)

    def info(self):
        if(self.is_over()):
            return ",".join(self.leading_players()) + " won"
        gibt = ""
        if(self.players and self.roundIndex != None):
            gibt = self.gibt() + " gibt " + str(self.rounds[self.roundIndex])
        return gibt
    
    def leading_players(self):
        if(not self.players): return []
        totals = list(map(self.player_total, range(len(self.players))))
        max_score = max(totals)
        return [self.players[idx] for idx, total in enumerate(totals) if total == max_score]

    def cell_output(self, player_round):
        play = self.get_play(player_round)    
        if(player_round.player is self.player_round.player and (not play.is_called() or not play.is_played())):
            return play.print_dran()
        return play.print()

    def get_current_play(self):
        return self.get_play(self.player_round)
    
    def set_current_play(self, play):
        self.plays[self.player_round] = play
    
    def get_play(self, player_round):
        if (player_round in self.plays): 
            return self.plays[player_round]
        return NotPlayed()


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

    def input(self, number):
        if(not self.is_called() and not self.is_played()):
            return Play(number, None)
        if(self.is_called() and not self.is_played()):
            return Play(self.called, number)
        return Play()

    def is_called(self):
        return self.called is not None
    
    def is_played(self):
        return self.actual is not None
    
    def points(self):
        if(self.correct()):
            return self.potential_points()
        if(self.wrong()):
            return self.potential_points() * -1
        return 0;
    
    def potential_points(self):
        if(not self.is_called()):
            return 0
        return 5 + self.called
    
    def correct(self):
        return self.is_called() and self.is_played() and self.called == self.actual

    def wrong(self):
        return self.is_called() and self.is_played() and self.called != self.actual
    
    def print(self):
        if(self.is_played()):
            return str(self.called) + "/" + str(self.actual) + ":" + str(self.points())
        elif(self.is_called()):
            return str(self.called)
        else:
            return ""
        
    def print_dran(self):
        if(self.is_called()):
            return str(self.called) + "/" + "?" 
        else:
            return "?"

    
def NotPlayed():
    return Play()

    
# wer beginnt zu rufen ist falsch