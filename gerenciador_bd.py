# GerenciadorBD: toda a persistência fica aqui. Recebe e devolve objetos,
# usa o parser de cada classe para virar registro (String) e monta o SQL.
# É a única classe que conhece os parsers e o SQL.

import mysql.connector
from mysql.connector.constants import ClientFlag

from entidades import Campeonato, Config, Jogador, Participantes, Partida, Serie, Time
from parsers import (ParserCampeonato, ParserConfig, ParserJogador, ParserParticipantes,
                     ParserPartida, ParserSerie, ParserTime, lerRegistro, montarRegistro)

# Colunas da chave primária de cada tabela (as que não estão aqui usam "id").
CHAVES = {
    "config": ["id_jogador"],
    "participantes": ["id_campeonato", "id_time"],
}


class GerenciadorBD:
    def __init__(self, url, usuario, senha):
        self.url = url            # formato "host:porta/banco", ex.: "localhost:3306/mydb"
        self.usuario = usuario
        self.senha = senha
        self.conexao = None
        # Para cada classe: a tabela dela e o parser que a converte em registro.
        self.parsers = {
            Campeonato: ("campeonato", ParserCampeonato()),
            Participantes: ("participantes", ParserParticipantes()),
            Time: ("time", ParserTime()),
            Jogador: ("jogador", ParserJogador()),
            Config: ("config", ParserConfig()),
            Serie: ("serie", ParserSerie()),
            Partida: ("partida", ParserPartida()),
        }

    def conectar(self):
        endereco, banco = self.url.split("/")
        host, porta = endereco.split(":")
        self.conexao = mysql.connector.connect(host=host, port=int(porta), database=banco,
                                               user=self.usuario, password=self.senha,
                                               # rowcount passa a contar as linhas encontradas,
                                               # mesmo quando o UPDATE não muda nenhum valor
                                               client_flags=[ClientFlag.FOUND_ROWS])

    def desconectar(self):
        if self.conexao is not None:
            self.conexao.close()

    def inserir(self, obj):
        tabela, parser = self.parsers[type(obj)]
        campos = self._valores(parser.serializar(obj))
        colunas = ", ".join(campos.keys())
        marcadores = ", ".join(["%s"] * len(campos))
        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({marcadores})"
        self._executar(sql, list(campos.values()))

    def atualizar(self, obj):
        tabela, parser = self.parsers[type(obj)]
        campos = self._valores(parser.serializar(obj))
        chave = CHAVES.get(tabela, ["id"])
        alterar = [c for c in campos if c not in chave]
        sql = (f"UPDATE {tabela} SET " + ", ".join(f"{c} = %s" for c in alterar)
               + " WHERE " + " AND ".join(f"{c} = %s" for c in chave))
        if self._executar(sql, [campos[c] for c in alterar] + [campos[c] for c in chave]) == 0:
            raise ValueError("Registro não encontrado para atualizar.")

    def remover(self, tabela, chave):
        # chave no formato do registro: "id=3" ou "id_campeonato=1;id_time=2"
        campos = self._valores(chave)
        sql = f"DELETE FROM {tabela} WHERE " + " AND ".join(f"{c} = %s" for c in campos)
        if self._executar(sql, list(campos.values())) == 0:
            raise ValueError("Registro não encontrado para remover.")

    def selecionar(self, tabela, filtro=""):
        # filtro vazio = todas as linhas; senão, no formato "coluna=valor"
        parser = next(p for t, p in self.parsers.values() if t == tabela)
        sql = f"SELECT * FROM {tabela}"
        valores = []
        if filtro:
            campos = self._valores(filtro)
            sql += " WHERE " + " AND ".join(f"{c} = %s" for c in campos)
            valores = list(campos.values())
        cursor = self.conexao.cursor()
        cursor.execute(sql, valores)
        colunas = [d[0] for d in cursor.description]
        linhas = cursor.fetchall()
        cursor.close()
        # Cada linha vira registro (String) e o parser monta o objeto.
        return [parser.desserializar(montarRegistro(dict(zip(colunas, linha)))) for linha in linhas]

    # ---------- apoio ----------

    def _valores(self, registro):
        # Converte a String em {coluna: valor}; texto vazio vira NULL.
        return {c: (None if v == "" else v) for c, v in lerRegistro(registro).items()}

    def _executar(self, sql, valores):
        # Roda um comando que altera dados: confirma (commit) ou desfaz tudo (rollback).
        cursor = self.conexao.cursor()
        try:
            cursor.execute(sql, valores)
            self.conexao.commit()
            return cursor.rowcount
        except mysql.connector.Error:
            self.conexao.rollback()
            raise
        finally:
            cursor.close()
