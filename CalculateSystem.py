from Position import positionClass
from collections import defaultdict


class CalculateSystemClass(object):
    def __init__(self, pos):
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.activeMissiles = 0
        self.requestSendsToCounterMeasures = 0
        self.enemyMissileData = defaultdict(list)
