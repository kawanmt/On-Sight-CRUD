# On Sight AI · CRUD em Python

Código que segue o diagrama de classes (persistência na Opção 2).

## Como rodar

1. Crie o banco: execute `schema.sql` e depois `dados_exemplo.sql` no MySQL Workbench.
2. Instale a biblioteca: `py -m pip install -r requirements.txt`
3. Em `main.py`, troque `SENHA = "sua_senha"` pela sua senha do MySQL.
4. Rode: `py main.py`

## Arquivos

| Arquivo | Classes do diagrama |
|---|---|
| `entidades.py` | Campeonato, Participantes, Time, Jogador, Config, Serie, Partida |
| `parsers.py` | ParserCampeonato, ParserParticipantes, ParserTime, ParserJogador, ParserConfig, ParserSerie, ParserPartida |
| `gerenciador_bd.py` | GerenciadorBD |
| `controlador.py` | Controlador |
| `interacao_usuario.py` | InteracaoUsuario |
| `main.py` | ponto de entrada |
