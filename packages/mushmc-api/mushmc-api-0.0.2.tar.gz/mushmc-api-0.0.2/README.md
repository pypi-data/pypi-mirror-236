## MushMC-API Overview
- **MushMC-API** is a Python library for developers that facilitates access to the [MushMC](https://mush.com.br/) server API, making project creation more efficient and dynamic. It is unofficial, but offers an improved and independent experience for interested developers.

<br>

## Table of Contents
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Disclaimer](#disclaimer)

## Installation
To install the library, use the command below:
```bash
python -m pip install mushmc-api
```

## Getting started
Importing the library into your Python project:
```python
from mushmc import MushMC
```
- To use the library, you must install it via pip. [Click here](#installation) to see how to install it.

<br>

Creating an instance of the MushMC class:
```python
mushmc = MushMC() # async_run=False
```
- The class has an optional parameter, which is `async_run`, which only accepts Boolean values. If `True`, the instance will be asynchronous, otherwise it will be synchronous. The default is `False`.

<br>

Using the created instance to obtain information about the "FHDP" player:
```python
player = mushmc.Player(nick_or_uuid='FHDP') # retries=0, timeout=5
```
- The class has a mandatory parameter, which is `nick_or_uuid`, which only accepts values of type `str`. The value can be the player's nick or uuid.
- Furthermore, it has two optional parameters, which are `retries` and `timeout`, which only accept values of type `int`. The `retries` is the number of attempts that the program will make to obtain the player's information, if an error occurs. The `timeout` is the maximum waiting time to obtain player information. `retries` defaults to `0` and `timeout` defaults to `5`.

<br>

Getting general player information:
```python
raw_response = player.raw_response

first_login = player.first_login
last_login = player.last_login
is_online = player.is_online
discord = player.discord
account = player.account
rank = player.rank
clan = player.clan
```
- The class has an attribute called `raw_response`, which returns a dictionary with all available player information, without any processing.
- In addition, it has other attributes, which are:
   - `first_login`: returns in [**unix**](https://www.unixtimestamp.com/) format the date and time of the first time the player entered the server.
   - `last_login`: returns in [**unix**](https://www.unixtimestamp.com/) format the date and time of the last time the player logged into the server.
   - `is_online`: returns a boolean value indicating whether the player is online or not.
   - `discord`: returns a dictionary with the player's Discord account information, if they have linked it.
   - `account`: returns a dictionary with the player's account information on the server.
   - `rank`: returns a dictionary with the player's rank information on the server.
   - `clan`: returns a dictionary with the player's clan information on the server.

<br>

Getting player information about game modes (example: "bedwars"):
```python
play_time = player.play_time
game_list = player.list_games()
game_stats = player.get_game_stats(game='bedwars')
```
- The class has other attributes and methods, which are:
   - `play_time`: returns a dictionary with information about the player's playing time in each game mode.
   - `list_games()`: returns a list with the names of game modes in which the player has played.
   - `get_game_stats(game)`: returns a dictionary with player information about the specified game mode. The `game` parameter is mandatory and only accepts values of type `str`. The value must be the name of the game mode and is case-sensitive.

<br>

## Disclaimer
- This library is unofficial and is not affiliated with the [MushMC](https://mush.com.br/) server. It is an independent project, developed by a fan of the server. The library is open source and can be found on my [GitHub](https://github.com/Henrique-Coder/mushmc-api) repository.