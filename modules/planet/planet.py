import logging
import re
from discord.ext import commands

from utils.playerData import PlayerData, DATATYPE

class Planet(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._PlayerData: PlayerData = PlayerData.instance()
        self._userNames: list = []

        self._PlayerData.subscribe(DATATYPE.userNames, self.updateUserNames)

        self.refresh()
    
    @commands.command(usage="<g>:<s>:<p> <username>",
                      brief="Speichert einen neuen Planeten",
                      help="Speichert den Planet an position <g>:<s>:<p> zu dem spieler <username> ab")
    async def planet(self, ctx: commands.context, position: str, username: str):
        position = position.lower()
        username = username.lower()

        if not username in self._userNames:
            await ctx.send('Spieler nicht gefunden')
            return
        try:
            result = re.search("^(\d{1,3}):(\d{1,3}):(\d{1,3})$",position)
            position = "{}:{}:{}".format(result.group(1),result.group(2),result.group(3))
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !planet 1:1:1 Name')
            return
        
        self._addPlanet(position, username)

        await ctx.send("TBD")

    @planet.error
    async def planet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !planet 1:1:1 sc0t')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def refresh(self):
        logging.info("Planet: Refreshing data")
        self._userNames = self._PlayerData.getUserNames()
    
    def updateUserNames(self, userNames: dict):
        logging.info("Planet: recieved subscribed UserNames")
        self._userNames = userNames

    def _addPlanet(self, position, user):
        self._PlayerData.addPlanet(position, user)

def setup(bot: commands.Bot):
    bot.add_cog(Planet(bot))
