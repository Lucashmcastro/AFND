from afnd import Automato

def read_File(automato):

    f = open("./file.txt", "r")
    text = []
    lines = f.read().splitlines()

    for x in lines:
        text.apped(x.split(" "))
    print(text)

    firstLine = text[0]
    lastLine = text[len(text) - 1]
    text.remove(lastLine)
    text.remove(firstLine)

    print("Primeira Linha: ", firstLine)
    print("Última Linha: ", lastLine)
    print("Texto: ", text)

    stateFirst = []
    stateLast = []
    transitions = []
    alphabet = []
    word = []
    states = []

    separator = firstLine.index(";")

    for x in firstLine:
        if(firstLine.index(x) < separator):
            stateFirst=x
        if(firstLine.index(x) > separator):
            stateLast.append(x)

    word = lastLine[len(lastLine) - 1]

    print("Estado Inicial: ", stateFirst)
    print("Estado Final: ", stateLast)
    print("Palavra: ", word)

    for x in text:
        list = []
        entrys = {}

        if x[1] == "/":
            x[1] = "lambda"

        if x[0] in transitions:
            entrys = transitions[x[0]]
            print(entrys)
            if x[1] in transitions[x[0]]:
                list = transitions[x[0]][x[1]]
                list.append(x[3])

                entrys[x[1]] = list
                transitions[x[0]] = dict[entrys]

        else:
            list.append(x[3])
            if x[1] == 'lambda':
                entrys['lamba'] = [x[3]]
                transitions[x[0]] = dict(entrys)

            else:
                entrys[x[1]] = list
                entrys['lambda'] = []
                transitions[x[0]] = dict(entrys)

        if x[0] not in states:
            states.append(x[0])
        if x[1] not in alphabet and x[1] != "lambda":
            alphabet.append(x[1])

    print("\n\n Estados: ", states)
    print(" Transições: ", transitions)
    print(" Alfabeto: ", alphabet)








