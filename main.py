import asyncio
import json
import time
import threading
import websockets
import utils
import discord

rainAmount = 0
contestants = 0

client = discord.Client()

token = "<discord_bot_token>"
guildId = <guild_id>
channelId = <channel_id>

async def handle_msg(websocket):
    async for message in websocket:
        msg = utils.strip_msg(message)

        print(message)

        # Ping message #
        if message == "2":
            await websocket.send("3")

        elif type(msg) is list and msg[0] == "events:rain:updatePotVariables":
            rainAmount = msg[1]["newPrize"]
            contestants = msg[1]["newJoinedPlayersCount"]
        
        elif type(msg) is list and msg[0] == "events:rain:setState":
            if msg[1]["newState"] == "ENDING":
                # Send message to discord
                guild = client.get_guild(guildId)
                channel = client.get_channel(channelId)

                embed = discord.Embed()
                embed.title = "RBLXWILD - Tip rain ending soon!"
                embed.description = f"Tip rain ending in 2 minutes with {rainAmount}R$ prize pool!"
                embed.url = "https://rblxwild.com"
                embed.color = 0x008AD8 #0x00ff00
                embed.set_footer(text="betterNotifier")

                await channel.send(f"||{utils.calculate_role_pings(guild, rainAmount)}||", embed=embed)

            elif msg[1]["newState"] == "ENDED":
                channel = client.get_channel(channelId)

                embed = discord.Embed()
                embed.title = "RBLXWILD - Tip rain ended!"
                embed.description = f"Tip rain ended with a prize pool of {rainAmount}R$ with {contestants} contestants!"
                embed.url = "https://rblxwild.com"
                embed.color = 0x00ff00
                embed.set_footer(text="betterNotifier")

                await channel.send(embed=embed)

                rainAmount = 0
                contestants = 0

async def async_main(uri):
    async for websocket in websockets.connect(uri):
        try:
            await websocket.send("40")
            time.sleep(3)
            await websocket.send("42"+json.dumps([
                "authentication",
                {
                    "authToken": None,
                    "clientTime": int(time.time())
                }
            ]))

            print("Running now")
            await handle_msg(websocket)
        except websockets.ConnectionClosed:
            continue

    
@client.event
async def on_ready():
    print("Discord bot logged in")

    await async_main("wss://rblxwild.com/socket.io/?EIO=4&transport=websocket")




# Start bot #
client.run(token)
