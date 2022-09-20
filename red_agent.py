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
    def __init__(self):
        self.followers = 0
        self.potency = 0
    
    def red_move(self, green_team):
        for green_agent in green_team:
            if(green_agent.communicate == False or green_agent.vote_status == True):
                continue
            green_agent_uncertainty = green_agent.uncertainty
            potency = random.randint(1, 5)

            uncertainty = (green_agent_uncertainty * potency) / 10


        return





