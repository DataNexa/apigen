"""
    Reader:
    - Lê as tabelas no banco de dados e gera as consultas adhoc
"""
from reader.gen_querys import gen_querys
from config.Config import Config
from util.mysqli   import *

# função: montar as consultas adhoc que serão utilizadas pelo repositorio

# Algoritimo:
# necessita do objeto config
# 1 - cria uma conexão com o banco de dados
# 2 - em cada serviço 
    # A - pega a tabela relacionada
    # B - pega os atributos de cada tabela 
        # B1 - em cada atributo verificar o tipo e fazer a tranformação e se pode ser nulo
        # B2 - salvar os dados gerados
    # se houver um tree 
        # pega cada tabela para fazer o relacionamento configurando 
        # --- o campo do relacionamento como obrigatorio
        # tendo o tree, significa que haverá joins nas consultas, inserção, update ou delete
        # salva o join para ser usado posteriormente
        # --- se o campo do relaciomento pode ser nulo, use o left join


def reader(config:Config):
    for serv in config.getServices():
        gen_querys(serv)
        