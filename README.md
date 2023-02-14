# Discord Admin Bot
Simple administration bot (Inspired by [DBS DAO](https://t.me/bomzhuem))

# Install
## Requirements
- Python3.8+
## Dependencies
- discord.py 2.0.0+
## Installation
1. ```cmd
    sudo apt update && sudo apt upgrade -y
    sudo apt install git
    git clone git@github.com:Sometimesfunny/discord_admin_bot.git
    pip3 install -r requirements.txt
    ```
2. Create admin_bot_config.ini
3. Insert this template:
```ini
[AUTH]
bot_token = 'YOUR_DISCORD_BOT_TOKEN'
```
4. Save file
## Run
```python
python3 discord_admin_bot.py
```
# Features
- Raffles protected with captcha*
- Verification message
- Calls timetable**

*Protected with captcha using opensource pictures of animals

# Calls timetable setup
1. Create file calls_timetable.json
2. Fill the template:
```json
{
    "1": {
    
    },
    "2": {
        "19:00": {
            "1" : "AMBASSADOR PROGRAMS",
            "2" : "NFT & P2E"
        }
    },
    "3": {
    
    },
    "4": {
        "19:00": {
            "1" : "NODES & TESTNETS",
            "2" : "MULTIACCING & RETRODROPS"
        }
    },
    "5": {
    
    },
    "6": {
    
    },
    "7": {
    
    }
}
```
Where 1,2,3,...,7 - weekday number. 1 - Monday, 7 - Sunday

19:00 - call time

1,2 - number of week. For this example:
```json
"19:00": {
        "1" : "NODES & TESTNETS",
        "2" : "MULTIACCING & RETRODROPS"
    }
```
first week - Nodes & Testnets call at 19:00

second week - Multiaccing & Retrodrops call at 19:00

>You can add as much weeks as you want
