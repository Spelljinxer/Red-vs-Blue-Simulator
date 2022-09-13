import random

class red_agent:
    messages = {
        "A" :  0, 
        "B" :  1, 
        "C" :  2,
        "D" :  3,
        "E" :  4,
        "F" :  5,
    }

    def __init__(self):
        pass


    def uncertainty(self, potency):
        uncertainty = potency - 1 + (random.random() * (potency - (potency - 1)))
        return uncertainty
    
    def red_move(self, green_team):
        potency = random.randint(1,5)
        print(potency)
        for agent in green_team:
            if(agent.vote_status == "undecided"):
                uncertainty = self.uncertainty(potency)
        
        pass






