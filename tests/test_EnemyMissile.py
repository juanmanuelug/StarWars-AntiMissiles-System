import random

import EnemyMissile
import strategicLocations
import Position
import unittest


class TestEnemyMissile(unittest.TestCase):
    def setUp(self):
        self.objectives = []
        self.objectivesId = []
        position = Position.positionClass(0, 0, 0)
        self.objective = strategicLocations.strategicLocationsClass(0, position)

        self.enemyMissile = EnemyMissile.EnemyMissileClass(Position.positionClass(1.1, 1.1, 1.1),
                                                           self.objective.position, 0,
                                                           self.objective.id)

    def testEnemyMissileObjectiveExist(self):
        self.assertEqual(self.enemyMissile.objectiveId, self.objective.id)

    def testEnemyMissileStatusChangeAfterGetIntercepted(self):
        self.assertFalse(self.enemyMissile.intercepted)

        self.enemyMissile.hasBeenIntercepted()

        self.assertTrue(self.enemyMissile.intercepted)

    def testEnemyMissileStatusChangeAfterReachObjective(self):
        self.assertFalse(self.enemyMissile.objectiveImpacted)

        self.enemyMissile.goToObjective()

        self.assertTrue(self.enemyMissile.objectiveImpacted)

    def testEnemyMissileHasCorrectOrientation(self):
        expectedOrientation = {"x": -1, "y": -1}
        orientation = self.enemyMissile.getObjectiveDirection(self.enemyMissile.position, self.objective.position)

        self.assertEqual(expectedOrientation["x"], orientation["x"])
        self.assertEqual(expectedOrientation["y"], orientation["y"])


if __name__ == '__main__':
    unittest.main()
