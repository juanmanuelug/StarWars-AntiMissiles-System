import unittest

import EnemyMissile
import Position
import Radar


class TestRadar(unittest.TestCase):
    def setUp(self):
        self.position = Position.positionClass(0, 0, 0)
        self.enemyMissile = EnemyMissile.EnemyMissileClass(Position.positionClass(1.1, 1.1, 1.1),
                                                           Position.positionClass(0.1, 0.1, 0.1), 0, 0)
        self.enemyMissileOutOfRange = EnemyMissile.EnemyMissileClass(Position.positionClass(101, 101, 101),
                                                                     Position.positionClass(0.1, 0.1, 0.1), 0, 0)
        self.radar = Radar.RadarClass(self.position, [-100, 100], [-100, 100])
        self.enemyMissiles = [self.enemyMissile, self.enemyMissileOutOfRange]

    def testRadarDetectEnemyMissileThatIsInItsRange(self):
        self.assertEqual(self.radar.missilesDetected, 0)

        self.radar.detectMissiles(self.enemyMissiles)

        self.assertEqual(self.radar.missilesDetected, 1)

    def testRadarDeleteEnemyMissile(self):
        self.radar.detectMissiles(self.enemyMissiles)
        self.radar.deleteDeadEnemyMissile(self.enemyMissile.id)

        self.assertEqual(self.radar.missilesDetected, 0)

if __name__ == '__main__':
    unittest.main()
