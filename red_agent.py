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
        
    def get_message_potency_follower_loss(self, message):
        potency = 0
        follower_loss = 0
        uncertainty_change = 0
        if message == self.messages[0] or message == self.messages[1]:
            potency = 0.2
            follower_loss = 0.02
            uncertainty_change = 0.04
        elif message == self.messages[2] or message == self.messages[3]:
            potency = 0.4
            follower_loss = 0.04
            uncertainty_change = 0.08
        elif message == self.messages[4] or message == self.messages[5]:
            potency = 0.6
            follower_loss = 0.06
            uncertainty_change = 0.12
        elif message == self.messages[6] or message == self.messages[7]:
            potency = 0.8
            follower_loss = 0.08
            uncertainty_change = 0.16
        elif message == self.messages[8] or message == self.messages[9]:
            potency = 1.0
            follower_loss = 0.1
            uncertainty_change = 0.2
        return [potency, follower_loss, uncertainty_change]

    def valid_move(self, output, choice, green_team):
        if(int(choice) > len(output) or int(choice) < 1):
            print("Invalid move. Moves have been randomised again.")
            self.red_move(green_team)
        else:
            print("You have chosen: " + output[int(choice) - 1])

    def will_vote_status_change(self, potency):
        chance = potency * 100
        if (random.randint(0, 100) <= chance):
            return True
    
    def red_move(self, green_team):
        follower_loss_count = 0
        if (self.user_playing):
            output = []
            for i in range(3):
                message = random.choice(list(self.massages.values()))
                if message not in output:
                    output.append(message)
                choice = input("Choose a message to send: (1-3): " + str(output) + "\n")
                self.valid_move(output, choice, green_team)
        
        if green_team.communicate == True:
            for green_agent in green_team.agents:
                #placeholder until we map the user input/AI choice to this variable 
                potency_followerloss_uncertaintychange = self.get_message_potency_follower_loss(message)
                potency = potency_followerloss_uncertaintychange[0]
                follower_loss = potency_followerloss_uncertaintychange[1]
                follower_loss_count += follower_loss
                uncertainty_change = potency_followerloss_uncertaintychange[2]
                #uncertainty change 
                if green_agent.vote_status == True:
                    uncertainty_change = -uncertainty_change
                    #red only wants to improve the certainty of those whose vote status is false, decrease otherwise 
                #opinion change
                will_it = self.will_vote_status_change(potency)
                if (will_it == True):
                    green_agent.vote_status = False
    
        return [uncertainty_change, follower_loss]





