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

    def call(self, name, stiche):
        if(self.round == 0): return
        self.calls[(self.round, name)] = stiche
        self.calling = (self.calling + 1) % len(self.players)

    def record_actual(self, name, stiche):
        self.actuals[(self.round, name)] = stiche

    def is_player_to_record_actuals_from(self, player):
        return self.player_to_record_actuals() == player

    def player_to_record_actuals(self):
        for player in self.players:
            if((self.round, player) not in self.actuals):
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
            " ".join(self.cell_output(round, player) for player in self.players)
            for round in self.rounds_played()
        ]

        return "\n".join(round_outputs) + "\n"

    def cell_output(self, round, player):
        if(not self.has_called(round, player)): return "?"
        if(self.everybody_called()):
            if(self.actuals_given(round, player)):
                if(self.correct(round, player)):
                    return str(5 + self.actual_of2(round, player)) +"("+self.called_vs_actual(round, player)+")" 
                else:
                    return "-6"+"("+self.called_vs_actual(round, player)+")" 
            return self.called_vs_actual(round, player)      
        return self.call_of(round, player)

    def has_called(self, round, player):
        return (round, player) in self.calls

    def everybody_called(self):
        for player in self.players:
            if((self.round, player) not in self.calls):
                return False
        return True

    def called_vs_actual(self, round, player):
        call_value = self.call_of(round, player)
        actual_value = self.actual_output(round, player)
        return "/".join([call_value, actual_value])

    def correct(self, round, player):
        return self.calls[round, player] == self.actuals[(round, player)]

    def actual_output(self, round, player):
        if(self.actuals_given(round, player)):
            return self.actual_of(round, player)
        if(self.is_player_to_record_actuals_from(player)):
            return "?"
        return ""
                            
    def call_of(self, round, player):
        return str(self.calls[round, player])

    def actual_of(self, round, player):
        return str(self.actuals[(round, player)])

    def actual_of2(self, round, player):
        return self.actuals[(round, player)]

    def actuals_given(self, round, player):
        return (round, player) in self.actuals

    def calling_player(self):
        return self.players[self.calling]