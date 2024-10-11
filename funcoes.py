import pandas as pd
from automata.fa.dfa import DFA
from automata.base.exceptions import InvalidStateError
import os

def leArquivo(arq):
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
    
    if(not automatoValido(alfabeto, estados, transicoes)):
        raise ValueError("A entrada não é um AFD")
                  

    return alfabeto, estados, inicial, finais, transicoes

def automatoValido(alfabeto, estados, transicoes):

    #a ideia é criar uma matriz de estados x alfabeto, que armazena quantas transições daquele simbolo do alfabeto tem naquele estado
    contagem_em_zero = [[0 for _ in range(len(alfabeto))] for _ in range(len(estados))]
    
    matriz = pd.DataFrame(contagem_em_zero, estados, alfabeto)

    for transicao in transicoes:
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

def geraDiagrama(estados, alfabeto, inicial, finais, transicoes, nome_do_arquivo):
    
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
        caminho = os.path.join('diagramas', f'diagrama_{nome_do_arquivo}_minimizado.png')
        dfa.show_diagram(path=caminho)
        print(f"Diagrama do AFD minimizado salvo na pasta 'diagramas' como 'diagrama_{nome_do_arquivo}_minimizado.png'")
    
    except InvalidStateError as e:
        print(f"Erro ao criar o AFD: {e}")

