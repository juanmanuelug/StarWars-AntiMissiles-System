import math

import pygame
import ctypes
import multiprocessing as multiprocess
import random

from strategicLocations import strategicLocationsClass
from EnemyMisile import EnemyMisileClass
from Position import positionClass

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

CITYSPAWNINFERIORLIMITWIDTH = int((MAPWIDTHLIMIT/2) - FOURTHCIRCLERADAR)
CITYSPAWNSUPERIORLIMITWIDTH = int(FOURTHCIRCLERADAR + (MAPWIDTHLIMIT/2))

CITYSPAWNINFERIORLIMITHEIGHT = int((WINDOWSHEIGHT/2) - FOURTHCIRCLERADAR)
CITYSPAWNSUPERIORLIMITHEIGHT = int((WINDOWSHEIGHT/2) + FOURTHCIRCLERADAR)

MISILESSPAWNINFERIORLIMIT = 0
MISILESSPAWNSUPERIORLIMITWIDTH = int(MAPWIDTHLIMIT)
MISILESSPAWNSUPERIORLIMITHEIGHT = int(WINDOWSHEIGHT)

CIRCLESIZE = 4
CITYPICTURESIZE = 40
# #####################################   FPS   ###########################################################
clock = pygame.time.Clock()

# #####################################   FUNCTIONS   ###########################################################
def convert_degrees(R, theta):
    y = math.cos(math.pi * theta / 180) * R
    x = math.sin(math.pi * theta / 180) * R
    return [x + (MAPWIDTHLIMIT / 2) - 10, -(y - (WINDOWSHEIGHT / 2))]

def CityHit(enemy, strategicLocations):
    for city in strategicLocations:
        if enemy.ObjectivePosition.positionX == city.position.positionX and enemy.ObjectivePosition.positionY == city.position.positionY:
            city.strategicLocationImpacted()

def text(text, positionX, positionY, font):
    screenText = font.render(text, True, (0,170,0))
    win.blit(screenText, (positionX, positionY))


def drawWindow(contActiveMisiles, contMisilesDestroyed, contActiveCities, CitiesDestroyed, enemies, strategicLocations):
    # fondo de la pantalla
    fontText = pygame.font.Font('./fonts/digital-7.ttf', 35)
    fontNumbers = pygame.font.Font('./fonts/digital-7.ttf', 20)
    win.fill((0,0,0)) #limpieza de la pantalla

    win.blit(radarPanel,(MAPWIDTHLIMIT,0))
    drawRadarPanel(fontNumbers)
    drawStrategicLocations(strategicLocations)
    drawEnemyMisile(enemies)

    text("Active misiles: " + str(contActiveMisiles), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.2, fontText)
    text("Misile Impact: " + str(contMisileImpact), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.3, fontText)
    text("Misiles destroyed: " + str(contMisilesDestroyed), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.45, fontText)
    text("Active cities: " + str(contActiveCities), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.6, fontText)
    text("Cities destroyed: " + str(CitiesDestroyed), TEXTWIDTHSTART, WINDOWSHEIGHT * 0.7, fontText)

    pygame.display.update()

def drawEnemyMisile(enemies):
    for enemy in enemies:
        if pygame.time.get_ticks() % 3 == 0 or enemy.isInObjectivePerimeter() == True:
            color = (0,170,0)
        else:
            color = (0,0,0)
        #Las restas a las posiciones es para centrar la foto en el punto
        pygame.draw.circle(win,color,(enemy.position.positionX - int(CIRCLESIZE / 2),enemy.position.positionY - int(CIRCLESIZE / 2)),CIRCLESIZE,CIRCLESIZE)

def drawStrategicLocations(strategicLocations):
    for city in strategicLocations:
        # Las restas a las posiciones es para centrar la foto en el punto
        win.blit(cityPicture, (city.position.positionX - int(CITYPICTURESIZE / 2), city.position.positionY - int(CITYPICTURESIZE / 2)))

def drawRadarPanel(fontNumbers):
    color = (0,170,0)
    pygame.draw.circle(win, color,(MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), FIRSTCIRCLERADAR, 4)
    pygame.draw.circle(win, color,(MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), SECONDCIRCLERADAR, 4)
    pygame.draw.circle(win, color,(MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), THIRDCIRCLERADAR, 4)
    pygame.draw.circle(win, color,(MAPWIDTHLIMIT / 2, WINDOWSHEIGHT / 2), FOURTHCIRCLERADAR, 4)

    for number in range(0, 360, 45):
        positionNumbers = convert_degrees(FOURTHCIRCLERADAR + 20, number)
        text(str(number), positionNumbers[0], positionNumbers[1], fontNumbers)

def spawnEnemyMisiles(enemies, strategicLocations):
    if len(enemies) < 2:
        InferiorX = random.randint(MISILESSPAWNINFERIORLIMIT,CITYSPAWNINFERIORLIMITWIDTH)
        SuperiorX = random.randint(CITYSPAWNSUPERIORLIMITWIDTH,MISILESSPAWNSUPERIORLIMITWIDTH)

        InferiorY = random.randint(MISILESSPAWNINFERIORLIMIT, CITYSPAWNINFERIORLIMITHEIGHT)
        SuperiorY = random.randint(CITYSPAWNSUPERIORLIMITHEIGHT, MISILESSPAWNSUPERIORLIMITHEIGHT)

        x = InferiorX if InferiorX%2 == 0 else SuperiorX
        y = InferiorY if SuperiorY%2 == 0 else SuperiorY
        z = random.randint(100,200)
        positionRandom = positionClass(x,y,z)
        x = random.randint(0, len(strategicLocations) - 1)
        ObjpositionRandom = positionClass(strategicLocations[x].position.positionX,
                                          strategicLocations[x].position.positionY,
                                          strategicLocations[x].position.positionZ)
        enemy = EnemyMisileClass(positionRandom, ObjpositionRandom)
        enemies.append(enemy)


def spawnStrategicLocations(strategicLocations):
    x = random.randint(CITYSPAWNINFERIORLIMITWIDTH,CITYSPAWNSUPERIORLIMITWIDTH)
    y = random.randint(CITYSPAWNINFERIORLIMITHEIGHT,CITYSPAWNSUPERIORLIMITHEIGHT)
    z = random.randint(0,50)
    strategicLocationPosition = positionClass(x,y,z)
    city = strategicLocationsClass(strategicLocationPosition)
    strategicLocations.append(city)


if __name__ == "__main__":
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

    contActiveMisiles = 0
    contMisileImpact = 0
    contMisilesDestroyed= 0
    contActiveCities = 0
    CitiesDestroyed = 0

    pool = multiprocess.Pool(processes=4)

    while run:
        multiprocess.freeze_support()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if len(strategicLocations) > 0:
            spawnEnemyMisiles(enemies, strategicLocations)

        for enemy in enemies:
            if enemy.getIntercepted():
                enemies.pop(enemies.index(enemy))
                contMisilesDestroyed += 1
            if enemy.getObjectiveImpacted():
                CityHit(enemy, strategicLocations)
                enemies.pop(enemies.index(enemy))
                contMisileImpact += 1
            pool.map_async(enemy.goToObjective(),{})

        for city in strategicLocations:
            if city.getCityStatus():
                CitiesDestroyed += 1
                strategicLocations.pop(strategicLocations.index(city))

        contActiveMisiles = len(enemies)
        contActiveCities = len(strategicLocations)
        drawWindow(contActiveMisiles,contMisilesDestroyed,contActiveCities,CitiesDestroyed, enemies, strategicLocations)
