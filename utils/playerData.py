import logging

from utils.singleton import Singleton
from utils.myData import MyData
from utils.fileHandler import FileHandler

@Singleton
class PlayerData:
    def __init__(self):
        self._fileHandler = FileHandler.instance()
        self._userData = {}
        self._historyData = {}
        self._planetData = {}
        self._userNames = []

        self.updateData()
    
    def updateData(self):
        logging.info("PlayerData: Updating data")
        #_updateUserData needs to be first
        self._updateUserData()
        self._updateHistoryData()
        self._updatePlanetData()

    def getUserData(self):
        return self._userData
    
    def getUserNames(self):
        return self._userNames

    def getHistoryData(self):
        return self._historyData

    def getPlanetData(self):
        return self._planetData

    def addPlanet(self, position, username):
        self._userData[username]["planets"].append(position)
        #save planet as file

    def _updateUserData(self):
        myData: MyData = self._fileHandler.getCurrentData()
        if(myData.valid):
            self._userData = myData.data
            self._setupUserNames()
        else:
            logging.warning("PlayerData: Invalid userData to update")
    
    def _setupUserNames(self):
        for user in self._userData:
            self._userNames.append(user)
    
    def _updateHistoryData(self):
        historyData: MyData = self._fileHandler.getHistoryData()
        
        if historyData.valid:
            self._historyData = historyData.data
        else:
            logging.warning("PlayerData: Invalid historyData to update")
        
        self._insertDiffDataToUser()
    
    def _insertDiffDataToUser(self):
        for user in self._historyData:
            userData = self._historyData[user][0]
            for element in userData:
                data = str(userData[element]).replace(".","")
                if data.isnumeric():
                    try:
                        currentData = str(self._historyData[user][-1][element]).replace(".","")
                        lastData = str(self._historyData[user][-2][element]).replace(".","")
                        self._userData[user]["diff_"+element] = "{:+g}".format(int(currentData) - int(lastData))
                    except:
                        #No history Data
                        if user in self._userData:
                            self._userData[user]["diff_"+ element] = "N/A"

    def _updatePlanetData(self):
        myData: MyData = self._fileHandler.getPlanetData()
        if(myData.valid):
            self._planetData = myData.data
        else:
            logging.warning("PlayerData: Invalid userData to update")

