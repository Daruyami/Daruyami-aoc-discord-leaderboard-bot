# AoC bot by Daruyami - also known on Discord as Green#7964
import os
import json
import urllib.request
import discord
import time

#discord token
dtoken = ""
#session id from a cookie
sessid = ""
#url to the api page from your private leaderboards list
url = "https://adventofcode.com/2020/leaderboard/private/view/xxxxxx.json"
#have fun
callsign = ">aoc"

getTime = 0
output = "" #<-- yes i know that this is frickin awful
#gets the json and after some bs puts it into embed
def get():
    global getTime #<--frick this horribleness
    global output #<--and this
    #checking if 15 minutes from previous request has already passed
    #its important because we dont want to cause issues to the creator of AoC!!!!
    if(getTime != 0):
        if((time.time() - getTime) < 900):
            return output
    
    #getting the json of your leaderboards
    response = urllib.request.urlopen( urllib.request.Request(url, headers = { 'Cookie' : 'session='+sessid }) )
    #check if server is alive
    if(response.getcode() != 200):
        return "The site has died, please try again later"
    #checking if cookie hasnt expired, they tend to expire after around a month so putting a fresh one on the start of december should last until the end
    try:
        variables = json.loads(response.read())
    except ValueError as e:
        return "The Cookie has expired :("
    
    #some json magic to put it all into embed
    getTime = time.time()
    output = ""
    for x, user in variables["members"].items():
        output += str(user["name"]) + " has " + str(user["stars"]) + " stars\n"
    output += "\nStats from " + str(time.ctime(getTime))
    return output

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds)
    print(f'{client.user} has connected to Discord! Hiyah World!\n')

@client.event
async def on_message(message):
    if message.content == callsign:
        embedVar = discord.Embed(title="Displaying private leaderboard stats: ", description=get(), color=0x009900, url="https://adventofcode.com")
        await message.channel.send(embed=embedVar)


#link start!
client.run(dtoken)
#after this insanity...
#...i just might need some exorcism...
#...or at least mental therapy
