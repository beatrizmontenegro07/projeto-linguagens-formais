from funcoes import *
            
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
    
except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado")
except PermissionError:
    print("Erro: Não foi possível abrir o arquivo")
except Exception as e:
    print(f"Erro: {e}")


valido = EhValido(alfabeto, estados, transicoes)

print(valido)
