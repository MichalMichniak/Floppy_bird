from control import Net
from control import Connection
from typing import List
import random
from copy import deepcopy
from floppy_with_control import Flopy_control

from control import Control
X_FLOPY = 50
class NEAT:
    def __init__(self):
        """
        convention nr of neurons starts with inputs then outputs next are additional neurons
        """
        self.dictionary_of_connections = {"0,4":0,"1,4":1,"2,4":2,"3,4":3}
        self.next_innovation_nr = 4
        self.mutation_connection_probability = 0.2
        self.mutation_neuron_probability = 0.005
        self.mutation_weight_probability = 1 - self.mutation_connection_probability - self.mutation_neuron_probability
        self.input_neurons_nr = [0,1,2,3]
        self.output_neurons_nr = [4]
        self.additional_neurons = []


    def evolve_population(self, lst_insta : List[Flopy_control], score_avg = False):
        if score_avg:
            for i in range(len(lst_insta)):
                if lst_insta[i].survived_rounds == 0:
                    lst_insta[i].avg_score = lst_insta[i].score
                    lst_insta[i].survived_rounds += 1
                else:
                    lst_insta[i].avg_score = (lst_insta[i].avg_score*lst_insta[i].survived_rounds + lst_insta[i].score)/(lst_insta[i].survived_rounds + 1)
                    lst_insta[i].survived_rounds += 1
            lst_insta.sort(key= lambda x: x.avg_score, reverse=True)
        else:
            lst_insta.sort(key= lambda x: x.score, reverse=True)
        pop_count = len(lst_insta)
        lst_insta = lst_insta[:len(lst_insta)//2 + 1]
        ## mutation
        for i in range(pop_count-len(lst_insta)):
            r1 = random.randint(0,len(lst_insta)-1)
            r2 = random.randint(0,len(lst_insta)-1)
            new_network = self.mutate(self.cross(lst_insta[r1].control_.net,lst_insta[r2].control_.net))
            lst_insta.append(Flopy_control(X_FLOPY,250+random.randint(-120,120),Control(len(self.input_neurons_nr),len(self.output_neurons_nr),new_network)))
        return lst_insta
    
    def mutate(self, insta : Net)-> Net:
        p = random.uniform(0,1)
        list_of_conn = deepcopy(insta.connections)
        list_of_neurons = deepcopy(insta.neurons)
        if p < self.mutation_neuron_probability:
            # neuron addition
            r = random.randint(0,len(insta.list_of_non_disabled_conn)-1)
            if self.additional_neurons == []:
                neuron_nr = self.output_neurons_nr[-1]+1
            else:
                neuron_nr = self.additional_neurons[-1] +1
            self.additional_neurons.append(neuron_nr)
            list_of_conn[r].disabled_enabled = False
            ## neuron with highest number always last
            list_of_neurons.append(neuron_nr)
            ## connection with highest innovation number always last
            conn1 = f"{list_of_conn[r].input_neuron},{neuron_nr}"
            list_of_conn.append(Connection(list_of_conn[r].input_neuron,neuron_nr,list_of_conn[r].weight))
            conn2 = f"{neuron_nr},{list_of_conn[r].output_neuron}"
            list_of_conn.append(Connection(neuron_nr,list_of_conn[r].output_neuron,list_of_conn[r].weight))
            self.dictionary_of_connections[conn1] = self.next_innovation_nr
            self.next_innovation_nr+=1
            self.dictionary_of_connections[conn2] = self.next_innovation_nr
            self.next_innovation_nr+=1

        elif p < self.mutation_connection_probability + self.mutation_neuron_probability:
            # connection addition 
            n1 = random.randint(0,len(list_of_neurons)+len(self.input_neurons_nr)-1)
            n2 = random.randint(len(self.input_neurons_nr),len(list_of_neurons)+len(self.input_neurons_nr)+len(self.output_neurons_nr)-1)
            n1 = (self.input_neurons_nr + list_of_neurons + self.output_neurons_nr)[n1]
            n2 = (self.input_neurons_nr + list_of_neurons + self.output_neurons_nr)[n2]
            if f"{n1},{n2}" in self.dictionary_of_connections.keys():
                ## it can be done by bisection O(log n) but through linear search O(n)
                for i in list_of_conn:
                    if str(i) == f"{n1},{n2}":
                        p+=1
                        break
                else:
                    for i in range(len(list_of_conn)):
                        if self.dictionary_of_connections[str(list_of_conn[i])] > self.dictionary_of_connections[f"{n1},{n2}"]:
                            list_of_conn.insert(i,Connection(n1,n2,0.0001))
                            break
                    else:
                        list_of_conn.append(Connection(n1,n2,0.0001))
            else:
                self.dictionary_of_connections[f"{n1},{n2}"] = self.next_innovation_nr
                self.next_innovation_nr+=1
                list_of_conn.append(Connection(n1,n2,0.0001))

        if p>=self.mutation_connection_probability + self.mutation_neuron_probability:
            if len(insta.list_of_non_disabled_conn)-1 == -1:
                pass
            elif len(insta.list_of_non_disabled_conn)-1 == 0:
                list_of_conn[0].weight += random.uniform(-1,1)
            else:
                r = random.randint(0,len(insta.list_of_non_disabled_conn)-1)
                list_of_conn[r].weight += random.uniform(-1,1)
            pass
        return Net(deepcopy(self.input_neurons_nr),deepcopy(self.output_neurons_nr),list_of_neurons,list_of_conn)


    def cross(self, parent1 : Net,parent2 : Net):
        list_of_conn1 = deepcopy(parent1.connections)
        list_of_neurons1 = deepcopy(parent1.neurons)
        list_of_conn2 = deepcopy(parent2.connections)
        list_of_neurons2 = deepcopy(parent2.neurons)
        list_of_neurons = list(set(list_of_neurons1+list_of_neurons2))
        list_of_conn = []
        run = True
        conn1_idx = 0
        conn2_idx = 0
        while run:
            if self.dictionary_of_connections[str(list_of_conn1[conn1_idx])] > self.dictionary_of_connections[str(list_of_conn2[conn2_idx])]:
                list_of_conn.append(list_of_conn2[conn2_idx])
                conn2_idx+=1
            elif self.dictionary_of_connections[str(list_of_conn1[conn1_idx])] < self.dictionary_of_connections[str(list_of_conn2[conn2_idx])]:
                list_of_conn.append(list_of_conn1[conn1_idx])
                conn1_idx+=1
            else:
                # check if any of genes sleep and chose 50%
                genne1 = list_of_conn1[conn1_idx]
                genne2 = list_of_conn2[conn2_idx]
                if genne1.disabled_enabled != genne2.disabled_enabled:
                    if genne1.disabled_enabled:
                        list_of_conn.append(list_of_conn1[conn1_idx])
                    else:
                        list_of_conn.append(list_of_conn2[conn2_idx])
                else:
                    r = random.randint(0,1)
                    if r == 0:
                        list_of_conn.append(list_of_conn1[conn1_idx])
                    else:
                        list_of_conn.append(list_of_conn2[conn2_idx])
                conn1_idx+=1
                conn2_idx+=1
            if conn1_idx == len(list_of_conn1):
                list_of_conn.extend(list_of_conn2[conn2_idx:])
                run = False
            elif conn2_idx == len(list_of_conn2):
                list_of_conn.extend(list_of_conn1[conn1_idx:])
                run = False
            elif conn2_idx == len(list_of_conn2) and conn1_idx == len(list_of_conn1):
                run = False
        return Net(deepcopy(self.input_neurons_nr),deepcopy(self.output_neurons_nr),list_of_neurons,list_of_conn)