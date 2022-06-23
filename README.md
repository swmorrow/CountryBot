![CountryBot logo github](https://i.imgur.com/rSMISgD.png)

# CountryBot
A Discord bot written in Python to manage Nation RP servers, where users can claim and play as their own custom countries.

## Features
The following section outlines CountryBot's client-side and dev-side features.

### Client-side
- Sets RP date
- Keeps track of in-RP time
- Posts date reminders in a specified channel every 24 hours

### Dev-side
- Data storage with sqlite3
- Command line interface with Fire for easy interaction with the database
- (WIP) Feature testing with unittest


## Roadmap
The following section is a rough outline for features to be added and a progress checker of current updates.

### Before v0.2.0
- [ ] Help command
- [x] Change footer image
- [x] Switch success/denial emoji to the title
- [x] Change config to ini
- [x] Add roadmap to readme

### v0.2.x Updates
- Fix rpdate reposting when the bot turns off and on again bug
- Autorole users when approved
- Switch database to postgres asyncio
- Settings command
- Undo button for approvals/denials
- Add installation instructions to readme

### V0.3.X Plans:
- Support expansion tracking
- Support map queue tracking

### V0.4.X Plans:
- Country registration and tracking

### Long Term
- Warfare

### Backburner
- Remove need for member intents 
