import random
import unittest

import EnemyMissile
import Position
import strategicLocations
import main


class TestStrategicLocations(unittest.TestCase):
    def setUp(self):
        self.position = Position.positionClass(0, 0, 0)
        self.strategicLocation = strategicLocations.strategicLocationsClass(0, self.position)
        self.strategicLocations = [self.strategicLocation]
        self.enemyMissile = EnemyMissile.EnemyMissileClass(Position.positionClass(1.1, 1.1, 1.1),
                                                           self.strategicLocation.position, 0,
                                                           self.strategicLocation.id)

    def testStrategicLocationStatusChangeAfterGetImpactedByEnemyMissile(self):
        self.assertEqual(5, self.strategicLocation.lifes)

        main.cityHit(self.enemyMissile, self.strategicLocations)

        self.assertLess(self.strategicLocation.lifes, 5)

    def testStrategicLocationIsDestroyedWhenItHasNoLifesLeft(self):
        self.strategicLocation.lifes = 1

        main.cityHit(self.enemyMissile, self.strategicLocations)

        self.assertTrue(self.strategicLocation.getCityStatus())


if __name__ == '__main__':
    unittest.main()
