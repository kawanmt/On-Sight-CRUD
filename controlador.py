class Controlador:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

    def cadastrarCampeonato(self, campeonato):
        self.gerenciador.inserir(campeonato)

    def inscreverTime(self, idCampeonato, idTime):
        campeonato = self._buscar("campeonato", f"id={idCampeonato}", "Campeonato não encontrado.")
        self.gerenciador.inserir(campeonato.inscreverTime(idTime))

    def cadastrarTime(self, time):
        self.gerenciador.inserir(time)

    def cadastrarJogador(self, jogador):
        self.gerenciador.inserir(jogador)

    def cadastrarConfig(self, config):
        self.gerenciador.inserir(config)

    def registrarSerie(self, serie):
        self.gerenciador.inserir(serie)

    def registrarPartida(self, partida):
        self.gerenciador.inserir(partida)

    def consultarRanking(self):
        times = self.gerenciador.selecionar("time")
        return sorted(times, key=lambda t: (t.ranking is None, t.ranking))

    def registrarVencedor(self, idSerie, idTime):
        serie = self._buscar("serie", f"id={idSerie}", "Série não encontrada.")
        if idTime not in (serie.idTime1, serie.idTime2):
            raise ValueError("Esse time não joga a série.")
        serie.registrarVencedor(idTime)
        self.gerenciador.atualizar(serie)

    def definirColocacao(self, idCampeonato, idTime, pos, premio):
        inscricao = self._buscar("participantes", f"id_campeonato={idCampeonato};id_time={idTime}",
                                 "Esse time não está inscrito nesse campeonato.")
        inscricao.definirColocacao(pos, premio)
        self.gerenciador.atualizar(inscricao)

    def listar(self, tabela):
        return self.gerenciador.selecionar(tabela)

    def atualizar(self, obj):
        self.gerenciador.atualizar(obj)

    def remover(self, tabela, chave):
        self.gerenciador.remover(tabela, chave)

    # ---------- apoio ----------

    def _buscar(self, tabela, filtro, erro):
        encontrados = self.gerenciador.selecionar(tabela, filtro)
        if not encontrados:
            raise ValueError(erro)
        return encontrados[0]
