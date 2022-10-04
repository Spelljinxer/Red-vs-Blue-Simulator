"""
Grey Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""

import random

class grey_agent:
    blue_messages = {
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
        10: "summon grey agent",
    }
    
    red_messages = {
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
    
    def __init__(self, team, id):
        #which team they are working for
        self.team = team
        #agents unique ID
        self.id = id
        
    def get_message_certainty_energy_loss(self, message):
        certainty = 0.0
        energy_loss = 0.0
        uncertainty_change = 0.0
        if message == self.messages[10]:
            #idk yet
            return True
        elif message == self.messages[0]:
            certainty = 0.1
            energy_loss = 0.005
            uncertainty_change = 0.02
        elif message == self.messages[1]:
            certainty = 0.2
            energy_loss = 0.01
            uncertainty_change = 0.04
        elif message == self.messages[2]:
            certainty = 0.3
            energy_loss = 0.015
            uncertainty_change = 0.06
        elif message == self.messages[3]:
            certainty = 0.4
            energy_loss = 0.02
            uncertainty_change = 0.08
        elif message == self.messages[4]:
            certainty = 0.5
            energy_loss = 0.025
            uncertainty_change = 0.10
        elif message == self.messages[5]:
            certainty = 0.6
            energy_loss = 0.03
            uncertainty_change = 0.12
        elif message == self.messages[6]:
            certainty = 0.7
            energy_loss = 0.035
            uncertainty_change = 0.14
        elif message == self.messages[7]:
            certainty = 0.8
            energy_loss = 0.04
            uncertainty_change = 0.16
        elif message == self.messages[8]:
            certainty = 0.9
            energy_loss = 0.045
            uncertainty_change = 0.18
        elif message == self.messages[9]:
            certainty = 1.0
            energy_loss = 0.05
            uncertainty_change = 0.2
        return [certainty, energy_loss, uncertainty_change]                                                        

    def valid_move(self, output, choice, green_team, grey_team):
        if(int(choice) > len(output) or int(choice) < 1):
            print("Invalid move. Moves have been randomised again.")
            self.blue_move(green_team, grey_team)
        else:
            print("You have chosen: " + output[int(choice) - 1])
    
    def will_vote_status_change(self, certainty):
        chance = certainty * 100
        if (random.randint(0, 100) <= chance):
            return True
    
    def blue_move(self, green_team, grey_team):
        #if the human is playing as the blue agent
        if (self.user_playing):
            output = [] 
            for i in range(3):
                # TODO make this UNIQUE
                message = random.choice(list(self.messages.values()))
                if message not in output:
                    output.append(message)
            if(self.messages[10] not in output):
                output.append(self.messages[10])  
                choice = input("Choose a message to send (1-4): " + str(output) +"\n")
                self.valid_move(output, choice, green_team, grey_team)
            else:
                choice = input("Choose a message to send (1-3): " + str(output) +"\n")
                self.valid_move(output, choice, green_team, grey_team)
        
        #Execute the rest of the code if human is not playing as blue agent
        for green_agent in green_team:
            uncertainty = 0
            #placeholder until we map the user input/AI choice to this variable 
            message = "RUN YOUR BOY OVER THE GRASS"
            certainty_energyloss_uncertaintychange = self.get_message_certainty_energy_loss(message)
            certainty = certainty_energyloss_uncertaintychange[0]
            energy_loss = certainty_energyloss_uncertaintychange[1]
            if (message != self.messages[10]): #if not grey agent
                self.energy_level -= energy_loss
            uncertainty_change = certainty_energyloss_uncertaintychange[2]
            #uncertainty chance
            if green_agent.status == False:
                #blue only wants to improve the certainty of those whose vote status is true, decrease it if false otherwise
                uncertainty_change = -uncertainty_change
            #opinion change 
            will_it = self.will_vote_status_change(certainty)
            if (will_it == True):
                green_agent.vote_status == True
        return uncertainty_change
    
    def get_message_potency_follower_loss(self, message):
        potency = 0
        follower_loss = 0
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

    def will_vote_status_change(self, potency):
        chance = potency * 100
        if (random.randint(0, 100) <= chance):
            return True
    
    def red_move(self, green_team):
        follower_loss_count = 0
        if green_team.communicate == False:
            for green_agent in green_team.agents:
                uncertainty = 0
                #placeholder until we map the user input/AI choice to this variable 
                message = "Had to run a boy down in my Air Force. Pissed, cah now they got a crease in the middle"
                potency_followerloss_uncertaintychange = self.get_message_potency_follower_loss(message)
                potency = potency_followerloss_uncertaintychange[0]
                follower_loss = potency_followerloss_uncertaintychange[1]
                follower_loss_count += follower_loss
                uncertainty_change = potency_followerloss_uncertaintychange[2]
                #uncertainty change 
                if green_agent.vote_status == True:
                    uncertainty_change = -uncertainty_change
                    #since agents should not know uncertainty, how do we handle this? return a dictionary with key as green_agent id and value as appropriate change of uncertainty change?
                    #red only wants to improve the certainty of those whose vote status is false, decrease otherwise 
                #opinion change
                will_it = self.will_vote_status_change(potency)
                if (will_it == True):
                    green_agent.vote_status = False
        return uncertainty_change
        
    def grey_move(self, team, green_team):
        if team == "Red": #red move without follower loss 
           yourmother = self.red_move(green_team)
        else: #blue move without energy loss
           yourmother = self.blue_move(green_team)  
        return yourmother

            
        