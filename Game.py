
import red_agent
import blue_agent
import green_agent
import grey_agent

import csv
import random
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
        green_team = []
        
        ranva = random.randint(0,1)
        for i in range(0, (self.agent_total - 10)):
            green_team.append(green_agent.green_agent(ranva))
        
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
            pass
        else:
            
            #not election day
            pass
    
    
    def execute(self):
        while self.current_date < self.election_date:
            print("Day: " + str(self.current_date))
            red_agent.red_move()
            blue_agent.blue_move()
            self.next_day()

        if(self.current_date == self.election_date):
            print("Election Day: " + str(self.current_date))
            self.next_day()

        print("---------------------")
        #end of game
        print("The election is over!\n")
        pass



'''
TODO - read in the csv data from /tests
'''
if __name__ == "__main__":
    dict = {

    }
    with open('tests/node-attributes', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        #add the data to the dict with id as key and team as value
        for row in reader:
            dict[row[0]] = row[1]
            pass
    
        
    # print(dict)
    Game = Game(10)

    # total_dates = int(input("How many days would you like to run the simulation for? "))
    # game = Game(total_dates)
    # game.execute()






   
