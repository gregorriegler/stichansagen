class Stichansagen:

    rounds = [1,2]

    def __init__(self) -> None:
        self.round = 0
        self.players = []
        self.calls = {}
        self.actuals = {}
        self.calling = 0

    def add_player(self, name):
        self.players.append(name)

    def start(self):
        self.round = 1

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

    def player_to_record_actuals(self):
        for player in self.players:
            if((self.round, player) not in self.actuals):
                return player        

    def __str__(self):
        header = ""
        if(self.players):
            header = " ".join(self.players)
            header += "\n===\n"

        everybody_called = self.everybody_called()

        calls_output = ""
        if(self.calls):
            for round in self.rounds:
                for player in self.players:
                    if((round, player) in self.calls):
                        call_of_player = str(self.calls[(round, player)]) 
                        if(everybody_called): 
                            if((round, player) in self.actuals):
                                call_of_player += "/" + str(self.actuals[(round, player)])
                            if(self.player_to_record_actuals() == player):
                                call_of_player += "/?"
                            call_of_player += " "
                        calls_output += call_of_player              
                calls_output = calls_output.rstrip()       
            calls_output += "\n"
        
        gibt = ""
        call = ""
        
        if(self.players and self.round and not self.everybody_called()):
            gibt = "\n" + self.players[0] + " gibt " + "1" + "\n"
            call = self.calling_player() + " sagt:" + "\n"

        return header + calls_output + gibt + call

    def calling_player(self):
        return self.players[self.calling]