import math

import pygame
import ctypes
import multiprocessing as multiprocess
import random

from strategicLocations import strategicLocationsClass
from EnemyMissile import EnemyMissileClass
from Position import positionClass
from Radar import RadarClass

pygame.init()

# ####################################### CONSTS  ##################################################
screenResolution = ctypes.windll.user32
WINDOWSWIDTH = screenResolution.GetSystemMetrics(0) - 100
WINDOWSHEIGHT = screenResolution.GetSystemMetrics(1) - 100

MAPWIDTHLIMIT = int(WINDOWSWIDTH * 0.65)
TEXTWIDTHSTART = WINDOWSWIDTH * 0.72

SMALLESTWINDOWSSIZE = MAPWIDTHLIMIT if MAPWIDTHLIMIT < WINDOWSHEIGHT else WINDOWSHEIGHT

FIRSTCIRCLERADAR = int(SMALLESTWINDOWSSIZE * 0.1)
SECONDCIRCLERADAR = int(SMALLESTWINDOWSSIZE * 0.2)
THIRDCIRCLERADAR = int(SMALLESTWINDOWSSIZE * 0.3)
FOURTHCIRCLERADAR = int(SMALLESTWINDOWSSIZE * 0.4)

CITYSPAWNINFERIORLIMITWIDTH = int((MAPWIDTHLIMIT / 2) - FOURTHCIRCLERADAR)
CITYSPAWNSUPERIORLIMITWIDTH = int(FOURTHCIRCLERADAR + (MAPWIDTHLIMIT / 2))

CITYSPAWNINFERIORLIMITHEIGHT = int((WINDOWSHEIGHT / 2) - FOURTHCIRCLERADAR)
CITYSPAWNSUPERIORLIMITHEIGHT = int((WINDOWSHEIGHT / 2) + FOURTHCIRCLERADAR)

MISSILESSPAWNINFERIORLIMIT = 0
MISSILESSPAWNSUPERIORLIMITWIDTH = int(MAPWIDTHLIMIT)
MISSILESSPAWNSUPERIORLIMITHEIGHT = int(WINDOWSHEIGHT)

CIRCLESIZE = 4
CITYPICTURESIZE = 40

DEGRESSPERGRAME = 1

GREEN = (0, 170, 0)
# #####################################   FPS   ###########################################################
clock = pygame.time.Clock()


# #####################################   FUNCTIONS   ###########################################################
def convert_degrees(R, theta):
    y = math.cos(math.pi * theta / 180) * R
    x = math.sin(math.pi * theta / 180) * R

    return [x + (MAPWIDTHLIMIT / 2), -(y - (WINDOWSHEIGHT / 2))]


def CityHit(enemy, strategicLocations):
    for city in strategicLocations:
        if enemy.ObjectivePosition.positionX == city.position.positionX and enemy.ObjectivePosition.positionY == city.position.positionY:
            city.strategicLocationImpacted()


def text(text, positionX, positionY, font):
    screenText = font.render(text, True, GREEN)
    win.blit(screenText, (positionX, positionY))


def drawWindow(contActiveMissiles, contMissilesDestroyed, contActiveCities, CitiesDestroyed, enemies, strategicLocations,
               angle):
    # fondo de la pantalla
    fontText = pygame.font.Font('./fonts/digital-7.ttf', 35)
    fontNumbers = pygame.font.Font('./fonts/digital-7.ttf', 20)
    win.fill((0, 0, 0))  # limpieza de la pantalla

    win.blit(radarPanel, (MAPWIDTHLIMIT, 0))
    drawRadarLine(angle)
    drawRadarCircles(fontNumbers)
    drawStrategicLocations(strategicLocations)
    drawEnemyMissile(enemies)

    text("Active missiles: " + str(contActiveMissiles), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.2, fontText)
    text("Missile Impact: " + str(contMissileImpact), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.3, fontText)
    text("Missiles destroyed: " + str(contMissilesDestroyed), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.45, fontText)
    text("Active cities: " + str(contActiveCities), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.6, fontText)
    text("Cities destroyed: " + str(CitiesDestroyed), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.7, fontText)

    pygame.display.update()


def drawEnemyMissile(enemies):
    for enemy in enemies:
        if pygame.time.get_ticks() % 3 == 0 or enemy.isInObjectivePerimeter() == True:
            color = GREEN
        else:
            color = (0, 0, 0)
        # Las restas a las posiciones es para centrar la foto en el punto
        pygame.draw.circle(win, color, (enemy.position.positionX - int(CIRCLESIZE / 2),
                                        enemy.position.positionY - int(CIRCLESIZE / 2)), CIRCLESIZE, CIRCLESIZE)


def drawStrategicLocations(strategicLocations):
    for city in strategicLocations:
        # Las restas a las posiciones es para centrar la foto en el punto
        win.blit(cityPicture, (city.position.positionX - int(CITYPICTURESIZE / 2),
                               city.position.positionY - int(CITYPICTURESIZE / 2)))


def drawRadarCircles(fontNumbers):
    color = GREEN
    pygame.draw.circle(win, color, (MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), FIRSTCIRCLERADAR, 4)
    pygame.draw.circle(win, color, (MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), SECONDCIRCLERADAR, 4)
    pygame.draw.circle(win, color, (MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), THIRDCIRCLERADAR, 4)
    pygame.draw.circle(win, color, (MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), FOURTHCIRCLERADAR, 4)

    for number in range(0, 360, 45):
        positionNumbers = convert_degrees(FOURTHCIRCLERADAR + 20, number)
        text(str(number), positionNumbers[0] - 10, positionNumbers[1], fontNumbers)


def drawRadarLine(angle):
    color = GREEN
    R = FOURTHCIRCLERADAR - 3
    pygame.draw.line(win, color, (MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), convert_degrees(R, angle), 4)


def spawnEnemyMissiles(enemies, strategicLocations):
    global missileId
    if len(enemies) < 2:
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
    win = pygame.display.set_mode((WINDOWSWIDTH, WINDOWSHEIGHT))

    cityPicture = pygame.image.load('./img/city.png').convert_alpha()
    cityPicture = pygame.transform.scale(cityPicture, (CITYPICTURESIZE, CITYPICTURESIZE))

    radarPanel = pygame.image.load('./img/panel.png').convert_alpha()
    radarPanel = pygame.transform.scale(radarPanel, (WINDOWSWIDTH - MAPWIDTHLIMIT, WINDOWSHEIGHT))

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
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pool.map_async(radar.detectMissiles(enemies), {})

        if len(strategicLocations) > 0:
            spawnEnemyMissiles(enemies, strategicLocations)

        for enemy in enemies:
            if enemy.getIntercepted():
                enemies.pop(enemies.index(enemy))
                contMissilesDestroyed += 1
            if enemy.getObjectiveImpacted():
                CityHit(enemy, strategicLocations)
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

        drawWindow(contActiveMissiles, contMissilesDestroyed, contActiveCities, CitiesDestroyed, enemies,
                   strategicLocations, angle)
