import re
import json
import discord.utils

roleList = {
    3000: "All", # All
    10000: "10k",
    25000: "25k",
    50000: "50k",
    100000: "100k"
}

def strip_msg(message):
    try:
        return json.loads(re.sub(r'\d+\{', '{', message))
    except:
        return json.loads(re.sub(r'\d+\[', '[', message))


def calculate_role_pings(guild, number):
    role_mentions = ""

    for amount in roleList:
        if number >= amount:
            role = discord.utils.get(guild.roles, name=roleList[amount])
            role_mentions += f"{role.mention} "


    return role_mentions