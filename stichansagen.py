class Stichansagen:

    def __init__(self) -> None:
        self.round = 0
        self.players = []

    def add_player(self, name):
        self.players.append(name)

    def next(self):
        self.round = 1
    #def call(self, name, stiche):


    def __str__(self):
        header = ""
        if(self.players):
            header = " ".join(self.players)
            header += "\n===\n"
        gibt = ""
        if(self.players and self.round):
            gibt = "\n" + self.players[0] + " gibt " + "1" + "\n"
        return header + gibt
