#should this be a class or not?
import red_agent
import blue_agent
import green_agent
import grey_agent

class Game:
    
    election_date = 0
    
    def __init__(self, days):
        self.election_date = days
        red_agent = red_agent()
        blue_agent = blue_agent()