## Purpose
Shows issues spread across multiple boards and shows dependencies.

Could be useful for example to show how Epics are doing across several teams/projects, like so:

![alt tag](https://raw.githubusercontent.com/davidedc/JIRA-multi-board-view/master/docs/multiboard_animation.gif)

## Setup:
- have Python installed (if you are on OSX you are sorted already)
- install the "jira" library (usually "pip install jira")
- install jsonpickle ("pip install -U jsonpickle")
- add your own epic groups and queries in a config.coffee file (a template is provided in the config.coffee.example file)

## Usage:
- python vizit portNumber jiraServerURL login password
- then go to http://localhost:portNumber/index.html

## Interpreting the arrows:
A healthy issue has no dependencies, or depends on another issue which is on any of the columns (on any of the boards) to its _right_ . An unhealthy issue depends on an issue to the left of it (either on the same board or on another board).

