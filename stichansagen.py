class Stichansagen:

    def __init__(self) -> None:
        self.round = 0
        self.players = []
        self.calls = {}
        self.calling = 0

    def add_player(self, name):
        self.players.append(name)

    def start(self):
        self.round = 1

    def call(self, name, stiche):
        if(self.round == 0): return
        self.calls[(self.round, name)] = stiche
        self.calling = (self.calling + 1) % len(self.players)

    def __str__(self):
        header = ""
        if(self.players):
            header = " ".join(self.players)
            header += "\n===\n"

        calls_output = ""
        if(self.calls):
            for _,stiche in self.calls.items():
                calls_output += str(stiche)
            calls_output += "\n"
        
        gibt = ""
        call = ""
        
        if(self.players and self.round):
            gibt = "\n" + self.players[0] + " gibt " + "1" + "\n"
            call = self.calling_player() + " sagt:" + "\n"

        return header + calls_output + gibt + call

    def calling_player(self):
        return self.players[self.calling]