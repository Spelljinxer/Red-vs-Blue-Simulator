import random

class red_agent:


    def __init__(self):
        pass


    def uncertainity(self, potency):
        uncertainity = potency - 1 + (random.random() * (potency - (potency - 1)))
        return uncertainity
    
    def red_move(self, green_team):
        for agent in green_team:
            if(agent.vote_status == "undecided"):
                agent.vote_status = "red"
                print("Red agent converted a green agent to red")
        pass





