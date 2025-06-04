import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=80, height=10, color=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        # starting pos
        self.rect = self.image.get_rect(midtop=(x, y))

    def update(self, mouse_x, screen_rect):
        # update x coord
        self.rect.centerx = mouse_x
        # make sure paddle doesnt go offscreen
        if self.rect.left < screen_rect.left:
            self.rect.left = screen_rect.left
        if self.rect.right > screen_rect.right:
            self.rect.right = screen_rect.right
