"""
Blue Agent
@Authors | @Student ID
+-------------------+
Reiden Rufin | 22986337
Nathan Eden | 22960674    
"""
import random
import prettytable as pt
class blue_agent:
    messages = {
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
        10: "summon grey agent",
    }
    followers = None
    energy_level = 100
    grey_agent_num = 0
    uncertainty_lower_limit = 0.0
    uncertainty_upper_limit = 0.0
    def __init__(self, user_playing, lower_limit, upper_limit):
        self.followers = 0
        self.user_playing = user_playing
        self.uncertainty_lower_limit = lower_limit
        self.uncertainty_upper_limit = upper_limit
    
    #the certainty scales from 0.1 - > 1.0
    #the energy loss scales from 0.05 -> 0.5
    #the uncertainty change scales from 0.02 -> 0.2
    def get_message_certainty_energy_loss(self, message):
        certainty = 0.0
        energy_loss = 0.0
        uncertainty_change = 0.0
        if message == self.messages[10]:
            pass
        elif message == self.messages[0]:
            certainty = 0.1
            energy_loss = 0.05
            uncertainty_change = 0.02
        elif message == self.messages[1]:
            certainty = 0.2
            energy_loss = 0.1
            uncertainty_change = 0.04
        elif message == self.messages[2]:
            certainty = 0.3
            energy_loss = 0.15
            uncertainty_change = 0.06
        elif message == self.messages[3]:
            certainty = 0.4
            energy_loss = 0.2
            uncertainty_change = 0.08
        elif message == self.messages[4]:
            certainty = 0.5
            energy_loss = 0.25
            uncertainty_change = 0.10
        elif message == self.messages[5]:
            certainty = 0.6
            energy_loss = 0.3
            uncertainty_change = 0.12
        elif message == self.messages[6]:
            certainty = 0.7
            energy_loss = 0.35
            uncertainty_change = 0.14
        elif message == self.messages[7]:
            certainty = 0.8
            energy_loss = 0.4
            uncertainty_change = 0.16
        elif message == self.messages[8]:
            certainty = 0.9
            energy_loss = 0.45
            uncertainty_change = 0.18
        elif message == self.messages[9]:
            certainty = 1
            energy_loss = 0.5
            uncertainty_change = 0.2
        return [certainty, energy_loss, uncertainty_change]                                                        
    
    #See Assmption 6 as to why it is harder for blue to generate the change
    def will_vote_status_change(self, certainty):
        return random.randint(0, 200) <= certainty * 100

    def blue_move(self, green_agent, message):
        certainty, energy_loss, uncertainty_change = self.get_message_certainty_energy_loss(message)
        if (message != self.messages[10]): #if not grey agent
            self.energy_level -= energy_loss
            pass
        if(green_agent.vote_status):
            uncertainty_change *= -1
        if(self.will_vote_status_change(certainty)):
            green_agent.vote_status = True
        return uncertainty_change, energy_loss
        #self.energy_level += (0.01 * self.followers)
    
    def send_message(self):
        message_to_send = ""
        message_output = []
        if(self.user_playing):
            for i in range(10):
                message_output.append(self.messages[i])
            message = ""
            if(self.grey_agent_num > 0):
                message_output.append(self.messages[10])
                table = pt.PrettyTable()
                table.field_names = ["Message Number", '\x1b[0;36;44m' + "Message" + '\x1b[0m']
                for i in range(len(message_output)):
                    table.add_row([i, message_output[i]])
                print(table)
                message = input("Please enter a message(0 - 10): ")
            else:
                table = pt.PrettyTable()
                table.field_names = ["Message Number", '\x1b[0;36;44m' + "Message" + '\x1b[0m']
                for i in range(len(message_output)):
                    table.add_row([i, message_output[i]])
                print(table)
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
            for i in range(10):
                message_output.append(self.messages[i])
            if(self.grey_agent_num > 0):
                message_output.append(self.messages[10])        
            message_to_send = random.choice(message_output)

        print("Blue Sending message: ", message_to_send)
        return message_to_send

    #Our evaluation for minimax just checks,
    #for each agent, if their opinion is voting, then add score, else subtract score
    def evaluate(self, green_team):
        score = 0
        for green_agent in green_team:
            if(green_agent.vote_status):
                score += 0.5
            else:
                score -= 0.5
        return score