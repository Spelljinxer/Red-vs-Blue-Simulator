"""
Grey Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""

import random
class grey_agent:
    blue_messages = {
        0: "Vote for blue team!",
        1: "Please vote for us!",
        2: "If you vote for us you are a good citizen!",
        3: "Vote for us, we are the best",
        4: "Show your support for our nations future by voting for us!",
        5: "Red team are full of criminals, vote for us!",
        6: "Red team will take away our freedom!",
        7: "Voting for red teams means voting for the end of our nation",
        8: "If you vote for us we will give free healthcare and increase wages!",
        9: "if you don't vote for us you are a loser RIP BOZO",
    }
    
    red_messages = {
        0: "Vote for red team!",
        1: "Please vote for us",
        2: "If you dont vote for us you are a bad person",
        3: "Blue team a democratic left wing upper right alt full circle libtard",
        4: "If blue team wins the future will be dark",
        5: "Blue team is going to lead us to the ground",
        6: "Why vote for blue team? they will destroy our future",
        7: "Blue voters will be punished severely and publicly and will be beaten",
        8: "if do not vote for us we will find you and burn your house down",
        9: "Blue voters and their families will be publically tortured and killed",
    }
    
    def __init__(self, team, unique_id):
        #which team they are working for
        self.team = team
        #agents unique ID
        self.unique_id = unique_id
        
    def get_message_certainty_energy_loss(self, message):
        certainty = 0.0
        uncertainty_change = 0.0
        if message == self.blue_messages[0]:
            certainty = 0.1
            uncertainty_change = 0.02
        elif message == self.blue_messages[1]:
            certainty = 0.2
            uncertainty_change = 0.04
        elif message == self.blue_messages[2]:
            certainty = 0.3
            uncertainty_change = 0.06
        elif message == self.blue_messages[3]:
            certainty = 0.4
            uncertainty_change = 0.08
        elif message == self.blue_messages[4]:
            certainty = 0.5
            uncertainty_change = 0.10
        elif message == self.blue_messages[5]:
            certainty = 0.6
            uncertainty_change = 0.12
        elif message == self.blue_messages[6]:
            certainty = 0.7
            uncertainty_change = 0.14
        elif message == self.blue_messages[7]:
            certainty = 0.8
            uncertainty_change = 0.16
        elif message == self.blue_messages[8]:
            certainty = 0.9
            uncertainty_change = 0.18
        elif message == self.blue_messages[9]:
            certainty = 1.0
            uncertainty_change = 0.2
        return certainty, uncertainty_change                                                     
    
    def will_vote_status_change(self, certainty):
        return random.randint(0, 200) <= certainty * 100

    def blue_move(self, green_agent, message):
        certainty, uncertainty_change = self.get_message_certainty_energy_loss(message)
        if(green_agent.vote_status == False):
            uncertainty_change *= -1
        if(self.will_vote_status_change(certainty)):
            green_agent.vote_status = True
        return uncertainty_change
    
    def get_message_potency_follower_loss(self, message):
        potency = 0
        uncertainty_change = 0.0
        if message == self.red_messages[0] or message == self.red_messages[1]:
            potency = 0.2
            uncertainty_change = 0.03125
        elif message == self.red_messages[2] or message == self.red_messages[3]:
            potency = 0.4
            uncertainty_change = 0.0625
        elif message == self.red_messages[4] or message == self.red_messages[5]:
            potency = 0.6
            uncertainty_change = 0.124
        elif message == self.red_messages[6] or message == self.red_messages[7]:
            potency = 0.8
            uncertainty_change = 0.25
        elif message == self.red_messages[8] or message == self.red_messages[9]:
            potency = 1.0
            uncertainty_change = 0.5
        return [potency, uncertainty_change]

    def will_vote_status_change_red(self, potency):
        return random.randint(0, 100) <= potency * 100

    def red_move(self, green_agent, message):
        uncertainty_change = 0.0
        # if(green_agent.communicate):
        potency, uncertainty_change = self.get_message_potency_follower_loss(message)
        if (green_agent.vote_status):
            uncertainty_change *= -1
        if(self.will_vote_status_change_red(potency)):
            green_agent.vote_status = False
        
        return uncertainty_change

    def grey_message(self, team):
        message_to_send = ""
        if(team == "Red"):
            message_to_send = random.choice(list(self.red_messages.values()))
        else:
            message_to_send = random.choice(list(self.blue_messages.values()))
        
        print("Grey Sending message: ", message_to_send)
        return message_to_send
            
        