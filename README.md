# CITS3001-Project

# Requirements

```console
username@machine:~$ pip install igraph
username@machine:~$ 
username@machine:~$ pip install matplotlib
```

> Report Drafting
> [https://docs.google.com/document/d/1XoNAPVyNEpUasD-rrc3I7k6QzF49HbfPvaAK0cTerEA/edit?usp=sharing](https://docs.google.com/document/d/1XoNAPVyNEpUasD-rrc3I7k6QzF49HbfPvaAK0cTerEA/edit?usp=sharing)

# Agents
```
Red Team
- 1 Agent that has 5 levels of potent messages
    - Each level has 2 messages
    - The messages' goal is to not make green agent vote
    - Although, sending one could still affect uncertainty of green agent
- In other words, INCREASE UNCERTAINTY
- Has Follower Loss

Blue Team
- 1 Agent with 10 levels of correct messaging
- Certainty Levels
- Energy Levels
- Can let a grey agent in (although they dont know their allegiance)
- Goal is to make green agents vote (DECREASE UNCERTAINTY) 

Green Team
- Majority of Agents (probably 80-90)
- If they are willing to vote (means they are voting for blue)
- If they are not willing to vote (means they are not voting for blue)
- Has an uncertainty level
    - Higher Uncertainty (+) means they are uncertain of whether to vote
    - Lower Uncertainty (-) means they are certain of whether to vote

Grey Team
- Secret Allegiance to red team (unknown)
- Rest of agents from green
```

# The Game
```
Will run for a simulated amount of days OR until the blue team expends all their energy
The goal of red team is not make and green agents vote
The goal of blue team is to make green agents vote
```

