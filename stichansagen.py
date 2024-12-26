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

    def actual(self, name, stiche):
        self.actuals[(self.round, name)] = stiche

    def everybody_called(self):
        for player in self.players:
            if((self.round, player) not in self.calls):
                return False
        return True

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
            " ".join(self.call_output(round, player) for player in self.players)
            for round in self.rounds_played()
        ]

        return "\n".join(round_outputs) + "\n"


    def call_output(self, round, player):
        dran = (round, player)
        if(dran in self.calls):
            if(self.everybody_called()): 
                if(self.actuals_given(round, player)):
                    return str(self.calls[dran]) + "/" + self.actual_as_string(round, player)
                if(self.is_player_to_record_actuals_from(player)):
                    return str(self.calls[dran]) + "/" + "?"
        else:
            return "?"
        return str(self.calls[dran])

    def actual_as_string(self, round, player):
        return str(self.actuals[(round, player)])

    def actuals_given(self, round, player):
        return (round, player) in self.actuals

    def calling_player(self):
        return self.players[self.calling]