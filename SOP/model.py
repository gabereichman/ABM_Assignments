from mesa import Model
from mesa.space import SingleGrid
from agents import SOPAgent
from mesa.datacollection import DataCollector

class SOPModel(Model):
    ## Define initiation, requiring all needed parameter inputs
    def __init__(self, width = 20, height = 20,
                 order = 'Synchronous', neighborhood = '5-Neighbor', seed = None):
        ## Inherit seed trait from parent class and ensure seed is integer
        if seed is not None:
            seed = int(seed)
        super().__init__(rng=seed)
        ## Define parameter values for model instance
        self.width = width
        self.height = height
        self.agent_count = width * height
        self.order = order
        self.neighborhood = neighborhood
        ## Create grid with boundaries
        self.grid = SingleGrid(width, height, torus = False)
        ## Instantiate global standing tracker
        self.standing = 0
        ## Define data collector, to collect standing agents and share of
        # agents currently standing
        self.datacollector = DataCollector(
            model_reporters = {
                "standing" : "standing",
                "share_standing" : lambda m : (m.standing / m.agent_count) * 100
            }
        )
        ## Place agents in each grid space
        for cont, pos in self.grid.coord_iter():
            quality = self.random.random()
            self.grid.place_agent(SOPAgent(self, quality), pos)
        ## Initialize datacollector
        self.datacollector.collect(self)

    ## Define a step: reset global standing tracker
    def step(self):
        self.standing = 0
        ## For synchronous updating, all agents decide then they update
        # (see agent code)
        if self.order == 'Synchronous':
            self.agents.do("decide")
            self.agents.do("update_stand")
        ## For asynchronous-random updating, agents decide and update in a random order
        elif self.order == 'Asynchronous-Random':
            self.agents.shuffle_do("decide")
        ## For asynchronous-incentive-based updating, agent order is determined
        # by degree of difference to neighbors
        else:
            ## Agents first determine their own incentive to move based on the
            # proportion of opposite neighbors
            self.agents.do("update_incentive")

            ## A list of agents is generated to be transformed
            agent_list = [agent for agent in self.agents]
            ## The list is shuffled so that agents with the same incentive are
            # randomly ordered
            self.random.shuffle(agent_list)
            ## The agent list is sorted based on incentive, starting with the
            # highest incentive
            agent_list.sort(key=lambda x: x.incentive, reverse=True)
            ## Agents are manually called to step due to the specified ordering
            for agent in agent_list:
                agent.decide()


        self.datacollector.collect(self)
        ## Run model until all agents are sitting or standing
        self.running = self.standing not in {0, self.agent_count}
