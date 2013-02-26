
class GameOverLogic:
    game = None
    def __init__(self, nick):
        self.nick = nick
        stage = GameOverLogic.game.mapa.stage
        players = GameOverLogic.game.players
        teamScores = None
        if players != None:
            if stage == "STAGE1_4":
                self.setStatus(self.getWinnersXMuertes())
                print self.getWinnersXMuertes()
            elif stage == "STAGE2_4":
                self.setStatus(self.getWinnersXScores())
            elif stage == "STAGE3_4":
                self.setStatus(self.getWinnersXMuertes())
            elif stage == "STAGE4_4":
                self.setStatus(self.getWinnersXScores())
            elif stage == "STAGE5_4":
                self.setStatus(self.getWinnersXScores())

            
    def setStatus(self, winnerTeams):
        self.winner = False
        self.empate = False
        for player in GameOverLogic.game.players:
            if player.nombre == self.nick and (player.team in winnerTeams):
                if len(winnerTeams) == 1:
                    self.winner = True
                else:
                    self.empate = True

    def getWinnersXMuertes(self):
        teams = []
        game = GameOverLogic.game
        teamScores = dict()
        for p in game.players:
            if teamScores.has_key(p.team):
                teamScores[p.team] += p.muertes
            else:
                teamScores[p.team] = p.muertes
        minim = min(list(teamScores.viewvalues()))
        for t in teamScores:
            if teamScores[t] == minim:
                teams.append(t)

        self.teamScores = teamScores
        return teams

    def getWinnersXScores(self):
        teams = []
        game = GameOverLogic.game
        teamScores = dict()
        for p in game.players:
            if teamScores.has_key(p.team):
                teamScores[p.team] += p.score
            else:
                teamScores[p.team] = p.score
        maxim = max(list(teamScores.viewvalues()))
        for t in teamScores:
            if teamScores[t] == maxim:
                teams.append(t)
        self.teamScores = teamScores
        return teams

    def Summary(self):
        teams = []
        game = GameOverLogic.game
        teamScores = dict()
        for p in game.players:
            if teamScores.has_key(p.team):
                tupla = teamScores[p.team]
                newTupla = (tupla[0]+p.muertes,tupla[1]+p.score)
                teamScores[p.team] = newTupla
            else:
                teamScores[p.team] = (p.muertes, p.score)

        return teamScores
