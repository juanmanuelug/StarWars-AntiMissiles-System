from Position import positionClass
from collections import defaultdict


class RadarClass(object):

    def __init__(self, pos, widthRange, heightRange):
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.radarWidthRange = [widthRange[0], widthRange[1]]
        self.radarHeightRange = [heightRange[0], heightRange[1]]
        self.missilesDetected = 0
        self.enemyMissileLastPosition = defaultdict(list)

    def detectMissiles(self, enemyMissiles):
        for missile in enemyMissiles:
            if self.radarWidthRange[0] < missile.position.positionX < self.radarWidthRange[1] \
                    and self.radarHeightRange[0] < missile.position.positionY < self.radarHeightRange[1]:
                enemyMissilePosition = [missile.position.positionX, missile.position.positionY,
                                        missile.position.positionZ]
                if len(self.enemyMissileLastPosition[missile.id]) == 2:
                    self.enemyMissileLastPosition[missile.id].pop()
                    self.enemyMissileLastPosition[missile.id].append(enemyMissilePosition)
                else:
                    self.enemyMissileLastPosition[missile.id].append(enemyMissilePosition)
        self.missilesDetected = len(self.enemyMissileLastPosition)

    def deleteDeadEnemyMissile(self, enemyId):
        if enemyId in self.enemyMissileLastPosition:
            self.enemyMissileLastPosition.pop(enemyId)
