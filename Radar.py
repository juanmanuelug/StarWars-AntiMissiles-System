from Position import positionClass
from collections import defaultdict


class RadarClass(object):

    def __init__(self, pos, widthRange, heightRange):
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.radarWidthRange = [widthRange[0], widthRange[1]]
        self.radarHeightRange = [heightRange[0], heightRange[1]]
        self.missilesDetected = 0
        self.enemyMissileFistLastPosition = defaultdict(list)

    def detectMissiles(self, enemyMissiles):
        for missile in enemyMissiles:
            if self.radarWidthRange[0] < missile.position.positionX < self.radarWidthRange[1] \
                    and self.radarHeightRange[0] < missile.position.positionY < self.radarHeightRange[1]:
                enemyMissilePositionAndInstant = [missile.position.positionX, missile.position.positionY,
                                        missile.position.positionZ]
                if len(self.enemyMissileFistLastPosition[missile.id]) == 2:
                    self.enemyMissileFistLastPosition[missile.id].pop()
                    self.enemyMissileFistLastPosition[missile.id].append(enemyMissilePositionAndInstant)
                else:
                    self.enemyMissileFistLastPosition[missile.id].append(enemyMissilePositionAndInstant)
        self.missilesDetected = len(self.enemyMissileFistLastPosition)

    def deleteDeadEnemyMissile(self, enemyId):
        self.enemyMissileFistLastPosition.pop(enemyId)
