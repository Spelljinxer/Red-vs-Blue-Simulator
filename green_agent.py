"""
Green Agent
@Authors | @StudentId
    Reiden Rufin | 22986337
    Nathan Eden  | 22960674      
"""
import random
class green_agent:
    connections = []
    communicate = None
    def __init__(self, connections, unique_id, vote_status, uncertainty, opinion):
        self.connections = connections
        self.unique_id = unique_id
        self.vote_status = vote_status
        self.uncertainty = uncertainty
        self.opinion = opinion
        self.communicate = True



        