import math

import pygame

pygame.init()


class InterfaceClass(object):

    def __init__(self, windowswidth, windowsheight):
        self.windowsWidth = windowswidth
        self.windowsHeight = windowsheight
        self.mapWidthLimit = int(self.windowsWidth * 0.65)
        self.textWidthStart = self.windowsWidth * 0.72
        self.smallestWindowSize = self.mapWidthLimit if self.mapWidthLimit < self.windowsHeight else self.windowsHeight
        self.firstCircleRadar = int(self.smallestWindowSize * 0.1)
        self.secondCircleRadar = int(self.smallestWindowSize * 0.2)
        self.thirdCircleRadar = int(self.smallestWindowSize * 0.3)
        self.fourthCircleRadar = int(self.smallestWindowSize * 0.4)
        self.win = pygame.display.set_mode((self.windowsWidth, self.windowsHeight))
        self.cityPictureSize = 40
        self.circleSize = 4
        self.greenColor = (0, 170, 0)
        self.cityPicture = pygame.image.load('./img/city.png').convert_alpha()
        self.radarPanel = pygame.image.load('./img/panel.png').convert_alpha()

    def loadPictures(self):
        self.cityPicture = pygame.transform.scale(self.cityPicture, (self.cityPictureSize, self.cityPictureSize))
        self.radarPanel = pygame.transform.scale(self.radarPanel, (self.windowsWidth - self.mapWidthLimit,
                                                                   self.windowsHeight))

    def convert_degrees(self, R, theta):
        y = math.cos(math.pi * theta / 180) * R
        x = math.sin(math.pi * theta / 180) * R

        return [x + (self.mapWidthLimit / 2), -(y - (self.windowsHeight / 2))]

    def text(self, text, positionX, positionY, font):
        screenText = font.render(text, True, self.greenColor)
        self.win.blit(screenText, (positionX, positionY))

    def drawWindow(self, contActiveMissiles, contMissilesDestroyed, contActiveCities, contMissileImpact,
                   CitiesDestroyed, enemies,
                   strategicLocations,
                   angle):
        # fondo de la pantalla
        fontText = pygame.font.Font('./fonts/digital-7.ttf', 35)
        fontNumbers = pygame.font.Font('./fonts/digital-7.ttf', 20)
        self.loadPictures()
        self.win.fill((0, 0, 0))  # limpieza de la pantalla

        self.win.blit(self.radarPanel, (self.mapWidthLimit, 0))
        self.drawRadarLine(angle)
        self.drawRadarCircles(fontNumbers)
        self.drawStrategicLocations(strategicLocations)
        self.drawEnemyMissile(enemies)

        self.text("Active missiles: " + str(contActiveMissiles), self.textWidthStart, self.windowsHeight * 0.2,
                  fontText)
        self.text("Missile Impact: " + str(contMissileImpact), self.textWidthStart, self.windowsHeight * 0.3, fontText)
        self.text("Missiles destroyed: " + str(contMissilesDestroyed), self.textWidthStart, self.windowsHeight * 0.45,
                  fontText)
        self.text("Active cities: " + str(contActiveCities), self.textWidthStart, self.windowsHeight * 0.6, fontText)
        self.text("Cities destroyed: " + str(CitiesDestroyed), self.textWidthStart, self.windowsHeight * 0.7, fontText)

        pygame.display.update()

    def drawEnemyMissile(self, enemies):
        for enemy in enemies:
            if pygame.time.get_ticks() % 3 == 0 or enemy.isInObjectivePerimeter() == True:
                color = self.greenColor
            else:
                color = (0, 0, 0)
            # Las restas a las posiciones es para centrar la foto en el punto
            pygame.draw.circle(self.win, color, (enemy.position.positionX - int(self.circleSize / 2),
                                                 enemy.position.positionY - int(self.circleSize / 2)), self.circleSize,
                               self.circleSize)

    def drawStrategicLocations(self, strategicLocations):
        for city in strategicLocations:
            # Las restas a las posiciones es para centrar la foto en el punto
            self.win.blit(self.cityPicture, (city.position.positionX - int(self.cityPictureSize / 2),
                                             city.position.positionY - int(self.cityPictureSize / 2)))

    def drawRadarCircles(self, fontNumbers):
        pygame.draw.circle(self.win, self.greenColor, (self.mapWidthLimit / 2, self.windowsHeight / 2),
                           self.firstCircleRadar, 4)
        pygame.draw.circle(self.win, self.greenColor, (self.mapWidthLimit / 2, self.windowsHeight / 2),
                           self.secondCircleRadar, 4)
        pygame.draw.circle(self.win, self.greenColor, (self.mapWidthLimit / 2, self.windowsHeight / 2),
                           self.thirdCircleRadar, 4)
        pygame.draw.circle(self.win, self.greenColor, (self.mapWidthLimit / 2, self.windowsHeight / 2),
                           self.fourthCircleRadar, 4)

        for number in range(0, 360, 45):
            positionNumbers = self.convert_degrees(self.fourthCircleRadar + 20, number)
            self.text(str(number), positionNumbers[0] - 10, positionNumbers[1], fontNumbers)

    def drawRadarLine(self, angle):
        color = self.greenColor
        R = self.fourthCircleRadar - 3
        pygame.draw.line(self.win, color, (self.mapWidthLimit / 2, self.windowsHeight / 2),
                         self.convert_degrees(R, angle), 4)
