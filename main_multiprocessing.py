import pygame
import ctypes
import multiprocessing as multiprocess
import random

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


def spawnEnemyMissiles(enemies, strategicLocations):
    global missileId
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
    enemies.append(enemy)
    missileId += 1


def configSimulation(menuOption, rotationAngle, simulationFPS, strategicLocations, counterMeasuresSystems, interface):
    global numberOfEnemyMissiles
    while menuOption:
        for eventCatcher in pygame.event.get():
            if eventCatcher.type == pygame.QUIT:
                menuOption = False

        rotationAngle += DEGRESSPERFRAME
        Option = interface.drawConfigWindow(strategicLocations, counterMeasuresSystems, rotationAngle, numberOfEnemyMissiles)
        if Option == 'Start':
            menuOption = False
        elif Option == 'Stop':
            menuOption = False
        clock.tick(simulationFPS)
    return Option


if __name__ == "__main__":
    run = True
    pause = False
    menu = True
    hasSpawnMissiles = False

    numberOfEnemyMissiles = [0]
    contActiveMissiles = 0
    contMissileImpact = 0
    contMissilesDestroyed = 0
    contActiveCities = 0
    CitiesDestroyed = 0
    angle = 0
    missileId = 0
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

    menuOption = configSimulation(menu, angle, FPS, strategicLocations, counterMeasuresSystems, interface)

    if menuOption == 'Start':
        menu = False
    elif menuOption == 'Stop':
        menu = False
        run = False


    calculateSystem = CalculateSystemClass(calculateSystemPosition)
    calculateSystem.setCounterMeasuresPosition(counterMeasuresSystems)

    pool = multiprocess.Pool(processes=4)

    while run:
        multiprocess.freeze_support()
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

        if not hasSpawnMissiles and numberOfEnemyMissiles[0] >= missileId:
            spawnEnemyMissiles(enemies, strategicLocations)
            if missileId == numberOfEnemyMissiles[0]:
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
                pool.starmap_async(enemy.goToObjective(), {})
                enemy.objectiveStillAlive = False
            else:
                if enemy in enemies:
                    radar.deleteDeadEnemyMissile(enemy.id)
                    enemies.pop(enemies.index(enemy))

        pool.starmap_async(radar.detectMissiles(enemies), {})

        pool.starmap_async(calculateSystem.updateEnemyMissileData(radar.enemyMissileLastPosition), {})

        pool.starmap_async(calculateSystem.assignCounterMeasureSystemToEnemyMissile(), {})

        for counterMeasuresSystem in counterMeasuresSystems:
            pool.starmap_async(counterMeasuresSystem.updateEnemyMissileAssignedData(calculateSystem.enemyMissileData,
                                                                                    calculateSystem.enemyMissilesIdAssignedToCounterMeasuresId),
                               {})
            actualTime = pygame.time.get_ticks()
            pool.starmap_async(counterMeasuresSystem.launchCounterMeasure(counterMeasuresMissiles, actualTime), {})
            print(f'misiles asignado a sistema[{counterMeasuresSystem.id}] = {len(counterMeasuresSystem.enemyMissilesAssigned)}')

        for counterMeasuresMissile in list(counterMeasuresMissiles):
            pool.starmap_async(counterMeasuresMissile.updateObjectivePosition(
                counterMeasuresSystems[counterMeasuresMissile.counterMeasureSystemId].enemyMissilesAssigned), {})
            pool.starmap_async(counterMeasuresMissile.goToObjective(), {})

            if counterMeasuresMissile.enemyMissileIntercepted:
                for enemy in enemies:
                    if enemy.id == counterMeasuresMissile.enemyId:
                        enemy.hasBeenIntercepted()
                counterMeasuresMissiles.pop(counterMeasuresMissiles.index(counterMeasuresMissile))

        for city in strategicLocations:
            if city.getCityStatus():
                CitiesDestroyed += 1
                strategicLocations.pop(strategicLocations.index(city))

        endTime = pygame.time.get_ticks()
        #print(f'time {round(endTime - startTime, 25)}')
        contActiveMissiles = len(enemies)
        contActiveCities = len(strategicLocations)
        angle += DEGRESSPERFRAME

        buttonAction = interface.drawSimulationWindow(contActiveMissiles, contMissilesDestroyed, contActiveCities,
                                                      contMissileImpact,
                                                      CitiesDestroyed, enemies, strategicLocations,
                                                      counterMeasuresSystems,
                                                      counterMeasuresMissiles, angle, enemiesDestroyedPositions)

        if buttonAction == 'Stop':
            run = False
        elif buttonAction == 'Config':
            menu = True

        if menu:
            hasSpawnMissiles = False
            contMissileImpact = 0
            contMissilesDestroyed = 0
            CitiesDestroyed = 0
            angle = 0
            missileId = 0
            counterMeasuresMissiles.clear()
            counterMeasuresSystems.clear()
            enemies.clear()
            enemiesDestroyedPositions.clear()
            strategicLocations.clear()
            radar.enemyMissileLastPosition.clear()
            calculateSystem.clear()
            menuOption = configSimulation(menu, angle, FPS, strategicLocations, counterMeasuresSystems, interface)
            calculateSystem.setCounterMeasuresPosition(counterMeasuresSystems)
            if menuOption == 'Start':
                menu = False
            elif menuOption == 'Stop':
                menu = False
                run = False

        clock.tick(FPS)
