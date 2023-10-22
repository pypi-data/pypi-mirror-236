import os
import json
from datetime import datetime
import pickle
# from IPython.display import clear_output
from threading import Thread



def TipoArquivo():
    try:
        a = (__file__[-2:])
        return 'py'
    except:
        a = os.getcwd()[-2:]
        return 'jupter'

def LimparTela(self):
    if self.TipoArquivo() != 'py':
        pass
    else:
        os.system('cls')

def DeletarArquivo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)

def CriarPasta(caminho_da_pasta):
    os.makedirs(caminho_da_pasta)

    
def Pasta_do_Arquivo(caminho_arquivo):
    return  os.path.dirname(caminho_arquivo)  

def Juntar(a, b):
    return os.path.join(a, b)


def Escrever_json(nomedodicionario, nomedoarquivo):
    if nomedoarquivo[-4:] != 'json':
        nomedoarquivo = nomedoarquivo+'.json'
    with open(nomedoarquivo, 'w') as f2:
        json.dump(nomedodicionario, f2, indent=4)


def Ler_json(nomedoarquivo):  # retorna um dicionário
    if nomedoarquivo[-4:] != 'json':
        nomedoarquivo = nomedoarquivo+'.json'
    with open(nomedoarquivo, 'r') as f2:
        try:
            a = json.load(f2)
            return a
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return {}


def Data():
    current_time = datetime.now()
    formatted_time = current_time.strftime('%d-%m-%Y-%H:%M:%S')
    return formatted_time


def SalvarPickle(var, nome):
    if nome[-3:] != 'plk':
        nome = nome+'.plk'
        with open(nome+'.plk', 'wb') as arquivo:
            pickle.dump(var, arquivo)


def LerPickle(nome):
    if nome[-3:] != 'plk':
        nome = nome+'.plk'
    with open(nome+'.plk', 'rb') as arquivo:
        return pickle.load(arquivo)

def IniciarThread(funcao, argu = ''):
    if argu == '':
        Thread(target=funcao, daemon=True).start()
    else:
        Thread(target=funcao, arqgs = argu, daemon=True).start()
        
