import pydot
import os
os.environ["PATH"] +=os.pathsep + "C:\Program Files\Graphviz\bin"
dir_path = os.path.dirname(os.path.realpath(__file__))

class state:
    def __init__(self):
        self.name = None
        self.nextState = None
        self.previousState = None

    def get_nextState(self):
        return self.nextState
    
    def set_nextState(self, next):
        self.nextState = next

    def get_previousState(self):
        return self.previousState
    
    def set_previousState(self, previous):
        self.previousState = previous

class Automato:
    def __init__(self):
        self.alphabet = []
        self.transitions = {}
        self.states = []
        self.stateFirst = None
        self.statesLast = []
        self.first_state = None
        self.last_state = None
        self.amount_states = 0
        
        self.count=0
        self.missingToRead = []
        self.alreadyRead = []
        self.completeWord = ''
    
    def check_repeated(self, data):
        vector = []
        for i in data:
            if(i not in vector):
                vector.append(i)
        return vector

    def set_alphabet(self, alphabet):
        self.alphabet = self.check_repeated(alphabet)

    def set_states(self, states):
        self.states = self.check_repeated(states)
        self.states.sort()
        self.alphabet.append("lambda")
    
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
                        for i in transitions[state][insertion]:
                            if(i not in self.states):
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

    def transition_loop(self,symbol):
        state = self.first_state
        aux_first = None
        aux_end = None
        #if state != None:
        while state.get_nextState() != None:
            self.toCreateFork(state,symbol,"red")
            aux1, aux2 = self.execution_transitions(symbol, state)            
            if((aux_first and aux_first) == None):
                aux_first = aux1
                aux_end = aux2
            else:
                aux_end.set_nextState(aux1)
                if aux1 != None:
                    aux1.set_previousState(aux_end)
                    aux_end = aux2
            state = state.get_nextState()
            if(state == None):
                break
            
        else:
            
            self.toCreateFork(state,symbol,"red")
            aux1, aux2 = self.execution_transitions(symbol, state)
            if((aux1 and aux2) != None):
                if((aux_first and aux_end) == None):
                    aux_first = aux1
                    aux_end = aux2
                else:
                    aux_end.set_nextState(aux1)
                    aux1.set_previousState(aux_end)
                    aux_end = aux2
        
        if((aux_first and aux_end) != None):
            state.set_nextState(aux_first)
            aux_first.set_previousState(state)
            self.last_state = aux_end

    def lambda_def(self, state, start_row, end_row):
        if((start_row and end_row) == None):
            start_row = state
            end_row = state
        else:
            end_row.set_nextState(state)
            state.set_previousState(end_row)
            state.set_previousState(end_row)
            end_row = state
        return start_row,end_row


    def lambda_transition(self,state_now):
        start_row = None
        end_row = None
        controle = False
        for i in range(len(self.transitions[state_now]["lambda"])):
            newState = state()
            newState.name = self.transitions[state_now]["lambda"][i]
            if(i == len(self.transitions[state_now]["lambda"])):
                controle = True
            while(self.transitions[newState.name]["lambda"] != []):
                state_guard = newState.name
                for j in range(len(self.transitions[newState.name]["lambda"])):
                    if(j>0):
                        newstate = state()
                        newstate.name = self.transitions[state_guard]["lambda"][j]
                        start_row, end_row = self.lambda_def(newstate,start_row,end_row)
                    else:
                        newState.name = self.transitions[newState.name]["lambda"][j]
                        #print(newState.name)
                        start_row, end_row = self.lambda_def(newState,start_row,end_row)
                    self.amount_states += 1
            else:
                if(controle == False):
                    start_row, end_row = self.lambda_def(newState,start_row,end_row)
                    self.amount_states += 1
        return start_row,end_row
 
    def execution_transitions(self, symbol,state_now):    
        aux_first = None
        aux_end = None
        states = state_now.name
        
        for i in range(len(self.transitions[states][symbol])):
            if(i == 0):
                state_now.name = self.transitions[states][symbol][i]
                lambda_first, lambda_end = self.lambda_transition(state_now.name) 
                if((aux_first and aux_end) == None):
                    aux_first = lambda_first
                    aux_end = lambda_end
                else:  
                    print(lambda_first.name, lambda_end.name)
                    aux_end.set_nextState(lambda_first)
                    lambda_first.set_previousState(aux_end)
                    aux_end =lambda_end
            else:
                newState = state()
                newState.name = self.transitions[states][symbol][i]
                lambda_first, lambda_end = self.lambda_transition(newState.name)
                if((aux_first and aux_end) == None):
                    aux_first = newState
                    aux_end = newState
                else:
                    aux_end.set_nextState(newState)
                    newState.set_previousState(aux_end)
                    aux_end = newState
                if((lambda_first and lambda_end) != None):
                    aux_end.set_nextState(lambda_first)
                    lambda_first.set_previousState(aux_end)
                    aux_end =lambda_end

                self.amount_states += 1
        if(len(self.transitions[states][symbol]) == 0):
            self.insertion_without(state_now)
        return aux_first, aux_end

    def insertion_without(self, state):
        if(state == self.first_state):
            self.first_state = self.first_state.get_nextState()
        elif(state == self.last_state):
            self.last_state = self.last_state.get_previousState()
            self.last_state.set_nextState(None)
        else:
            state1 = state.get_previousState()
            state2 = state.get_nextState()
            state1.set_nextState(state2)
            state2.set_previousState(state1)
        self.amount_states += -1

    def set_string(self, string):
        self.missingToRead.extend(string)
        self.completeWord=string

        for symbol in list(set(string)):
            if(symbol not in self.alphabet):
                print("'" +symbol+ "' não faz parte do alfabeto. ")
                return

        if(self.amount_states == 0):
            if(self.stateFirst == None):
                print(" Automato não possui estado inicial!! ")
                return

            newState = state()
            newState.name = self.stateFirst
            self.first_state = newState
            self.last_state = newState
            self.amount_states += 1

        for symbol in string:
            self.transition_loop(symbol)   
        state_now = self.first_state

        if(state_now != None):
            while(state_now.get_nextState() != None):
                if(self.check_automato(state_now.name) == True):
                    self.end()
                    return True
                state_now = state_now.get_nextState()
            else:
                if(self.check_automato(state_now.name) == True):
                    self.end()
                    return True
                else:
                    print("A string foi negada.")
                    os.system("copy .\\img\\rejected.jpg .\\temp")
                    self.end()
                    return False
        else:
            print("A string foi negada.")
            os.system("copy .\\img\\rejected.jpg .\\temp")
            self.end()
            return False

    def check_automato(self, state):
        if(state in self.statesLast):
            print("A string foi aceita")
            os.system("copy .\\img\\accepted.jpg .\\temp")
            return True

    def end(self):
        self.first_state = None
        self.last_state = None
        self.amount_states = 0

    def toCreateFork(self,stateCurrent,symbol,color):
        if(symbol=="lambda"):
            symbol = u'\u03BB'
        txt = "Palavra para testar: "+ self.completeWord + "\n Lendo: " + symbol

        self.alreadyRead.append(symbol)
        graph = pydot.Dot('my_graph', graph_type='digraph', bgcolor='white', label=str(txt))

        for n in self.states:
            if n in self.stateFirst:
                my_node = pydot.Node(n, label=n, shape="invtriangle")
              
            elif n in self.statesLast:
                my_node = pydot.Node(n, label=n, shape="doublecircle")
            
            else:
                my_node = pydot.Node(n, label=n, shape="circle")
             
            for insertion in self.transitions[n]:
                if insertion =="episilon":
                    insertion = u'\u03BB'

                if n == stateCurrent.name and insertion == symbol:
                    if n in self.stateFirst:
                        my_node = pydot.Node(n, label=n, shape="invtriangle",color=color)
                     
                    elif n in self.statesLast:
                        my_node = pydot.Node(n, label=n, shape="doublecircle", color=color)
                    
                    else:
                        my_node = pydot.Node(n, label=n, shape="circle", color=color)
                       
                    for x in self.transitions[n][insertion]:
                        config = pydot.Edge(n, x,  color=color, label=" "+insertion, arrowhead='vee')
                        graph.add_edge(config)
                 
                else:
                
                    for x in self.transitions[n][insertion]:
                        
                        config = pydot.Edge(n, x,  color='black', label=" "+insertion, arrowhead='vee')
                        graph.add_edge(config)
                
            graph.add_node(my_node)
            tempfile = "./temp/"+str(color)+str(''.join(self.alreadyRead))+".jpg"

        graph.write_jpg(".\\temp\\"+str(''.join(self.alreadyRead))+".jpg")
        self.count+=1

    def toCreateGif(self):
        try:
            print(dir_path)
            os.system("magick convert -delay 120 -loop 0 .\\temp\\*.jpg -resize 500x500 img.gif")
            os.startfile("img.gif")
        
            pathAtual = dir_path+"\\temp\\"
            dir = os.listdir(pathAtual)
            for file in dir:
                os.remove(pathAtual+"\\"+file)   
        except:
                print("Inválido, ocorreu um erro na criação do Gif.")