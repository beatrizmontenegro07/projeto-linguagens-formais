import pandas as pd
import numpy as np
from automata.fa.dfa import DFA
from automata.base.exceptions import InvalidStateError

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


    #essa lista tem os estados concatenados, começa com uma lista de listas representando os estados
    estados_concatenados = []
    for e in estados:
        estados_concatenados.append([e])

    print(estados_concatenados)

    for p in pares:
        print(f'PAR = {p}')

        if p[0] == p[1] : continue
        
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

        print(estados_concatenados)

    print("MATRIZ FINAL")
    print(matriz_relacao)

    novo_estado, novo_inicial, novo_final = estados_minimizados(estados_concatenados, inicial, finais)

    print(novo_estado)
    print(novo_inicial)
    print(novo_final)

    #criar funcao que faz uma nova variavel 'transicoes', similar a primeira, mas agora com base na matriz relacao

    #retornar novo_estado, _novo_inicial, novo_final, novo_transicoes para a chamada da funcao no main.py, para ser usado como parametro da funcao de criar o diagrama

    #return

    novo_transicoes = []

    for t in transicoes:
        partida = t['partida']
        chegada = t['chegada']
        simbolo = t['simbolo']

        for estados_concatenados in estados_concatenados:
            if partida in estados_concatenados:
                partida_min = ''.join(estados_concatenados)
            if chegada in estados_concatenados:
                chegada_min = ''.join(estados_concatenados)

        #adicionando transição no novo afd minimizado
        nova_transicao = {'partida': partida_min, 'chegada': chegada_min, 'simbolo': simbolo}
        if nova_transicao not in novo_transicoes:
            novo_transicoes.append(nova_transicao)

    #garantindo que todos os estados minimizados têm transições definidas para todos os símbolos do alfabeto
    #adicionando um estado armadilha caso nenhuma transição esteja definida

    trap_state = 'TRAP'
    for estado in novo_estado:
        for simbolo in alfabeto:
            found_transition = False
            for t in novo_transicoes:
                if t['partida'] == estado and t['simbolo'] == simbolo:
                    found_transition = True
                    break
            if not found_transition:
                nova_transicao = {'partida': estado, 'chegada': trap_state, 'simbolo': simbolo}
                novo_transicoes.append(nova_transicao)

    for simbolo in alfabeto:
        nova_transicao = {'partida': trap_state, 'chegada': trap_state, 'simbolo': simbolo}
        if nova_transicao not in novo_transicoes:
            novo_transicoes.append(nova_transicao)

    print("Novas transições:")
    print(novo_transicoes)

    return novo_estado, novo_inicial, novo_final, novo_transicoes


def cria_matriz_relacao(transicoes, estados):
    matriz_relacao = pd.DataFrame(np.nan, estados, estados, dtype=object)

    for t in transicoes:

        if isinstance(matriz_relacao.loc[t['partida'], t['chegada']], set):
            matriz_relacao.loc[t['partida'], t['chegada']].add(t['simbolo'])
        else:
            matriz_relacao.loc[t['partida'], t['chegada']] = {t['simbolo']}
    
    print(matriz_relacao)

    return matriz_relacao

def generate_dfa_diagram(estados, alfabeto, inicial, finais, transicoes):
    #adicionando estado armadilha
    if 'TRAP' not in estados:
        estados.append('TRAP')
    
    # define as transições no formato da biblioteca automata-lib
    transicoes_dfa = {}
    for estado in estados:
        transicoes_dfa[estado] = {}

    for t in transicoes:
        partida, chegada, simbolo = t['partida'], t['chegada'], t['simbolo']
        if partida not in transicoes_dfa:
            transicoes_dfa[partida] = {}
        transicoes_dfa[partida][simbolo] = chegada

    try:
        #cria o AFD com a biblioteca automata-lib
        dfa = DFA(
            states=set(estados),
            input_symbols=set(alfabeto),
            transitions=transicoes_dfa,
            initial_state=inicial[0],
            final_states=set(finais)
        )

        #desenha o diagrama do AFD 
        dfa.show_diagram(path='afd_minimizado.png')
        print("Diagrama do AFD minimizado salvo como 'afd_minimizado.png'")
    
    except InvalidStateError as e:
        print(f"Erro ao criar o AFD: {e}")
    
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