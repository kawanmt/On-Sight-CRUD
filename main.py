# Ponto de entrada: monta as classes e abre o menu.
#
#   py main.py      (Windows)
#   python3 main.py (Linux/macOS)

from controlador import Controlador
from gerenciador_bd import GerenciadorBD
from interacao_usuario import InteracaoUsuario

# Troque pela sua senha do MySQL.
URL = "localhost:3306/mydb"
USUARIO = "root"
SENHA = "root"

gerenciador = GerenciadorBD(URL, USUARIO, SENHA)
gerenciador.conectar()
try:
    InteracaoUsuario(Controlador(gerenciador)).menuInicial()
finally:
    gerenciador.desconectar()
