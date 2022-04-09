from discord.ext import commands
from dotenv import load_dotenv
import os
import logging


from modules import *

def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logging.info("Programm started")

    client = commands.Bot(command_prefix="!", case_insensitive=True)
    
    #load stast at first containing userData
    client.load_extension(f"modules.stats.stats")
    for name in os.listdir("modules"):
        if name == "stats":
            continue
        if os.path.exists(os.path.join("modules", name)):
            client.load_extension(f"modules.{name}.{name}")
            logging.info(f"Bot: Module {name} loaded")

    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
    main()