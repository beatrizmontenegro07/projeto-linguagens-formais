# Minimizador de Autômato Finito Determinístico

Esse projeto foi desenvolvido para a disciplina de Linguagens Formais e Computabilidade e tem como objetivo minimizar um AFD.

O método utilizado para encontrar o AFD mínimo foi o algoritmo de Myhill Nerode

## Entrada

O arquivo [main.py](main.py) recebe como argumento o nome de um arquivo `.txt` com as informações do AFD, seguindo o formato a seguir: 

```bash
alfabeto:a,b,c,d  # Lista de símbolos do alfabeto aceito pelo autômato
estados:q0,q1,q2  # Lista de estados no autômato
inicial:q0 # Indica qual é o estado inicial
finais:q1,q2 # Especifica os estados finais do autômato.
transicoes
q0,q1,a # Representa uma transição de q0 para q1 com o símbolo "a"
q1,q2,b # Representa uma transição de q1 para q2 com o símbolo "b"
... 
`````

## Saída

O programa mostra no terminal o passo a passo executado pelo algoritmo, assim como o diagrama do AFD final.




