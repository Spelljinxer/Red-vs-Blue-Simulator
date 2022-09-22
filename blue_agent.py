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
        if(int(choice) > len(output) or int(choice) < 1):
            print("Invalid move. Moves have been randomised again.")
            self.blue_move(green_team, grey_team)
        else:
            print("You have chosen: " + output[int(choice) - 1])
    
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
            if(green_agent.vote_status == True):
                continue
        
            green_agent_uncertainty = green_agent.uncertainty

            self.energy_level -= (0.05 * (1 + green_agent_uncertainty))


        #passive buff
        self.energy_level += (0.01 * self.followers)
        

