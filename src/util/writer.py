import os
import shutil

def write(directory, filename, content):
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as file:
        file.write(content)

def delete_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def read(caminho_arquivo):

    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
        return conteudo
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_arquivo}")
        return None