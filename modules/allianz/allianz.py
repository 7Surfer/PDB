import logging
from logging.config import DEFAULT_LOGGING_CONFIG_PORT
from discord.ext import commands
from numpy import number

from utils.fileHandler import FileHandler
from utils.myData import MyData

class Allianz(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot = bot
        self._fileHandler = FileHandler.instance()
        self._allianzData = {}
        self.updateData()
    
    @commands.command()
    async def allianz(self, ctx: commands.context, *,allianzName):
        """Zeigt die Top 10 Spieler der Allianz <allianzname> an"""
        allianzName = allianzName.lower()

        if not allianzName in self._allianzData:
            await ctx.send('Allianzname nicht gefunden')
            return

        await ctx.send(self._getAllianzString(allianzName))

    @allianz.error
    async def allianz_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Allianzname fehlt!\nBsp.: !allianz Allianz mit Poll')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def updateData(self):
        logging.info("Allianz: Updating data")
        self._setupAllianzData()
  
    def _getAllianzString(self, allianzName):
        returnMsg = f"```Top 10 von Allianz {allianzName}\n"
        returnMsg +="{:1} {:4} {:20} {:<10} {:10} \n\n".format("","","Name", "Punkte", "Flotte")

        for userData in self._allianzData[allianzName]:           
            arrow = "-" #equal
            try:
                diff = int(userData["diff_platz"])
            except:
                arrow = "" # no history data
            
            if diff > 0:
                arrow = "\u2193" #down
            elif diff < 0:
                arrow = "\u2191" #up
            
            returnMsg +="{:1} {:4} {:20} {:<10} {:10}\n".format(arrow, 
                                                                userData["platz"],
                                                                userData["username"],
                                                                userData["gesamt"],
                                                                userData["flotte"])
        return returnMsg + "```"

    def _setupAllianzData(self):
        #rework to save only usernames and not complete Data
        userData: dict = self._bot.get_cog('Stats').getUserData()

        fullAllianzData: dict = self._getAllAllianzMember(userData)
        self._allianzData: dict = self._getAllTopAllianzMembers(fullAllianzData)

    def _getAllAllianzMember(self, userdata: dict):
        fullAllianzData = {}
        for user in userdata:
            name: str = userdata[user]["allianz"].lower().strip()
            if name in fullAllianzData:
                fullAllianzData[name].append(userdata[user])
            else:
                fullAllianzData[name] = [userdata[user]]
        
        return fullAllianzData
    
    def _getAllTopAllianzMembers(self, fullAllianzData: dict):
        topAllianzUsers = {}
        for allianzName in fullAllianzData:
            allianzUsers: list = fullAllianzData[allianzName]
            
            #sort users by rank and keep only top 10
            topAllianzUsers[allianzName] = sorted(allianzUsers,key=lambda d: d['platz'])[:10]
        
        return topAllianzUsers

def setup(bot: commands.Bot):
    bot.add_cog(Allianz(bot))
