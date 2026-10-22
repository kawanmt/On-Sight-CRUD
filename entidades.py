class Campeonato:
    def __init__(self, id, nome, localizacao, premiacaoTotal, fase):
        self.id = id
        self.nome = nome
        self.localizacao = localizacao
        self.premiacaoTotal = premiacaoTotal
        self.fase = fase

    def inscreverTime(self, idTime):
        return Participantes(self.id, idTime, 0, 0)

    def avancarFase(self, novaFase):
        self.fase = novaFase

    def premiacaoDistribuida(self, lista):
        return sum(p.premiacao for p in lista if p.idCampeonato == self.id)


class Participantes:
    def __init__(self, idCampeonato, idTime, classificacao, premiacao):
        self.idCampeonato = idCampeonato
        self.idTime = idTime
        self.classificacao = classificacao
        self.premiacao = premiacao

    def definirColocacao(self, pos, premio):
        self.classificacao = pos
        self.premiacao = premio


class Time:
    def __init__(self, id, nome, ranking, titulos):
        self.id = id
        self.nome = nome
        self.ranking = ranking
        self.titulos = titulos

    def adicionarTitulo(self):
        self.titulos += 1

    def atualizarRanking(self, posicao):
        self.ranking = posicao


class Jogador:
    def __init__(self, id, nome, idade, nick, ganhos, rating, premiacoes, idTime):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.nick = nick
        self.ganhos = ganhos
        self.rating = rating
        self.premiacoes = premiacoes
        self.idTime = idTime

    def transferir(self, idNovoTime):
        self.idTime = idNovoTime

    def atualizarRating(self, rating):
        self.rating = rating

    def adicionarPremiacao(self, valor):
        self.ganhos += valor
        self.premiacoes += 1


class Config:
    def __init__(self, idJogador, dpi, sensibilidade, resolucao, codMira):
        self.idJogador = idJogador
        self.dpi = dpi
        self.sensibilidade = sensibilidade
        self.resolucao = resolucao
        self.codMira = codMira

    def calcularEDPI(self):
        # eDPI = DPI x sensibilidade
        return self.dpi * self.sensibilidade

    def alterarSensibilidade(self, sens):
        self.sensibilidade = sens


class Serie:
    def __init__(self, id, idCampeonato, idTime1, idTime2, idVencedor, status, formato, fase):
        self.id = id
        self.idCampeonato = idCampeonato
        self.idTime1 = idTime1
        self.idTime2 = idTime2
        self.idVencedor = idVencedor
        self.status = status
        self.formato = formato
        self.fase = fase

    def vitoriasNecessarias(self):
        # MD1 -> 1, MD3 -> 2, MD5 -> 3
        return int(self.formato[2:]) // 2 + 1

    def registrarVencedor(self, idTime):
        self.idVencedor = idTime
        self.status = "finalizada"

    def adversarioDe(self, idTime):
        if idTime == self.idTime1:
            return self.idTime2
        return self.idTime1


class Partida:
    def __init__(self, id, idSerie, idVencedor, idPerdedor, mapa, placar, ordem):
        self.id = id
        self.idSerie = idSerie
        self.idVencedor = idVencedor
        self.idPerdedor = idPerdedor
        self.mapa = mapa
        self.placar = placar
        self.ordem = ordem

    def registrarResultado(self, venc, placar):
        self.idVencedor = venc
        self.placar = placar
