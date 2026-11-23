"""Caminhos compartilhados entre os modulos do jogo."""
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_DIR / "assets"
IMAGE_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"


def background_path(name):
    web_image = IMAGE_DIR / f"{name}.jpg"
    return web_image if web_image.is_file() else IMAGE_DIR / f"{name}.png"
