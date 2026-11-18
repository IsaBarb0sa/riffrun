"""Indicadores de vida e animacao de derrota dos inimigos."""
import pygame


def draw_enemy_health(screen, anchor, health, max_health, fill, highlight):
    segment_width = 20
    gap = 3
    width = max_health * segment_width + (max_health - 1) * gap + 8
    frame = pygame.Rect(0, 0, width, 16)
    frame.midbottom = anchor
    pygame.draw.rect(screen, (10, 8, 15), frame.inflate(4, 4))
    pygame.draw.rect(screen, (28, 23, 34), frame)
    pygame.draw.rect(screen, highlight, frame, 1)

    for index in range(max_health):
        segment = pygame.Rect(frame.x + 4 + index * (segment_width + gap),
                              frame.y + 4, segment_width, 8)
        pygame.draw.rect(screen, (57, 48, 62), segment)
        if index < health:
            pygame.draw.rect(screen, fill, segment)
            pygame.draw.rect(screen, highlight, (segment.x, segment.y, segment.width, 2))


def begin_defeat(enemy, image):
    enemy.death_timer = 55
    enemy.defeat_image = image.copy()
    enemy.defeat_pos = pygame.Vector2(enemy.rect.center)
    enemy.defeat_velocity = pygame.Vector2(-2 * getattr(enemy, "direction", 1), -5)


def update_defeat(enemy):
    if getattr(enemy, "death_timer", 0) > 0:
        enemy.death_timer -= 1
        enemy.defeat_velocity.y += 0.65
        enemy.defeat_pos += enemy.defeat_velocity


def draw_defeat(enemy, screen, camera_x):
    if getattr(enemy, "death_timer", 0) <= 0:
        return
    image = pygame.transform.rotate(enemy.defeat_image,
                                    max(0, 47 - enemy.death_timer) * 3)
    if enemy.death_timer > 47:
        image.fill((255, 120, 120, 255), special_flags=pygame.BLEND_RGBA_MULT)
    if enemy.death_timer < 15:
        image.set_alpha(enemy.death_timer * 17)
    screen.blit(image, image.get_rect(center=(round(enemy.defeat_pos.x - camera_x),
                                             round(enemy.defeat_pos.y))))
