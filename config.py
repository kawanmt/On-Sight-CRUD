"""Configuração da conexão com o MySQL.

Os valores podem ser trocados aqui ou por variáveis de ambiente
(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME), assim cada pessoa
do grupo usa a própria senha sem precisar editar o código.
"""

import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "mydb"),
}
