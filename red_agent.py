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
                if green_agent.vote_status == False:
                    #those who are not voting (on red side) uncertainty decreases 
                    new_uncertainty -= 0.25
                else:
                    #those who are voting (on blue side) uncertainty increases
                    new_uncertainty += 0.25
            #something the code is yet to consider is if it stays within the bounds of the uncertainty interval, in other words, what to do if it does exceed the bounds
            #could be a simple fix just take current value and the maximum value, if +/-0.25 causes it to exceed the bounds just make it equal to the maximum value instead
            
            #next is to calculate probability of changing vote status based off uncertainty lower uncertainty should produce lower probability vice versa 
            #for now i'm using hard coded values pepelaff, I will assume for now green agents uncertainty is between -0.5 - 0.5
            hypothetical_uncertainty_interval = [-0.5, 0.5] #the following assumes that the first value passed into the uncertainty interval is the negative value 
            base_probability = 0.5 #chance of switching vote_status
            #for our current uncertainty_interval the maximum increase/decrease to 0.5 is 0.25, highest chance of swapping vote status is 0.25 vs 0.75
            if new_uncertainty < 0: #negative uncertainty 
                base_probability -= (new_uncertainty/2)
            else:
                base_probability += (new_uncertainty/2)
            #now a positive uncertainty makes it more likely to change, a negative uncertainty makes it less likely to change
            #also now it scales with different uncertainty intervals
            base_probability = base_probability * 100
            chance = random.randint(1, 100)
            if chance <= base_probability:
                if vote_status == False:
                    vote_status = True
                else:
                    vote_status = False
            

        return 





