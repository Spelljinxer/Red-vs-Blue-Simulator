# Red vs Blue Political Simulator

# Synopsis

```scala
"The game itself is set in a fictitious country where two teams are seeking geopolitical
influence over its population. The population of the country - the green team will either
be voting or not voting, this will later represent the winner of the game. Two major teams
- Red and Blue team, are trying to outclass and outsmart each other by sending
messages that will hopefully influence the voting statuses of each member of the green
population. The Red Team is an authoritarian state with radicalised ideologies that are
similar to an upper-right government. On the other hand, the Blue Team is a democratic
sector, maximising community freedom identical to a bottom-left government . To
elaborate further, let us first take a look at how each team will run. The Red team’s
inherent goal is to stop as many of the green population from voting by the end of the
game. On the other hand, the Blue team is simply the antithesis of this; in that they are
trying to make as many green members vote by the end of the game. During the game,
each team will take turns distributing their messages across the green population (see
further below). This process will repeat until the Blue team eventually expels all of its
energy, in which the game will end. The winner will be based on the total number of the
voting population contrasted against the total number of the green population."
```
# Agents
```
Red Agent
- 1 Agent that has 5 levels of potent messages
    - Each level has 2 messages
    - The messages' goal is to not make green agent vote
    - Although, sending one could still affect uncertainty of green agent
- In other words, Increases uncertainty of agents that are voting, and vice versa for non-voters
- Has Follower Loss

Blue Team
- 1 Agent with 10 levels of correct messaging
- Certainty Levels
- Energy Levels
- Can let a grey agent in (although they dont know their allegiance)
- In other words, Increases uncertainty of agents that are non-voting, and vice versa for voters

Green Team
- The population to be influenced
- If they are willing to vote (means they are voting for blue)
- If they are not willing to vote (means they are not voting for blue)
- Has an uncertainty level
    - Higher Uncertainty (+) means they are uncertain of whether to vote
    - Lower Uncertainty (-) means they are certain of whether to vote

Grey Team
- Secret Allegiance to red team (unknown)
```

# The Game
```
The goal of red team is not make and green agents vote
The goal of blue team is to make green agents vote
```

# Report

[Report](https://github.com/Spelljinxer/CITS3001-Project/blob/LEE-NAGYUNG/report_22986337_22960674.pdf)

