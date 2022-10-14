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
# import networkx as nx
# import matplotlib.pyplot as plt
import random
import sys
import copy
import math

class Game:
    blue_energy_level = None
    red_agent = red_agent.red_agent(False)
    blue_agent = blue_agent.blue_agent(False)
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
        self.blue_agent.energy_level = green_total * 1.5
        print("Blue Energy Level: ", self.blue_agent.energy_level)
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


    #returns the best message that the red agent should send to the green team
    def red_agent_minimax(self, green_team, red_agent, depth, maximizing_player, blue_agent):
        red_agent_messages = []
        for messages in red_agent.messages:
            red_agent_messages.append(red_agent.messages[messages])
        blue_agent_messages = []
        for messages in blue_agent.messages:
            blue_agent_messages.append(blue_agent.messages[messages])
        
        if(depth == 0 or len(red_agent_messages) == 0):
            return None, red_agent.evaluate(green_team)

        if(maximizing_player):
            value = -math.inf
            message_to_send = random.choice(blue_agent_messages)
            for message in red_agent_messages:
                green_team_copy = copy.deepcopy(green_team)
                for green_agent in green_team_copy:
                    red_uncertainty_change, follower_loss = red_agent.red_move(green_agent, message)
                    self.change_green_uncertainty(green_agent.uncertainty, red_uncertainty_change)
                new_score = self.red_agent_minimax(green_team_copy, red_agent, depth - 1, False, blue_agent)[1]
                if(new_score > value):
                    value = new_score
                    message_to_send = message
            return message_to_send, value
        else:
            value = math.inf
            message_to_send = random.choice(red_agent_messages)
            for message in red_agent_messages:
                green_team_copy = copy.deepcopy(green_team)
                for green_agent in green_team_copy:
                    blue_uncertainty_change, energy_loss = blue_agent.blue_move(green_agent, message)
                    self.change_green_uncertainty(green_agent.uncertainty, blue_uncertainty_change)
                new_score = self.red_agent_minimax(green_team_copy, red_agent, depth - 1, True, blue_agent)[1]
                if(new_score < value):
                    value = new_score
                    message_to_send = message
            return message_to_send, value

    def blue_agent_minimax(self, green_team, blue_agent, depth, maximizing_player, red_agent, grey_agent):
        red_agent_messages = []
        for messages in red_agent.messages:
            red_agent_messages.append(red_agent.messages[messages])
        blue_agent_messages = []
        no_send_grey_agent = False
        if(grey_agent):
            no_send_grey_agent = True
            for messages in range(len(blue_agent.messages)-1):
                blue_agent_messages.append(blue_agent.messages[messages])
        else:
            for messages in blue_agent.messages:
                blue_agent_messages.append(blue_agent.messages[messages])
        blue_agent_copy = copy.deepcopy(blue_agent)
        if(depth == 0 or len(blue_agent_messages) == 0):
            return None, blue_agent.evaluate(green_team)

        if(maximizing_player):
            value = -math.inf
            message_to_send = random.choice(red_agent_messages)
            for message in blue_agent_messages:
                green_team_copy = copy.deepcopy(green_team)
                for green_agent in green_team_copy:
                    blue_uncertainty_change, energy_loss = blue_agent_copy.blue_move(green_agent, message)
                    self.change_green_uncertainty(green_agent.uncertainty, blue_uncertainty_change)
                new_score = self.blue_agent_minimax(green_team_copy, blue_agent, depth - 1, False, red_agent, no_send_grey_agent)[1]
                if(new_score > value):
                    value = new_score
                    message_to_send = message
            return message_to_send, value
        else:
            value = math.inf
            message_to_send = random.choice(blue_agent_messages)
            for message in blue_agent_messages:
                green_team_copy = copy.deepcopy(green_team)
                for green_agent in green_team_copy:
                    red_uncertainty_change, follower_loss = red_agent.red_move(green_agent, message)
                    self.change_green_uncertainty(green_agent.uncertainty, red_uncertainty_change)
                new_score = self.blue_agent_minimax(green_team_copy, blue_agent, depth - 1, True, red_agent, no_send_grey_agent)[1]
                if(new_score < value):
                    value = new_score
                    message_to_send = message
            return message_to_send, value

    def execute(self):
        #Every round...
        turn = 0
        while self.blue_agent.energy_level > 0:
            if(self.blue_agent.energy_level <= 0):
                break
            print("Starting Blue Energy: ", self.blue_agent.energy_level)
            total_voting = 0
            
            red_message = ""
            if(red_user):
                red_message = self.red_agent.send_message()
            else:
                red_message = self.red_agent_minimax(self.green_team, self.red_agent, 2, True, self.blue_agent)[0]
                print("RED AI SENT --> ", red_message)
            
            total_follower_loss = 0
            
            for green_agent in self.green_team:
                red_uncertainty_change, follower_loss = self.red_agent.red_move(green_agent, red_message)
                total_follower_loss += follower_loss
                self.change_green_uncertainty(green_agent.uncertainty, red_uncertainty_change)
            # print("before minimax BLUE ENERGY: ", self.blue_agent.energy_level)
            total_energy_loss = 0
            blue_message = ""
            if(blue_user):
                blue_message = self.blue_agent.send_message()
            else:
                blue_message = self.blue_agent_minimax(self.green_team, self.blue_agent, 2, True, self.red_agent, True)[0]
                # print("after minimax BLUE ENERGY: ", self.blue_agent.energy_level)
                print("BLUE AI SENT --> ", blue_message)

            if(blue_message == "summon grey agent"):
                grey_agent = random.choice(self.grey_team)
                print("Grey Agent: ", grey_agent.unique_id, "has been summoned!", "Team: ", grey_agent.team)
                grey_message = ""

                if(grey_agent.team == "Red"):
                    grey_message = self.red_agent_minimax(self.green_team, self.red_agent, 2, True, self.blue_agent)[0]
                elif(grey_agent.team == "Blue"):
                    grey_message = self.blue_agent_minimax(self.green_team, self.blue_agent, 2, True, self.red_agent, True)[0]

                print("The Grey Agent Sent ----->", grey_message)
                uncertainty_change = 0.0
                for green_agent in self.green_team:
                    
                    if(grey_agent.team == "Red"):
                        uncertainty_change = grey_agent.red_move(green_agent, grey_message)
                        # print("uncertainty change for red grey agent: ", uncertainty_change)
                    else:
                        uncertainty_change = grey_agent.blue_move(green_agent, grey_message)
                        # print("uncertainty change for blue grey agent: ", uncertainty_change)
                    
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
            for green_agent in self.green_team:
                if(green_agent.connections):
                    for neighbor in green_agent.connections:
                        if(neighbor > green_agent.unique_id):
                            continue
                        else:
                            if((green_agent.unique_id, neighbor) not in green_nodes_visited):
                                green_nodes_visited.append((green_agent.unique_id, neighbor))
                                self.green_interaction(green_agent, self.green_team[neighbor])

            print("Status of Green Agents")
            for green_agent in self.green_team:
                # print("Green Agent: ", green_agent.unique_id, "vote_status: ", green_agent.vote_status, "uncertainty: ", green_agent.uncertainty)
                if(green_agent.vote_status):
                    total_voting += 1
                if(green_agent.communicate):
                    self.red_agent.followers += 1
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
            turn += 1
            print("====== NEXT ROUND ======\n")
            
        print("----------------------------------")
        #end of game
        print("Blue has run out of energy!\n")
        vote_count = 0
        
        for green_agent in self.green_team:
            # print("Green Agent: ", green_agent.unique_id, "vote_status: ", green_agent.vote_status, "uncertainty: ", green_agent.uncertainty)
            if(green_agent.vote_status):
                vote_count += 1

        if(vote_count > len(self.green_team)/2):
            print("The Winner is Blue!!!")
        elif(vote_count == len(self.green_team)/2):
            print("The Game is a Tie!!!")
        elif(vote_count < len(self.green_team)/2):
            print("The Winner is Red!!!")
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
    import prettytable as pt

    
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
    

    # print("Confirming...")
    # print("\t- Total Green Agents: " + str(total_Green))
    # print("\t- Probability of Connections: " + str(probability_of_connections))
    # print("\t- % of pop that are grey agents: ", grey_agent_percentage)
    # print("\t- uncertainty_range: ", uncertainty_range)
    # print("\t- initial_voting: ", initial_voting)
    sentence = "Confirming Your Selection...\n"
    sentence += '\x1b[6;30;42m' +"- Total Green Agents: " +  str(total_Green) + '\x1b[0m' + "\n"
    sentence += '\x1b[1;33;45m' +"- Probability of Connections: " + str(probability_of_connections) + '\x1b[0m' + "\n"
    sentence += '\x1b[0;34;47m' +"- % of pop that are grey agents: " + str(grey_agent_percentage) + '\x1b[0m' + "\n"
    sentence += '\x1b[1;33;41m' +"- uncertainty_range: " + str(uncertainty_range) + '\x1b[0m' + "\n"
    sentence += '\x1b[0;36;44m' +"- initial_voting: " + str(initial_voting) + '\x1b[0m' + "\n"

    width = 650

    t = pt.PrettyTable()

    t.field_names = ['Red vs Blue Political Simulator']
    [t.add_row([sentence[i:i + width]]) for i in range(0, len(sentence), width)]

    print(t)
    confirm = input("Confirm Your Selection? (y/n): ")
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







   
