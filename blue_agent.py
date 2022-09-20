"""
Blue Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""
import random
class blue_agent:
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
        10: "summon grey agent",
    }
    followers = None
    def __init__(self, energy_level, user_playing):
        self.energy_level = energy_level
        self.followers = 0
        self.user_playing = user_playing

    def valid_move(self, output, choice, green_team, grey_team):
        if(int(choice) > len(output)):
            print("Invalid move. Moves have been randomised again.")
            self.blue_move(green_team, grey_team)
        else:
            print("You have chosen: " + output[int(choice) - 1])
    
    def blue_move(self, green_team, grey_team):
        #if the human is playing as the blue agent
        if self.user_playing == True:
            output = [] 
            for i in range(3):
                output.append(self.messages[random.randint(0, 9)])
            if(len(grey_team) != 0):
                output.append(self.messages[10])  
                choice = input("Choose a message to send (1-4): " + str(output) +"\n")
                self.valid_move(output, choice, green_team, grey_team)
            else:
                choice = input("Choose a message to send (1-3): " + str(output) +"\n")
                self.valid_move(output, choice, green_team, grey_team)

        for green_agent in green_team:
            if(green_agent.vote_status == True):
                continue
        
            green_agent_uncertainty = green_agent.uncertainty
        self.energy_level += (0.01 * self.followers)
        

agent = blue_agent(100, True)
agent.blue_move([], [1])
