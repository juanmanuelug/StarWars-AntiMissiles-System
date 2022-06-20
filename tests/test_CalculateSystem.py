import unittest

import CalculateSystem
import CounterMeasureSystem
import EnemyMissile
import Position


class TestCalculateSystem(unittest.TestCase):
    def setUp(self):
        self.finalPosition = [0, 0, 0]
        self.calculateSystemPosition = Position.positionClass(1, 1, 1)
        self.nearestPosition = Position.positionClass(0, 0, 0)
        self.farestPosition = Position.positionClass(100, 100, 100)

        self.calculateSystem = CalculateSystem.CalculateSystemClass(self.calculateSystemPosition)
        self.nearestCounterMeasureSystem = CounterMeasureSystem.CounterMeasureSystemClass(self.nearestPosition, 1)
        self.farestCounterMeasureSystem = CounterMeasureSystem.CounterMeasureSystemClass(self.farestPosition, 2)

        self.counterMeasureSystems = [self.nearestCounterMeasureSystem, self.farestCounterMeasureSystem]
        self.calculateSystem.setCounterMeasuresPosition(self.counterMeasureSystems)

    def testCalculateSystemAssingTheNearestCounterMeasureSystemToTheEnemyMissile(self):
        idNearestCounterMeasure = self.calculateSystem.getNearestCounterMeasureSystem(self.finalPosition)

        self.assertEqual(idNearestCounterMeasure, 1)


if __name__ == '__main__':
    unittest.main()
