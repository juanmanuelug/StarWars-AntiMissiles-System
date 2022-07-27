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

    def updateEnemyMissileData(self, enemyData):
        self.enemyMissileData = enemyData
        for enemyMissile in list(self.enemyMissilesIdAssignedToCounterMeasuresId):
            if enemyMissile not in self.enemyMissileData:
                self.deleteDeadEnemyMissile(enemyMissile)

    def deleteDeadEnemyMissile(self, enemyId):
        self.enemyMissilesIdAssignedToCounterMeasuresId.pop(enemyId)

    def setCounterMeasuresPosition(self, counterMeasuresSystems):
        for counterMeasureSystem in counterMeasuresSystems:
            counterMeasurePosition = [counterMeasureSystem.position.positionX, counterMeasureSystem.position.positionY,
                                      counterMeasureSystem.position.positionZ]
            self.counterMeasuresPositions[counterMeasureSystem.id].append(counterMeasurePosition)

    def assignCounterMeasureSystemToEnemyMissile(self):
        for enemyMissile in self.enemyMissileData:
            if enemyMissile not in self.enemyMissilesIdAssignedToCounterMeasuresId:
                if len(self.enemyMissileData[enemyMissile]) > 1:
                    missilePosition = self.enemyMissileData[enemyMissile][0]
                    nearestCounterMeasureSystemId = self.getNearestCounterMeasureSystem(missilePosition)
                    self.enemyMissilesIdAssignedToCounterMeasuresId.update({enemyMissile: nearestCounterMeasureSystemId})

    def getNearestCounterMeasureSystem(self, finalPosition):
        nearestSystemId = 0
        shortestDistance = sys.maxsize
        for counterMeasureSystem in self.counterMeasuresPositions:
            xDist = finalPosition[0] - self.counterMeasuresPositions[counterMeasureSystem][0][0]
            yDist = finalPosition[1] - self.counterMeasuresPositions[counterMeasureSystem][0][1]
            dist = math.sqrt((xDist * xDist) + (yDist * yDist))
            if dist < shortestDistance:
                shortestDistance = dist
                nearestSystemId = counterMeasureSystem
        return nearestSystemId
