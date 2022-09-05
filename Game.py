#should this be a class or not?
import red_agent
import blue_agent
import green_agent
import grey_agent

class Game:

    election_date = 0
    current_date = 0
    
    agent_total = 100 #total number of agents (modify later to match with tests)
    red_agent = red_agent.red_agent()
    blue_agent = blue_agent.blue_agent()
    
    '''
    Constructor for the Game
    '''
    def __init__(self, days):
        self.election_date = days
        #make a list of green agents
        
        green_team = []
        for i in range(0, self.agent_total - (10)):
            green_team.append(green_agent.green_agent())
        
        grey_team = []
        for i in range(0, 10):
            grey_team.append(grey_agent.grey_agent())
    
    '''
    Increment to go the next round
    '''
    def next_day(self):
        self.current_date += 1
        if self.current_date == self.election_date:
            #election day
            print("It is Election Day!\n")
            pass
        else:
            
            #not election day
            pass

g = Game(100)
print(g.election_date)




   
