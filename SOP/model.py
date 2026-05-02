from mesa import Model
from mesa.space import SingleGrid
from agents import SOPAgent
from mesa.datacollection import DataCollector

class SOPModel(Model):
    ## Define initiation, requiring all needed parameter inputs
    def __init__(self, width = 30, height = 30, radius = 1, order = 'Synchronous', seed = None):
        ## Inherit seed trait from parent class and ensure seed is integer
        if seed is not None:
            seed = int(seed)
        super().__init__(rng=seed)
        ## Define parameter values for model instance
        self.width = width
        self.height = height
        self.agent_count = width * height
        self.radius = radius
        self.order = order
        ## Create grid
        self.grid = SingleGrid(width, height, torus = False)
        ## Instantiate global standing tracker
        self.standing = 0
        ## Define data collector, to collect standing agents and share of agents currently standing
        self.datacollector = DataCollector(
            model_reporters = {
                "standing" : "standing",
                "share_standing" : lambda m : (m.standing / m.agent_count) * 100
            }
        )
        ## Place agents randomly around the grid, randomly assigning them to agent types.
        for cont, pos in self.grid.coord_iter():
            quality = self.random.random()
            threshold = self.random.random()
            self.grid.place_agent(SOPAgent(self, quality, threshold), pos)
        ## Initialize datacollector
        self.datacollector.collect(self)

    ## Define a step: reset global happiness tracker, agents move in random order, collect data
    def step(self):
        self.standing = 0
        if self.order == 'Synchronous':
            self.agents.shuffle_do("decide")
            self.agents.shuffle_do("update_stand")
        elif self.order == 'Asynchronous-Random':
            self.agents.shuffle_do("decide")
        self.datacollector.collect(self)
        ## Run model until all agents are sitting or standing
        self.running = self.standing not in {0, self.agent_count}
