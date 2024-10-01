from funcoes import *
import numpy as np
import pandas as pd
            
#Main

try:
    arq = str(input("Digite a instancia do arquivo(.txt): ")) 
    arquivo = open(arq, 'r')
    alfabeto, estados, inicial, finais, transicoes = readFile(arquivo)
    print(alfabeto)
    print(estados)
    print(inicial)
    print(finais)
    print(transicoes)

    #fazendo uma matriz de transição no formato Q X ALFABETO

    matriz_transicao = pd.DataFrame(np.nan, estados, alfabeto, dtype=object)

    for t in transicoes:
        matriz_transicao.loc[t['partida'], t['simbolo']] = t['chegada']

    print("Matrix de transição")
    print(matriz_transicao)

    minimizationOfDFA(matriz_transicao, alfabeto, estados, inicial, finais, transicoes)
    
except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado")
except PermissionError:
    print("Erro: Não foi possível abrir o arquivo")
except Exception as e:
    print(f"Erro: {e}")
