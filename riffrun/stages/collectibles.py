"""Instrumentos coletaveis e objetivos das fases."""
from functools import lru_cache

import pygame

from riffrun.paths import IMAGE_DIR


@lru_cache(maxsize=4)
def collectible_frame(index):
    """Recorta guitarra, microfone, bateria e baixo sem dividir instrumentos."""
    path = IMAGE_DIR / "coletaveis_atlas.png"
    sheet = pygame.image.load(str(path)).convert_alpha()
    width, height = sheet.get_size()
    edges = (0, 0.29, 0.46, 0.77, 1)
    left, right = round(edges[index] * width), round(edges[index + 1] * width)
    frame = sheet.subsurface((left, 0, right - left, height))
    bounds = frame.get_bounding_rect(min_alpha=10)
    if not bounds.width or not bounds.height:
        raise ValueError(f"Coletável vazio no índice {index}")
    return frame.subsurface(bounds).copy()


class Guitar(pygame.sprite.Sprite):

    _sprites = None

    def __init__(self, x, y, phase_number=1):
        super().__init__()

        self.rect = pygame.Rect(x, y, 28, 42)
        self.collected = False
        self.phase_number = phase_number

        if Guitar._sprites is None:
            Guitar._sprites = self.load_sprites()

    @staticmethod
    def load_sprites():
        """Carrega os quatro instrumentos do spritesheet."""

        sprites = []
        for index in range(4):
            frame = collectible_frame(index)
            max_width, max_height = (80, 76) if index == 2 else (56, 72)
            scale = min(
                max_width / frame.get_width(),
                max_height / frame.get_height()
            )
            new_size = (
                max(1, round(frame.get_width() * scale)),
                max(1, round(frame.get_height() * scale))
            )
            frame = pygame.transform.smoothscale(frame, new_size)
            sprites.append(frame)
        return sprites

    def draw(self, screen, camera_x):
        if self.collected:
            return
        sprite_index = {
            1: 3,
            2: 0,
            3: 2
        }.get(self.phase_number, 0)
        image = self._sprites[sprite_index]
        draw_rect = image.get_rect(
            midbottom=(self.rect.centerx, self.rect.bottom + 4)
        )

        draw_rect.x -= camera_x
        screen.blit(image, draw_rect)


class GoalInstrument:

    _image = None

    def __init__(self, x, y):
        if GoalInstrument._image is None:
            GoalInstrument._image = self.load_image()
        # O argumento ancora a base; desenho e área de coleta são iguais.
        self.rect = self._image.get_rect(midbottom=(x + 35, y + 90))

    @staticmethod
    def load_image():
        image = collectible_frame(1)
        scale = min(
            95 / image.get_width(),
            115 / image.get_height()
        )
        size = (
            max(1, round(image.get_width() * scale)),
            max(1, round(image.get_height() * scale))
        )

        return pygame.transform.scale(image, size)

    def draw(self, screen, camera_x):
        image = self._image
        draw_rect = self.rect.move(-camera_x, 0)
        screen.blit(image, draw_rect)
