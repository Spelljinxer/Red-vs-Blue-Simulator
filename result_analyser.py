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