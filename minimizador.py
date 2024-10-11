import os
import pandas as pd
import numpy as np

def minimizaAFD(matriz_transicao, alfabeto, estados, inicial, finais, transicoes):

    #criando um dicionario que relaciona um estado a um indice, seguindo a ordem da lista "estados"
    dic_indices = {}
    index = 0
    for e in estados:
        dic_indices[e] = index
        index += 1
    
    #criando um dicionario em que cada chave é um estado, e cada eh elemento é uma lista que representa a linha de cada matriz triangular
    print("O passo 1 do algoritmo consiste em criar a relação em pares dos estados do AFD\n")
    table = primeiroPasso(estados, dic_indices)

    print("Após a execução do passo 1:\n\n")
    mostra_tabela(table, estados)

    print("O segundo passo consiste em marcar os pares (Qa, Qb), tal que Qa é um estado final e Qb não é um estado final\n")
    table = segundoPasso(estados, dic_indices, table, finais)

    print("Após a execução do passo 2: \n\n")
    mostra_tabela(table, estados)

    print("O terceiro passo consiste em verificar cada par (Qa, Qb) que não esteja marcado. Caso o par formado pelos estados de chegada da transições (Qa, x) e (Qb, x), em que x é um símbolo do alfabeto, estiver marcado, então (Qa, Qb) será marcado\n")
    table = terceiroPasso(table, matriz_transicao, dic_indices, alfabeto)

    print("Após a execução do passo 3: \n\n")
    mostra_tabela(table, estados)

    print("O quarto passo passo consiste em combinar os pares que não estão marcados em um único estado\n")

    matriz_relacao, estados_concatenados = quartoPasso(transicoes, estados, table, dic_indices)
    
    print("\nMATRIZ RELAÇÃO FINAL\n")
    print(matriz_relacao)

    # a partir dos resultados da matriz relacao, cria variaveis que representam os estados e transicoes do novo AFD
    novo_estado, novo_inicial, novo_final = estados_minimizados(estados_concatenados, inicial, finais)
    novo_estado_indices = cria_dicionario_novos_estados(dic_indices, estados_concatenados, novo_estado)
    novo_transicoes = transicoes_minimizadas(novo_estado_indices, matriz_relacao)
    
    """ print(novo_estado_indices)
    print(novo_estado)
    print(novo_inicial)
    print(novo_final)
    print(novo_transicoes) """

    return novo_estado, novo_inicial, novo_final, novo_transicoes

def primeiroPasso(estados, dic_indices):
    table = {}

    for linha in estados:
        lista = []
        for coluna in estados:
            if dic_indices[linha] > dic_indices[coluna]:
                lista.append(0)
        
        if lista:
            table[linha] = lista
    
    return table

def segundoPasso(estados, dic_indices, table, finais):
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
    
    return table

def terceiroPasso(table, matriz_transicao, dic_indices, alfabeto):
    #realiza o processo ate não ter como fazer mais marcações
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
    
    return table

def quartoPasso(transicoes, estados, table, dic_indices):
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


    #essa lista tem os estados concatenados, começa com uma lista de listas representando os estados
    estados_concatenados = []
    for e in estados:
        estados_concatenados.append([e])

    print(estados_concatenados)

    for p in pares:

        if p[0] == p[1] : continue

        print(f'\nCOMBINANDO O PAR = {p}\n')
        
        e1 = p[0]
        e2 = p[1]

        if(dic_indices[p[1]] < dic_indices[p[0]]):
            e1 = p[1]
            e2 = p[0]

        for e in estados_concatenados:

            if not e: continue #se a lista do estado for vazia, continue
            else:
                e = e[0] # pega o primeiro elemento da lista, que é o estado "original" da lista
                
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


        estados_concatenados[dic_indices[e1]].append(e2) # a lista que representa o estado e1 agora tem e2        
        estados_concatenados[dic_indices[e2]].clear() # a lista que representa e2 agora está vazia

        print("\nEstados após a combinação dos estados: ")
        print(estados_concatenados)
    
    return matriz_relacao, estados_concatenados

def cria_matriz_relacao(transicoes, estados):
    matriz_relacao = pd.DataFrame(np.nan, estados, estados, dtype=object)

    for t in transicoes:

        if isinstance(matriz_relacao.loc[t['partida'], t['chegada']], set):
            matriz_relacao.loc[t['partida'], t['chegada']].add(t['simbolo'])
        else:
            matriz_relacao.loc[t['partida'], t['chegada']] = {t['simbolo']}

    return matriz_relacao

   
def estados_minimizados(estados_concatenados, inicial, finais):
    estados_minimizados = []
    inicial_minimizado = []
    finais_minimizados = []

    for estados in estados_concatenados:
        s = ""
        if not estados:
            continue
        
        ini = False
        fin = False
        for e in estados:
            if e == inicial[0]: 
                ini = True
            for f in finais:
                if(f == e):
                    fin = True
            s += e
        
        estados_minimizados.append(s)
        if ini:
            inicial_minimizado.append(s)
        if fin:
            finais_minimizados.append(s)
    
    return estados_minimizados, inicial_minimizado, finais_minimizados


def transicoes_minimizadas(novo_estado_indices, matriz_relacao):

    novo_transicoes = []

    for key1, value1 in novo_estado_indices.items():
        for key2, value2 in novo_estado_indices.items():
            if isinstance(matriz_relacao.loc[value1,value2], set):
                for sim in matriz_relacao.loc[value1,value2]:
                    nova_transicao = {'partida': key1, 'chegada': key2, 'simbolo': sim}
                    novo_transicoes.append(nova_transicao)
    
    return novo_transicoes


def cria_dicionario_novos_estados(dic_indices, estados_concatenados, novo_estado):
    # relaciona os estados novos e seu nome com os estados velhos, que sao os indices da matriz relacao
    novo_estado_indices = {}
    
    cont = 0

    for chave, valor in dic_indices.items():
        if not estados_concatenados[valor]:
            continue
        else:
            novo_estado_indices[novo_estado[cont]] = chave
            cont = cont+1
    
    return novo_estado_indices

def mostra_tabela(tabela, estados):
    coluna = [f"  {e}  " for e in estados[:-1]]
    titulo = " " * 6 + "|" + "|".join(coluna) + "|"
    print(titulo)
    

    for estado, values in tabela.items():
        componentes = [f"  {estado}  "]
        for v in values:
            if (v == 0): componentes.append("     ")
            else: componentes.append("  X  ")
        linha = "|" + "|".join(componentes) + "|"
        print("-" * len(linha))
        print(linha)
    print("-" * len(linha) + "\n\n")

