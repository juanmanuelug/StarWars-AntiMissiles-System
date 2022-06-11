from Position import positionClass
from collections import defaultdict
from CounterMeasuresMissile import CounterMeasuresMissileClass


class CounterMeasureSystemClass(object):
    def __init__(self, pos, id):
        self.id = id
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.enemyMissilesAssigned = defaultdict(list)
        self.counterMeasuresLaunchedAgainstMissile = {} #idMissile, idCounterMeasure
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
        for enemyMissile in list(self.counterMeasuresLaunchedAgainstMissile):
            if enemyMissile not in enemyMissileData:
                self.counterMeasuresLaunchedAgainstMissile.pop(enemyMissile)
                self.enemyMissilesAssigned.pop(enemyMissile)

    def launchCounterMeasure(self, counterMeasuresMissiles, actualTime):
        if len(self.enemyMissilesAssigned) > 0:
            for enemyMissile in self.enemyMissilesAssigned:
                if enemyMissile not in self.counterMeasuresLaunchedAgainstMissile:
                    if (actualTime - self.lastLaunchTime) / 1000 > 1:
                        counterMeasuresMissile = CounterMeasuresMissileClass(self.position, self.idCounterMeasuresMissiles,
                                                                             self.id,
                                                                             self.enemyMissilesAssigned[enemyMissile],
                                                                             enemyMissile)
                        counterMeasuresMissiles.append(counterMeasuresMissile)
                        self.idCounterMeasuresMissiles += 1
                        self.counterMeasuresLaunchedAgainstMissile.update({enemyMissile: self.idCounterMeasuresMissiles})
                        self.lastLaunchTime = actualTime
