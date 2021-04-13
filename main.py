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



