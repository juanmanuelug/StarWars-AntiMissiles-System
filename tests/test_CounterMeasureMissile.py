import unittest
import CounterMeasuresMissile
import Position
from collections import defaultdict

class TestCounterMeasureMissile(unittest.TestCase):
    def setUp(self):
        position = Position.positionClass(0, 0, 0)
        self.objPosition = [5, 5, 5]
        self.enemyMissiles = defaultdict(list)
        self.enemyMissiles[0] = [2, 2, 2]
        self.counterMeasureMissile = CounterMeasuresMissile.CounterMeasuresMissileClass(position, 0, 1, self.objPosition, 0)

    def testCounterMeasureMissileInterceptObjective(self):
        self.counterMeasureMissile.goToObjective()

        self.assertTrue(self.counterMeasureMissile.enemyMissileIntercepted)

    def testCounterMeasureMissileHasCorrectOrientation(self):
        expectedOrientation = {"x": 1, "y": 1}
        orientation = self.counterMeasureMissile.getObjectiveDirection(self.counterMeasureMissile.position, self.counterMeasureMissile.objectivePosition)

        self.assertEqual(expectedOrientation["x"], orientation["x"])
        self.assertEqual(expectedOrientation["y"], orientation["y"])

    def testCounterMeasureMissileUpdateData(self):
        self.counterMeasureMissile.updateObjectivePosition(self.enemyMissiles)

        self.assertNotEqual(self.objPosition[0], self.counterMeasureMissile.objectivePosition.positionX)
        self.assertNotEqual(self.objPosition[1], self.counterMeasureMissile.objectivePosition.positionY)
        self.assertNotEqual(self.objPosition[2], self.counterMeasureMissile.objectivePosition.positionZ)


if __name__ == '__main__':
    unittest.main()
