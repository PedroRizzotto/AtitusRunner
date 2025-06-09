import os, json
from datetime import datetime

def cls():
    os.system('cls')

def inicializar_banco_dados():
    try:
        banco = open('recursos/log.dat','r')
    except:
        banco = open("recursos/log.dat",'w')

def escrever_dados(nome,nanos,conhecimento,networking):
    banco = open("recursos/log.dat","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    data_br = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")
    dadosDict[nome] = (nanos, conhecimento, networking, data_br, hora)

    banco = open("recursos/log.dat","w")
    banco.write(json.dumps(dadosDict))
    banco.close()