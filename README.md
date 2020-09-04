# Weather Bot for Telegram

This code is for a simple bot that gets information about weather in chosen area. You can try it out at [@weather_notify_test_bot](https://t.me/weather_notify_test_bot).

### Features
The bot tells user about the weather, gives warnings about some dangerous conditions, and does some very simple recommendations of outerwear. Available commands:
* `/set_location` (`/start` does the same) allows user to set their location by sharing or searching
* `/my_location` tells user the last location they set
* `/current_weather` sends weather summary for the place set by user

### Technology
The bot is fully written in Python3 (v3.8.2 to be exact). User data is kept in PostgreSQL database. Used APIs:
* LocationIQ for forward and reverse geocoding
* OpenWeather for weather data

The code is prepared to be deployed on Heroku. Used libs are as seen in [requirements](../master/requirements.txt)

### Launching
The bot can be launched by running `python3 ./main.py` in a shell from the root of the project.
