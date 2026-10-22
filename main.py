from controlador import Controlador
from gerenciador_bd import GerenciadorBD
from interacao_usuario import InteracaoUsuario

URL = "localhost:3306/mydb"
USUARIO = "root"
SENHA = "root"

gerenciador = GerenciadorBD(URL, USUARIO, SENHA)
gerenciador.conectar()
try:
    InteracaoUsuario(Controlador(gerenciador)).menuInicial()
finally:
    gerenciador.desconectar()
