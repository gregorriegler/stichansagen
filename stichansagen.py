class Stichansagen:

    def __init__(self) -> None:
        self.players = []

    def add_player(self, name):
        self.players.append(name)

    def __str__(self):
        return " ".join(self.players)
