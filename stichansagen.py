from tabulate import tabulate

class Stichansagen:

    def __init__(self, rounds = [1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1,"K"]) -> None:
        self.round = None
        self.roundIndex = None
        self.rounds = rounds
        self.players = []
        self.calls = {}
        self.actuals = {}
        self.calling = 0

    def add_player(self, name):
        self.players.append(name)

    def start(self):
        if(self.roundIndex == None):
            self.roundIndex = 0
        elif (len(self.rounds) > self.roundIndex + 1):
            self.roundIndex += 1
        self.round = self.rounds[self.roundIndex]
        print("start round " + str(self.round))
        
    def call(self, player, stiche):
        if(self.round == 0): return
        print("call " + player)
        self.calls[PlayerRound(player, self.round)] = stiche
        self.calling = (self.calling + 1) % len(self.players)

    def record_actual(self, player, stiche):
        self.actuals[PlayerRound(player, self.round)] = stiche
        self.calling = (self.calling + 1) % len(self.players)
        print("record actuals" + player)
        if(self.all_actuals_given()):
            self.start()

    def input(self, number):
        calling_player = self.calling_player()
        player_round = PlayerRound(calling_player, self.round)
        if(not self.has_called(player_round)):
            self.call(player_round.player, number)
        else:
            self.record_actual(player_round.player, number)
            
        
        
    def is_player_to_record_actuals_from(self, player):
        return self.player_to_record_actuals() == player

    def player_to_record_actuals(self):
        for player in self.players:
            if(PlayerRound(player, self.round) not in self.actuals):
                return player        

    def rounds_played(self):
        if(self.round == None):
            return [self.rounds[0]]
        return self.rounds[:self.round]
    
    def __str__(self):
        return self.table() + "\n" + self.info()

    def table(self):
        return tabulate(self.body(), self.headers())
    
    def headers(self):
        return ["", *self.players]
    
    def body(self):
        if self.round is None:
            return []
        
        body = []
        for round in self.rounds_played():
            row = []
            row.append(str(round))
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
    
    def info(self):
        gibt = ""
        if(self.players and self.round and not self.everybody_called(self.round)):
            gibt = self.players[0] + " gibt " + "1"
        return gibt

    def cell_output(self, player_round):
        if(not self.has_called(player_round)):
            if(player_round.player is self.calling_player()): 
                return "?"
            else:
                return ""
        if(self.everybody_called(player_round.round)):
            if(self.actuals_given(player_round)):
                return str(self.points(player_round)) + "(" + self.called_vs_actual(player_round) + ")" 
            else:
                return self.called_vs_actual(player_round)      
        return str(self.call_of(player_round))

    def everybody_called(self, round):
        for player in self.players:
            if(not self.has_called(PlayerRound(player, round))):
                return False
        return True
    
    def has_called(self, player_round):
        return player_round in self.calls
    
    def all_actuals_given(self):
        for player in self.players:
            if(not self.actuals_given(PlayerRound(player, self.round))):
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
        if(not self.has_called(player_round)):
            return 0
        return 5 + self.call_of(player_round)

    def called_vs_actual(self, player_round):
        call_value = str(self.call_of(player_round))
        actual_value = self.actual_output(player_round)
        return "/".join([call_value, actual_value])

    def correct(self, player_round):
        return self.has_called(player_round) and self.actuals_given(player_round) and self.calls[player_round] == self.actuals[player_round]

    def wrong(self, player_round):
        return self.has_called(player_round) and self.actuals_given(player_round) and self.calls[player_round] != self.actuals[player_round]

    def actual_output(self, player_round):
        if(self.actuals_given(player_round)):
            return str(self.actual_of(player_round))
        if(self.is_player_to_record_actuals_from(player_round.player)):
            return "?"
        return ""

    def call_of(self, player_round):
        if(not self.has_called(player_round)):
            return None
        return self.calls[(player_round)]

    def actual_of(self, player_round):
        return self.actuals[(player_round)]

    def actuals_given(self, player_round):
        return player_round in self.actuals

    def calling_player(self):
        return self.players[self.calling]


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

