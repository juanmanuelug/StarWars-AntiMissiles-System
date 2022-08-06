import pygame
import ctypes
import random
import threading

from strategicLocations import strategicLocationsClass
from EnemyMissile import EnemyMissileClass
from Position import positionClass
from Radar import RadarClass
from SimulationInterface import InterfaceClass
from CalculateSystem import CalculateSystemClass
from CounterMeasureSystem import CounterMeasureSystemClass

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

DEGRESSPERFRAME = 1

clock = pygame.time.Clock()


def cityHit(enemy, strategicLocations):
    for city in strategicLocations:
        if enemy.ObjectivePosition.positionX == city.position.positionX and enemy.ObjectivePosition.positionY == city.position.positionY:
            city.strategicLocationImpacted()


def spawnEnemyMissiles(enemies, strategicLocations, enemyMissileMaxNumber):
    global missileId
    for _ in range(enemyMissileMaxNumber):
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
        ObjIdRandom = strategicLocations[x].id
        enemy = EnemyMissileClass(positionRandom, ObjpositionRandom, missileId, ObjIdRandom)
        missileId += 1
        enemies.append(enemy)


def spawnStrategicLocations(strategicLocations):
    global cityId
    x = random.randint(CITYSPAWNINFERIORLIMITWIDTH, CITYSPAWNSUPERIORLIMITWIDTH)
    y = random.randint(CITYSPAWNINFERIORLIMITHEIGHT, CITYSPAWNSUPERIORLIMITHEIGHT)
    z = random.randint(0, 50)
    strategicLocationPosition = positionClass(x, y, z)
    city = strategicLocationsClass(cityId, strategicLocationPosition)
    cityId += 1
    strategicLocations.append(city)


def spawnCounterMeasuresSystems(counterMeasuresSystems):
    x = random.randint(CITYSPAWNINFERIORLIMITWIDTH, CITYSPAWNSUPERIORLIMITWIDTH)
    y = random.randint(CITYSPAWNINFERIORLIMITHEIGHT, CITYSPAWNSUPERIORLIMITHEIGHT)
    z = random.randint(0, 50)
    counterMeasuresSystemPosition = positionClass(x, y, z)
    counterMeasureSystem = CounterMeasureSystemClass(counterMeasuresSystemPosition, len(counterMeasuresSystems))
    counterMeasuresSystems.append(counterMeasureSystem)


if __name__ == "__main__":
    contActiveMissiles = 0
    contMissileImpact = 0
    contMissilesDestroyed = 0
    contActiveCities = 0
    CitiesDestroyed = 0
    angle = 0
    missileId = 0
    cityId = 0
    FPS = 30

    calculateSystemPosition = positionClass(MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2, 0)

    radarPosition = positionClass(MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2, 0)
    radarWidthRange = [0, MAPWIDTHLIMIT]
    radarHeightRange = [0, WINDOWSHEIGHT]

    radar = RadarClass(radarPosition, radarWidthRange, radarHeightRange)

    interface = InterfaceClass(WINDOWSWIDTH, WINDOWSHEIGHT)

    counterMeasuresMissiles = []
    counterMeasuresSystems = []
    enemies = []
    enemiesDestroyedPositions = []
    strategicLocations = []
    threads = []  # hebras enemigos
    threadsCounterSystem = []
    threadsCounterMissile = []

    spawnStrategicLocations(strategicLocations)


    spawnCounterMeasuresSystems(counterMeasuresSystems)

    calculateSystem = CalculateSystemClass(calculateSystemPosition)
    calculateSystem.setCounterMeasuresPosition(counterMeasuresSystems)

    run = True
    pause = False
    hasSpawnMissiles = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w]:
                    if FPS < 30:
                        FPS += 10
                if pressed[pygame.K_s]:
                    if FPS > 10:
                        FPS -= 10
                if pressed[pygame.K_SPACE]:
                    pause = not pause

            while pause:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        run = False
                    if e.type == pygame.KEYDOWN:
                        pressed = pygame.key.get_pressed()
                        if pressed[pygame.K_SPACE]:
                            pause = not pause
        startTime = pygame.time.get_ticks()

        if not hasSpawnMissiles:
            spawnEnemyMissiles(enemies, strategicLocations, 100)
            hasSpawnMissiles = True

        for enemy in enemies:
            if enemy.getIntercepted():
                enemiesDestroyedPositions.append(enemy.position)
                radar.deleteDeadEnemyMissile(enemy.id)
                enemies.pop(enemies.index(enemy))
                contMissilesDestroyed += 1
            if enemy.getObjectiveImpacted():
                cityHit(enemy, strategicLocations)
                if enemy in enemies:
                    radar.deleteDeadEnemyMissile(enemy.id)
                    enemies.pop(enemies.index(enemy))
                contMissileImpact += 1
            for city in strategicLocations:
                if enemy.ObjectivePosition.positionX == city.position.positionX \
                        and enemy.ObjectivePosition.positionY == city.position.positionY \
                        and enemy.ObjectivePosition.positionZ == city.position.positionZ:
                    enemy.objectiveStillAlive = True
            if enemy.objectiveStillAlive:
                thread = threading.Thread(target=enemy.goToObjective(), args=())
                thread.start()
                threads.append(thread)
                enemy.objectiveStillAlive = False
            else:
                if enemy in enemies:
                    radar.deleteDeadEnemyMissile(enemy.id)
                    enemies.pop(enemies.index(enemy))

        for thread in threads:
            thread.join()

        radar.detectMissiles(enemies)

        calculateSystem.updateEnemyMissileData(radar.enemyMissileLastPosition)

        calculateSystem.assignCounterMeasureSystemToEnemyMissile()

        for counterMeasuresSystem in counterMeasuresSystems:
            counterMeasuresSystem.updateEnemyMissileAssignedData(calculateSystem.enemyMissileData,
                                                                 calculateSystem.enemyMissilesIdAssignedToCounterMeasuresId)
            actualTime = pygame.time.get_ticks()
            threadCounterSystem = threading.Thread(
                target=counterMeasuresSystem.launchCounterMeasure(counterMeasuresMissiles, actualTime), args=())
            threadCounterSystem.start()
            threadsCounterSystem.append(threadCounterSystem)

        for thread in threadsCounterSystem:
            thread.join()

        for counterMeasuresMissile in list(counterMeasuresMissiles):
            counterMeasuresMissile.updateObjectivePosition(
                counterMeasuresSystems[counterMeasuresMissile.counterMeasureSystemId].enemyMissilesAssigned)
            threadCounterMissile = threading.Thread(target=counterMeasuresMissile.goToObjective(), args=())
            threadCounterMissile.start()
            threadsCounterMissile.append(threadCounterMissile)

            if counterMeasuresMissile.enemyMissileIntercepted:
                for enemy in enemies:
                    if enemy.id == counterMeasuresMissile.enemyId:
                        enemy.hasBeenIntercepted()
                counterMeasuresMissiles.pop(counterMeasuresMissiles.index(counterMeasuresMissile))

        for thread in threadsCounterMissile:
            thread.join()

        for city in strategicLocations:
            if city.getCityStatus():
                CitiesDestroyed += 1
                strategicLocations.pop(strategicLocations.index(city))

        endTime = pygame.time.get_ticks()
        print(f'time {round(endTime - startTime,25)}')
        contActiveMissiles = len(enemies)
        contActiveCities = len(strategicLocations)
        angle += DEGRESSPERFRAME

        interface.drawSimulationWindow(contActiveMissiles, contMissilesDestroyed, contActiveCities, contMissileImpact,
                             CitiesDestroyed, enemies, strategicLocations, counterMeasuresSystems,
                             counterMeasuresMissiles, angle, enemiesDestroyedPositions)

        clock.tick(FPS)
