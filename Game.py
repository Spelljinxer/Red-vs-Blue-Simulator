"""
Game Class to Execute the Game
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674 

saving this here: python Game.py -ge 15 -gp 10 -gr 10 -u 0.0,1.0 -p 75 
"""
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
    election_date = 0
    current_date = 1
    blue_energy_level = None
    red_agent = red_agent.red_agent(False)
    blue_agent = blue_agent.blue_agent( False)
    green_team = []
    grey_team = []
    '''
    Constructor for the Game
    '''
    def __init__(self, days, uncertainty_range, green_total, grey_percent, edge_probability, initial_voting, red_user, blue_user):
        self.election_date = days
        self.red_agent = red_agent.red_agent(red_user)
        self.blue_agent = blue_agent.blue_agent(blue_user)
        gp_as_percent = grey_percent / 100
        
        grey_total = int(green_total * gp_as_percent)
        for agent_id in range(int(gp_as_percent * green_total)):
            if random.random() < 0.5:
                self.grey_team.append(grey_agent.grey_agent("Red", agent_id))
            else:
                self.grey_team.append(grey_agent.grey_agent("Blue", agent_id))
        
        new_green_total = green_total - (green_total * gp_as_percent)
        voting_pop = int(new_green_total * (initial_voting/100))
        # print("voting_pop:", voting_pop)
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
    
    def green_interaction(opinion_a, uncertainty_a, opinion_b, uncertainty_b):
        #dominating (LOWER UNCERTAINTY) opinion wins
        lowest_uncertainty = min(uncertainty_a, uncertainty_b)
        new_uncertainty = 0
        opinion_to_use = opinion_a
        if lowest_uncertainty == uncertainty_b:
            opinion_to_use = opinion_b
        
        return opinion_to_use, new_uncertainty

    def execute(self):
        while self.blue_agent.energy_level != 0:
            # red_agent.red_move()
            # blue_agent.blue_move()
            # red_agent_uncertainty_change, follower_loss = self.red_agent.red_move(self.green_team)
            # val3, val4, = self.blue_agent.blue_move(self.green_team, self.grey_team)
            # who_wants_to_vote = 0

            #might not be needed here (only used for checking)
            edge_list = []
            for agent in self.green_team:
                for neighbour in agent.connections:
                    edge_list.append((agent.unique_id, neighbour))

            green_nodes_visited = []    
            for green_agent in self.green_team:
                if(green_agent.connections):
                    # print("Green Agent: ", green_agent.unique_id, "|", "connections:", green_agent.connections, "|", "uncertainty:", green_agent.uncertainty)
                    for neighbor in green_agent.connections:
                        if(neighbor > green_agent.unique_id):
                            continue
                        else:
                            if((green_agent.unique_id, neighbor) not in green_nodes_visited):
                                green_nodes_visited.append((green_agent.unique_id, neighbor))
                                
                                neighbor_uncertainty = self.green_team[neighbor].uncertainty
                                neighbor_vote_status = self.green_team[neighbor].vote_status
                                # print("green_agent_uncertainty:", green_agent.uncertainty)
                                # print("neighbor_uncertainty:", neighbor_uncertainty)
                                if(green_agent.vote_status == True):
                                    pass
                                else:
                                    pass
            # for green_agent in self.green_team:
            #     # print("Green Agent", green_agent.unique_id, ":", "Vote Status:", green_agent.vote_status, "Uncertainty:", green_agent.uncertainty)
            #     if(green_agent.connections):
            #         green_nodes_visited.append(green_agent.unique_id)
            #         print("Green Agent: ", green_agent.unique_id, "|", "connections: ", green_agent.connections)
            #         for neighbour in green_agent.connections:
            #             if neighbour not in green_nodes_visited:
            #                 pass
            #             # print("Neighbor:", neighbour, "vote_status:", self.green_team[neighbour].vote_status, "uncertainty:", self.green_team[neighbour].uncertainty)
            #             # if self.green_team[neighbour].vote_status == True:
            # print("Total Green Agents Voting:", who_wants_to_vote)
            self.blue_agent.energy_level -= 1
            print("====== NEXT ROUND ======\n")
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
    Game = Game(2, uncertainty_range, total_Green, grey_agent_percentage, probability_of_connections, initial_voting, False, False)
    Game.execute()

    # user_playing = None
    # red_user = False
    # blue_user = False
    # playing = input("Do you want to play? (y/n): ")
    # if playing == "y":
    #     user_playing = True
    #     choice = input("Do you want to play as red or blue? (r/b): ")
    #     if choice == "r":
    #         red_user = True
    #         blue_user = False
    #     elif choice == "b":
    #         red_user = False
    #         blue_user = True
    # else:
    #     print("You have chosen not to play. The AI's will instead play.")
    #     user_playing = False
            
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







   
