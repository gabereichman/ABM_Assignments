from mesa import Model
from mesa.space import SingleGrid
from agents import SchellingAgent
from mesa.datacollection import DataCollector
import random

class SchellingModel(Model):
    ## Define initiation, requiring all needed parameter inputs
    def __init__(self, width = 30, height = 30, density = 0.7, desired_share_alike_min = 0.25, desired_share_alike_max = 0.75, group_one_share = 0.7, radius = 1, seed = None):
        ## Inherit seed trait from parent class and ensure seed is integer
        if seed is not None:
            seed = int(seed)
        super().__init__(rng=seed)
        ## Define parameter values for model instance
        self.width = width
        self.height = height
        self.density = density
        ## Min and max desired share alike parameters are added
        self.desired_share_alike_min = desired_share_alike_min
        self.desired_share_alike_max = desired_share_alike_max
        self.group_one_share = group_one_share
        self.radius = radius
        ## Create grid
        self.grid = SingleGrid(width, height, torus = True)
        ## Instantiate global happiness tracker
        self.happy = 0
        ## Define data collector, to collect happy agents and share of agents currently happy
        self.datacollector = DataCollector(
            model_reporters = {
                "happy" : "happy",
                "share_happy" : lambda m : (m.happy / len(m.agents)) * 100
                if len(m.agents) > 0
                else 0
            }
        )
        ## Place agents randomly around the grid, randomly assigning them to agent types.
        for cont, pos in self.grid.coord_iter():
            ## New agent's desired share alike assigned by uniform distribution
            desired_share_alike = random.uniform(self.desired_share_alike_min, self.desired_share_alike_max)
            if self.random.random() < self.density:
                ## Parameter for agent desired share alike is passed
                if self.random.random() < self.group_one_share:
                    self.grid.place_agent(SchellingAgent(self, 1, desired_share_alike), pos)
                else:
                    self.grid.place_agent(SchellingAgent(self, 0, desired_share_alike), pos)
        ## Initialize datacollector
        self.datacollector.collect(self)

    ## Define a step: reset global happiness tracker, agents move in random order, collect data
    def step(self):
        self.happy = 0
        self.agents.shuffle_do("move")
        self.datacollector.collect(self)
        ## Run model until all agents are happy
        self.running = self.happy < len(self.agents)
