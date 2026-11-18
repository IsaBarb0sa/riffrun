"""Ponto de entrada do Riff Run."""
import asyncio
import sys

import pygame

from riffrun.game import Game
from riffrun.settings import HEIGHT, TITLE, WIDTH


async def main():
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    try:
        on_web = sys.platform == "emscripten"
        flags = 0 if on_web else pygame.FULLSCREEN | pygame.SCALED
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        await Game(screen).run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
