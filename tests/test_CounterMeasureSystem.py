import sys
import unittest

import CounterMeasureSystem
import Position
from collections import defaultdict


class TestCounterMeasureSystem(unittest.TestCase):
    def setUp(self):
        self.counterMeasureSystemPosition = Position.positionClass(0, 0, 0)
        self.counterMeasureSystem = CounterMeasureSystem.CounterMeasureSystemClass(self.counterMeasureSystemPosition, 0)

        self.enemyMissiles = defaultdict(list)
        self.enemyMissiles[0] = [[1, 1, 1], [2, 2, 2]]
        self.enemyMissileIdCounterMeasureId = {0: 0}

        self.counterMeasuresMissiles = []

    def testCounterMeasureSystemUpdateData(self):
        self.counterMeasureSystem.updateEnemyMissileAssignedData(self.enemyMissiles, self.enemyMissileIdCounterMeasureId)

        self.assertGreater(len(self.counterMeasureSystem.enemyMissilesAssigned), 0)

    def testCounterMeasureSystemLaunchACounterMeasureMissileWhenItHasAndAssignedEnemyMissile(self):
        self.counterMeasureSystem.updateEnemyMissileAssignedData(self.enemyMissiles, self.enemyMissileIdCounterMeasureId)
        self.counterMeasureSystem.launchCounterMeasure(self.counterMeasuresMissiles, sys.maxsize)

        self.assertGreater(len(self.counterMeasureSystem.enemyMissileIdAssignedToCounterMeasureMissileId), 0)

    def testCounterMeasureSystemDeleteData(self):
        self.counterMeasureSystem.updateEnemyMissileAssignedData(self.enemyMissiles, self.enemyMissileIdCounterMeasureId)
        self.enemyMissiles.clear()
        self.enemyMissileIdCounterMeasureId.clear()
        self.counterMeasureSystem.updateEnemyMissileAssignedData(self.enemyMissiles, self.enemyMissileIdCounterMeasureId)

        self.assertEqual(len(self.counterMeasureSystem.enemyMissilesAssigned), 0)


if __name__ == '__main__':
    unittest.main()
