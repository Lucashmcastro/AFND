from afnd import Automato


def readFile(automato):
    f = open("./file.txt", "r")
    text = []
    lines = f.read().splitlines()

    for x in lines:
        text.append(x.split(" "))
    print(text)

    firstLine = text[0]
    lastLine = text[len(text)-1]
    text.remove(lastLine)
    text.remove(firstLine)

    print("Primeira Linha: ", firstLine)
    print("Última Linha: ", lastLine)
    print("Texto: ", text)

    stateLast = [] 
    transitions = {}
    alphabet = []
    word = []
    states = []

    separator = firstLine.index(";")

    for x in firstLine:
        if(firstLine.index(x)<separator):
            stateFirst=x
        if(firstLine.index(x)>separator):
            stateLast.append(x)

    word = lastLine[len(lastLine) - 1]
    print("Estado Inicial: ", stateFirst)
    print("Estado Final: ", stateLast)
    print("Palavra: ", word)

    for x in text:
        list = []        
        dicEntrys = {}

        if x[1] == '/':
            x[1] = "lambda"
        if x[0] in transitions:
            dicEntry = transitions[x[0]] 
            print(dicEntry)
            if x[1] in transitions[x[0]]:
                list = transitions[x[0]][x[1]]                
            list.append(x[3])
            
            dicEntry[x[1]] = list
            transitions[x[0]] = dict(dicEntry)
        else:            
            list.append(x[3])
            if x[1] == 'lambda':
                dicEntrys['lambda'] = [x[3]]                 
                transitions[x[0]] = dict(dicEntrys)
            else:
                dicEntrys[x[1]] = list
                dicEntrys['lambda'] = [] 
                transitions[x[0]] = dict(dicEntrys)

        if x[0] not in states:
            states.append(x[0])
        if x[1] not in alphabet and x[1]!="lambda":
            alphabet.append(x[1])

    print("\n\n Estados: ", states)
    print(" Transições: ", transitions)
    print(" Alfabeto: ", alphabet)

    automato.set_alphabet(alphabet)
    automato.set_states(states)
    automato.set_stateFirst(stateFirst)
    automato.set_statesLast(stateLast)
    automato.set_transitions(transitions)
    automato.set_string(word)
    automato.toCreateGif()

def main():
    fnd = Automato()
    readFile(fnd)

if __name__ == '__main__':
    main()