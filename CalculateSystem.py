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
        self.enemyMissilesIdAssignedToCounterMeasuresId = {}  # idMissile, idCounterMeasureSystem
        self.numberOfMissilesAssignedToCounterMeasuresId = defaultdict(int)

    def updateEnemyMissileData(self, enemyData):
        self.enemyMissileData = enemyData
        for enemyMissile in list(self.enemyMissilesIdAssignedToCounterMeasuresId):
            if enemyMissile not in self.enemyMissileData:
                self.deleteDeadEnemyMissile(enemyMissile)

    def deleteDeadEnemyMissile(self, enemyId):
        self.enemyMissilesIdAssignedToCounterMeasuresId.pop(enemyId)

    def clear(self):
        self.enemyMissileData.clear()
        self.counterMeasuresPositions.clear()
        self.enemyMissilesIdAssignedToCounterMeasuresId.clear()
        self.numberOfMissilesAssignedToCounterMeasuresId.clear()

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
                    self.enemyMissilesIdAssignedToCounterMeasuresId.update(
                        {enemyMissile: nearestCounterMeasureSystemId})
                    self.numberOfMissilesAssignedToCounterMeasuresId[nearestCounterMeasureSystemId] = \
                        self.numberOfMissilesAssignedToCounterMeasuresId[nearestCounterMeasureSystemId] + 1

    def getNearestCounterMeasureSystem(self, finalPosition):
        nearestSystemId = 0
        assignedMissiles = self.numberOfMissilesAssignedToCounterMeasuresId[0]
        xDist = finalPosition[0] - self.counterMeasuresPositions[0][0][0]
        yDist = finalPosition[1] - self.counterMeasuresPositions[0][0][1]
        shortestDistance = math.sqrt((xDist * xDist) + (yDist * yDist))
        i = 1
        while i < len(self.counterMeasuresPositions):
            xDist = finalPosition[0] - self.counterMeasuresPositions[i][0][0]
            yDist = finalPosition[1] - self.counterMeasuresPositions[i][0][1]
            dist = math.sqrt((xDist * xDist) + (yDist * yDist))
            if self.numberOfMissilesAssignedToCounterMeasuresId[i] < assignedMissiles - 2:
                shortestDistance = dist
                nearestSystemId = i
                assignedMissiles = self.numberOfMissilesAssignedToCounterMeasuresId[i]
            elif self.numberOfMissilesAssignedToCounterMeasuresId[i] == assignedMissiles:
                if dist < shortestDistance:
                    shortestDistance = dist
                    nearestSystemId = i
                    assignedMissiles = self.numberOfMissilesAssignedToCounterMeasuresId[i]
            elif assignedMissiles > self.numberOfMissilesAssignedToCounterMeasuresId[i] >= assignedMissiles - 2:
                if dist < shortestDistance:
                    shortestDistance = dist
                    nearestSystemId = i
                    assignedMissiles = self.numberOfMissilesAssignedToCounterMeasuresId[i]

            i += 1
        return nearestSystemId
