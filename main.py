from funcoes import *
import numpy as np
import pandas as pd
import sys
import os
            
#Main

if len(sys.argv) < 2:
    print("Erro: nenhum arquivo foi passado como argumento.")
    exit(0)

try:
    arq = sys.argv[1]

    # arq = str(input("Digite a instancia do arquivo(.txt): ")) 
    arquivo = open(arq, 'r')
    alfabeto, estados, inicial, finais, transicoes = readFile(arquivo)
    """ print(alfabeto)
    print(estados)
    print(inicial)
    print(finais)
    print(transicoes) """

    #fazendo uma matriz de transição no formato Q X ALFABETO

    matriz_transicao = pd.DataFrame(np.nan, estados, alfabeto, dtype=object)

    for t in transicoes:
        matriz_transicao.loc[t['partida'], t['simbolo']] = t['chegada']

    """ print("Matrix de transição")
    print(matriz_transicao) """

    novo_estado, novo_inicial, novo_final, novo_transicoes = minimizationOfDFA(matriz_transicao, alfabeto, estados, inicial, finais, transicoes)
    
    # pegando só o nome do arquivo, e depois tirando a extensao '.txt' do nome
    nome_do_arquivo = os.path.basename(arq)
    nome_do_arquivo = os.path.splitext(nome_do_arquivo)[0]
    
    # gerando o diagrama 
    generate_dfa_diagram(novo_estado, alfabeto, novo_inicial, novo_final, novo_transicoes, nome_do_arquivo)
    
except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado")
except PermissionError:
    print("Erro: Não foi possível abrir o arquivo")
except Exception as e:
    print(f"Erro: {e}")
