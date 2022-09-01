class red_agent:
    def __init__(self, message, potency, followerloss):
        self.message = message
        self.potency = potency
        self.followerloss = followerloss


a1 = red_agent("hello, join the read team", 2, 0)


import csv
import random
import time

with open('network-2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    network = list(reader)
    for row in network:
        print(row)

