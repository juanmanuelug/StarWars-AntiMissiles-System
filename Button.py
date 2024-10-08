import time

import pygame

class Button():
    def __init__(self, x, y, image, backimage, window, scale_image):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_image), int(height * scale_image)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.win = window
        self.button_clicked = False
        self.elevation = 6
        self.original_x = x
        self.original_y = y
        self.imageUpper = pygame.transform.scale(backimage, (int(width * scale_image), int(height * scale_image)))
        self.upperButton = self.image.get_rect()
        self.upperButton.topleft = (x - self.elevation, y - self.elevation)

    def draw_button(self):
        action = False
        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.button_clicked: #left click
                self.button_clicked = True
                action = True
                time.sleep(0.1)
        if pygame.mouse.get_pressed()[0] == 0: #reset the button
            self.button_clicked = False

        self.win.blit(self.imageUpper, (self.upperButton.x, self.upperButton.y))
        self.win.blit(self.image, (self.rect.x, self.rect.y))

        return action
