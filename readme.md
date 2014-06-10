Will show issues spread across multiple boards (draft alert: this is work in progress).

Could be useful for example to show how Epics are doing across several teams/projects.

Setup:
- have Python installed (if you are on OSX you are sorted already)
- install the "jira" library (usually "pip install jira")
- add your own epic groups and queries in a config.coffee file (a template is provided in the config.coffee.example file)

Usage:
- python vizit portNumber jiraServerURL login password
- then go to http://localhost:portNumber/index.html
