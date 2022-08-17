import math

from Position import positionClass
from collections import defaultdict
from CounterMeasuresMissile import CounterMeasuresMissileClass


class CounterMeasureSystemClass(object):
    def __init__(self, pos, id):
        self.id = id
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.enemyMissilesAssigned = defaultdict(list)
        self.enemyMissileIdAssignedToCounterMeasureMissileId = {} #idMissile, idCounterMeasure
        self.idCounterMeasuresMissiles = 0
        self.lastLaunchTime = 0

    def updateEnemyMissileAssignedData(self, enemyMissileData, enemyMissileAssignedList):
        self.deleteDeadEnemyMissiles(enemyMissileData)
        enemyMissiles = defaultdict(list)
        for enemyId in enemyMissileAssignedList:
            if self.id == enemyMissileAssignedList[enemyId]:
                enemyMissiles[enemyId] = enemyMissileData[enemyId][1]
        self.enemyMissilesAssigned = enemyMissiles

    def deleteDeadEnemyMissiles(self, enemyMissileData):
        for enemyMissile in list(self.enemyMissileIdAssignedToCounterMeasureMissileId):
            if enemyMissile not in list(enemyMissileData):
                self.enemyMissileIdAssignedToCounterMeasureMissileId.pop(enemyMissile)

    def launchCounterMeasure(self, counterMeasuresMissiles, actualTime):
        if len(self.enemyMissilesAssigned) > 0 and len(self.enemyMissilesAssigned) != len(self.enemyMissileIdAssignedToCounterMeasureMissileId):
            self.sortEnemyMissilesByDistance()
            for enemyMissile in list(self.enemyMissilesAssigned):
                if enemyMissile not in self.enemyMissileIdAssignedToCounterMeasureMissileId:
                    if (actualTime - self.lastLaunchTime) / 1000 > 1:
                        counterMeasuresMissile = CounterMeasuresMissileClass(self.position, self.idCounterMeasuresMissiles,
                                                                             self.id,
                                                                             self.enemyMissilesAssigned[enemyMissile],
                                                                             enemyMissile)
                        counterMeasuresMissiles.append(counterMeasuresMissile)
                        self.idCounterMeasuresMissiles += 1
                        self.enemyMissileIdAssignedToCounterMeasureMissileId.update({enemyMissile: self.idCounterMeasuresMissiles})
                        self.lastLaunchTime = actualTime
                        self.enemyMissilesAssigned.pop(enemyMissile)

    def sortEnemyMissilesByDistance(self):
        enemyIdArray = []
        enemyPosition = []
        enemyDict = defaultdict(list)
        for enemyId in list(self.enemyMissilesAssigned):
            enemyIdArray.append(enemyId)
            enemyPosition.append(self.enemyMissilesAssigned[enemyId])

        i = 0
        j = i + 1
        while i < len(self.enemyMissilesAssigned):
            xDist = self.position.positionX - enemyPosition[i][0]
            yDist = self.position.positionY - enemyPosition[i][1]
            zDist = self.position.positionZ - enemyPosition[i][2]
            dist = math.sqrt((xDist * xDist) + (yDist * yDist) + (zDist * zDist))
            while j < len(self.enemyMissilesAssigned):
                xDistNew = self.position.positionX - enemyPosition[j][0]
                yDistNew = self.position.positionY - enemyPosition[j][1]
                zDistNew = self.position.positionZ - enemyPosition[j][2]
                distNew = math.sqrt((xDistNew * xDistNew) + (yDistNew * yDistNew) + (zDistNew * zDistNew))
                if distNew < dist:
                    auxPos = enemyPosition[j]
                    enemyPosition[j] = enemyPosition[i]
                    enemyPosition[i] = auxPos
                    auxId = enemyIdArray[j]
                    enemyIdArray[j] = enemyIdArray[i]
                    enemyIdArray[i] = auxId
                    dist = distNew
                j += 1
            i += 1

        i = 0
        while i < len(enemyIdArray):
            enemyDict[enemyIdArray[i]] = enemyPosition[i]
            i += 1
        self.enemyMissilesAssigned = enemyDict

