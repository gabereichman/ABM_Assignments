import solara
from model import SOPModel
from mesa.visualization import (  
    SolaraViz,
    make_space_component,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

## Define agent portrayal: color, shape, and size
def agent_portrayal(agent):
    return AgentPortrayalStyle(
        color = "blue" if agent.stand else "red",
        marker= "s",
        size= 75,
    )

## Enumerate variable parameters in model
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": {
        "type": "SliderInt",
        "value": 20,
        "label": "Width",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 20,
        "label": "Height",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "order": {
        "type": "Select",
        "value": "Synchronous",
        "values": ["Synchronous",
                   "Asynchronous-Random",
                   "Asynchronous-Incentive-Based"],
        "label": "Activation Order",
    },
    "neighborhood": {
        "type": "Select",
        "value": "5-Neighbor",
        "values": ["5-Neighbor", "Cone"],
        "label": "Neighborhood Type",
    }
}

## Instantiate model
SOP_model = SOPModel()

## Define standing over time plot
StandingPlot = make_plot_component({"share_standing": "tab:green"})

## Define space component
SpaceGraph = make_space_component(agent_portrayal, draw_grid=False)

## Instantiate page inclusing all components
page = SolaraViz(
    SOP_model,
    components=[SpaceGraph, StandingPlot],
    model_params=model_params,
    name="Standing Ovation Problem Model",
)
## Return page
page
    
