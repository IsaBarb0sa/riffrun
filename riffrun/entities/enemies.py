"""Inimigos terrestres e aereos da campanha."""
from functools import lru_cache

import pygame

from riffrun.entities.effects import begin_defeat, draw_defeat, draw_enemy_health, grounded_sprite, update_defeat
from riffrun.paths import IMAGE_DIR
from riffrun.stages.platforms import draw_rivet


@lru_cache(maxsize=4)
def load_enemy_frames(filename, frame_size):

    path = (
        IMAGE_DIR
        / filename
    )

    sheet = pygame.image.load(str(path)).convert_alpha()

    sheet_width, sheet_height = sheet.get_size()

    frames = []

    for row in range(2):
        for col in range(4):

            left = round(col * sheet_width / 4)
            right = round((col + 1) * sheet_width / 4)

            top = round(row * sheet_height / 2)
            bottom = round((row + 1) * sheet_height / 2)

            frame = sheet.subsurface(
                (
                    left,
                    top,
                    right - left,
                    bottom - top
                )
            ).copy()

            frame = pygame.transform.scale(
                frame,
                frame_size
            )

            frames.append(frame)

    return frames


@lru_cache(maxsize=1)
def load_cloud_frames():
    """Carrega as animações da nuvem de relâmpagos."""

    path = (
        IMAGE_DIR
        / "nuvem_relampago_atlas.png"
    )

    sheet = pygame.image.load(str(path)).convert_alpha()

    # Recortes: x, y, largura, altura.
    # Cinco poses de voo e uma de ataque.
    frame_rects = [
        (0, 0, 305, 320),
        (305, 0, 300, 320),
        (605, 0, 290, 320),
        (895, 0, 305, 320),
        (1200, 0, 336, 320),
        (305, 340, 310, 290),
    ]

    frames = []

    for rect in frame_rects:
        frame = sheet.subsurface(rect).copy()

        bounds = frame.get_bounding_rect(min_alpha=10)

        if bounds.width == 0 or bounds.height == 0:
            raise ValueError(
                f"Recorte vazio no spritesheet da nuvem: {rect}"
            )

        frame = frame.subsurface(bounds).copy()

        # Mantém a proporção original da nuvem.
        scale = min(
            112 / frame.get_width(),
            96 / frame.get_height()
        )

        new_size = (
            max(1, round(frame.get_width() * scale)),
            max(1, round(frame.get_height() * scale))
        )

        frame = pygame.transform.scale(frame, new_size)

        canvas = pygame.Surface((112, 96), pygame.SRCALPHA)

        canvas.blit(
            frame,
            frame.get_rect(center=(56, 48))
        )

        frames.append(canvas)

    return frames


@lru_cache(maxsize=1)
def load_cloud_effects():
    """
    Carrega os efeitos especiais da nuvem:
    - Projétil elétrico
    - Quatro quadros da animação de derrota
    """

    path = (
        IMAGE_DIR
        / "nuvem_relampago_atlas.png"
    )

    sheet = pygame.image.load(str(path)).convert_alpha()

    def crop_effect(rect, max_width, max_height):
        image = sheet.subsurface(rect).copy()

        bounds = image.get_bounding_rect(min_alpha=10)

        if bounds.width == 0 or bounds.height == 0:
            raise ValueError(f"Efeito vazio: {rect}")

        image = image.subsurface(bounds).copy()

        scale = min(
            max_width / image.get_width(),
            max_height / image.get_height()
        )

        size = (
            max(1, round(image.get_width() * scale)),
            max(1, round(image.get_height() * scale))
        )

        return pygame.transform.scale(image, size)

    # Raio da terceira linha do spritesheet.
    lightning = crop_effect(
        (890, 630, 205, 115),
        42,
        25
    )

    # Sequência de desaparecimento da quarta linha.
    death_rects = [
        (0, 750, 310, 274),
        (350, 750, 380, 274),
        (740, 750, 280, 274),
        (1020, 750, 260, 274),
    ]

    death_frames = [
        crop_effect(rect, 112, 96)
        for rect in death_rects
    ]

    return lightning, death_frames


@lru_cache(maxsize=1)
def load_bone_bat_frames():
    """Seis poses completas do atlas exclusivo do morcego ósseo."""
    path = IMAGE_DIR / "morcego_osseo_fase3_atlas.png"
    sheet = pygame.image.load(str(path)).convert_alpha()
    rects = ((12, 459, 325, 156), (347, 495, 318, 159),
             (676, 485, 314, 170), (1022, 459, 331, 191),
             (1380, 509, 296, 162), (1741, 520, 417, 151))
    frames = []
    scale = 125 / 417
    for rect in rects:
        frame = sheet.subsurface(rect).copy()
        frame = pygame.transform.smoothscale(frame, (round(rect[2] * scale), round(rect[3] * scale)))
        canvas = pygame.Surface((132, 96), pygame.SRCALPHA)
        canvas.blit(frame, frame.get_rect(center=(66, 48)))
        frames.append(canvas)
    return frames


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__()
        self.rect = pygame.Rect(x, y, 46, 46)
        self.x = float(x)
        self.speed = 2
        self.min_x = min_x
        self.max_x = max_x
        self.alive = True

    def take_hit(self):
        if not self.alive:
            return
        image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        original_rect = self.rect
        self.rect = image.get_rect()
        self.draw(image, 0)
        self.rect = original_rect
        self.alive = False
        begin_defeat(self, image)

    def update(self):
        if not self.alive:
            update_defeat(self)
            return

        self.x += self.speed
        if self.x <= self.min_x or self.x + self.rect.width >= self.max_x:
            self.speed *= -1
            self.x += self.speed

        self.rect.x = round(self.x)

    def draw(self, screen, camera_x):
        if not self.alive:
            draw_defeat(self, screen, camera_x)
            return

        r = self.rect.move(-camera_x, 0)
        # Caixa de som possuída: mantém a hitbox simples, mas combina com o palco.
        pygame.draw.rect(screen, (11, 15, 20), r, border_radius=4)
        pygame.draw.rect(screen, (111, 119, 124), r, 3, border_radius=4)
        pygame.draw.circle(screen, (41, 50, 58), (r.centerx, r.y + 28), 12)
        pygame.draw.circle(screen, (5, 8, 12), (r.centerx, r.y + 28), 6)
        pygame.draw.polygon(screen, (219, 59, 54), [
            (r.x + 8, r.y + 10), (r.x + 18, r.y + 13), (r.x + 9, r.y + 16)
        ])
        pygame.draw.polygon(screen, (219, 59, 54), [
            (r.right - 8, r.y + 10), (r.right - 18, r.y + 13), (r.right - 9, r.y + 16)
        ])
        for x in (r.x + 5, r.right - 5):
            draw_rivet(screen, x, r.y + 5)
            draw_rivet(screen, x, r.bottom - 5)


class SpiderEnemy(Enemy):
    """Aranha de contato que percorre um trecho inteiro de chão."""

    @staticmethod
    @lru_cache(maxsize=1)
    def load_frames():
        path = IMAGE_DIR / "aranha_fase1.png"
        sheet = pygame.image.load(str(path)).convert_alpha()
        frames = []
        for index in range(4):
            left = round(index * sheet.get_width() / 4)
            right = round((index + 1) * sheet.get_width() / 4)
            frame = sheet.subsurface((left, 0, right - left, sheet.get_height()))
            frame = frame.subsurface(frame.get_bounding_rect(min_alpha=20)).copy()
            scale = min(96 / frame.get_width(), 54 / frame.get_height())
            frame = pygame.transform.smoothscale(
                frame, (round(frame.get_width() * scale), round(frame.get_height() * scale)))
            canvas = pygame.Surface((96, 54), pygame.SRCALPHA)
            canvas.blit(frame, frame.get_rect(midbottom=(48, 54)))
            frames.append(canvas)
        return frames

    def __init__(self, x, ground_y, min_x, max_x):
        super().__init__(x, ground_y - 50, min_x, max_x)
        self.rect.size = (96, 50)
        self.x = float(max(min_x, min(x, max_x - self.rect.width)))
        self.rect.x = round(self.x)
        self.speed = 1.6
        self.direction = -1
        self.animation_tick = 0
        self.frames = self.load_frames()

    def update(self):
        if not self.alive:
            update_defeat(self)
            return
        self.animation_tick += 1
        self.x += self.speed * self.direction
        if self.x <= self.min_x:
            self.x = float(self.min_x)
            self.direction = 1
        elif self.x >= self.max_x - self.rect.width:
            self.x = float(self.max_x - self.rect.width)
            self.direction = -1
        self.rect.x = round(self.x)

    def current_frame(self):
        frame = self.frames[(self.animation_tick // 7) % len(self.frames)]
        # O atlas original está olhando para a esquerda.
        return pygame.transform.flip(frame, True, False) if self.direction > 0 else frame

    def take_hit(self):
        if self.alive:
            self.alive = False
            begin_defeat(self, self.current_frame())

    def draw(self, screen, camera_x):
        if not self.alive:
            draw_defeat(self, screen, camera_x)
            return
        frame = self.current_frame()
        screen.blit(frame, frame.get_rect(midbottom=(self.rect.centerx - camera_x,
                                                      self.rect.bottom)))


class FlyingEnemy(pygame.sprite.Sprite):
    """
    Morcego guitarrista.

    Comportamentos:
    - Patrulha aérea
    - Flutuação
    - Mergulho contra o jogador
    - Disparo de projéteis
    """

    PROJECTILE_SOUND = "enemy_shot"

    def __init__(self, x, y, min_x, max_x):
        super().__init__()

        self.rect = pygame.Rect(x, y, 58, 48)

        self.x = float(x)
        self.y = float(y)
        self.base_y = float(y)

        self.min_x = min_x
        self.max_x = max_x

        self.speed = 2.2
        self.direction = 1

        self.health = 1
        self.alive = True
        self.hurt_timer = 0

        # Animação
        self.animation_tick = 0
        self.animation_index = 0

        # Flutuação
        self.float_timer = 0

        # Inteligência
        self.state = "patrol"

        self.detection_range = 280
        self.attack_cooldown = 0

        # Mergulho
        self.dive_timer = 0
        self.dive_target = pygame.Vector2(x, y)

        # Projéteis
        self.projectiles = []
        self.projectile_speed = 5

        self.frames = self.load_frames()

    @staticmethod
    def load_frames():
        return load_enemy_frames("morcego_guitarrista_atlas.png", (112, 96))

    # ATUALIZAÇÃO

    def update(self, player=None, *, play_sfx=None):

        if not self.alive:
            update_defeat(self)
            return

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        # Cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Atualiza projéteis
        self.update_projectiles()

        # Patrulha
        if self.state == "patrol":

            self.update_patrol()

            # Detecta jogador
            if player is not None:

                distance_x = abs(
                    player.rect.centerx - self.rect.centerx
                )

                distance_y = abs(
                    player.rect.centery - self.rect.centery
                )

                if (
                    distance_x <= self.detection_range
                    and distance_y <= 260
                    and self.attack_cooldown == 0
                ):

                    self.start_attack(player)
                    if play_sfx:
                        play_sfx("enemy_dive" if self.state == "dive" else self.PROJECTILE_SOUND)

        # Mergulho
        elif self.state == "dive":

            self.update_dive()

        # Retorno
        elif self.state == "return":

            self.update_return()

        self.update_animation()

    # PATRULHA

    def update_patrol(self):

        self.x += self.speed * self.direction

        if self.x <= self.min_x:

            self.x = self.min_x
            self.direction = 1

        elif self.x + self.rect.width >= self.max_x:

            self.x = self.max_x - self.rect.width
            self.direction = -1

        self.float_timer += 0.08

        import math

        floating = math.sin(self.float_timer) * 15

        self.y = self.base_y + floating

        self.rect.topleft = (
            round(self.x),
            round(self.y)
        )

    # DECISÃO DO ATAQUE

    def start_attack(self, player):

        self.attack_cooldown = 150

        # Olha na direção do jogador
        if player.rect.centerx < self.rect.centerx:
            self.direction = -1
        else:
            self.direction = 1

        # Alterna os tipos de ataque
        if not hasattr(self, "attack_count"):
            self.attack_count = 0

        self.attack_count += 1

        if self.attack_count % 2 == 1:

            # Ataque de mergulho
            self.state = "dive"
            self.dive_timer = 35

            self.dive_target = pygame.Vector2(
                player.rect.center
            )

        else:

            # Ataque de projétil
            self.shoot(player)

    # MERGULHO

    def update_dive(self):

        if self.dive_timer <= 0:

            self.state = "return"
            return

        current = pygame.Vector2(
            self.rect.center
        )

        direction = self.dive_target - current

        if direction.length_squared() > 0:

            direction = direction.normalize()

            current += direction * 8

            self.rect.center = (
                round(current.x),
                round(current.y)
            )

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.dive_timer -= 1

        if self.dive_timer <= 0:
            self.state = "return"

    # RETORNAR À ALTURA ORIGINAL

    def update_return(self):

        target_y = self.base_y

        if self.y > target_y:

            self.y -= 4

            if self.y < target_y:
                self.y = target_y

        elif self.y < target_y:

            self.y += 4

            if self.y > target_y:
                self.y = target_y

        self.rect.y = round(self.y)

        if abs(self.y - target_y) < 2:

            self.state = "patrol"

    # PROJÉTEIS

    def shoot(self, player):

        origin = pygame.Vector2(
            self.rect.center
        )

        target = pygame.Vector2(
            player.rect.center
        )

        direction = target - origin

        if direction.length_squared() == 0:
            direction = pygame.Vector2(
                self.direction, 0
            )

        direction = direction.normalize()

        projectile = {
            "pos": origin.copy(),
            "velocity": direction * self.projectile_speed,
            "rect": pygame.Rect(0, 0, 14, 14),
            "lifetime": 120,
        }

        projectile["rect"].center = (
            round(origin.x),
            round(origin.y)
        )

        self.projectiles.append(projectile)

    def update_projectiles(self):

        for projectile in self.projectiles[:]:

            projectile["pos"] += projectile["velocity"]

            projectile["rect"].center = (
                round(projectile["pos"].x),
                round(projectile["pos"].y)
            )

            projectile["lifetime"] -= 1

            if projectile["lifetime"] <= 0:

                self.projectiles.remove(projectile)

    # DANO

    def take_hit(self):

        if not self.alive:
            return

        self.health -= 1
        self.hurt_timer = 16

        if self.health <= 0:

            self.alive = False
            self.projectiles.clear()
            image = self.frames[min(6, len(self.frames) - 1)]
            if self.direction < 0:
                image = pygame.transform.flip(image, True, False)
            begin_defeat(self, image)

    # ANIMAÇÃO

    def update_animation(self):

        self.animation_tick += 1

        if self.hurt_timer > 0:
            self.animation_index = min(6, len(self.frames) - 1)

        elif self.state == "dive":

            self.animation_index = 4

        elif self.attack_cooldown > 120:

            if self.attack_count % 2 == 0:
                self.animation_index = 5
            else:
                self.animation_index = 4

        elif self.animation_tick >= 9:

            self.animation_tick = 0

            self.animation_index = (
                self.animation_index + 1
            ) % 4

    # DESENHO

    def draw(self, screen, camera_x):

        if not self.alive:
            draw_defeat(self, screen, camera_x)
            return

        frame = self.frames[self.animation_index]

        if self.direction < 0:

            frame = pygame.transform.flip(
                frame, True, False
            )

        draw_rect = frame.get_rect(
            center=self.rect.center
        )

        draw_rect.x -= camera_x

        screen.blit(frame, draw_rect)

        # Desenha os projéteis
        for projectile in self.projectiles:

            r = projectile["rect"].move(
                -camera_x, 0
            )

            pygame.draw.circle(
                screen,
                (214, 65, 219),
                r.center,
                8
            )

            pygame.draw.circle(
                screen,
                (255, 152, 255),
                r.center,
                4
            )


class BoneBatEnemy(FlyingEnemy):
    """
    Morcego ósseo da fase 3.

    Mantém as mecânicas do FlyingEnemy:
    - Patrulha aérea
    - Detecção do jogador
    - Investida
    - Disparo de projéteis
    """

    PROJECTILE_SOUND = "bone_shot"
    load_frames = staticmethod(load_bone_bat_frames)

    def __init__(self, x, y, min_x, max_x):
        super().__init__(x, y, min_x, max_x)
        # Um pouco mais rápido para aumentar o desafio.
        self.speed = 2.6
        # Distância de detecção.
        self.detection_range = 300
        # Velocidade dos disparos.
        self.projectile_speed = 5.5
        self.bone_sprite = pygame.Surface((34, 18), pygame.SRCALPHA)
        # Osso com haste e duas articulações, em vez de um losango.
        for color, radius, thickness in (((65, 55, 58), 5, 9),
                                         ((230, 221, 195), 3, 5)):
            pygame.draw.line(self.bone_sprite, color, (7, 9), (27, 9), thickness)
            for x in (5, 28):
                for y in (5, 12):
                    pygame.draw.circle(self.bone_sprite, color, (x, y), radius)
        pygame.draw.line(self.bone_sprite, (255, 247, 220), (9, 7), (24, 7), 2)

    def shoot(self, player):
        super().shoot(player)
        projectile = self.projectiles[-1]
        center = projectile["rect"].center
        projectile["rect"].size = (24, 12)
        projectile["rect"].center = center

    def draw(self, screen, camera_x):

        if not self.alive:
            draw_defeat(self, screen, camera_x)
            return

        # Desenha o morcego.
        frame = self.frames[self.animation_index]

        if self.direction < 0:
            frame = pygame.transform.flip(
                frame,
                True,
                False
            )

        draw_rect = frame.get_rect(
            center=self.rect.center
        )

        draw_rect.x -= camera_x
        screen.blit(frame, draw_rect)

        # O osso gira em torno do próprio centro durante o voo.
        for projectile in self.projectiles:
            angle = -pygame.Vector2(projectile["velocity"]).as_polar()[1]
            angle += (120 - projectile["lifetime"]) * 12
            image = pygame.transform.rotate(self.bone_sprite, angle)
            center = (projectile["rect"].centerx - camera_x, projectile["rect"].centery)
            screen.blit(image, image.get_rect(center=center))


class HeavyEnemy(pygame.sprite.Sprite):
    """
    Robô Roadie.

    Inimigo pesado com:
    - 3 pontos de vida
    - Patrulha
    - Detecção do jogador
    - Investida
    - Animação de dano e derrota
    """

    MAX_HEALTH = 3

    def __init__(
            self,
            x,
            y,
            min_x,
            max_x,
            charge_min_x=None,
            charge_max_x=None
    ):
        super().__init__()

        self.rect = pygame.Rect(x, y, 76, 92)

        self.x = float(x)

        self.min_x = min_x
        self.max_x = max_x

        # Limites separados para a investida
        self.charge_min_x = (
            charge_min_x
            if charge_min_x is not None
            else min_x
        )

        self.charge_max_x = (
            charge_max_x
            if charge_max_x is not None
            else max_x
        )

        self.speed = 1.1
        self.charge_speed = 5.2

        self.direction = 1

        self.health = self.MAX_HEALTH
        self.alive = True

        self.state = "patrol"

        self.detection_range = 240

        self.charge_timer = 0
        self.attack_cooldown = 0

        # Tempo de preparação antes da investida
        self.windup_timer = 0

        # Tempo de recuperação após atacar
        self.recovery_timer = 0

        self.hurt_timer = 0
        self.death_timer = 0

        self.animation_tick = 0
        self.animation_index = 0

        self.frames = load_enemy_frames(
            "robo_roadie_atlas.png",
            (192, 192)
        )
        self.health_bar_offset = max(
            frame.get_bounding_rect(min_alpha=10).height for frame in self.frames
        ) + 8

    # ATUALIZAÇÃO

    def update(self, player=None, *, play_sfx=None):
        if not self.alive:
            update_defeat(self)
            return

        # Atualiza cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Atualiza animação de dano
        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        # Patrulha
        if self.state == "patrol":
            self.update_patrol()
            if player is not None:
                self.detect_player(player)

        # Preparação
        elif self.state == "windup":
            self.update_windup()
            if self.state == "charge" and play_sfx:
                play_sfx("enemy_charge")

        # Investida
        elif self.state == "charge":
            self.update_charge()

        # Recuperação
        elif self.state == "recovery":
            self.update_recovery()

        self.update_animation()

    # PATRULHA

    def update_patrol(self):

        self.x += self.speed * self.direction

        self.check_patrol_limits()

        self.rect.x = round(self.x)

    def check_patrol_limits(self):

        if self.x <= self.min_x:

            self.x = self.min_x
            self.direction = 1

        elif self.x + self.rect.width >= self.max_x:

            self.x = self.max_x - self.rect.width
            self.direction = -1

    # DETECÇÃO DO JOGADOR

    def detect_player(self, player):

        distance_x = abs(
            player.rect.centerx - self.rect.centerx
        )

        distance_y = abs(
            player.rect.centery - self.rect.centery
        )

        if (
            distance_x <= self.detection_range
            and distance_y <= 100
            and self.attack_cooldown == 0
            and self.hurt_timer == 0
        ):

            self.start_charge(player)

    # INVESTIDA

    def start_charge(self, player):
        # Primeiro entra em preparação
        self.state = "windup"
        # 30 frames = aproximadamente 0,5 segundo
        self.windup_timer = 30
        # Duração da investida
        self.charge_timer = 32
        # Cooldown entre ataques
        self.attack_cooldown = 150
        # Escolhe a direção do jogador
        if player.rect.centerx < self.rect.centerx:
            self.direction = -1

        else:
            self.direction = 1

    def update_charge(self):
        # Avança na direção escolhida
        self.x += (
                self.charge_speed * self.direction
        )

        # Limites seguros da investida
        if self.x <= self.charge_min_x:
            self.x = self.charge_min_x
            self.charge_timer = 0
        elif (
                self.x + self.rect.width
                >= self.charge_max_x
        ):
            self.x = (
                    self.charge_max_x
                    - self.rect.width
            )
            self.charge_timer = 0

        self.rect.x = round(self.x)
        self.charge_timer -= 1

        # Finaliza a investida
        if self.charge_timer <= 0:
            self.state = "recovery"
            self.recovery_timer = 35

    # RECEBER DANO

    def take_hit(self):

        if not self.alive:
            return

        self.health -= 1

        self.hurt_timer = 18
        self.animation_index = 6

        # Interrompe a investida
        self.state = "patrol"

        if self.health <= 0:

            self.alive = False

            image = self.frames[7]
            if self.direction < 0:
                image = pygame.transform.flip(image, True, False)
            begin_defeat(self, image)

    # ANIMAÇÃO

    def update_animation(self):
        self.animation_tick += 1

        # Recebendo dano
        if self.hurt_timer > 0:
            self.animation_index = 6

        # Preparando a investida
        elif self.state == "windup":
            self.animation_index = 0

        # Investida
        elif self.state == "charge":
            self.animation_index = 3

        # Recuperação
        elif self.state == "recovery":
            self.animation_index = 1

        # Patrulha
        elif self.animation_tick >= 10:
            self.animation_tick = 0

            if self.animation_index == 0:
                self.animation_index = 2

            else:
                self.animation_index = 0

    # DESENHO

    def draw(self, screen, camera_x):

        if not self.alive:
            draw_defeat(self, screen, camera_x)
            return

        else:

            frame = self.frames[
                self.animation_index
            ]

        frame, visible_bottom = grounded_sprite(frame, self.direction < 0)
        draw_rect = frame.get_rect()
        draw_rect.x = self.rect.centerx - frame.get_width() // 2
        draw_rect.y = self.rect.bottom - visible_bottom

        draw_rect.x -= camera_x

        screen.blit(frame, draw_rect)
        draw_enemy_health(
            screen, (self.rect.centerx - camera_x, self.rect.bottom - self.health_bar_offset),
            self.health, self.MAX_HEALTH, (209, 117, 32), (255, 213, 122),
        )

    def update_windup(self):
        self.windup_timer -= 1

        if self.windup_timer <= 0:
            self.state = "charge"

    def update_recovery(self):
        self.recovery_timer -= 1

        if self.recovery_timer <= 0:
            self.state = "patrol"


class CloudEnemy(FlyingEnemy):
    """
    Nuvem elétrica da fase 1.

    Mecânicas:
    - Patrulha aérea
    - Detecção do jogador
    - Investida
    - Disparo elétrico
    - Animação de derrota
    """

    load_frames = staticmethod(load_cloud_frames)

    def __init__(self, x, y, min_x, max_x):
        super().__init__(x, y, min_x, max_x)


        self.lightning_sprite, self.death_frames = load_cloud_effects()

        # Movimento da nuvem.
        self.speed = 1.8

        # A nuvem detecta o jogador a uma distância maior.
        self.detection_range = 320

        # Os relâmpagos são mais rápidos.
        self.projectile_speed = 6.5

        # Animação de derrota.
        self.death_timer = 0
        self.death_duration = 32

    def take_hit(self):
        """Recebe dano e inicia a animação de desaparecimento."""

        if not self.alive:
            return

        super().take_hit()

        if not self.alive:
            self.death_timer = self.death_duration

    def update(self, player=None, *, play_sfx=None):
        """Atualiza o comportamento ou a animação de derrota."""

        if not self.alive:

            if self.death_timer > 0:
                self.death_timer -= 1

            return

        super().update(player, play_sfx=play_sfx)

    def draw(self, screen, camera_x):
        """Desenha a nuvem, os efeitos e os relâmpagos."""

        # Animação de desaparecimento.
        if not self.alive:

            if self.death_timer <= 0:
                return

            progress = 1 - (
                self.death_timer / self.death_duration
            )

            index = min(
                int(progress * len(self.death_frames)),
                len(self.death_frames) - 1
            )

            frame = self.death_frames[index]

            rect = frame.get_rect(
                center=self.rect.center
            )

            rect.x -= camera_x

            screen.blit(frame, rect)

            return

        # Animação normal.
        frame = self.frames[self.animation_index]

        if self.direction < 0:
            frame = pygame.transform.flip(
                frame,
                True,
                False
            )

        draw_rect = frame.get_rect(
            center=self.rect.center
        )

        draw_rect.x -= camera_x

        screen.blit(frame, draw_rect)

        # Desenha os disparos elétricos.
        for projectile in self.projectiles:

            lightning = self.lightning_sprite

            # O disparo acompanha a direção horizontal.
            if projectile["velocity"].x < 0:
                lightning = pygame.transform.flip(
                    lightning,
                    True,
                    False
                )

            rect = lightning.get_rect(
                center=projectile["rect"].center
            )

            rect.x -= camera_x

            screen.blit(lightning, rect)
