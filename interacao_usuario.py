import mysql.connector

from entidades import Campeonato, Config, Jogador, Partida, Serie, Time


# ---------- leitura do teclado ----------

def lerTexto(msg, opcional=False):
    while True:
        valor = input(msg).strip()
        if valor or opcional:
            return valor or None
        print("  Campo obrigatório.")


def lerInt(msg, opcional=False):
    while True:
        valor = input(msg).strip()
        if valor == "" and opcional:
            return None
        try:
            return int(valor)
        except ValueError:
            print("  Digite um número inteiro.")


def lerFloat(msg, opcional=False):
    while True:
        valor = input(msg).strip().replace(",", ".")
        if valor == "" and opcional:
            return None
        try:
            return float(valor)
        except ValueError:
            print("  Digite um número (ex.: 1.5).")


def mostrar(objetos):
    if not objetos:
        print("  (nenhum registro)")
    for obj in objetos:
        print("  " + " | ".join(f"{k}: {v}" for k, v in vars(obj).items()))


# ---------- formulários: pedem todos os campos e devolvem o objeto ----------

def lerCampeonato():
    return Campeonato(lerInt("ID: "), lerTexto("Nome: "), lerTexto("Localização: "),
                      lerInt("Premiação total: "), lerTexto("Fase: "))


def lerTime():
    return Time(lerInt("ID: "), lerTexto("Nome: "), lerInt("Ranking (opcional): ", True),
                lerInt("Títulos: "))


def lerJogador():
    return Jogador(lerInt("ID: "), lerTexto("Nome: "), lerInt("Idade: "), lerTexto("Nick: "),
                   lerInt("Ganhos: "), lerFloat("Rating: "), lerInt("Premiações: "),
                   lerInt("ID do time (opcional): ", True))


def lerConfig():
    return Config(lerInt("ID do jogador: "), lerInt("DPI (opcional): ", True),
                  lerFloat("Sensibilidade (opcional): ", True),
                  lerTexto("Resolução (opcional): ", True),
                  lerTexto("Código de mira (opcional): ", True))


def lerSerie():
    return Serie(lerInt("ID: "), lerInt("ID do campeonato (opcional): ", True),
                 lerInt("ID do time 1: "), lerInt("ID do time 2: "),
                 lerInt("ID do vencedor (opcional): ", True), lerTexto("Status: "),
                 lerTexto("Formato MD1/MD3/MD5 (opcional): ", True),
                 lerTexto("Fase (opcional): ", True))


def lerPartida():
    return Partida(lerInt("ID: "), lerInt("ID da série: "),
                   lerInt("ID do vencedor (opcional): ", True),
                   lerInt("ID do perdedor (opcional): ", True),
                   lerTexto("Mapa (opcional): ", True), lerTexto("Placar ex. 13-9 (opcional): ", True),
                   lerInt("Ordem na série (opcional): ", True))


# ---------- menus do diagrama ----------

class InteracaoUsuario:
    def __init__(self, controlador):
        self.controlador = controlador

    def menuInicial(self):
        while True:
            print("\n=== On Sight AI ===")
            print("1. Campeonatos")
            print("2. Times e jogadores")
            print("3. Séries e partidas")
            print("0. Sair")
            opcao = input("Opção: ").strip()
            if opcao == "1":
                self.menuCampeonatos()
            elif opcao == "2":
                self.menuTimes()
            elif opcao == "3":
                self.menuPartidas()
            elif opcao == "0":
                break

    def menuCampeonatos(self):
        c = self.controlador
        opcoes = {
            "1": ("Cadastrar campeonato", lambda: c.cadastrarCampeonato(lerCampeonato())),
            "2": ("Listar campeonatos", lambda: mostrar(c.listar("campeonato"))),
            "3": ("Atualizar campeonato (digite os dados de novo)",
                  lambda: c.atualizar(lerCampeonato())),
            "4": ("Remover campeonato", lambda: c.remover("campeonato", f"id={lerInt('ID: ')}")),
            "5": ("Inscrever time", lambda: c.inscreverTime(lerInt("ID do campeonato: "),
                                                            lerInt("ID do time: "))),
            "6": ("Listar inscrições", lambda: mostrar(c.listar("participantes"))),
            "7": ("Definir colocação de um time", lambda: c.definirColocacao(
                lerInt("ID do campeonato: "), lerInt("ID do time: "),
                lerInt("Colocação: "), lerInt("Prêmio: "))),
            "8": ("Remover inscrição", lambda: c.remover(
                "participantes",
                f"id_campeonato={lerInt('ID do campeonato: ')};id_time={lerInt('ID do time: ')}")),
        }
        self._executarMenu("Campeonatos", opcoes)

    def menuTimes(self):
        c = self.controlador
        opcoes = {
            "1": ("Cadastrar time", lambda: c.cadastrarTime(lerTime())),
            "2": ("Listar times", lambda: mostrar(c.listar("time"))),
            "3": ("Atualizar time (digite os dados de novo)", lambda: c.atualizar(lerTime())),
            "4": ("Remover time", lambda: c.remover("time", f"id={lerInt('ID: ')}")),
            "5": ("Consultar ranking", lambda: mostrar(c.consultarRanking())),
            "6": ("Cadastrar jogador", lambda: c.cadastrarJogador(lerJogador())),
            "7": ("Listar jogadores", lambda: mostrar(c.listar("jogador"))),
            "8": ("Atualizar jogador (digite os dados de novo)",
                  lambda: c.atualizar(lerJogador())),
            "9": ("Remover jogador", lambda: c.remover("jogador", f"id={lerInt('ID: ')}")),
            "10": ("Cadastrar config de jogador", lambda: c.cadastrarConfig(lerConfig())),
            "11": ("Listar configs", lambda: mostrar(c.listar("config"))),
            "12": ("Atualizar config (digite os dados de novo)",
                   lambda: c.atualizar(lerConfig())),
            "13": ("Remover config", lambda: c.remover("config",
                                                       f"id_jogador={lerInt('ID do jogador: ')}")),
        }
        self._executarMenu("Times e jogadores", opcoes)

    def menuPartidas(self):
        c = self.controlador
        opcoes = {
            "1": ("Registrar série", lambda: c.registrarSerie(lerSerie())),
            "2": ("Listar séries", lambda: mostrar(c.listar("serie"))),
            "3": ("Atualizar série (digite os dados de novo)", lambda: c.atualizar(lerSerie())),
            "4": ("Remover série", lambda: c.remover("serie", f"id={lerInt('ID: ')}")),
            "5": ("Registrar vencedor de uma série", lambda: c.registrarVencedor(
                lerInt("ID da série: "), lerInt("ID do time vencedor: "))),
            "6": ("Registrar partida", lambda: c.registrarPartida(lerPartida())),
            "7": ("Listar partidas", lambda: mostrar(c.listar("partida"))),
            "8": ("Atualizar partida (digite os dados de novo)",
                  lambda: c.atualizar(lerPartida())),
            "9": ("Remover partida", lambda: c.remover("partida", f"id={lerInt('ID: ')}")),
        }
        self._executarMenu("Séries e partidas", opcoes)

    # ---------- apoio ----------

    def _executarMenu(self, titulo, opcoes):
        while True:
            print(f"\n--- {titulo} ---")
            for codigo, (texto, _) in opcoes.items():
                print(f"{codigo}. {texto}")
            print("0. Voltar")
            opcao = input("Opção: ").strip()
            if opcao == "0":
                return
            if opcao not in opcoes:
                print("Opção inválida.")
                continue
            try:
                opcoes[opcao][1]()
                print("OK.")
            except mysql.connector.Error as erro:
                print(f"Erro do banco: {erro.msg}")
            except ValueError as erro:
                print(f"Erro: {erro}")
