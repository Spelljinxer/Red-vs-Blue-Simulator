import random

class red_agent:


    def __init__(self):
        pass


    def uncertainity(self, potency):
        uncertainity = potency - 1 + (random.random() * (potency - (potency - 1)))
        return uncertainity
    






