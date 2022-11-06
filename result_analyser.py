'''
This Program is just used to analyse the number of wins/ties from results.txt
@Authors | @Student ID
+-------------------+
Reiden Rufin | 22986337
Nathan Eden | 22960674
'''

with open("results.txt", "r") as f:
    blue = 0
    red = 0
    tie = 0
    for line in f:
        chars = line.split(" ")
        for a in chars:
            if a == 'Blue':
                blue += 1
            elif a == 'Red':
                red += 1
            elif a == 'Tie':
                tie += 1
    print("Blue: " + str(blue))
    print("Red: " + str(red))
    print("Tie: " + str(tie))