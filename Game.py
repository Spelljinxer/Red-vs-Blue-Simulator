"""
Game Class to Execute the Game
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674 

saving this here: python Game.py -ge 15 -gp 10 -gr 10 -u 0.0,1.0 -p 75 
"""
from itertools import count
import red_agent
import blue_agent
import green_agent
import grey_agent

# import csv
# import igraph as ig
# import networkx as nx
# import matplotlib.pyplot as plt
import random
import sys

class Game:
    blue_energy_level = None
    red_agent = red_agent.red_agent(False)
    blue_agent = blue_agent.blue_agent( False)
    green_team = []
    grey_team = []
    '''
    Constructor for the Game
    '''
    def __init__(self, uncertainty_range, green_total, grey_percent, edge_probability, initial_voting, red_user, blue_user):
        self.red_agent = red_agent.red_agent(red_user)
        self.blue_agent = blue_agent.blue_agent(blue_user)
        gp_as_percent = grey_percent / 100
        
        if(red_user):
            print("You are the red agent!")
        if(blue_user):
            print("You are the blue agent!")
        for agent_id in range(int(gp_as_percent * green_total)):
            if random.random() < 0.5:
                self.grey_team.append(grey_agent.grey_agent("Red", agent_id))
            else:
                self.grey_team.append(grey_agent.grey_agent("Blue", agent_id))
        
        new_green_total = green_total - (green_total * gp_as_percent)
        voting_pop = int(new_green_total * (initial_voting/100))
        for agent_id in range(int(new_green_total)):
            vote_status = False
            uncertainty = round(random.uniform(uncertainty_range[0], uncertainty_range[1]), 1)
            connections = []
            while(agent_id < voting_pop):
                vote_status = True
                break
            self.green_team.append(green_agent.green_agent(connections, agent_id, vote_status, uncertainty))
           
        
        #generate an undirected graph with n nodes with p probability of an edge between any two nodes
        for agent in self.green_team:
            for agent2 in self.green_team:
                if agent2.unique_id > agent.unique_id:
                    if random.randint(0, 100) <= edge_probability:
                        agent.connections.append(agent2.unique_id)
                        agent2.connections.append(agent.unique_id)

    def green_interaction(self, green_agent, neighbor_node):
        #dominating (LOWER UNCERTAINTY) opinion wins
        if(green_agent.uncertainty == neighbor_node.uncertainty):
            #empty for now.
            pass
        #neighbor agent wins so update green agent
        elif(green_agent.uncertainty > neighbor_node.uncertainty):
            new_uncertainty = abs(green_agent.uncertainty - neighbor_node.uncertainty) * 0.125
            green_agent.vote_status = neighbor_node.vote_status
            green_agent.uncertainty -= new_uncertainty
            green_agent.uncertainty = round(green_agent.uncertainty, 2)
            pass
        #green agent wins so update neighbor node
        elif(green_agent.uncertainty < neighbor_node.uncertainty):
            new_uncertainty = abs(neighbor_node.uncertainty - green_agent.uncertainty) * 0.125
            neighbor_node.vote_status = green_agent.vote_status
            neighbor_node.uncertainty -= new_uncertainty
            neighbor_node.uncertainty = round(neighbor_node.uncertainty, 2)
            pass

    def execute(self):
        #Every round...
        while self.blue_agent.energy_level != 0:
            total_voting = 0
            red_message = self.red_agent.send_message()
            for green_agent in self.green_team:
                if(green_agent.vote_status == True):
                    total_voting += 1
                if(green_agent.communicate == True):
                    self.red_agent.followers += 1
                
                self.red_agent.new_red_move(green_agent, red_message)
            
            #green interaction with each other per round
            green_nodes_visited = []    
            for green_agent in self.green_team:
                if(green_agent.connections):
                    for neighbor in green_agent.connections:
                        if(neighbor > green_agent.unique_id):
                            continue
                        else:
                            if((green_agent.unique_id, neighbor) not in green_nodes_visited):
                                green_nodes_visited.append((green_agent.unique_id, neighbor))
                                self.green_interaction(green_agent, self.green_team[neighbor])
            #reset the count 
            # print("Total Voting:", total_voting)
            # print("Total red followers this round=", self.red_agent.followers)
            self.red_agent.followers = 0
            print("====== NEXT ROUND ======\n")
            self.blue_agent.energy_level -= 1
            


        print("---------------------")
        #end of game
        print("The election is over!\n")
        pass


#---------------------------------EVERYTHING BELOW RELATE TO THE MAIN EXECUTION----------------------------
def print_usage():
    print("""
                Usage: python Game.py -ge [n] -gp [%] -gr [% gr_agents] -u [x,y] -p [z]
                    -ge: number of green agents
                    -gp: probability of connections between green agents
                    -gr: percentage of green_pop that are grey_agents
                    -u: x,y, is the uncertainty range
                        E.g. ( -u 0,1 ) will give us an uncertainty range
                                between 0 and 1
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


    uncertainty_range = sys.argv[8]
    uncertainty_range = [float(x.strip()) for x in uncertainty_range.split(',')]

    initial_voting = int(sys.argv[10])
    

    print("Confirming...")
    print("\t- Total Green Agents: " + str(total_Green))
    print("\t- Probability of Connections: " + str(probability_of_connections))
    print("\t- % of pop that are grey agents: ", grey_agent_percentage)
    print("\t- uncertainty_range: ", uncertainty_range)
    print("\t- initial_voting: ", initial_voting)
    print("Are you sure you want to continue? (y/n)")
    confirm = input()
    if(confirm != "y"):
        print("Exiting...")
        sys.exit(1)
    
    # user_playing = None
    # red_user = False
    # blue_user = False
    # playing = input("Do you wish to play? (y/n): ")
    # if playing == "y":
    #     user_playing = True
    #     choice = input("Do you wish to play as red or blue? (r/b): ")
    #     if choice == "r":
    #         red_user = True
    #         blue_user = False
    #     elif choice == "b":
    #         red_user = False
    #         blue_user = True
    # else:
    #     print("You have chosen not to play. The AI's will instead play.")
    #     user_playing = False
    
    Game = Game(uncertainty_range, total_Green, grey_agent_percentage, probability_of_connections, initial_voting, True, False)
    Game.execute()

    sys.exit(1)
            
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
    # fig, ax = plt.subplots()
    # ig.plot(g, target=ax)
    # plt.show()







   
