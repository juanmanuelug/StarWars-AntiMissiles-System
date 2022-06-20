import sys
import unittest

import CounterMeasureSystem
import Position
from collections import defaultdict


class TestCounterMeasureSystem(unittest.TestCase):
    def setUp(self):
        self.counterMeasureSystemPosition = Position.positionClass(0, 0, 0)
        self.counterMeasureSystem = CounterMeasureSystem.CounterMeasureSystemClass(self.counterMeasureSystemPosition, 0)

        enemyMissiles = defaultdict(list)
        enemyMissiles[0] = [[1, 1, 1], [2, 2, 2]]
        enemyMissileIdCounterMeasureId = {0: 0}

        self.counterMeasuresMissiles = []
        self.counterMeasureSystem.updateEnemyMissileAssignedData(enemyMissiles, enemyMissileIdCounterMeasureId)

    def testCounterMeasureSystemLaunchACounterMeasureMissileWhenItHasAndAssignedEnemyMissile(self):
        self.counterMeasureSystem.launchCounterMeasure(self.counterMeasuresMissiles, sys.maxsize)

        self.assertGreater(len(self.counterMeasureSystem.counterMeasuresLaunchedAgainstMissile), 0)


if __name__ == '__main__':
    unittest.main()
