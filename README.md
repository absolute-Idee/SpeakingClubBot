# ITMOSpeakingClubBot

Speaking Club bot for filtering messages from channel depending on chosen language.
Just add bot to your channel and it will forward to you chosen messages.
https://t.me/ITMOSpeakingClubBot

![image](https://user-images.githubusercontent.com/67152968/189161066-4c641185-a51c-47d3-bd7b-176e314ff714.png)
![image](https://user-images.githubusercontent.com/67152968/189162237-feb7be38-08f9-471d-b6da-c0a62ea1818b.png)
![image](https://user-images.githubusercontent.com/67152968/189162508-09371919-f0e8-4b19-bc0e-9b4dada3c858.png)



## requirement.txt
file with all dependencies 

## Dockerfile
image for code container

## docker-compose.yml
db container with postgres image and volume

bot container with image from dockerfile and command for bot start

## bot.py
Entry point for the whole project. It uses TeleBotAPI. 

## database.py 
FIle for database class.
