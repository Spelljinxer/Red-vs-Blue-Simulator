"""
Grey Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""

class grey_agent:
    connections = []
    def __init__(self, connections, team, id):
        self.connections = connections
        #which team they are working for
        self.team = team
        #agents unique ID
        self.id = id
        