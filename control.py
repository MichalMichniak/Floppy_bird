import random

class Control:
    def __init__(self,n_inputs, n_outputs) -> None:
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        pass

    def predict(self, input):
        return int(random.randint(0,14)==10)