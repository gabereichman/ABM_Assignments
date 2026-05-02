*Code adapted from Mesa Examples project*
*Code adapted from Schelling Model from Dr. David Peterson*

# Standing Ovation Problem Model

## Summary

The Standing Ovation Problem Model demonstrates how standing ovations can occur through propogation of standing audience members through a crowd. In the model, each agent represents an audienc member. They have a random chance of standing or remaining seated. Then they look at their fellow audience members and match their state based on the majority in their vision.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```


## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class, currently incomplete
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.