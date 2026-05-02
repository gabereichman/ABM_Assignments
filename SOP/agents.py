from mesa import Agent

class SOPAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, quality, threshold):
        super().__init__(model)
        ## Set agent initial standing status
        self.stand = quality > threshold
    ## Define basic decision rule
    def decide(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore = True, radius = self.model.radius, include_center = False)
        neighbors_seen = [neighbor for neighbor in neighbors if neighbor.pos[1] >= self.pos[1]]
        ## Count neighbors of same type as self
        standing_neighbors = sum([neighbor.stand for neighbor in neighbors_seen])
        ## If an agent has equal standing and sitting neighbors, randomly decide
        prop_standing = standing_neighbors / len(neighbors_seen)
        if prop_standing == .5:
            self.decision = self.model.random.random() < .5
        else:
            self.decision = prop_standing > .5

        if self.model.order != 'Synchronous':
            self.update_stand()
    def update_stand(self):
        self.stand = self.decision
        ## If agent will stand, add 1 to standing agents
        if self.stand:
            self.model.standing +=1
