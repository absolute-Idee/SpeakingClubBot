# ITMOSpeakingClubBot

Speaking Club bot

## requirement.txt
file with all dependencies 

## Dockerfile
image for code container

## docker-compose.yml
db container with postgres image and volume
bot container with image from dockerfile and command for bot start
for build use "docker-compose up" command

## bot.py
Entry point for the whole project. It uses TeleBotAPI. 

## database.py 
FIle for database class.
