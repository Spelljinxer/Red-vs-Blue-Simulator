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
            follower_loss = 1
            uncertainty_change = 0.04
        elif message == self.messages[2] or message == self.messages[3]:
            potency = 0.4
            follower_loss = 2
            uncertainty_change = 0.08
        elif message == self.messages[4] or message == self.messages[5]:
            potency = 0.6
            follower_loss = 3
            uncertainty_change = 0.12
        elif message == self.messages[6] or message == self.messages[7]:
            potency = 0.8
            follower_loss = 4
            uncertainty_change = 0.16
        elif message == self.messages[8] or message == self.messages[9]:
            potency = 1.0
            follower_loss = 5
            uncertainty_change = 0.2
        return [potency, follower_loss, uncertainty_change]

    def will_vote_status_change(self, potency):
        return random.randint(0, 100) <= potency * 100
    
    def red_move(self, green_team):
        follower_loss_count = 0
        for green_agent in green_team:
            if(green_agent.communicate):
                #placeholder until we map the user input/AI choice to this variable 
                message = "Had to run a boy down in my Air Force. Pissed, cah now they got a crease in the middle"
                potency_followerloss_uncertaintychange = self.get_message_potency_follower_loss(message)
                potency = potency_followerloss_uncertaintychange[0]
                follower_loss = potency_followerloss_uncertaintychange[1]
                follower_loss_count += follower_loss
                uncertainty_change = potency_followerloss_uncertaintychange[2]
                if green_agent.vote_status:
                    uncertainty_change = -uncertainty_change
                    #since agents should not know uncertainty, how do we handle this? return a dictionary with key as green_agent id and 
                    # value as appropriate change of uncertainty change?
                    #red only wants to improve the certainty of those whose vote status is false, decrease otherwise 
                #opinion change
                will_it = self.will_vote_status_change(potency)
                if (will_it):
                    green_agent.vote_status = False
    
        return [uncertainty_change, follower_loss]

    def send_message(self):
        if(self.user_playing):
            message_output = []
            for messages in self.messages:
                message_output.append(self.messages[messages])
            
            print("Available Messages=", message_output)
            message = input("Please enter a message(0 - 9): ")
            if(int(message) > 9 or int(message) < 0):
                print("Invalid message")
                self.new_red_move()
            else:
                message_to_send = self.messages[int(message)]
                
        else:
            #this is what the AI's best move will be later
            message_to_send = random.choice(list(self.messages.values()))
        
        print("Sending message: ", message_to_send)
        return message_to_send
        
    def new_red_move(self, green_agent, message):
        potency, follower_loss, uncertainty_change = self.get_message_potency_follower_loss(message)
        # print("Potency: ", potency, "Follower Loss: ", follower_loss, "Uncertainty Change: ", uncertainty_change)
        
        #red agent can only talk to it's followers
        if(green_agent.communicate):
            if(green_agent.vote_status):
                #TODO: change uncertainty appropriately
                uncertainty_change = abs(green_agent.uncertainty - uncertainty_change) * 0.125

                
            
        return (uncertainty_change, follower_loss)
        pass





