"""Desenho dos menus e composição visual da partida."""

import pygame

from riffrun.paths import IMAGE_DIR
from riffrun.settings import FINAL_PHASE, HEIGHT, LEVEL_WIDTH, WIDTH
from riffrun.ui.hud import Hud
from riffrun.ui.victory import VictoryScreen


def load_background(path):
    try:
        image = pygame.image.load(str(path)).convert()
        return pygame.transform.smoothscale(
            image, (WIDTH, HEIGHT)
        )
    except (pygame.error, FileNotFoundError):
        return None


def menu_card_rects():
    """Áreas clicáveis sobre os cards da imagem."""

    return [
        pygame.Rect(100, 194, 356, 433),
        pygame.Rect(474, 194, 336, 433),
        pygame.Rect(826, 194, 359, 433),
    ]


def home_button_rects():
    """
    Áreas clicáveis dos botões da imagem inicial.

    Coordenadas ajustadas para 1280x720.
    """

    return {
        "play": pygame.Rect(480, 308, 320, 65),
        "options": pygame.Rect(492, 387, 296, 60),
        "credits": pygame.Rect(492, 458, 296, 60),
        "quit": pygame.Rect(492, 529, 296, 60),
    }


class GameView:
    def __init__(self, screen):
        self.screen = screen
        first_background = load_background(IMAGE_DIR / "visualFase1.png")
        backgrounds = (
            first_background,
            load_background(IMAGE_DIR / "visualFase2.png") or first_background,
            load_background(IMAGE_DIR / "visualFase3.png") or first_background,
        )
        tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.stage_backgrounds = []
        for background, color in zip(backgrounds, ((0, 0, 0), (42, 8, 8), (7, 28, 35))):
            if background is None:
                canvas = pygame.Surface((WIDTH, HEIGHT)).convert()
                canvas.fill((9, 13, 25))
            else:
                canvas = background.copy()
            tint.fill((*color, 24))
            canvas.blit(tint, (0, 0))
            self.stage_backgrounds.append(canvas)
        self.stage_haze = pygame.Surface((WIDTH, 110), pygame.SRCALPHA)
        self.stage_haze.fill((24, 37, 58, 38))
        self.home_background = load_background(IMAGE_DIR / "menu_inicial.png")
        self.phase_menu_background = load_background(IMAGE_DIR / "menu_fases.png")
        self.hud = Hud()
        self.victory_screen = VictoryScreen()
        self.defeat_screen = VictoryScreen(defeated=True)
        self.lock_font = pygame.font.SysFont("consolas", 27, bold=True)
        self.title_font = pygame.font.SysFont("consolas", 42, bold=True)
        self.text_font = pygame.font.SysFont("consolas", 23)

    def draw_background(self, camera_x, phase_number=1):
        screen = self.screen

        screen.blit(self.stage_backgrounds[phase_number - 1], (0, 0))

        # Parallax do cenário
        parallax = int(camera_x * 0.22)
        spacing = 310

        for i in range(-1, 7):

            x = i * spacing - (parallax % spacing)

            pygame.draw.rect(
                screen,
                (11, 17, 28),
                (x, 515, 14, 125)
            )

            pygame.draw.rect(
                screen,
                (43, 53, 66),
                (x + 3, 515, 3, 125)
            )

            pygame.draw.line(
                screen,
                (35, 45, 58),
                (x, 530),
                (x + 118, 640),
                4
            )

            pygame.draw.line(
                screen,
                (20, 28, 41),
                (x + 118, 530),
                (x, 640),
                4
            )

        screen.blit(self.stage_haze, (0, 530))

    def draw_map_menu(self, selected_phase, unlocked_phases):
        """Desenha a seleção de fases usando a imagem personalizada."""
        screen = self.screen

        if self.phase_menu_background is not None:
            screen.blit(self.phase_menu_background, (0, 0))
        else:
            screen.fill((12, 18, 30))

        cards = menu_card_rects()
        mouse_pos = pygame.mouse.get_pos()

        for index, rect in enumerate(cards):

            unlocked = index < unlocked_phases
            selected = index == selected_phase
            hovered = rect.collidepoint(mouse_pos)

            # Escurece as fases ainda bloqueadas.
            if not unlocked:

                overlay = pygame.Surface(
                    rect.size,
                    pygame.SRCALPHA
                )

                overlay.fill((0, 0, 0, 145))

                screen.blit(
                    overlay,
                    rect.topleft
                )

                label = self.lock_font.render(
                    "BLOQUEADA",
                    True,
                    (225, 220, 220)
                )

                label_rect = label.get_rect(
                    center=rect.center
                )

                screen.blit(label, label_rect)

            # Destaca a fase selecionada.
            elif selected or hovered:

                pygame.draw.rect(
                    screen,
                    (255, 220, 135),
                    rect.inflate(-8, -8),
                    3,
                    border_radius=8
                )

    def draw_info_panel(self, title, lines):
        """Desenha um painel informativo sobre o menu inicial."""
        screen = self.screen

        self.draw_home()

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 185))

        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(
            WIDTH // 2 - 290,
            HEIGHT // 2 - 190,
            580,
            380
        )

        pygame.draw.rect(
            screen,
            (19, 25, 39),
            panel,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (200, 75, 65),
            panel,
            3,
            border_radius=12
        )

        title_image = self.title_font.render(
            title,
            True,
            (245, 235, 225)
        )

        screen.blit(
            title_image,
            title_image.get_rect(
                centerx=panel.centerx,
                top=panel.y + 32
            )
        )

        for index, line in enumerate(lines):

            text_image = self.text_font.render(
                line,
                True,
                (220, 225, 235)
            )

            screen.blit(
                text_image,
                text_image.get_rect(
                    centerx=panel.centerx,
                    top=panel.y + 120 + index * 42
                )
            )

        hint = self.text_font.render(
            "ESC - VOLTAR",
            True,
            (235, 155, 110)
        )

        screen.blit(
            hint,
            hint.get_rect(
                centerx=panel.centerx,
                bottom=panel.bottom - 22
            )
        )

    def draw_home(self):
        """Desenha o menu inicial."""
        screen = self.screen

        if self.home_background is not None:
            screen.blit(self.home_background, (0, 0))
        else:
            screen.fill((12, 18, 30))

        # Destaca discretamente o botão sob o mouse.
        mouse_pos = pygame.mouse.get_pos()

        for rect in home_button_rects().values():

            if rect.collidepoint(mouse_pos):

                highlight_rect = rect.inflate(-6, -6)

                highlight = pygame.Surface(
                    highlight_rect.size,
                    pygame.SRCALPHA
                )

                pygame.draw.rect(
                    highlight,
                    (255, 255, 255, 28),
                    highlight.get_rect(),
                    border_radius=18
                )

                screen.blit(highlight, highlight_rect.topleft)

                break

    def draw_playing(self, player, level, phase_number, victory, game_over):
        camera_x = 0
        if phase_number == FINAL_PHASE:
            level.draw_background(self.screen)
        else:
            camera_x = max(0, min(player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))
            self.draw_background(camera_x, phase_number)

        level.draw(self.screen, camera_x)
        player.draw(self.screen, camera_x)
        self.hud.draw(self.screen, player, phase_number)

        if victory:
            self.victory_screen.draw(self.screen, level.run_score.result, phase_number)
        if game_over and player.death_tick >= 50:
            self.defeat_screen.draw(self.screen, level.run_score.result, phase_number)
