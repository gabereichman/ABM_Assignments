from mesa import Agent

class SOPAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, quality):
        super().__init__(model)
        ## Set agent initial standing status based on quality
        self.stand = quality >= .5
    ## Define basic decision rule
    def decide(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore = True, radius = 1, include_center = False)
        ## We only want neighbors in the same row or rows in front of the agent
        neighbors_seen = [neighbor for neighbor in neighbors
                          if neighbor.pos[1] <= self.pos[1]]

        ## For cones, we want to add additional agents in view
        if self.model.neighborhood == 'Cone':
            neighbors_seen += [neighbor for neighbor in self.model.agents
                              if (neighbor.pos[1] < self.pos[1]-1 and 
                                  abs(neighbor.pos[0] - self.pos[0]) 
                                  <= (self.pos[1] - neighbor.pos[1]))]
        ## Count neighbors standing
        standing_neighbors = sum([neighbor.stand for neighbor in neighbors_seen])
        ## If an agent has equal standing and sitting neighbors, randomly decide
        prop_standing = standing_neighbors / len(neighbors_seen)
        if prop_standing == .5:
            self.decision = self.model.random.random() < .5
        else:
            ## If not equal, an agent follows the majority in their vision
            self.decision = prop_standing > .5

        ## For non-synchronous time parameters, agents should update status immediately
        if self.model.order != 'Synchronous':
            self.update_stand()

    def update_stand(self):
        ## Agents update their standing/sitting status based on their decision
        self.stand = self.decision
        ## If agent will stand, add 1 to standing agents
        if self.stand:
            self.model.standing +=1

    def update_incentive(self):
        ## Sets an agent's incentive to move based on difference from neighbors
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore = True, radius = 1, include_center = False)
        ## We only want neighbors in the same row or rows in front of the agent
        neighbors_seen = [neighbor for neighbor in neighbors
                          if neighbor.pos[1] <= self.pos[1]]

        ## For cones, we want to add additional agents in view
        if self.model.neighborhood == 'Cone':
            neighbors_seen += [neighbor for neighbor in self.model.agents
                              if (neighbor.pos[1] < self.pos[1]-1 and 
                                  abs(neighbor.pos[0] - self.pos[0])
                                  <= (self.pos[1] - neighbor.pos[1]))]

        ## Calculates the number of neighbors in the opposite state
        diff_neighbors = sum([neighbor.stand != self.stand for neighbor in neighbors_seen])
        ## The incentive to change is the proportion of different neighbors
        self.incentive = diff_neighbors / len(neighbors_seen)
