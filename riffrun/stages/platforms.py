"""Plataformas e desenho dos pisos de cada fase."""
from functools import lru_cache

import pygame

from riffrun.paths import IMAGE_DIR


STEEL_DARK = (20, 27, 36)
STEEL = (54, 66, 78)
STEEL_LIGHT = (117, 132, 142)
CYAN = (100, 210, 231)
AMBER = (225, 157, 48)

GRAVE_STONE_DARK = (12, 17, 29)
GRAVE_STONE = (37, 48, 67)
GRAVE_STONE_MID = (57, 70, 91)
GRAVE_STONE_LIGHT = (111, 125, 145)
GRAVE_MOSS = (57, 75, 48)

PHASE3_PLATFORM_ATLAS_PATH = (
    IMAGE_DIR
    / "fase3_platforms_atlas.png"
)

PHASE3_ATLAS_RECTS = {
    "ground": (22, 101, 2130, 203),
    "grave_platform": (47, 396, 500, 119),
    "grave_moss": (577, 396, 432, 120),
    "grave_arch": (1058, 395, 490, 246),
    "grave_skull": (1601, 427, 176, 181),
    "grave_crate": (1790, 426, 178, 180),
    "grave_pillar": (1977, 396, 152, 244),
}

PHASE2_PLATFORM_ATLAS_PATH = (
    IMAGE_DIR
    / "fase2_platforms_atlas.png"
)

PHASE2_ATLAS_RECTS = {
    "highway_ground": (16, 90, 2140, 190),
    "highway_platform": (17, 349, 480, 153),
    "highway_platform2": (544, 347, 480, 156),
    "highway_bottom": (18, 522, 480, 136),
    "highway_hazard": (543, 522, 480, 118),
    "highway_arch": (1053, 347, 494, 301),
    "highway_lightning": (1570, 431, 150, 165),
    "highway_bars": (1724, 431, 148, 165),
    "highway_crate": (1880, 431, 148, 165),
    "highway_pillar": (2042, 396, 114, 215),
}

PHASE1_PLATFORM_ATLAS_PATH = (
    IMAGE_DIR
    / "fase1_plataforms_atlas.png"
)

PHASE1_ATLAS_RECTS = {
    "metal_ground": (22, 85, 2133, 191),
    "metal_platform": (40, 374, 477, 127),
    "metal_platform2": (572, 373, 537, 127),
    "metal_arch": (1150, 373, 474, 259),
    "metal_bottom": (40, 563, 421, 98),
    "metal_speaker": (518, 559, 392, 73),
    "metal_small": (907, 559, 189, 78),
    "metal_block": (1670, 430, 170, 148),
    "metal_lightning": (1839, 430, 140, 148),
    "metal_hazard": (2010, 447, 141, 90),
}

_phase3_platform_atlas = None
_phase2_platform_atlas = None
_phase1_platform_atlas = None

def load_phase3_platform_atlas():
    global _phase3_platform_atlas
    if _phase3_platform_atlas is None:
        _phase3_platform_atlas = pygame.image.load(
            str(PHASE3_PLATFORM_ATLAS_PATH)
        )
        if pygame.display.get_surface():
            _phase3_platform_atlas = _phase3_platform_atlas.convert_alpha()
    return _phase3_platform_atlas


def load_phase2_platform_atlas():
    global _phase2_platform_atlas
    if _phase2_platform_atlas is None:
        _phase2_platform_atlas = pygame.image.load(
            str(PHASE2_PLATFORM_ATLAS_PATH)
        )
        if pygame.display.get_surface():
            _phase2_platform_atlas = _phase2_platform_atlas.convert_alpha()
    return _phase2_platform_atlas

def load_phase1_platform_atlas():
    global _phase1_platform_atlas
    if _phase1_platform_atlas is None:
        _phase1_platform_atlas = pygame.image.load(
            str(PHASE1_PLATFORM_ATLAS_PATH)
        )
        if pygame.display.get_surface():
            _phase1_platform_atlas = (
                _phase1_platform_atlas.convert_alpha()
            )
    return _phase1_platform_atlas

def draw_rivet(screen, x, y):
    pygame.draw.circle(screen, STEEL_LIGHT, (x, y), 3)
    pygame.draw.circle(screen, (37, 45, 53), (x, y), 1)


@lru_cache(maxsize=128)
def scaled_platform_sprite(atlas, source_rect, size, *, preserve_aspect=False):
    source = atlas.subsurface(source_rect)
    bounds = source.get_bounding_rect(min_alpha=20)
    if not bounds.width or not bounds.height:
        return None

    width, height = size
    if preserve_aspect:
        height = max(1, round(bounds.height * (width / bounds.width)))
    return pygame.transform.scale(source.subsurface(bounds), (width, height))


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, kind="ground", style="beam"):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.kind = kind
        self.style = style

    def draw(self, screen, camera_x):
        r = self.rect.move(-camera_x, 0)
        # Não desenha objetos fora da câmera
        if (
                r.right < -80
                or r.left > screen.get_width() + 80
        ):
            return
        # CHÃO
        if self.kind == "ground":

            if self.style == "metal":

                self.draw_phase1_atlas_sprite(
                    screen,
                    r,
                    "metal_ground"
                )
            elif self.style == "grave":
                self.draw_grave_ground(
                    screen,
                    r
                )
            elif self.style == "highway":
                self.draw_phase2_atlas_sprite(
                    screen,
                    r,
                    "highway_ground"
                )
            else:
                self.draw_ground(
                    screen,
                    r
                )
        # PLATAFORMAS DA FASE 1
        elif self.style.startswith("metal_"):

            self.draw_phase1_atlas_sprite(
                screen,
                r,
                self.style
            )
        # PLATAFORMAS DA FASE 3
        elif self.style.startswith("grave"):
            self.draw_grave_obstacle(
                screen,
                r
            )
        # PLATAFORMAS DA FASE 2
        elif self.style.startswith("highway"):
            self.draw_phase2_atlas_sprite(
                screen,
                r,
                self.style
            )
        # PLATAFORMAS ANTIGAS
        elif self.style == "brick":
            self.draw_bricks(screen, r)
        elif self.style == "case":
            self.draw_case(screen, r)
        elif self.style == "amp":
            self.draw_amp(screen, r)
        elif self.style == "pipe":
            self.draw_pipe(screen, r)
        else:
            self.draw_beam(screen, r)

    def draw_grave_ground(self, screen, r):
        self.draw_phase3_atlas_sprite(screen, r, "ground")

    def draw_grave_obstacle(self, screen, r):
        self.draw_phase3_atlas_sprite(screen, r, self.style)

    def draw_atlas_sprite(self, screen, r, atlas, source_rect):
        sprite = scaled_platform_sprite(atlas, source_rect, r.size)
        if sprite is not None:
            screen.blit(sprite, r.topleft)

    def draw_phase3_atlas_sprite(self, screen, r, sprite_name):
        atlas = load_phase3_platform_atlas()
        source_rect = PHASE3_ATLAS_RECTS[sprite_name]
        self.draw_atlas_sprite(
            screen,
            r,
            atlas,
            source_rect
        )

    def draw_phase2_atlas_sprite(self, screen, r, sprite_name):
        atlas = load_phase2_platform_atlas()
        source_rect = PHASE2_ATLAS_RECTS[sprite_name]
        self.draw_atlas_sprite(
            screen,
            r,
            atlas,
            source_rect
        )

    def draw_phase1_atlas_sprite(
            self,
            screen,
            r,
            sprite_name
    ):
        atlas = load_phase1_platform_atlas()
        source_rect = PHASE1_ATLAS_RECTS[sprite_name]
        sprite = scaled_platform_sprite(
            atlas, source_rect, r.size, preserve_aspect=sprite_name != "metal_ground",
        )
        if sprite is not None:
            screen.blit(sprite, r.topleft)

    def draw_grave_arch(self, screen, r):
        pygame.draw.rect(screen, GRAVE_STONE_DARK, r)
        pygame.draw.rect(screen, GRAVE_STONE, (r.x, r.y, r.w, 18))
        pygame.draw.rect(screen, GRAVE_STONE_LIGHT, (r.x, r.y, r.w, 4))

        pillar_w = max(14, r.w // 8)
        for x in (r.x + 18, r.right - pillar_w - 18):
            pygame.draw.rect(screen, GRAVE_STONE_MID, (x, r.y + 16, pillar_w, r.h - 16))
            pygame.draw.rect(screen, GRAVE_STONE_LIGHT, (x - 3, r.y + 16, pillar_w + 6, 5))
            pygame.draw.rect(screen, GRAVE_STONE_DARK, (x - 5, r.bottom - 9, pillar_w + 10, 9))

        arch_rect = pygame.Rect(r.x + 28, r.y + 18, r.w - 56, r.h + 8)
        pygame.draw.arc(screen, GRAVE_STONE_MID, arch_rect, 0, 3.14, 8)
        pygame.draw.arc(screen, GRAVE_STONE_LIGHT, arch_rect.inflate(-5, -4), 0, 3.14, 3)

    def draw_grave_skull_block(self, screen, r):
        pygame.draw.rect(screen, GRAVE_STONE_DARK, r, border_radius=5)
        inner = r.inflate(-6, -6)
        pygame.draw.rect(screen, GRAVE_STONE, inner, border_radius=3)
        pygame.draw.rect(screen, GRAVE_STONE_LIGHT, inner, 3, border_radius=3)
        center = inner.center
        pygame.draw.circle(screen, (17, 22, 32), (center[0] - 8, center[1] - 3), 5)
        pygame.draw.circle(screen, (17, 22, 32), (center[0] + 8, center[1] - 3), 5)
        pygame.draw.polygon(screen, (17, 22, 32), [
            (center[0] - 7, center[1] + 5),
            (center[0] + 7, center[1] + 5),
            (center[0], center[1] + 12),
        ])
        pygame.draw.line(screen, GRAVE_STONE_LIGHT,
                         (center[0] - 8, center[1] + 14),
                         (center[0] + 8, center[1] + 14), 2)

    def draw_grave_crate(self, screen, r):
        pygame.draw.rect(screen, GRAVE_STONE_DARK, r, border_radius=4)
        pygame.draw.rect(screen, GRAVE_STONE, r.inflate(-5, -5), border_radius=3)
        pygame.draw.rect(screen, GRAVE_STONE_LIGHT, r.inflate(-5, -5), 3, border_radius=3)
        pygame.draw.line(screen, GRAVE_STONE_MID, r.topleft, r.bottomright, 3)
        pygame.draw.line(screen, GRAVE_STONE_MID, r.topright, r.bottomleft, 3)

    def draw_ground(self, screen, r):
        pygame.draw.rect(screen, (12, 17, 24), r)
        pygame.draw.rect(screen, STEEL, (r.x, r.y, r.w, 16))
        pygame.draw.rect(screen, (151, 159, 158), (r.x, r.y, r.w, 4))
        pygame.draw.line(screen, (7, 11, 17), (r.x, r.y + 16), (r.right, r.y + 16), 3)

        start_x = r.x - (r.x % 72)
        for x in range(start_x, r.right + 72, 72):
            pygame.draw.line(screen, (4, 8, 13), (x, r.y), (x, r.bottom), 3)
            if r.y + 9 < r.bottom:
                draw_rivet(screen, x + 9, r.y + 9)
                draw_rivet(screen, x + 63, r.y + 9)

        # Blocos de concreto rachado sob o deck metálico.
        for row, y in enumerate(range(r.y + 20, r.bottom, 30)):
            shift = 28 if row % 2 else 0
            for x in range(start_x - 72 + shift, r.right + 72, 56):
                block = pygame.Rect(x, y, 53, 27)
                pygame.draw.rect(screen, (45, 42, 45), block)
                pygame.draw.rect(screen, (78, 71, 70), block, 2)
                if (x // 56 + row) % 3 == 0:
                    pygame.draw.line(screen, (20, 21, 26), (x + 30, y + 2), (x + 24, y + 14), 2)
                    pygame.draw.line(screen, (20, 21, 26), (x + 24, y + 14), (x + 34, y + 24), 2)

    def draw_beam(self, screen, r):
        pygame.draw.rect(screen, STEEL_DARK, r)
        pygame.draw.rect(screen, STEEL_LIGHT, (r.x, r.y, r.w, 5))
        pygame.draw.rect(screen, (5, 10, 16), (r.x, r.bottom - 5, r.w, 5))
        for x in range(r.x + 12, r.right - 8, 34):
            pygame.draw.line(screen, (83, 99, 110), (x, r.y + 6), (x + 22, r.bottom - 6), 3)
            pygame.draw.line(screen, (32, 41, 51), (x + 22, r.y + 6), (x, r.bottom - 6), 3)
            draw_rivet(screen, x, r.centery)

    def draw_bricks(self, screen, r):
        pygame.draw.rect(screen, (31, 28, 31), r)
        brick_h = 22
        for row, y in enumerate(range(r.y, r.bottom, brick_h)):
            shift = -24 if row % 2 else 0
            for x in range(r.x + shift, r.right, 48):
                brick = pygame.Rect(x + 2, y + 2, 44, min(18, r.bottom - y - 3))
                pygame.draw.rect(screen, (82, 69, 66), brick)
                pygame.draw.rect(screen, (132, 109, 97), brick, 2)
                pygame.draw.line(screen, (47, 39, 40), (brick.x + 8, brick.bottom - 4), (brick.right - 5, brick.y + 5), 1)
        pygame.draw.line(screen, (187, 165, 143), (r.x, r.y), (r.right, r.y), 4)

    def draw_case(self, screen, r):
        pygame.draw.rect(screen, (17, 23, 30), r)
        pygame.draw.rect(screen, (104, 117, 126), r, 4)
        pygame.draw.line(screen, (46, 58, 67), (r.x, r.centery), (r.right, r.centery), 3)
        for x in (r.x + 8, r.right - 8):
            pygame.draw.rect(screen, (148, 155, 155), (x - 4, r.centery - 6, 8, 12))
            draw_rivet(screen, x, r.y + 8)
            draw_rivet(screen, x, r.bottom - 8)
        pygame.draw.rect(screen, (7, 12, 18), (r.centerx - 14, r.centery - 5, 28, 10))
        pygame.draw.rect(screen, AMBER, (r.centerx - 2, r.centery - 3, 4, 6))

    def draw_amp(self, screen, r):
        pygame.draw.rect(screen, (9, 11, 15), r)
        pygame.draw.rect(screen, (112, 119, 122), r, 4)
        pygame.draw.rect(screen, (25, 29, 33), (r.x + 7, r.y + 8, r.w - 14, r.h - 15))
        speaker_y = r.centery + 3
        for x in range(r.x + 27, r.right - 12, 42):
            pygame.draw.circle(screen, (4, 7, 11), (x, speaker_y), min(15, r.h // 3))
            pygame.draw.circle(screen, (48, 57, 63), (x, speaker_y), min(15, r.h // 3), 3)
            pygame.draw.circle(screen, (13, 19, 25), (x, speaker_y), 5)
        pygame.draw.rect(screen, (51, 55, 55), (r.x + 8, r.y + 5, r.w - 16, 8))
        for x in range(r.x + 18, min(r.right - 8, r.x + 70), 13):
            pygame.draw.circle(screen, AMBER, (x, r.y + 9), 2)

    def draw_pipe(self, screen, r):
        pygame.draw.rect(screen, (38, 51, 62), r, border_radius=r.h // 2)
        pygame.draw.line(screen, (143, 158, 163), (r.x + 12, r.y + 6), (r.right - 12, r.y + 6), 4)
        pygame.draw.line(screen, (13, 21, 29), (r.x + 12, r.bottom - 5), (r.right - 12, r.bottom - 5), 4)
        for x in (r.x + 18, r.right - 18):
            pygame.draw.rect(screen, (74, 87, 96), (x - 7, r.y - 4, 14, r.h + 8))
            pygame.draw.rect(screen, STEEL_LIGHT, (x - 7, r.y - 4, 14, r.h + 8), 2)
