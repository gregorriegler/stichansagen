class Stichansagen:

    rounds = [1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1,"K"]

    def __init__(self) -> None:
        self.round = None
        self.players = []
        self.calls = {}
        self.actuals = {}
        self.calling = 0

    def add_player(self, name):
        self.players.append(name)

    def start(self):
        self.round = self.rounds[0]

    def call(self, player, stiche):
        if(self.round == 0): return
        self.calls[(player, self.round)] = stiche
        self.calling = (self.calling + 1) % len(self.players)

    def record_actual(self, player, stiche):
        self.actuals[(player, self.round)] = stiche

    def is_player_to_record_actuals_from(self, player):
        return self.player_to_record_actuals() == player

    def player_to_record_actuals(self):
        for player in self.players:
            if((player, self.round) not in self.actuals):
                return player        

    def rounds_played(self):
        print(self.round)
        if(self.round == None):
            return [self.rounds[0]]
        return self.rounds[:self.round]

    def __str__(self):
        header = ""
        if(self.players):
            header = " ".join(self.players)
            header += "\n===\n"

        calls_output = self.calls_output()
        
        gibt = ""
        call = ""
        
        if(self.players and self.round and not self.everybody_called()):
            gibt = "\n" + self.players[0] + " gibt " + "1" + "\n"
            call = self.calling_player() + " sagt:" + "\n"

        return header + calls_output + gibt + call

    def calls_output(self):
        if self.round is None:
            return ""

        round_outputs = [
            " ".join(self.cell_output(player, round) for player in self.players)
            for round in self.rounds_played()
        ]

        return "\n".join(round_outputs) + "\n"

    def cell_output(self, player, round):
        if(not self.has_called(player, round)): return "?"
        if(self.everybody_called()):
            if(self.actuals_given(player, round)):
                return str(self.points(player, round)) + "(" + self.called_vs_actual(player, round) + ")" 
            return self.called_vs_actual(player, round)      
        return self.call_of_str(player, round)

    def has_called(self, player, round):
        return (player, round) in self.calls

    def everybody_called(self):
        for player in self.players:
            if((player, self.round) not in self.calls):
                return False
        return True

    def points(self, player, round):
        potential_points = self.potential_points(player, round)
        return potential_points if(self.correct(player, round)) else potential_points * -1

    def potential_points(self, player, round):
        return 5 + self.call_of(player, round)

    def called_vs_actual(self, player, round):
        call_value = self.call_of_str(player, round)
        actual_value = self.actual_output(player, round)
        return "/".join([call_value, actual_value])

    def correct(self, player, round):
        return self.calls[player, round] == self.actuals[(player, round)]

    def actual_output(self, player, round):
        if(self.actuals_given(player, round)):
            return self.actual_of_str(player, round)
        if(self.is_player_to_record_actuals_from(player)):
            return "?"
        return ""
                            
    def call_of_str(self, player, round):
        return str(self.calls[player, round])

    def call_of(self, player, round):
        return self.calls[(player, round)]

    def actual_of_str(self, player, round):
        return str(self.actual_of(player, round))

    def actual_of(self, player, round):
        return self.actuals[(player, round)]

    def actuals_given(self, player, round):
        return (player, round) in self.actuals

    def calling_player(self):
        return self.players[self.calling]


class PlayerRound:
    def __init__(self, player, round) -> None:
        self.players = player
        self.round = round
    