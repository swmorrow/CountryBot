![CountryBot logo github](https://i.imgur.com/rSMISgD.png)

# CountryBot
A Discord bot written in Python to manage Nation RP servers, where users can claim and play as their own custom countries.

## Features
The following section outlines CountryBot's client-side and dev-side features.

### Client-side
- Sets RP date
- Keeps track of in-RP time
- Posts date reminders in a specified channel every 24 hours
- Allows users to claim a country by sending a command to fill out a dialog
- Allows admins to keep track of claims with the click of a button

### Dev-side
- Data storage with sqlite3
- Command line interface with Fire for easy interaction with the database
- (WIP) Feature testing with unittest

## Installation
Ensure that you have Python >=3.10.x before setting up your virtual environment.
1. Clone this repo: `git clone https://github.com/swmorrow/CountryBot.git`
1. Set up your virtual environment
    1. Navigate into the CountryBot directory and create a virtual environment
        - On Linux/Mac: `$ python3.10 -m venv .venv`
        - On Windows: `C:> py -m venv .venv`
    1. Activate the virtual environment on your system
        - On Linux/Mac: `$ source .venv/bin/activate`
        - On Windows: `C:> .\env\Scripts\activate`
1. Install the required dependencies with pip
    - On Linux/Mac: `$ pip install -r requirements.txt`
        - if you do not have pip, do `$ python3 -m ensurepip --upgrade`
    - On Windows: `C:> py -m pip install -r requirements.txt`
        - if you do not have pip, do `C:> py -m ensurepip --upgrade`
1. Run the `main.py` file
    - On Windows: `C:> py main.py`
    - On Linux/Mac: `$ python3 main.py`
    
## Roadmap
The following section is a rough outline for features to be added and a progress checker of current updates.

### v0.2.x Updates
- [x] "Flagify" command to convert user uploaded images to discord-style flag emojis
- [ ] Help command
- [ ] Fix rpdate reposting when the bot turns off and on again bug
- [ ] Autorole users when approved
- [ ] Switch database to asyncio sqlite3
- [ ] Settings command
- [ ] Undo button for approvals/denials
- [ ] Add installation instructions to readme

### V0.3.X Plans:
- Support expansion tracking
- Support map queue tracking

### V0.4.X Plans:
- Country registration and tracking

### Long Term
- Warfare

### Backburner
- Remove need for member intents 