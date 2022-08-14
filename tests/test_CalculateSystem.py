import unittest

import CalculateSystem
import CounterMeasureSystem
import EnemyMissile
import Position
from collections import defaultdict


class TestCalculateSystem(unittest.TestCase):
    def setUp(self):
        self.calculateSystem = CalculateSystem.CalculateSystemClass(Position.positionClass(1, 1, 1))
        self.CounterMeasureSystem = CounterMeasureSystem.CounterMeasureSystemClass(
            Position.positionClass(100, 100, 100), 0)

        self.counterMeasureSystems = [self.CounterMeasureSystem]

        self.enemyMissile = EnemyMissile.EnemyMissileClass(Position.positionClass(1.1, 1.1, 1.1),
                                                           Position.positionClass(0.1, 0.1, 0.1), 0, 0)

        self.enemyMissiles = [self.enemyMissile]
        self.dataList = defaultdict(list)
        self.dataList[self.enemyMissile.id].append(
            [self.enemyMissile.position.positionX, self.enemyMissile.position.positionY,
             self.enemyMissile.position.positionZ])
        self.dataList[self.enemyMissile.id].append([100, 100, 100])

    def testCalculateSystemUpdateData(self):
        self.calculateSystem.updateEnemyMissileData(self.dataList)

        self.assertEqual(len(self.calculateSystem.enemyMissileData), len(self.dataList))

    def testCalculateSystemSetCounterMeasurePosition(self):
        self.calculateSystem.setCounterMeasuresPosition(self.counterMeasureSystems)

        self.assertEqual(len(self.calculateSystem.counterMeasuresPositions), len(self.counterMeasureSystems))

    def testCalculateSystemDeleteData(self):
        self.calculateSystem.setCounterMeasuresPosition(self.counterMeasureSystems)
        self.calculateSystem.updateEnemyMissileData(self.dataList)
        self.calculateSystem.assignCounterMeasureSystemToEnemyMissile()
        self.calculateSystem.deleteDeadEnemyMissile(self.enemyMissile.id)

        self.assertEqual(len(self.calculateSystem.enemyMissilesIdAssignedToCounterMeasuresId), 0)

    def testCalculateSystemAssignMissileToCounterMeasure(self):
        self.calculateSystem.setCounterMeasuresPosition(self.counterMeasureSystems)
        self.calculateSystem.updateEnemyMissileData(self.dataList)
        self.calculateSystem.assignCounterMeasureSystemToEnemyMissile()

        self.assertEqual(len(self.calculateSystem.enemyMissilesIdAssignedToCounterMeasuresId), 1)


if __name__ == '__main__':
    unittest.main()
