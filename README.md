# PC Idle

Here's a little script I wrote to track when a PC is being used or not, and change a boolean in HomeAssistant based on
that. I use it to enhance room-prescence detection, as bluetooth tracking is not very reliable when it comes to tracking
RSSI.

## Changes from the original

- Remove webcam based face detection
- Use `poetry` for dependencies management

## Installation

Currently only Windows is supported, ~~Linux support will come some day~~.

1. If you don't have it yet, download Python 3.x from python.org and install it.
2. Install `poetry` from <https://python-poetry.org/>
3. Install dependencies with `poetry install`
4. Open config.yaml and enter your HomeAssistant API URL. Could be an IP or a domain name.
5. Go to your HomeAssistant -> Profile -> and generate a long lived token
6. Paste it into config after `token:`... Well, if you use HomeAssistant you should know YAML :D
7. Adjust other parameters to your liking
8. In the shell type `poetry run python pc_idle.py` and hit enter.

You can also use Windows Scheduler to schedule it to start on boot or login.
