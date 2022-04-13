from enum import Enum
import logging
from pyclbr import Function

from utils.singleton import Singleton
from utils.myData import MyData
from utils.fileHandler import FileHandler


class DATATYPE(Enum):
    userData = 1
    historyData = 2
    allianzData = 3
    userNames = 4


@Singleton
class PlayerData:
    def __init__(self):
        self._fileHandler = FileHandler.instance()
        self._userData = {}
        self._historyData = {}
        self._planetData = {}
        self._allianzData = {}
        self._userNames = []
        self._subscriptions = {}

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

    def getAllianzData(self):
        return self._allianzData

    def getPlanetData(self):
        return self._planetData

    def addPlanet(self, position, username):
        #savePlanetData on currentClass
        self._planetData[username].append(position)
        self._userData[username]["planets"].append(position)

        #save planet as file
        self._fileHandler.setPlanetData(self._planetData)

        #Upadte all cogs who depend on planetData
        self._publish([DATATYPE.userData])

    def subscribe(self, dataType: DATATYPE, callback: Function ):
        if dataType in self._subscriptions:
            self._subscriptions[dataType].append(callback)
        else:
            self._subscriptions[dataType] = [callback]

    def _publish(self, datatypes: list):
        for datatype in datatypes:
            logging.info(f"PlayerData: Publish {datatype}")
            match datatype:
                case DATATYPE.userData:
                    for subscriber in self._subscriptions[datatype]:
                        print(subscriber)
                        subscriber(self._userData)
                case DATATYPE.historyData:
                    for subscriber in self._subscriptions[datatype]:
                        print(subscriber)
                        subscriber(self._historyData)
                case DATATYPE.allianzData:
                    for subscriber in self._subscriptions[datatype]:
                        print(subscriber)
                        subscriber(self._allianzData)
                case DATATYPE.userNames:
                    for subscriber in self._subscriptions[datatype]:
                        print(subscriber)
                        subscriber(self._userNames)

    def _updateUserData(self):
        myData: MyData = self._fileHandler.getCurrentData()
        if(myData.valid):
            self._userData = myData.data
            self._setupUserNames()
            self._setupAllianzData()
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
        
        self._insertPlanetDataToUsers()
    
    def _insertPlanetDataToUsers(self):
        for user in self._userData:
            if user in self._planetData:
                self._userData[user]["planets"] = self._planetData[user]
    
    def _setupAllianzData(self):
        fullAllianzData: dict = self._getAllAllianzMember(self._userData)
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
