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
            if (len(t) != 3):
                raise ValueError("A entrada contém transição que não está no padrão de AFD (<estado de partida>, <estado de chegada>, <simbolo>)")
            elif (t[0] not in estados or t[1] not in estados):
                raise ValueError("A entrada contém transição com estado(s) não pertencentes ao AFD")
            elif (t[2] not in alfabeto):
                raise ValueError("A entrada contém transição com símbolo não pertencente ao AFD")
            transicoes.append({'partida': t[0], 'chegada': t[1], 'simbolo': t[2]})
        else:
            raise ValueError('O arquivo de entrada não está nos padrões')
    
    if(not isValid(alfabeto, estados, transicoes)):
        raise ValueError("A entrada não é um AFD")
                  

    return alfabeto, estados, inicial, finais, transicoes

def isValid(alfabeto, estados, transicoes):
    #a ideia é criar uma matriz de estados por alfabeto, que armazena quantas transições daquele simbolo do alfabeto tem nquele estado
    contagem_em_zero = [[0 for _ in range(len(alfabeto))] for _ in range(len(estados))]

    #print(contagem_em_zero)
    
    matriz = pd.DataFrame(contagem_em_zero, estados, alfabeto)

    for transicao in transicoes:
        #print(transicao['partida'], transicao['simbolo'])
        matriz.loc[transicao['partida'], transicao['simbolo']] += 1

    #ao final dessa contagem, a matriz deve conter apenas 1s para ser considerada um AFD
    #print(matriz)

    #verificação dos valores da matriz
    AFD_valido = True
    for e in estados:
        for a in alfabeto:
            if matriz.loc[e, a] != 1:
                AFD_valido = False
                break
    
    return AFD_valido


def minimizationOfDFA(matriz_transicao, alfabeto, estados, inicial, finais, transicoes):

    #criando um dicionario que relaciona um estado a um indice, seguindo a ordem da lista "estados", a fim de consultá-lo para garantir o uso da matriz triangular de baixo
    dic_indices = {}
    index = 0
    for e in estados:
        dic_indices[e] = index
        index += 1

    print(dic_indices)
    

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
    print(table)
    for linha in table.values():
        print(linha)

    print("step 3")


    #realiza o processo ate nao tiver como fazer mais marcações
    process = True
    while(process):
        process = False
        for key, values in table.items():
            for indice, v in enumerate(values):
                if v == 0:
                    for a in alfabeto:
                        e1 = matriz_transicao.loc[key, a]
                        e2 = matriz_transicao.iloc[indice][a]
                        if (dic_indices[e1] == dic_indices[e2]):
                            continue
                        elif (dic_indices[e1] > dic_indices[e2]):
                            if (table[e1][dic_indices[e2]]):
                                table[key][indice] = 1
                                process = True
                                break
                        else:
                            if (table[e2][dic_indices[e1]]):
                                table[key][indice] = 1
                                process = True
                                break

    for linha in table.values():
        print(linha)   


    print("step 4")

    matriz_relacao = cria_matriz_relacao(transicoes, estados)
    print(matriz_relacao)


    pares = []

    for key, values in table.items():
            for indice, v in enumerate(values):
                if v == 0:
                    for estado, i in dic_indices.items():
                        if indice == i:
                            tupla = (estado, key)
                            pares.append(tupla)


    estados_copia = estados

    for p in pares:
        print(f'PAR = {p}')

        if p[0] == p[1] : continue
        
        e1 = p[0]
        e2 = p[1]

        if(dic_indices[p[1]] < dic_indices[p[0]]):
            e1 = p[1]
            e2 = p[0]

        for e in estados_copia:
            i = matriz_relacao.loc[e2][e]
            k = matriz_relacao.loc[e][e2]

            if isinstance(i, set):

                if not isinstance(matriz_relacao.loc[e1,e], set):
                    matriz_relacao.loc[e1,e] = i
                else:  
                    matriz_relacao.loc[e1,e] = matriz_relacao.loc[e1,e] | i

            if isinstance(k, set):

                if not isinstance(matriz_relacao.loc[e,e1], set):
                    matriz_relacao.loc[e,e1] = k
                else:
                    matriz_relacao.loc[e,e1] = matriz_relacao.loc[e,e1] | k



        matriz_relacao = matriz_relacao.drop([e2], axis=0)
        matriz_relacao = matriz_relacao.drop([e2], axis=1)

        print(matriz_relacao)


        for index in range(len(pares)):
            par = pares[index]

            novo_par = (e1 if par[0] == e2 else par[0], e1 if par[1] == e2 else par[1])

            pares[index] = novo_par

        estados_copia.remove(e2)

    print("MATRIZ FINAL")
    print(matriz_relacao)
        

    return

def cria_matriz_relacao(transicoes, estados):
    matriz_relacao = pd.DataFrame(np.nan, estados, estados, dtype=object)

    for t in transicoes:

        if isinstance(matriz_relacao.loc[t['partida'], t['chegada']], set):
            matriz_relacao.loc[t['partida'], t['chegada']].add(t['simbolo'])
        else:
            matriz_relacao.loc[t['partida'], t['chegada']] = {t['simbolo']}
    
    print(matriz_relacao)

    return matriz_relacao


    
