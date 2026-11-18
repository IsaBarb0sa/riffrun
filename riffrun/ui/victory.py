"""Resultado da tentativa sobre a arte de vitória."""

from math import cos, pi, sin

import pygame

from riffrun.paths import IMAGE_DIR
from riffrun.settings import COLLECTIBLES_PER_PHASE, FINAL_PHASE, HEIGHT, WIDTH


class VictoryScreen:
    def __init__(self, defeated=False):
        self.defeated = defeated
        filename = "derrota.png" if defeated else "vitoria.png"
        path = IMAGE_DIR / filename
        image = pygame.image.load(str(path)).convert_alpha()
        self.scale = min(WIDTH * 0.75 / image.get_width(), HEIGHT * 0.80 / image.get_height())
        self.image = pygame.transform.smoothscale(image, (
            round(image.get_width() * self.scale), round(image.get_height() * self.scale)))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.value_font = pygame.font.SysFont("consolas", round(44 * self.scale), bold=True)
        self.small_font = pygame.font.SysFont("consolas", round(27 * self.scale), bold=True)
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 140))
        self.final_image = None
        if not defeated:
            path = IMAGE_DIR / "final.png"
            self.final_image = pygame.transform.smoothscale(
                pygame.image.load(str(path)).convert(), (WIDTH, HEIGHT))

    def point(self, x, y):
        return self.rect.x + round(x * self.scale), self.rect.y + round(y * self.scale)

    def draw_stars(self, screen, stars, center):
        radius = round(31 * self.scale)
        spacing = round(80 * self.scale)
        for index in range(3):
            x = center[0] + (index - 1) * spacing
            y = center[1]
            points = []
            for point in range(10):
                angle = point * pi / 5 - pi / 2
                distance = radius if point % 2 == 0 else radius * 0.47
                points.append((round(x + cos(angle) * distance), round(y + sin(angle) * distance)))

            earned = index < stars
            fill = (241, 156, 38) if earned else (38, 42, 54)
            outline = (255, 221, 138) if earned else (112, 119, 137)
            pygame.draw.polygon(screen, (10, 11, 17), [(px, py + 2) for px, py in points])
            pygame.draw.polygon(screen, fill, points)
            pygame.draw.polygon(screen, outline, points, 2)

    def draw(self, screen, result, phase_number):
        if phase_number == FINAL_PHASE and not self.defeated:
            screen.blit(self.final_image, (0, 0))
            self.draw_stars(screen, result.stars, (WIDTH // 2, HEIGHT - 104))
            score = f"{result.total:,}".replace(",", ".")
            stats = self.value_font.render(f"{result.time_text}  |  {score} PTS", True, (255, 226, 157))
            screen.blit(stats, stats.get_rect(center=(WIDTH // 2, HEIGHT - 62)))
            hint = self.small_font.render("ENTER: FASES  |  R: NOVO DUELO", True, (235, 235, 245))
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 16)))
            return
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.image, self.rect)
        self.draw_stars(screen, result.stars, self.point(768, 508))
        for value, y in ((result.time_text, 650),
                         ("—" if phase_number == 4 else f"{result.riffs:02d}/{COLLECTIBLES_PER_PHASE}", 720),
                         (f"{result.total:,}".replace(",", "."), 794)):
            text = self.value_font.render(value, True, (255, 226, 157))
            screen.blit(text, text.get_rect(midright=self.point(1100, y)))
        detail = (f"RIFFS: {result.riff_points}  |  SEM BÔNUS DE CONCLUSÃO" if self.defeated
                  else f"RIFFS: {result.riff_points}  +  BÔNUS TEMPO: {result.time_bonus}")
        bonus = self.small_font.render(
            detail,
            True, (225, 232, 240))
        screen.blit(bonus, bonus.get_rect(center=self.point(768, 552)))
        if self.defeated:
            controls = "R: TENTAR NOVAMENTE  |  ESC: FASES"
        elif phase_number < 4:
            controls = "ENTER: PRÓXIMA FASE  |  R: REPETIR  |  M: FASES"
        else:
            controls = "ENTER: FASES  |  R: REPETIR"
        hint = self.small_font.render(controls, True, (235, 235, 240))
        screen.blit(hint, hint.get_rect(center=self.point(768, 935)))
        status = f"FASE {phase_number + 1} LIBERADA" if phase_number < 3 else "TODAS AS FASES CONCLUÍDAS"
        if phase_number == 3:
            status = "GUSTAVO AGUARDA NO PALCO FINAL"
        elif phase_number == 4:
            status = "GUSTAVO DERROTADO — O PALCO É SEU!"
        if self.defeated:
            status = f"FASE {phase_number}  |  MAIS UMA TENTATIVA!"
        text = self.small_font.render(status, True, (135, 235, 185))
        screen.blit(text, text.get_rect(center=self.point(768, 585)))
