# Parsers: um para cada entidade, como no diagrama (Opção 2).
#
# serializar(obj)          -> registro em String: "coluna=valor;coluna=valor;..."
# desserializar(registro)  -> objeto da entidade, a partir dessa String
#
# Um valor vazio (ex.: "ranking=") significa NULL no banco.

from entidades import Campeonato, Config, Jogador, Participantes, Partida, Serie, Time


# ---------- funções de apoio usadas por todos os parsers ----------

def montarRegistro(campos):
    # {"id": 1, "nome": "FURIA"} -> "id=1;nome=FURIA"
    for coluna, valor in campos.items():
        if valor is not None and (";" in str(valor) or "=" in str(valor)):
            raise ValueError(f"O campo {coluna} não pode conter ';' nem '='.")
    return ";".join(f"{coluna}={'' if valor is None else valor}" for coluna, valor in campos.items())


def lerRegistro(registro):
    # "id=1;nome=FURIA" -> {"id": "1", "nome": "FURIA"}
    campos = {}
    for parte in registro.split(";"):
        coluna, valor = parte.split("=", 1)
        campos[coluna] = valor
    return campos


def inteiro(valor):
    return None if valor == "" else int(valor)


def decimal(valor):
    return None if valor == "" else float(valor)


def texto(valor):
    return None if valor == "" else valor


# ---------- um parser por entidade ----------

class ParserCampeonato:
    def serializar(self, obj):
        return montarRegistro({"id": obj.id, "nome": obj.nome, "localizacao": obj.localizacao,
                               "premiacao_total": obj.premiacaoTotal, "fase": obj.fase})

    def desserializar(self, registro):
        c = lerRegistro(registro)
        return Campeonato(inteiro(c["id"]), c["nome"], c["localizacao"],
                          inteiro(c["premiacao_total"]), c["fase"])


class ParserParticipantes:
    def serializar(self, obj):
        return montarRegistro({"id_campeonato": obj.idCampeonato, "id_time": obj.idTime,
                               "classificacao": obj.classificacao, "premiacao": obj.premiacao})

    def desserializar(self, registro):
        c = lerRegistro(registro)
        return Participantes(inteiro(c["id_campeonato"]), inteiro(c["id_time"]),
                             inteiro(c["classificacao"]), inteiro(c["premiacao"]))


class ParserTime:
    def serializar(self, obj):
        return montarRegistro({"id": obj.id, "nome": obj.nome, "ranking": obj.ranking,
                               "titulos": obj.titulos})

    def desserializar(self, registro):
        c = lerRegistro(registro)
        return Time(inteiro(c["id"]), c["nome"], inteiro(c["ranking"]), inteiro(c["titulos"]))


class ParserJogador:
    def serializar(self, obj):
        return montarRegistro({"id": obj.id, "nome": obj.nome, "idade": obj.idade, "nick": obj.nick,
                               "ganhos": obj.ganhos, "rating": obj.rating,
                               "premiacoes": obj.premiacoes, "time_id": obj.idTime})

    def desserializar(self, registro):
        c = lerRegistro(registro)
        return Jogador(inteiro(c["id"]), c["nome"], inteiro(c["idade"]), c["nick"],
                       inteiro(c["ganhos"]), decimal(c["rating"]), inteiro(c["premiacoes"]),
                       inteiro(c["time_id"]))


class ParserConfig:
    def serializar(self, obj):
        return montarRegistro({"id_jogador": obj.idJogador, "dpi": obj.dpi,
                               "sensibilidade": obj.sensibilidade, "resolucao": obj.resolucao,
                               "cod_mira": obj.codMira})

    def desserializar(self, registro):
        c = lerRegistro(registro)
        return Config(inteiro(c["id_jogador"]), inteiro(c["dpi"]), decimal(c["sensibilidade"]),
                      texto(c["resolucao"]), texto(c["cod_mira"]))


class ParserSerie:
    def serializar(self, obj):
        return montarRegistro({"id": obj.id, "id_campeonato": obj.idCampeonato,
                               "id_time1": obj.idTime1, "id_time2": obj.idTime2,
                               "id_vencedor": obj.idVencedor, "status": obj.status,
                               "formato": obj.formato, "fase": obj.fase})

    def desserializar(self, registro):
        c = lerRegistro(registro)
        return Serie(inteiro(c["id"]), inteiro(c["id_campeonato"]), inteiro(c["id_time1"]),
                     inteiro(c["id_time2"]), inteiro(c["id_vencedor"]), c["status"],
                     texto(c["formato"]), texto(c["fase"]))


class ParserPartida:
    def serializar(self, obj):
        return montarRegistro({"id": obj.id, "id_serie": obj.idSerie,
                               "id_vencedor": obj.idVencedor, "id_perdedor": obj.idPerdedor,
                               "mapa": obj.mapa, "placar": obj.placar, "ordem": obj.ordem})

    def desserializar(self, registro):
        c = lerRegistro(registro)
        return Partida(inteiro(c["id"]), inteiro(c["id_serie"]), inteiro(c["id_vencedor"]),
                       inteiro(c["id_perdedor"]), texto(c["mapa"]), texto(c["placar"]),
                       inteiro(c["ordem"]))
