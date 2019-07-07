# DiscordRPC.py
A complete RPC interface for Discord's API.

_Original code by [qwertyquerty and LewdNeko](https://github.com/qwertyquerty/pypresence)_

This whole thing is a big TODO right now...

---
### Installation
Install from pip

### Extending BaseClient
If you are looking to extend BaseClient and implement your own behaviour / set of endpoints, please remember to implement the following:
- `close` - a way of tidying up any open files or the event loop
- `on_event` - If you do not want events, this can just `pass`, but if you do then you must handle them accordingly. The only argument passed is data, a dictionary created from Discord's event structure. You must be subscribed to receive these.

---
#### How to Use

#### License
Code that is indifferent from [pypresence v3.3.1 or earlier](https://github.com/qwertyquerty/pypresence) remains licensed under the MIT license and retain their copyright to the respective owner. Any changes that have been made are licensed and copyrighted under BSD 3-Clause "New" or "Revised" to LBots.  
