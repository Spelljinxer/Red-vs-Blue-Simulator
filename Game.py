#should this be a class or not?
import red_agent
import blue_agent
import green_agent
import grey_agent

class Game:

    election_date = 0
    agent_total = 100 #total number of agents (modify later to match with tests)
    red_agent = red_agent.red_agent()
    blue_agent = blue_agent.blue_agent()
    def __init__(self, days):
        self.election_date = days
        #make a list of green agents
        
        green_team = []
        for i in range(0, self.agent_total - (10)):
            green_team.append(green_agent.green_agent())


g = Game(100)



   
