import os, json
from datetime import datetime

def cls():
    os.system('cls')

def inicializar_banco_dados():
    try:
        banco = open('recursos/log.dat','r')
    except:
        banco = open("recursos/log.dat",'w')

def escrever_dados(nome,nanos,pontuacao,conhecimento,networking):
    banco = open("recursos/log.dat","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    data_br = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")

    chave_jogada = f"{nome} {data_br} {hora}"

    dadosDict[chave_jogada] = {
        "nome":nome,
        "nanos":nanos,
        "pontuacao":pontuacao,
        "conhecimento": conhecimento,
        "networking": networking,
        "data": data_br,
        "hora": hora
    }

    banco = open("recursos/log.dat","w")
    banco.write(json.dumps(dadosDict))
    banco.close()


def obter_ultimos_registros(limite=5):
    """Obtém os últimos registros do arquivo de dados"""
    try:
        banco = open("recursos/log.dat", "r")
        dados = banco.read()
        banco.close()
        
        if dados != "":
            dadosDict = json.loads(dados)
            registros = []
            
            for chave, valores in dadosDict.items():
                registros.append((chave, valores))
                print(f"Registro adicionado: {chave} -> {valores}")
            
            print(f"Total de registros antes da ordenação: {len(registros)}")
            
            # Ordenar por data/hora (mais recentes primeiro)
            # Convertendo data brasileira para formato ordenável
            def extrair_datetime(registro):
                try:
                    chave, valores = registro
                    
                    # Verificar se valores é tupla/lista ou dicionário
                    if isinstance(valores, (list, tuple)):
                        data_br = valores[4] if len(valores) > 4 else "01/01/2000"
                        hora = valores[5] if len(valores) > 5 else "00:00:00"
                    elif isinstance(valores, dict):
                        data_br = valores.get('data', "01/01/2000")
                        hora = valores.get('hora', "00:00:00")
                    else:
                        return "0000-00-00 00:00:00"
                    
                    # Converter data brasileira para formato americano para ordenação
                    dia, mes, ano = data_br.split('/')
                    data_ordenavel = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
                    datetime_completo = f"{data_ordenavel} {hora}"
                    
                    return datetime_completo
                except Exception as e:
                    print(f"Erro ao extrair datetime: {e}")
                    return "0000-00-00 00:00:00"  # fallback
            
            registros.sort(key=extrair_datetime, reverse=True)
            print(f"Registros após ordenação: {[r[0] for r in registros]}")
            
            return registros[:limite]
        return []
    except Exception as e:
        print(f"Erro ao obter registros: {e}")
        return []