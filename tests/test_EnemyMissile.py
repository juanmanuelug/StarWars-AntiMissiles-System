import random

import EnemyMissile
import strategicLocations
import Position
import unittest


class TestEnemyMissile(unittest.TestCase):
    def setUp(self):
        self.objectives = []
        self.objectivesId = []
        for i in range(5):
            position = Position.positionClass(random.randint(0, 2), random.randint(0, 2), random.randint(0, 2))
            objective = strategicLocations.strategicLocationsClass(i, position)
            self.objectives.append(objective)
            self.objectivesId.append(objective.id)

        x = random.randint(0, 4)

        self.enemyMissile = EnemyMissile.EnemyMissileClass(Position.positionClass(1.1, 1.1, 1.1),
                                                           self.objectives[x].position, 0,
                                                           self.objectives[x].id)

    def testEnemyMissileObjectiveExist(self):
        self.assertIn(self.enemyMissile.objectiveId, self.objectivesId)

    def testEnemyMissileStatusChangeAfterGetImpacted(self):
        self.assertFalse(self.enemyMissile.intercepted)

        self.enemyMissile.hasBeenIntercepted()

        self.assertTrue(self.enemyMissile.intercepted)

    def testEnemyMissileStatusChangeAfterReachObjective(self):
        self.assertFalse(self.enemyMissile.objectiveImpacted)

        self.enemyMissile.goToObjective()

        self.assertTrue(self.enemyMissile.objectiveImpacted)


if __name__ == '__main__':
    unittest.main()
