"""Ponto de entrada do Riff Run."""
import asyncio
import sys

import pygame

from riffrun.game import Game
from riffrun.settings import HEIGHT, TITLE, WIDTH


async def main():
    on_web = sys.platform == "emscripten"
    pygame.mixer.pre_init(22050, -16, 1, 1024 if on_web else 512)
    pygame.init()
    try:
        flags = 0 if on_web else pygame.FULLSCREEN | pygame.SCALED
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        await Game(screen).run(on_web=on_web)
    finally:
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
