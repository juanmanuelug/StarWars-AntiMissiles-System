import math
import time

from Button import Button
from strategicLocations import strategicLocationsClass
from CounterMeasureSystem import CounterMeasureSystemClass
from Position import positionClass
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
        self.counterMeasureSystemPictureSize = 30
        self.greenColor = (0, 170, 0)
        self.redColor = (255, 0, 0)
        self.cityPicture = pygame.image.load('./img/city.png').convert_alpha()
        self.radarPanel = pygame.image.load('./img/panel.png').convert_alpha()
        self.counterMeasureSystemPicture = pygame.image.load('./img/counterMeasure.png').convert_alpha()
        self.cityButtonPicture = pygame.image.load('./img/city_button.png').convert_alpha()
        self.counterMeasureSystemButtonPicture = pygame.image.load('./img/counterMeasureButton.png').convert_alpha()
        self.startButtonPicture = pygame.image.load('./img/startButton.png').convert_alpha()
        self.stopButtonPicture = pygame.image.load('./img/stopButton.png').convert_alpha()
        self.backgroundPictureButtonRed = pygame.image.load('./img/button_upper.png').convert_alpha()
        self.backgroundPictureButtonGreen = pygame.image.load('./img/button_upper_start.png').convert_alpha()
        self.cursor_img_rect = 0
        self.city_clicked = False
        self.counterMeasureSystem_clicked = False
        self.startButton_clicked = False
        self.stopButton_clicked = False
        self.stayInMenu = True
        self.keepRunning = True

    def loadPictures(self):
        self.cityPicture = pygame.transform.scale(self.cityPicture, (self.cityPictureSize, self.cityPictureSize))
        self.radarPanel = pygame.transform.scale(self.radarPanel, (self.windowsWidth - self.mapWidthLimit,
                                                                   self.windowsHeight))
        self.counterMeasureSystemPicture = pygame.transform.scale(self.counterMeasureSystemPicture,
                                                                  (self.counterMeasureSystemPictureSize,
                                                                   self.counterMeasureSystemPictureSize))

    def convert_degrees(self, R, theta):
        y = math.cos(math.pi * theta / 180) * R
        x = math.sin(math.pi * theta / 180) * R

        return [x + (self.mapWidthLimit / 2), -(y - (self.windowsHeight / 2))]

    def text(self, text, positionX, positionY, font):
        screenText = font.render(text, True, self.greenColor)
        self.win.blit(screenText, (positionX, positionY))

    def drawSimulationWindow(self, contActiveMissiles, contMissilesDestroyed, contActiveCities, contMissileImpact,
                             CitiesDestroyed, enemies, strategicLocations, counterMeasuresSystems,
                             counterMeasuresMissiles, angle
                             , enemiesDestroyedPositions):
        # fondo de la pantalla
        fontText = pygame.font.Font('./fonts/digital-7.ttf', 25)
        fontNumbers = pygame.font.Font('./fonts/digital-7.ttf', 20)
        self.loadPictures()
        self.win.fill((0, 0, 0))  # limpieza de la pantalla

        self.win.blit(self.radarPanel, (self.mapWidthLimit, 0))
        self.drawRadarLine(angle)
        self.drawRadarCircles(fontNumbers)
        self.drawStrategicLocations(strategicLocations)
        self.drawCounterMeasureSystem(counterMeasuresSystems)
        self.drawEnemyMissile(enemies)
        self.drawCounterMeasureMissiles(counterMeasuresMissiles)
        self.drawXWhenEnemyMissileIntercepted(enemiesDestroyedPositions)

        stopButton = Button(self.textWidthStart * 1.1, self.windowsHeight * 0.89, self.stopButtonPicture,
                             self.backgroundPictureButtonGreen, self.win, 0.15)

        if stopButton.draw_button():
            self.stopButton_clicked = not self.stopButton_clicked
            if self.stopButton_clicked:
                self.keepRunning = False

        self.text("Active missiles: " + str(contActiveMissiles), self.textWidthStart, self.windowsHeight * 0.2,
                  fontText)
        self.text("Missile Impact: " + str(contMissileImpact), self.textWidthStart, self.windowsHeight * 0.3, fontText)
        self.text("Missiles destroyed: " + str(contMissilesDestroyed), self.textWidthStart, self.windowsHeight * 0.45,
                  fontText)
        self.text("Active cities: " + str(contActiveCities), self.textWidthStart, self.windowsHeight * 0.6, fontText)
        self.text("Cities destroyed: " + str(CitiesDestroyed), self.textWidthStart, self.windowsHeight * 0.7, fontText)

        pygame.display.update()
        return  self.keepRunning

    def drawEnemyMissile(self, enemies):
        for enemy in enemies:
            # Las restas a las posiciones es para centrar la foto en el punto
            pygame.draw.circle(self.win, self.redColor, (enemy.position.positionX - int(self.circleSize / 2),
                                                         enemy.position.positionY - int(self.circleSize / 2)),
                               self.circleSize,
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

    def drawCounterMeasureSystem(self, counterMeasureSystems):
        for counterMeasureSystem in counterMeasureSystems:
            # Las restas a las posiciones es para centrar la foto en el punto
            self.win.blit(self.counterMeasureSystemPicture, (counterMeasureSystem.position.positionX -
                                                             int(self.counterMeasureSystemPictureSize / 2),
                                                             counterMeasureSystem.position.positionY -
                                                             int(self.counterMeasureSystemPictureSize / 2)))

    def drawCounterMeasureMissiles(self, counterMeasuresMissiles):
        for counterMeasuresMissile in counterMeasuresMissiles:
            # Las restas a las posiciones es para centrar la foto en el punto
            pygame.draw.circle(self.win, self.greenColor,
                               (counterMeasuresMissile.position.positionX - int(self.circleSize / 2),
                                counterMeasuresMissile.position.positionY - int(self.circleSize / 2)), self.circleSize,
                               self.circleSize)

    def drawXWhenEnemyMissileIntercepted(self, positions):
        for position in positions:
            pygame.draw.aaline(self.win, self.redColor, (position.positionX - 4, position.positionY - 4),
                               (5 + position.positionX - 4, 5 + position.positionY - 4))
            pygame.draw.aaline(self.win, self.redColor, (5 + position.positionX - 4, position.positionY - 4),
                               (position.positionX - 4, 5 + position.positionY - 4))

    def drawConfigWindow(self, strategicLocations, counterMeasuresSystems, angle):
        fontNumbers = pygame.font.Font('./fonts/digital-7.ttf', 20)
        self.loadPictures()
        self.win.fill((0, 0, 0))  # limpieza de la pantalla

        self.win.blit(self.radarPanel, (self.mapWidthLimit, 0))
        self.drawRadarLine(angle)
        self.drawRadarCircles(fontNumbers)
        self.drawStrategicLocations(strategicLocations)
        self.drawCounterMeasureSystem(counterMeasuresSystems)

        cityButton = Button(self.textWidthStart * 1.05, self.windowsHeight * 0.2, self.cityButtonPicture,
                            self.backgroundPictureButtonRed, self.win, 0.25)
        counterMeasureSystemButton = Button(self.textWidthStart * 1.05, self.windowsHeight * 0.5,
                                            self.counterMeasureSystemButtonPicture,
                                            self.backgroundPictureButtonRed, self.win, 0.25)

        startButton = Button(self.textWidthStart * 1.1, self.windowsHeight * 0.89, self.startButtonPicture,
                             self.backgroundPictureButtonGreen, self.win, 0.15)

        if startButton.draw_button():
            self.startButton_clicked = not self.startButton_clicked
            if self.startButton_clicked:
                self.stayInMenu = False

        if cityButton.draw_button():
            self.city_clicked = not self.city_clicked
            if self.city_clicked:
                pygame.mouse.set_visible(False)
                self.cursor_img_rect = self.cityPicture.get_rect()
            else:
                pygame.mouse.set_visible(True)

        if counterMeasureSystemButton.draw_button():
            self.counterMeasureSystem_clicked = not self.counterMeasureSystem_clicked
            if self.counterMeasureSystem_clicked:
                pygame.mouse.set_visible(False)
                self.cursor_img_rect = self.counterMeasureSystemPicture.get_rect()
            else:
                pygame.mouse.set_visible(True)

        if self.city_clicked:
            self.cursor_img_rect.center = pygame.mouse.get_pos()
            self.win.blit(self.cityPicture, self.cursor_img_rect)
            if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] < self.mapWidthLimit:
                cityPos = positionClass(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0)
                strategicLocation = strategicLocationsClass(len(strategicLocations), cityPos)
                strategicLocations.append(strategicLocation)
                time.sleep(0.1)
        if self.counterMeasureSystem_clicked:
            self.cursor_img_rect.center = pygame.mouse.get_pos()
            self.win.blit(self.counterMeasureSystemPicture, self.cursor_img_rect)
            if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] < self.mapWidthLimit:
                counterPos = positionClass(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0)
                counterMeasuresSystem = CounterMeasureSystemClass(counterPos, len(counterMeasuresSystems))
                counterMeasuresSystems.append(counterMeasuresSystem)
                time.sleep(0.1)

        pygame.display.update()

        return self.stayInMenu
