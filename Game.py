"""
Game Class to Execute the Game
@Authors | @Student ID
+-------------------+
Reiden Rufin | 22986337
Nathan Eden | 22960674

Example Usage: python Game.py -ge 100 -gp 5 -gr 10 -u 0.0,1.0 -p 50
"""

import red_agent
import blue_agent
import green_agent
import grey_agent

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import prettytable as pt
import random
import sys
import copy
import math
import time

class Game:
    blue_energy_level = None
    red_agent = red_agent.red_agent(False, 0, 0)
    blue_agent = blue_agent.blue_agent(False, 0, 0)
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
        self.red_agent = red_agent.red_agent(red_user, self.lower_limit, self.upper_limit)
        self.blue_agent = blue_agent.blue_agent(blue_user, self.lower_limit, self.upper_limit)
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

        #the total amount of green agents should be the total amount of green agents minus the amount of grey agents as %
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

        #generate an undirected graph with n nodes with p probability (Edge_probability) of an edge between any two nodes
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
    
    #How we change the green agent's uncertainty
    # if it reaches below the lower limit then it simply becomes the lower limit
    # vice versa.
    def change_green_uncertainty(self, green_agent_uncertainty, uncertainty_change):
        green_agent_uncertainty += uncertainty_change
        if green_agent_uncertainty > self.upper_limit:
            green_agent_uncertainty = self.upper_limit
        elif green_agent_uncertainty < self.lower_limit:
            green_agent_uncertainty = self.lower_limit

    #minimax with alpha beta pruning for red agent
    def red_agent_minimax(self, green_team, red_agent, depth, maximizing_player, blue_agent, alpha, beta):
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
                #creates the hypothetical move using a copy of the current game state
                for green_agent in green_team_copy:
                    red_uncertainty_change, follower_loss = red_agent.red_move(green_agent, message)
                    self.change_green_uncertainty(green_agent.uncertainty, red_uncertainty_change)
                new_score = self.red_agent_minimax(green_team_copy, red_agent, depth - 1, False, blue_agent, alpha, beta)[1]
                if(new_score > value):
                    value = new_score
                    message_to_send = message
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return message_to_send, value
        else:
            value = math.inf
            message_to_send = random.choice(red_agent_messages)
            for message in red_agent_messages:
                green_team_copy = copy.deepcopy(green_team)
                for green_agent in green_team_copy:
                    blue_uncertainty_change, energy_loss = blue_agent.blue_move(green_agent, message)
                    self.change_green_uncertainty(green_agent.uncertainty, blue_uncertainty_change)
                new_score = self.red_agent_minimax(green_team_copy, red_agent, depth - 1, True, blue_agent, alpha, beta)[1]
                if(new_score < value):
                    value = new_score
                    message_to_send = message
                beta = min(beta, value)
                if alpha >= beta:
                    break

            return message_to_send, value

    #minimax with alpha beta pruning for blue agent
    def blue_agent_minimax(self, green_team, blue_agent, depth, maximizing_player, red_agent, grey_agent, alpha, beta):
        red_agent_messages = []
        for messages in red_agent.messages:
            red_agent_messages.append(red_agent.messages[messages])
        blue_agent_messages = []
        no_send_grey_agent = False

        #As the grey agent cannot summon another grey agent, 
        # we do not add the "summon grey agent" option for this section
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
                new_score = self.blue_agent_minimax(green_team_copy, blue_agent_copy, depth - 1, False, red_agent, no_send_grey_agent, alpha, beta)[1]
                if(new_score > value):
                    value = new_score
                    message_to_send = message
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return message_to_send, value
        else:
            value = math.inf
            message_to_send = random.choice(blue_agent_messages)
            for message in blue_agent_messages:
                green_team_copy = copy.deepcopy(green_team)
                for green_agent in green_team_copy:
                    red_uncertainty_change, follower_loss = red_agent.red_move(green_agent, message)
                    self.change_green_uncertainty(green_agent.uncertainty, red_uncertainty_change)
                new_score = self.blue_agent_minimax(green_team_copy, blue_agent_copy, depth - 1, True, red_agent, no_send_grey_agent, alpha, beta)[1]
                if(new_score < value):
                    value = new_score
                    message_to_send = message
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return message_to_send, value
    
    #creates the network graph to display
    def visualisation(self, green_team):
        plt.figure(1,figsize=(12,12))
        green_connections = {}
        red_connections = {}
        color_map = []
        g = nx.Graph()
        
        #Adding Red Agent and Blue Agent
        g.add_node("RED")
        g.add_node("BLUE")
        color_map.append("Red")
        color_map.append("Blue")
        
        for green_agent in green_team:
            green_connections.update({green_agent.unique_id : green_agent.connections})
            red_connections.update({green_agent.unique_id : green_agent.communicate})
            #Paint nodes blue is they ARE voting, red if they ARE NOT voting
            if green_agent.vote_status == True:
                color_map.append("Blue")
            else:
                color_map.append("Red")
        for key, value in green_connections.items():
            for v in value:
                g.add_edge(key, v)
        for key, value in red_connections.items():
            g.add_edge(key, "BLUE")
            if value == True:
                g.add_edge(key, "RED")
        nx.draw(g, node_color = color_map, with_labels=True)
        plt.show()

    #creates the histogram plot for uncertainty distribution
    def uncertainties_graph(self, uncertainties):
        matplotlib.use('TkAgg')
        fig, ax = plt.subplots()
        ax.hist(uncertainties, bins = 50, color = 'red', edgecolor = 'blue')
        ax.set_title('Green Agent Uncertainty Distribution Graph', size = 15)
        ax.set_xlabel('Uncertainty Level', size = 18)
        ax.set_ylabel('Number of Nodes', size = 18)
        plt.show()
        return plt
    
    def execute(self):
        print("+-------------------------------------+")
        #Every round...
        turn = 0
        voting_pop = 0
        uncertainties = []
        while self.blue_agent.energy_level > 0:
            if(self.blue_agent.energy_level <= 0):
                break
            print("Starting Blue Energy: ", self.blue_agent.energy_level)
            
            total_voting = 0
            
            red_message = ""
            if(red_user):
                red_message = self.red_agent.send_message()
            else:
                red_message = self.red_agent_minimax(self.green_team, self.red_agent, 2, True, self.blue_agent, -math.inf, math.inf)[0]
                print("RED AI SENT --> ", red_message)
            total_follower_loss = 0
            #RED INTERACTION (RED TURN)
            for green_agent in self.green_team:
                red_uncertainty_change, follower_loss = self.red_agent.red_move(green_agent, red_message)
                total_follower_loss += follower_loss
                self.change_green_uncertainty(green_agent.uncertainty, red_uncertainty_change)
            

            #BLUE INTERACTION (BLUE TURN)
            total_energy_loss = 0
            blue_message = ""
            if(blue_user):
                blue_message = self.blue_agent.send_message()
            else:
                blue_message = self.blue_agent_minimax(self.green_team, self.blue_agent, 3, True, self.red_agent, True, -math.inf, math.inf)[0]
                # print("after minimax BLUE ENERGY: ", self.blue_agent.energy_level)
                print("BLUE AI SENT --> ", blue_message)

            #handle if the message is to summon a grey agent
            if(blue_message == "summon grey agent"):
                grey_agent = random.choice(self.grey_team)
                print("Grey Agent: ", grey_agent.unique_id, "has been summoned!", "Team: ", grey_agent.team)
                grey_message = ""

                if(grey_agent.team == "Red"):
                    grey_message = self.red_agent_minimax(self.green_team, self.red_agent, 2, True, self.blue_agent, -math.inf, math.inf)[0]
                elif(grey_agent.team == "Blue"):
                    grey_message = self.blue_agent_minimax(self.green_team, self.blue_agent, 3, True, self.red_agent, True, -math.inf, math.inf)[0]

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

            #cutoff communication based on the number of follower loss,
            #that is set communicate to False.
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
                        #we only want to visit edges once
                        if(neighbor > green_agent.unique_id):
                            continue
                        else:
                            if((green_agent.unique_id, neighbor) not in green_nodes_visited):
                                green_nodes_visited.append((green_agent.unique_id, neighbor))
                                self.green_interaction(green_agent, self.green_team[neighbor])
            
            #Displays the network graph followed by the uncertainty distribution graph
            print("Showing current status of the population...")
            self.visualisation(self.green_team)
            for green_agent in self.green_team:
                uncertainties.append(green_agent.uncertainty)
            lista  = self.uncertainties_graph(uncertainties)

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
            voting_pop = total_voting
            print("Total Red Followers:", self.red_agent.followers)
            #reset the count
            self.red_agent.followers = 0
            total_follower_loss = 0
            self.blue_agent.energy_level - total_energy_loss
            print("----------------------------------")
            turn += 1
            print("================== NEXT ROUND ==================\n")

        print("----------------------------------")
        #end of game
        print("Blue has run out of energy!\n")
        print("The game lasted for",turn, "rounds")
        vote_count = 0

        for green_agent in self.green_team:
            # print("Green Agent: ", green_agent.unique_id, "vote_status: ", green_agent.vote_status, "uncertainty: ", green_agent.uncertainty)
            if(green_agent.vote_status):
                vote_count += 1

        winner = ""
        if(vote_count > len(self.green_team)/2):
            print("The Winner is Blue!!!")
            winner = "Blue"
        elif(vote_count == len(self.green_team)/2):
            print("The Game is a Tie!!!")
            winner = "Tie"
        elif(vote_count < len(self.green_team)/2):
            print("The Winner is Red!!!")
            winner = "Red"

        
        with open("results.txt", "a") as f:
            f.write("Winner : " + str(winner) + " |" + " Voting Population : " + str(voting_pop) + " |" + " Total Population : " + str(len(self.green_team)) + "\n")
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
    start_time = time.time()
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
            print("Invalid choice, exiting...")
            sys.exit(1)
    else:
        print("You have chosen not to play. The AI's will instead play.")

    Game = Game(uncertainty_range, total_Green, grey_agent_percentage, probability_of_connections, initial_voting, red_user, blue_user)
    Game.execute()

    #Was only used explicitly for testing runtime
    #print ("took", time.time() - start_time, "to run")

