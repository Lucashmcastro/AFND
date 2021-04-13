import pydot
import os
os.environ["PATH"] += os.pathsep + "C:\Program Files\Graphviz\bin"
dir_path = os.path.dirname(os.path.realpath(__file__))

class Automato:

    def __init__(self):
        self.alphabet = []
        self.transitions = {}
        self.states = []
        self.stateFirst = None
        self.statesLast = []
        self.count = 0
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


