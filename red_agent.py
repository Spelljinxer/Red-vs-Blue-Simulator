"""
Red Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""

import random
class red_agent:
    messages = {
        0: "message 1",
        1: "message 2",
        2: "message 3",
        3: "message 4",
        4: "message 5",
        5: "message 6",
        6: "message 7",
        7: "message 8",
        8: "message 9",
        9: "message 10",
    }
    followers = None
    potency = None
    def __init__(self, user_playing):
        self.followers = 0
        self.potency = 0
        self.user_playing = user_playing 
    
    def return_threshold(self, potency):
        #potency can be any value from 0.1 - 5.0
        if (potency < 1.6):
            threshold = "Low"
        elif (potency >= 1.6 and potency < 2.6):
            threshold = "Medium low"
        elif (potency >= 2.6 and potency < 3.6):
            threshold = "Medium high"
        else:
            threshold = "High"
        return threshold

    def uncertainty_change_chance(self, probability):
        change = random.randint(1, 10)
        if (change <= probability):
            return True
        else:
            return False
    
    def red_move(self, green_team):
        potency = random.randint(1, 5)
        threshhold_potency = random.randdouble(0.0, potency)
        for green_agent in green_team:
            if(green_agent.communicate == False or green_agent.vote_status == True):
                continue
            new_uncertainty = green_agent.uncertainty
            threshhold_potency = random.random() * potency
            threshold = self.return_threshold(threshhold_potency)
            if threshold == "Low":
                probability = random.randint(1, 2)
            elif threshold == "Medium low":
                probability = random.randint(3, 5)
            elif threshold == "Medium high":
                probability = random.randint(6, 8)
            else:
                probability = random.randint(9, 10)
            willUncertaintyChange = self.uncertainty_change_chance(probability)
            if willUncertaintyChange == True:
                new_uncertainty += 0.25
            
            #next is to calculate probability of changing vote status based off uncertainty 
            
           
            

        return





