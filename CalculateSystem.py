import math
import sys

from Position import positionClass
from collections import defaultdict


class CalculateSystemClass(object):
    def __init__(self, pos):
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.activeMissiles = 0
        self.enemyMissileData = defaultdict(list)
        self.counterMeasuresPositions = defaultdict(list)
        self.enemyMissilesIdAssignedToCounterMeasuresId = {} #idMissile, idCounterMeasureSystem
        self.enemyMissilesIdAndIntersectionPoint = {}
        self.velocityObtained = False
        self.enemyMissilesVelocity = 0
        self.enemyMissilesIdAndIntersectionInstant = {}

    def updateEnemyMissileData(self, enemyData):
        self.enemyMissileData = enemyData
        for enemyMissileId in list(self.enemyMissilesIdAssignedToCounterMeasuresId):
            if enemyMissileId not in self.enemyMissileData:
                self.deleteDeadEnemyMissile(enemyMissileId)

    def deleteDeadEnemyMissile(self, enemyId):
        self.enemyMissilesIdAssignedToCounterMeasuresId.pop(enemyId)

    def setCounterMeasuresPosition(self, counterMeasuresSystems):
        for counterMeasureSystem in counterMeasuresSystems:
            counterMeasurePosition = [counterMeasureSystem.position.positionX, counterMeasureSystem.position.positionY,
                                      counterMeasureSystem.position.positionZ]
            self.counterMeasuresPositions[counterMeasureSystem.id].append(counterMeasurePosition)

    def assignCounterMeasureSystemToEnemyMissile(self):
        for enemyMissileId in self.enemyMissileData:
            if enemyMissileId not in self.enemyMissilesIdAssignedToCounterMeasuresId:
                if len(self.enemyMissileData[enemyMissileId]) > 1:
                    missilePosition = [self.enemyMissileData[enemyMissileId][1][0], #X
                                       self.enemyMissileData[enemyMissileId][1][1], #Y
                                       self.enemyMissileData[enemyMissileId][1][2]] #Z
                    nearestCounterMeasureSystemId = self.getNearestCounterMeasureSystem(missilePosition)
                    self.enemyMissilesIdAssignedToCounterMeasuresId.update({enemyMissileId: nearestCounterMeasureSystemId})

    def getNearestCounterMeasureSystem(self, finalPosition):
        nearestSystemId = 0
        shortestDistance = sys.maxsize
        for counterMeasureSystemId in self.counterMeasuresPositions:
            xDist = finalPosition[0] - self.counterMeasuresPositions[counterMeasureSystemId][0][0]
            yDist = finalPosition[1] - self.counterMeasuresPositions[counterMeasureSystemId][0][1]
            dist = math.sqrt((xDist * xDist) + (yDist * yDist))
            if dist < shortestDistance:
                shortestDistance = dist
                nearestSystemId = counterMeasureSystemId
        return nearestSystemId

    def getMissileLastPosition(self, enemyMissileId):
        if len(self.enemyMissileData[enemyMissileId]) > 1:
            return self.enemyMissileData[enemyMissileId][1]

    def getEnemyMissileVelocity(self, enemyMissileId):
        if enemyMissileId in self.enemyMissilesIdAssignedToCounterMeasuresId:
            xDist = (self.enemyMissileData[enemyMissileId][1][0]-self.enemyMissileData[enemyMissileId][0][0])
            yDist = (self.enemyMissileData[enemyMissileId][1][1]-self.enemyMissileData[enemyMissileId][0][1])
            dist = math.sqrt((xDist * xDist) + (yDist * yDist))
            self.enemyMissilesVelocity = dist / ((self.enemyMissileData[enemyMissileId][1][3]/1000) - (self.enemyMissileData[enemyMissileId][0][3]/1000))

    def getIntersectionInstant(self):
        for enemyMissileId in self.enemyMissileData:
            if enemyMissileId in self.enemyMissilesIdAssignedToCounterMeasuresId:
                counterMeasurePosition = self.counterMeasuresPositions[self.enemyMissilesIdAssignedToCounterMeasuresId[enemyMissileId]][0]
                enemyMissilePosition = [self.enemyMissileData[enemyMissileId][1][0], #X
                                       self.enemyMissileData[enemyMissileId][1][1], #Y
                                       self.enemyMissileData[enemyMissileId][1][2]] #Z
                xDist = (enemyMissilePosition[0] - counterMeasurePosition[0])
                yDist = (enemyMissilePosition[1] - counterMeasurePosition[1])
                zDist = (enemyMissilePosition[2] - counterMeasurePosition[2])
                dist = math.sqrt((xDist * xDist) + (yDist * yDist) + (zDist * zDist))
                instant = dist / ((self.enemyMissilesVelocity * 3) - self.enemyMissilesVelocity) #la velocidad no esta bien
                self.enemyMissilesIdAndIntersectionInstant.update({enemyMissileId: instant})