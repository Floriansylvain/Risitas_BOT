<h1 align="center">🤖 Risitas Discord Bot 🤖</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <img alt="Github Stars" src="https://img.shields.io/github/stars/Floriansylvain/Risitas_BOT?style=social">
</p>

>Risitas is a Discord bot that can connect your twitch chat to a discord channel in real time, make laugh your friends by playing the "Issou !" meme on command in a voce channel and even give you >your League Of Legend rank.

<br>

# 💻 Demo

<br>

![](chat_record1.gif)

<br>

# 📢 Commands

<br>

### **chat_set**
```
$chat_set {name_of_twitch_channel}
```
This command allows you to start the link between the channel where you use the command and a twitch chat.


### **chat_stop**
```
$chat_stop
```
This command allows you to stop the active chat in the channel.


### **issou**
```
$issou @{discord_member}
```
This command will make the bot shout the "Issou !" meme in a voice channel. By default it will do it in the voice channel where the user is connected but you can tag a user on your server to make the bot join their voice channel.


### **rank**
```
$rank {lol_username}
```
This command will display a message with the current League of Legend rank of the EUW account you ask for. Make surre to use quotes if there is spaces in the LoL username.

<br>

# ⚙ Configuration

>**To use this bot you'll have to create a private.py file and enter the different tokens to use the API's by assigning values to those variables**
```
External service tokens :
* token_bot
* token_riot
* token_twitch
* id_twitch

Socket related var :
* server
* port
* nickname
```

<br>

# 👨‍💻 Author

👤 **Florian Sylvain**

* Website: https://andhefallen.site/
* Github: [@Floriansylvain](https://github.com/Floriansylvain)

<br>

## ⭐️ Show your support

Give a ⭐️ if you liked this project!