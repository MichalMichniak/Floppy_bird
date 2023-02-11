import random
from typing import List,Callable,Dict
import numpy as np

class Connection:
    def __init__(self, input_neuron, output_neuron, weight, innovation_nr, disabled_enabled = True):
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.weight = weight
        self.disabled_enabled = disabled_enabled
        self.innovation_number = innovation_nr
        self.is_feedforward = False
        self.state = 0
    def __repr__(self):
        return f"{self.innovation_number}: ({self.input_neuron},{self.output_neuron}) w{self.weight},{'F' if self.is_feedforward else 'R'}"


class Net:
    """
    with recurent connections
    """
    def __init__(self,nr_inputs : List[int], nr_outputs : List[int], nr_neurons : List[int] , connections : List[Connection], activation_func : Callable[[float],float] = None):
        self.neurons = nr_neurons
        self.nr_inputs = nr_inputs
        self.nr_outputs = nr_outputs
        self.connections = connections
        dict_of_output_conn : Dict[int,List[Connection]] = {i:[] for i in self.nr_inputs+self.neurons+self.nr_outputs}
        dict_of_input_conn : Dict[int,List[Connection]] = {i:[] for i in self.nr_inputs+self.neurons+self.nr_outputs}
        for i in range(len(self.connections)):
            dict_of_output_conn[self.connections[i].input_neuron].append(self.connections[i])
            dict_of_input_conn
        if activation_func == None:
            activation_func = lambda x: 1/(1+np.exp(-x))
        self.activation_func = activation_func
        ## detection of feedforward and recurent connections
        visited = {i : False for i in self.nr_inputs+self.neurons+self.nr_outputs}
        recurent = {i : False for i in self.nr_inputs+self.neurons+self.nr_outputs}
        lst = []
        for i in self.nr_inputs:

            for j in range(len(dict_of_output_conn[i])):
                dict_of_output_conn[i][j].is_feedforward = True
        

    def count(self):
        pass

if __name__ == '__main__':

    conn = [Connection(0,4,1,0),Connection(0,5,1,0),Connection(5,4,1,0),Connection(2,5,1,0)]
    net = Net([0,1,2,3],[4],[5],conn)
    i = 0
    pass




class Control:
    def __init__(self,n_inputs, n_outputs) -> None:
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs

        pass

    def predict(self, input):
        if input[2] < 0:
            return 1
        else:
            return 0

    def predict(self, input):
        return 0