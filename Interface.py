import pygame
import ctypes

from EnemyMisile import EnemyMisileClass
from Position import positionClass

pygame.init()
# ####################################### Tam pantalla  ##################################################
screenResolution = ctypes.windll.user32
WINDOWSWIDTH = screenResolution.GetSystemMetrics(0) - 100
WINDOWSHEIGHT = screenResolution.GetSystemMetrics(1) - 100

win = pygame.display.set_mode((WINDOWSWIDTH, WINDOWSHEIGHT))

radarBackground = pygame.image.load('radar.png').convert_alpha()
radarBackground = pygame.transform.scale(radarBackground, (int(WINDOWSWIDTH * 0.65), WINDOWSHEIGHT))

font = pygame.font.SysFont('arial', 20)
# #####################################   FPS   ###########################################################
clock = pygame.time.Clock()

def text(text, positionX, positionY):
    screenText = font.render(text, True, (255,255,255))
    win.blit(screenText, (positionX, positionY))

def drawWindow(contActiveMisiles, contMisilesDestroyed, contActiveCities, CitiesDestroyed):
    # fondo de la pantalla
    win.fill((0,0,0)) #limpieza de la pantalla
    win.blit(radarBackground,(0,0))
    drawEnemyMisile()
    text("Active misiles: " + str(contActiveMisiles), WINDOWSWIDTH * 0.67, WINDOWSHEIGHT * 0.2)
    text("Misiles destroyed: " + str(contMisilesDestroyed), WINDOWSWIDTH * 0.67, WINDOWSHEIGHT * 0.35)
    text("Active cities: " + str(contActiveCities), WINDOWSWIDTH * 0.67, WINDOWSHEIGHT * 0.5)
    text("Cities destroyed: " + str(CitiesDestroyed), WINDOWSWIDTH * 0.67, WINDOWSHEIGHT * 0.65)

    pygame.display.update()

def drawEnemyMisile():
    if pygame.time.get_ticks() % 2 == 0:
        color  = (0,170,0)
    else:
        color = (0,0,0)

    for enemy in enemies:
        pygame.draw.circle(win,color,(enemy.position.positionX,enemy.position.positionY),3,3)


position = positionClass(200, 2, 150)
position2 = positionClass(100, 550, 200)
ObjPosition = positionClass(100, 150, 10)
ObjPosition2 = positionClass(600, 155, 15)
enemies = [ EnemyMisileClass(position2, ObjPosition2)]

def main():
    run = True
    contActiveMisiles = 0
    contMisilesDestroyed= 0
    contActiveCities = 0
    CitiesDestroyed = 0
    while run:
        clock.tick(60)
        # Si pulsamos lo de cerrar pestania, se cierra
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for enemy in enemies:
            if enemy.exploted:
                enemies.pop(enemies.index(enemy))
            enemy.goToObjective()

        drawWindow(contActiveMisiles,contMisilesDestroyed,contActiveCities,CitiesDestroyed)

main()
