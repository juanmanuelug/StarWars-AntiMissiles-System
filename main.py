import math

import pygame
import ctypes
import multiprocessing as multiprocess
import random

from strategicLocations import strategicLocationsClass
from EnemyMissile import EnemyMissileClass
from Position import positionClass
from Radar import RadarClass
from Interface import InterfaceClass

pygame.init()

screenResolution = ctypes.windll.user32
WINDOWSWIDTH = screenResolution.GetSystemMetrics(0) - 100
WINDOWSHEIGHT = screenResolution.GetSystemMetrics(1) - 100

MAPWIDTHLIMIT = int(WINDOWSWIDTH * 0.65)

SMALLESTWINDOWSSIZE = MAPWIDTHLIMIT if MAPWIDTHLIMIT < WINDOWSHEIGHT else WINDOWSHEIGHT

FOURTHCIRCLERADAR = int(SMALLESTWINDOWSSIZE * 0.4)

CITYSPAWNINFERIORLIMITWIDTH = int((MAPWIDTHLIMIT / 2) - FOURTHCIRCLERADAR)
CITYSPAWNSUPERIORLIMITWIDTH = int(FOURTHCIRCLERADAR + (MAPWIDTHLIMIT / 2))

CITYSPAWNINFERIORLIMITHEIGHT = int((WINDOWSHEIGHT / 2) - FOURTHCIRCLERADAR)
CITYSPAWNSUPERIORLIMITHEIGHT = int((WINDOWSHEIGHT / 2) + FOURTHCIRCLERADAR)

MISSILESSPAWNINFERIORLIMIT = 0
MISSILESSPAWNSUPERIORLIMITWIDTH = int(MAPWIDTHLIMIT)
MISSILESSPAWNSUPERIORLIMITHEIGHT = int(WINDOWSHEIGHT)

DEGRESSPERGRAME = 1

clock = pygame.time.Clock()


def spawnEnemyMissiles(enemies, strategicLocations):
    global missileId
    if len(enemies) < 10:
        InferiorX = random.randint(MISSILESSPAWNINFERIORLIMIT, CITYSPAWNINFERIORLIMITWIDTH)
        SuperiorX = random.randint(CITYSPAWNSUPERIORLIMITWIDTH, MISSILESSPAWNSUPERIORLIMITWIDTH)

        InferiorY = random.randint(MISSILESSPAWNINFERIORLIMIT, CITYSPAWNINFERIORLIMITHEIGHT)
        SuperiorY = random.randint(CITYSPAWNSUPERIORLIMITHEIGHT, MISSILESSPAWNSUPERIORLIMITHEIGHT)

        x = InferiorX if InferiorX % 2 == 0 else SuperiorX
        y = InferiorY if SuperiorY % 2 == 0 else SuperiorY
        z = random.randint(100, 200)
        positionRandom = positionClass(x, y, z)
        x = random.randint(0, len(strategicLocations) - 1)
        ObjpositionRandom = positionClass(strategicLocations[x].position.positionX,
                                          strategicLocations[x].position.positionY,
                                          strategicLocations[x].position.positionZ)
        enemy = EnemyMissileClass(positionRandom, ObjpositionRandom, missileId)
        missileId += 1
        enemies.append(enemy)


def spawnStrategicLocations(strategicLocations):
    x = random.randint(CITYSPAWNINFERIORLIMITWIDTH, CITYSPAWNSUPERIORLIMITWIDTH)
    y = random.randint(CITYSPAWNINFERIORLIMITHEIGHT, CITYSPAWNSUPERIORLIMITHEIGHT)
    z = random.randint(0, 50)
    strategicLocationPosition = positionClass(x, y, z)
    city = strategicLocationsClass(strategicLocationPosition)
    strategicLocations.append(city)

if __name__ == "__main__":
    radarPosition = positionClass(MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2, 0)
    radarWidthRange = [0, MAPWIDTHLIMIT]
    radarHeightRange = [0, WINDOWSHEIGHT]

    radar = RadarClass(radarPosition, radarWidthRange, radarHeightRange)
    enemies = []
    strategicLocations = []
    interface = InterfaceClass(WINDOWSWIDTH, WINDOWSHEIGHT)

    for _ in range(5):
        spawnStrategicLocations(strategicLocations)

    run = True

    contActiveMissiles = 0
    contMissileImpact = 0
    contMissilesDestroyed = 0
    contActiveCities = 0
    CitiesDestroyed = 0
    angle = 0
    missileId = 0

    pool = multiprocess.Pool(processes=4)

    while run:
        multiprocess.freeze_support()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pool.map_async(radar.detectMissiles(enemies), {})

        if len(strategicLocations) > 0:
            spawnEnemyMissiles(enemies, strategicLocations)

        for enemy in enemies:
            #print(f"id= {enemy.id}, x={enemy.position.positionX} | xobj={enemy.ObjectivePosition.positionX}, y={enemy.position.positionY} | xobj={enemy.ObjectivePosition.positionY} ")
            if enemy.getIntercepted():
                enemies.pop(enemies.index(enemy))
                contMissilesDestroyed += 1
            if enemy.getObjectiveImpacted():
                interface.CityHit(enemy, strategicLocations)
                enemies.pop(enemies.index(enemy))
                contMissileImpact += 1

            pool.map_async(enemy.goToObjective(), {})

        for city in strategicLocations:
            if city.getCityStatus():
                CitiesDestroyed += 1
                strategicLocations.pop(strategicLocations.index(city))

        contActiveMissiles = len(enemies)
        contActiveCities = len(strategicLocations)
        angle += DEGRESSPERGRAME

        interface.drawWindow(contActiveMissiles, contMissilesDestroyed, contActiveCities, contMissileImpact,CitiesDestroyed, enemies,
                   strategicLocations, angle)

        clock.tick(30)