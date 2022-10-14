"""
Red Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""

import random
import math
class red_agent:
    messages = {
        0: "red message 1",
        1: "red message 2",
        2: "red message 3",
        3: "red message 4",
        4: "red message 5",
        5: "red message 6",
        6: "red message 7",
        7: "red message 8",
        8: "red message 9",
        9: "red message 10",
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
            follower_loss = 0.002
            uncertainty_change = 0.04
        elif message == self.messages[2] or message == self.messages[3]:
            potency = 0.4
            follower_loss = 0.004
            uncertainty_change = 0.08
        elif message == self.messages[4] or message == self.messages[5]:
            potency = 0.6
            follower_loss = 0.006
            uncertainty_change = 0.12
        elif message == self.messages[6] or message == self.messages[7]:
            potency = 0.8
            follower_loss = 0.008
            uncertainty_change = 0.16
        elif message == self.messages[8] or message == self.messages[9]:
            potency = 1.0
            follower_loss = 0.01
            uncertainty_change = 0.2
        return [potency, follower_loss, uncertainty_change]

    def will_vote_status_change(self, potency):
        return random.randint(0, 100) <= potency * 100
    
    def red_move(self, green_agent, message):
        follower_loss_count = 0
        uncertainty_change = 0.0
        if(green_agent.communicate):
            potency, follower_loss, uncertainty_change = self.get_message_potency_follower_loss(message)
            follower_loss_count += follower_loss
            if (green_agent.vote_status == False):
                uncertainty_change *= -1
            if(self.will_vote_status_change(potency)):
                # print("CHANGED!!!")
                green_agent.vote_status = False
        
        return uncertainty_change, follower_loss_count

    def send_message(self):
        message_to_send = ""
        if(self.user_playing):
            message_output = []
            for messages in self.messages:
                message_output.append(self.messages[messages])
            print("Available Messages=", message_output)
            message = input("Please enter a message(0 - 9): ")
            try:
                message_to_send = message_output[int(message)]
            except:
                print("Invalid Move. Please Send Another Message.")
                self.send_message()
                
        else:
            #this is what the AI's best move will be later
            message_to_send = random.choice(list(self.messages.values()))
        
        print("Red Sending message: ", message_to_send)
        return message_to_send
        
    def evaluate(self, green_team):
        score = 0
        for green_agent in green_team:
            if(green_agent.communicate):
                if(green_agent.vote_status == False):
                    if(green_agent.uncertainty < 0.5):
                        score += 0.5
                    else:
                        score -= 0.25
                else:
                    score -= 0.5
        return score

