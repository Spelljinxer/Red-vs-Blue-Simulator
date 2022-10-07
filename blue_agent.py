"""
Blue Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""
import random
import sys
class blue_agent:
    messages = {
        0: "msg 1",
        1: "msg 2",
        2: "msg 3",
        3: "msg 4",
        4: "msg 5",
        5: "msg 6",
        6: "msg 7",
        7: "msg 8",
        8: "msg 9",
        9: "msg 10",
        10: "summon grey agent",
    }
    followers = None
    energy_level = 20
    grey_agent_num = 0
    def __init__(self, user_playing):
        self.followers = 0
        self.user_playing = user_playing
    
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
        return random.randint(0, 50) <= certainty * 100

    def blue_move(self, green_agent, message):
        certainty, energy_loss, uncertainty_change = self.get_message_certainty_energy_loss(message)
        if (message != self.messages[10]): #if not grey agent
            self.energy_level -= energy_loss
        if(green_agent.vote_status == False):
            uncertainty_change *= -1
        if(self.will_vote_status_change(certainty)):
            green_agent.vote_status = True
        return uncertainty_change, energy_loss
        #self.energy_level += (0.01 * self.followers)
    
    def send_message(self):
        message_to_send = ""
        if(self.user_playing):
            message_output = []
            #only append messages 1-9 from the dictionary
            for i in range(10):
                message_output.append(self.messages[i])
            message = ""
            if(self.grey_agent_num > 0):
                message_output.append(self.messages[10])
                print("Available Messages= ", message_output)
                message = input("Please enter a message(0 - 10): ")
            else:
                print("Available Messages= ", message_output)
                message = input("Please enter a message(0 - 9): ")
            
            try:
                message_to_send = message_output[int(message)]
            except:
                print("Invalid Move. Please Send Another Message.")
                message_to_send = ""
                self.send_message()
            if(int(message) < 0):
                print("Invalid Move. Please Send Another Message.")
                message_to_send = ""
                self.send_message()
        
        else:
            #this is what the AI's best move will be later
            message_to_send = random.choice(list(self.messages.values()))
        
        print("Blue Sending message: ", message_to_send)
        return message_to_send