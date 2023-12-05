import images
import vector
import pygame
import commons

from vector import Vector
from enum import Enum
from pygame.locals import *
from pygame.sprite import Sprite, Group


class PinType(Enum):
    DEFAULT = 0


class Pin(Sprite):
    all = Group()
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 18)
    def __init__(self, position: Vector, radius: float = 16, pin_type: PinType = PinType.DEFAULT, image: pygame.Surface = None):
        super().__init__()
        self.position = vector.copy(position)
        self.velocity = Vector(0, 0)
        self.radius = radius
        self.diameter = radius * 2.0
        self.width = self.diameter
        self.height = self.diameter
        self.image = image
        if self.image is None:
            # self.image = images.ball_default
            self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position.make_int_tuple())
        self.rect.width = self.rect.height = self.diameter
        self.alive = True
        self.health = 16

    def update(self):
        if not self.alive:
            self.kill()

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        text = Pin.font.render(str(self.health), True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)



