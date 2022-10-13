"""
Game Class to Execute the Game
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674 

saving this here: python Game.py -ge 100 -gp 5 -gr 10 -u 0.0,1.0 -p 50
"""
import red_agent
import blue_agent
import green_agent
import grey_agent

# import csv
# import igraph as ig
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

class Game:
    blue_energy_level = None
    red_agent = red_agent.red_agent(False)
    blue_agent = blue_agent.blue_agent( False)
    green_team = []
    grey_team = []
    upper_limit = 0.0
    lower_limit = 0.0
    '''
    Constructor for the Game
    '''
    def __init__(self, uncertainty_range, green_total, grey_percent, edge_probability, initial_voting, red_user, blue_user):
        self.upper_limit = uncertainty_range[1]
        self.lower_limit = uncertainty_range[0]
        self.red_agent = red_agent.red_agent(red_user)
        self.blue_agent = blue_agent.blue_agent(blue_user)
        gp_as_percent = grey_percent / 100
        
        if(red_user):
            print("You are the red agent!")
        if(blue_user):
            print("You are the blue agent!")
        for agent_id in range(int(gp_as_percent * green_total)):
            self.blue_agent.grey_agent_num += 1
            if random.random() < 0.5:
                self.grey_team.append(grey_agent.grey_agent("Red", agent_id))
            else:
                self.grey_team.append(grey_agent.grey_agent("Blue", agent_id))
        
        new_green_total = green_total - (green_total * gp_as_percent)
        voting_pop = int(new_green_total * (initial_voting/100))
        for agent_id in range(int(new_green_total)):
            vote_status = False
            uncertainty = round(random.uniform(uncertainty_range[0], uncertainty_range[1]), 2)
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
        
    def change_green_uncertainty(self, green_agent_uncertainty, uncertainty_change):
        green_agent_uncertainty += uncertainty_change
        if green_agent_uncertainty > self.upper_limit:
            green_agent_uncertainty = self.upper_limit
        elif green_agent_uncertainty < self.lower_limit:
            green_agent_uncertainty = self.lower_limit
            
    #this should return the results of sending a message 
    def fake_red_move(self, green_team, message):
        follower_loss_count = 0
        for green_agent in green_team:
            uncertainty_change, follower_loss = self.red_agent.red_move(green_agent, message)
            hypothetical_follower_loss += follower_loss
            self.change_green_uncertainty(green_agent.uncertainty, uncertainty_change)
        return green_team, hypothetical_follower_loss

     #this returns a dictionary where key = each message, value = green_team after that message is sent, follower loss after that message is sent
    def red_hypothetical_turn(self, red_agent, green_team):
        temp_green_team = green_team
        hypothetical_red_messages = red_agent.send_message(self.red_agent.messages)
        results_of_messages = {}
        for message in hypothetical_red_messages:
            new_green_team, follower_loss = self.fake_red_move(temp_green_team, message)
            results_of_messages.update({message : [new_green_team, follower_loss]})
        return results_of_messages
    
    #this would return the best message to send 
    def finding_best_red_move(self):
        pass
        #call red_hypothetical_turn(red_agent, current_green_team)
        #returns dictionary with results of sending each message
        #here we analyse the results of sending each message and return the best one to send?
        #unsure how to do this 🤔

    # def fake_blue_move(self, green_team, message):
    #     follower_loss_count = 0
    #     for green_agent in green_team:
    #         uncertainty_change, energy_loss = self.blue_agent.blue_move(green_agent, message)
    #         hypothetical_energy_loss += energy_loss
    #         self.change_green_uncertainty(green_agent.uncertainty, uncertainty_change)
    #     return green_team, hypothetical_energy_loss
      
    # def blue_hypothetical_turn(self, blue_agent, green_team):
    #     temp_green_team = green_team
    #     hypothetical_blue_messages = blue_agent.send_message(self.blue_agent.messages)
    #     results_of_messages = {}
    #     for message in hypothetical_blue_messages:
    #         new_green_team, energy_loss = self.fake_blue_move(temp_green_team, message)
    #         results_of_messages.update({message : [new_green_team, energy_loss]})
    #     return results_of_messages
    
    # def finding_best_blue_move(self, results):
    #     pass
            
    def execute(self):
        #Every round...
        while self.blue_agent.energy_level > 0:
            if(self.blue_agent.energy_level <= 0):
                break
            print("Starting Blue Energy: ", self.blue_agent.energy_level)
            total_voting = 0
            
            red_message = self.red_agent.send_message()
            total_follower_loss = 0
            for green_agent in self.green_team:
                if(green_agent.vote_status):
                    total_voting += 1
                if(green_agent.communicate):
                    self.red_agent.followers += 1
                
                red_uncertainty_change, follower_loss = self.red_agent.red_move(green_agent, red_message)
                total_follower_loss += follower_loss
                self.change_green_uncertainty(green_agent.uncertainty, red_uncertainty_change)
            
            total_energy_loss = 0
            blue_message = self.blue_agent.send_message()
            if(blue_message == "summon grey agent"):
                grey_agent = random.choice(self.grey_team)
                print("Grey Agent: ", grey_agent.unique_id, "has been summoned!", "Team: ", grey_agent.team)
                grey_message = grey_agent.grey_message(grey_agent.team)

                uncertainty_change = 0.0
                for green_agent in self.green_team:
                    
                    if(grey_agent.team == "Red"):
                        uncertainty_change = grey_agent.red_move(green_agent,grey_message)
                    else:
                        uncertainty_change = grey_agent.blue_move(green_agent ,grey_message)
                    
                    self.change_green_uncertainty(green_agent.uncertainty, uncertainty_change)

                self.grey_team.remove(grey_agent)
                self.blue_agent.grey_agent_num -= 1
            
            
            else:
                for green_agent in self.green_team:
                    uncertainty_change, energy_loss = self.blue_agent.blue_move(green_agent, blue_message)
                    total_energy_loss += energy_loss
                    self.change_green_uncertainty(green_agent.uncertainty, uncertainty_change)

            print("energy loss this round: ", total_energy_loss)
            #cutoff communication after follower loss
            index = 0
            while(index < round(total_follower_loss)):
                green_agent = random.choice(self.green_team)
                if(green_agent.communicate):
                    green_agent.communicate = False
                    self.red_agent.followers -= 1
                    index += 1

            #green interaction with each other per round
            green_nodes_visited = []    
            diction = {}
            for green_agent in self.green_team:
                diction.update({green_agent.unique_id : green_agent.connections})
                if(green_agent.connections):
                    for neighbor in green_agent.connections:
                        if(neighbor > green_agent.unique_id):
                            continue
                        else:
                            if((green_agent.unique_id, neighbor) not in green_nodes_visited):
                                green_nodes_visited.append((green_agent.unique_id, neighbor))
                                self.green_interaction(green_agent, self.green_team[neighbor])
            g = nx.Graph()
            for key, value in diction.items():
                for v in value:
                    g.add_edge(key, v)
            nx.draw(g, with_labels = True)
            plt.savefig("bitch.png")
            # print("Status of Green Agents")
            # for green_agent in self.green_team:
            #     print("Green Agent: ", green_agent.unique_id, "vote_status: ", green_agent.vote_status, "uncertainty: ", green_agent.uncertainty)
            print("----------------------------------")
            print("Total Population:", len(self.green_team))
            print("Total Voting Population: ", total_voting)
            print("Total Red Followers:", self.red_agent.followers)
            #reset the count 
            self.red_agent.followers = 0
            total_follower_loss = 0
            self.blue_agent.energy_level - total_energy_loss
            print("Blue Energy Level: ", self.blue_agent.energy_level)
            print("----------------------------------")
            print("====== NEXT ROUND ======\n")
            
        print("----------------------------------")
        #end of game
        print("Blue has run out of energy!\n")
        vote_count = 0
        for green_agent in self.green_team:
            if(green_agent.vote_status):
                vote_count += 1
        
        if(vote_count > len(self.green_team)/2):
            print("The Winner is Blue!!!")
        else:
            print("The Winner is RED!!!")
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
    
    red_user = False
    blue_user = False
    playing = input("Do you wish to play? (y/n): ")
    if playing == "y":
        choice = input("Do you wish to play as red or blue? (r/b): ")
        if choice == "r":
            red_user = True
        elif choice == "b":
            blue_user = True
    else:
        print("You have chosen not to play. The AI's will instead play.")
    
    Game = Game(uncertainty_range, total_Green, grey_agent_percentage, probability_of_connections, initial_voting, red_user, blue_user)
    Game.execute()

    sys.exit(1)
    #---------------------igraph???--------------
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







   
