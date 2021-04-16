import pydot
import os
os.environ["PATH"] +=os.pathsep + "C:\Program Files\Graphviz\bin"
dir_path = os.path.dirname(os.path.realpath(__file__))

class Automato:
    def __init__(self):
        self.alphabet = []
        self.transitions = {}
        self.states = []
        self.stateFirst = None
        self.statesLast = []
        self.count=0
        self.missingToRead = []
        self.alreadyRead = []
        self.completeWord = ''
    
    def check_repeated(self, dados):
        vector = []
        for i in dados:
            if(i not in vector):
                vector.append(i)
        return vector

    def set_alphabet(self, alphabet):
        self.alphabet = self.check_repeated(alphabet)

    def set_states(self, states):
        self.states = self.check_repeated(states)
        self.states.sort()

    def set_stateFirst(self, state):
        if state in self.states:
            self.stateFirst = state
        else:
            print(" Estado Inicial inválido. Verifique!! ")

    def set_statesLast(self, states):
        states = self.check_repeated(states)
        for i in states:
            if i in self.states:
                if i not in self.statesLast:
                    self.statesLast.append(i)
    
    def check_transitions(self, transitions):
        states_transitions = []

        for state in transitions:
            check_states = []; states_transitions.append(state)
            if(state not in check_states and state in self.states):
                check_states.append(state); check_alphabet = []
                for insertion in transitions[state]:
                    check_alphabet.append(insertion)
                    if(insertion in self.alphabet):
                        if(transitions[state][insertion] not in self.states):
                            return False
                    else:
                        return False  
                check_alphabet.sort()
                if(check_alphabet != self.alphabet):
                    return False           
            else:
                return False
        
        states_transitions.sort()
        if(states_transitions != self.states):
            return False
        return True

    def set_transitions(self, transitions):
        if(self.check_transitions(transitions) == True):
            self.transitions = transitions
        else:
            print(" Verifique os padrões de uma AFD. Funções de transições inválidas!! ")

    def execution_transitions(self, state_now,symbol):
        
        self.toCreateFork(state_now, symbol)
        state_now = self.transitions[state_now][symbol]
        return state_now

    def set_string(self, string):
        self.missingToRead.extend(string)
        self.completeWord=string

        for symbol in list(set(string)):
            if(symbol not in self.alphabet):
                print("'" +symbol+ "' não faz parte do alfabeto.")
                return

        state_now = self.stateFirst
        if(state_now != None):
            for symbol in string:
                state_now = self.execution_transitions(state_now, symbol)
        
            if(state_now in self.statesLast):
                 print("A string foi aceita.")
                 os.system("copy .\\img\\accepted.jpg .\\temp")
                 return True
            else:
                 print("A string foi negada.")
                 os.system("copy .\\img\\rejected.jpg .\\temp")
                 return False
        else:
            print(" Automato não possui estado inicial!!")

    def toCreateFork(self,stateNow,symbol):
        txt = "Palavra para testar: "+ self.completeWord+ "\n Lendo " + symbol
        self.missingToRead.remove(symbol)
        self.alreadyRead.append(symbol)
        txt+= " Falta: "+ ''.join(self.missingToRead)
        graph = pydot.Dot('my_graph', graph_type='digraph', bgcolor='white', label=str(txt))

        for n in self.states:
            if n in self.stateFirst:
                my_node = pydot.Node(n, label=n, shape="invtriangle")
            elif n in self.statesLast:
                my_node = pydot.Node(n, label=n, shape="doublecircle")
            else:
                my_node = pydot.Node(n, label=n, shape="circle")
            for insertion in self.transitions[n]:
                if n == stateNow and insertion == symbol:
                    if n in self.stateFirst:
                        my_node = pydot.Node(n, label=n, shape="invtriangle",color="green")
                    elif n in self.statesLast:
                        my_node = pydot.Node(n, label=n, shape="doublecircle", color="green")
                    else:
                        my_node = pydot.Node(n, label=n, shape="circle", color="green")
                    config = pydot.Edge(n, self.transitions[n][insertion],  color='red', label=" "+insertion, arrowhead='vee')
                    
                else:
                    config = pydot.Edge(n, self.transitions[n][insertion],  color='black', label=" "+insertion, arrowhead='vee')
                graph.add_edge(config)
            graph.add_node(my_node)
            
        graph.write_jpg(".\\temp\\"+str(''.join(self.alreadyRead))+".jpg")
        self.count+=1

    def toCreateGif(self):
        try:
            os.system("magick convert -delay 120 -loop 0 .\\temp\\*.jpg -resize 400x400 imagem.gif")
            os.startfile("imagem.gif")
            pathAtual = dir_path+"\\temp\\"
            dir = os.listdir(pathAtual)
            for file in dir:
                os.remove(pathAtual+"\\"+file)
        except:
            print("Inválido, ocorreu um erro na criação do Gif.")
