import pandas as pd
import numpy as np

def readFile(arq):
    alfabeto = []
    estados = []
    inicial = []
    finais = []
    transicoes = []
    transicao = False

    for linha in arq:
        linha = linha.strip()

        if (linha.startswith('alfabeto:')):
            indice = linha.find(':') + 1
            linha = linha[indice:]
            if linha: alfabeto = [a.strip() for a in linha.split(',')]
            if(len(alfabeto) == 0):
                raise ValueError('A entrada não possui informações sobre o alfabeto')

        elif (linha.startswith('estados:')):
            indice = linha.find(':') + 1
            linha = linha[indice:]
            if linha: estados = [e.strip() for e in linha.split(',')]
            if(len(estados) == 0):
                raise ValueError('A entrada não possui informações sobre os estados')
            
        elif (linha.startswith('inicial:')):
            indice = linha.find(':') + 1
            linha = linha[indice:]
            if linha: inicial = [i.strip() for i in linha.split(',')]
            if(len(inicial) == 0):
                raise ValueError('A entrada não possui informações sobre o estado inicial')
            elif(len(inicial) > 1):
                raise ValueError('A entrada possui mais de que um estado inicial')
            elif(inicial[0] not in estados):
                raise ValueError('O estado inicial não pertence aos estados de entrada')
            
        elif (linha.startswith('finais:')):
            indice = linha.find(':') + 1
            linha = linha[indice:]
            if linha: finais = [f.strip() for f in linha.split(',')]
            if any(f not in estados for f in finais):
                raise ValueError('A entrada possui estado(s) final não pertencentes aos estados de entrada')

        elif(linha.startswith('transicoes')):
            transicao = True    
        elif (transicao):
            t = [t.strip() for t in linha.split(',')]
            print(t)
            if (len(t) != 3):
                raise ValueError("A entrada contém transição que não está no padrão de AFD (<estado de partida>, <estado de chegada>, <simbolo>)")
            elif (t[0] not in estados or t[1] not in estados):
                raise ValueError("A entrada contém transição com estado(s) não pertencentes ao AFD")
            elif (t[2] not in alfabeto):
                raise ValueError("A entrada contém transição com símbolo não pertencente ao AFD")
            transicoes.append({'partida': t[0], 'chegada': t[1], 'simbolo': t[2]})
        else:
            raise ValueError('O arquivo de entrada não está nos padrões')
            
            

    return alfabeto, estados, inicial, finais, transicoes

def isValid(alfabeto, estados, transicoes):
    #a ideia é criar uma matriz de estados por alfabeto, que armazena quantas transições daquele simbolo do alfabeto tem nquele estado
    contagem_em_zero = [[0 for _ in range(len(alfabeto))] for _ in range(len(estados))]

    #print(contagem)
    
    matriz = pd.DataFrame(contagem_em_zero, estados, alfabeto)

    for transicao in transicoes:
        #print(transicao['partida'], transicao['simbolo'])
        matriz.loc[transicao['partida'], transicao['simbolo']] += 1

    #ao final dessa contagem, a matriz deve conter apenas 1s para ser considerada um AFD
    print(matriz)

    #verificação dos valores da matriz
    AFD_valido = True
    for e in estados:
        for a in alfabeto:
            if matriz.loc[e, a] != 1:
                AFD_valido = False
                break
    
    return AFD_valido


def minimizationOfDFA(matriz_transicao, alfabeto, estados, inicial, finais):

    #criando um dicionario que relaciona um estado a um indice, seguindo a ordem da lista "estados", a fim de consultá-lo para garantir o uso da matriz triangular de baixo
    dic_indices = {}
    index = 0
    for e in estados:
        dic_indices[e] = index
        index += 1
    

    #criando um dicionario em que cada chave é um estado, e cada eh elemento é uma lista que representa a linha de cada matriz triangular
    table = {}

    for linha in estados:
        lista = []
        for coluna in estados:
            if dic_indices[linha] > dic_indices[coluna]:
                lista.append(0)
        
        if lista:
            table[linha] = lista
    
    print("step 1")

    for linha in table.values():
        print(linha)
    
    #lista de nao finais
    nao_finais = []
    
    for e in estados:
        isFinal = False
        for f in finais:
            if f == e:
                isFinal = True
                break
        if isFinal == False:
            nao_finais.append(e)
    

    for f in finais:
        for nf in nao_finais:
            #como verificar se f e nf está na ordem da table, como garantir que stá fazendo na matriz triangular de baixo?
            #podemos usar um map que relaciona um estado a uma ordem
            if dic_indices[f] > dic_indices[nf]:
                table[f][dic_indices[nf]] = 1
            else:
                table[nf][dic_indices[f]] = 1
    
    print("step 2")
    for linha in table.values():
        print(linha)

    return

    