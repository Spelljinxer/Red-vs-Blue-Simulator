"""
Game Class to Execute the Game
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""
from xmlrpc.client import boolean
import red_agent
import blue_agent
import green_agent
import grey_agent

import csv
import igraph as ig
import matplotlib.pyplot as plt
import random
import sys

class Game:
    election_date = 0
    current_date = 1
    blue_energy_level = None
    red_agent = red_agent.red_agent(False)
    blue_agent = blue_agent.blue_agent(blue_energy_level, False)
    '''
    Constructor for the Game
    '''
    def __init__(self, days, green_total, grey_total, blue_energy_level, red_user, blue_user):
        self.election_date = days
        green_team = []
        grey_team = []
        self.red_agent = red_agent.red_agent(red_user)
        self.blue_agent = blue_agent.blue_agent(blue_energy_level, blue_user)

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
            # red_agent.red_move()
            # blue_agent.blue_move()
            self.next_day()

        if(self.current_date == self.election_date):
            print("Election Day: " + str(self.current_date))
            self.next_day()

        print("---------------------")
        #end of game
        print("The election is over!\n")
        pass




#---------------------------------EVERYTHING BELOW RELATE TO THE MAIN EXECUTION----------------------------
def print_usage():
    print("""
                Usage: python Game.py -ge [n] -gp [%] -gr [% gr_agents] -u [x,y] -p [z]
                    -ge: number of green agents
                    -gp: probability of connections
                    -gr: percentage of grey_agents
                    -u: x,y, is the uncertainty range
                        E.g. ( -u 0,1 )
                    -p: percentage of green agents that want to vote initially
            """)

'''
Execute.
'''
if __name__ == "__main__":
    n = len(sys.argv)
    #change this check if we're adding more
    if(n != 11):
        print_usage()
        sys.exit(1)
    total_Green = int(sys.argv[2])
    probability_of_connections = float(sys.argv[4])
    grey_agent_percentage = int(sys.argv[6])
    uncertainty_range = list(map(int, sys.argv[8].split(",")))
    voting_initial_prob = int(sys.argv[10])
    
    print("Total Green Agents: " + str(total_Green))
    print("Probability of Connections: " + str(probability_of_connections))
    print("grey_agent_percentage: ", grey_agent_percentage)
    print("uncertainty_range: ", uncertainty_range)
    print("voting_initial_prob: ", voting_initial_prob)

            
    #---------------------THIS IS WHERE WE EXECUTE THE GAME--------------
    # game = Game(10, 50, 10, 100, red_user, blue_user)
    # '''
    # Don't delete this, this is how we generate a graph
    # '''
    # green_nodes = 50
    # edges = 100
    # g = ig.Graph.Erdos_Renyi(n=green_nodes, m=edges)
    # g.add_vertices(2)
    # g.vs[-2]['colour'] = 'red'
    # g.vs[-1]['blue'] = 'blue'
    # for i in range(len(g.vs)-2):
    #     g.vs[i]['colour'] = 'green'
    
    # #connect all green nodes to each other and to the red node and blue node
    # for i in range(len(g.vs)-2):
    #     g.add_edges([(i, len(g.vs)-2), (i, len(g.vs)-1)])


    user_playing = None
    red_user = False
    blue_user = False
    playing = input("Do you want to play? (y/n): ")
    if playing == "y":
        user_playing = True
        choice = input("Do you want to play as red or blue? (r/b): ")
        if choice == "r":
            red_user = True
            blue_user = False
        elif choice == "b":
            red_user = False
            blue_user = True
    else:
        print("You have chosen not to play. The AI's will instead play.")
        user_playing = False

        

    
    
    # fig, ax = plt.subplots()
    # ig.plot(g, target=ax)
    # plt.show()

    # print("red user: " + str(red_user))
    # print("blue user: " + str(blue_user))







   
