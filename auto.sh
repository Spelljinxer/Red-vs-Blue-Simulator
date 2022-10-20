#!bin/bash

# @Authors | @Student ID
# +-------------------+
# Reiden Rufin | 22986337
# Nathan Eden | 22960674


#this is just a shell script to automate game testing
#to change numebr of iterations, change the number in the for loop
echo "Running The Game..."
for ((i=1; i<=100; i++))
do
    python Game.py -ge 100 -gp 10 -gr 10 -u 0.0,10.0 -p 0
done