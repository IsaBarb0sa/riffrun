"""Coordena eventos, simulação e transições entre as telas do jogo."""
import asyncio
import json
import os

import pygame

from riffrun.audio import AudioManager
from riffrun.stages.boss import BossArena
from riffrun.ui.game_view import GameView, home_button_rects, menu_card_rects
from riffrun.stages.level import Level
from riffrun.entities.player import Player
from riffrun.progress import load_unlocked_phases, save_unlocked_phases
from riffrun.settings import CAMPAIGN_PHASES, FINAL_PHASE, FPS, GROUND_Y, HEIGHT


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.audio = AudioManager()
        self.view = GameView(screen)
        self.selected_phase = 0
        self.unlocked_phases = load_unlocked_phases()
        self.running = True
        self.on_web = False
        self.mobile_web = False
        self.pending_phase = None
        self.enemies_hit_this_attack = set()
        self.start_phase(1)
        self.screen_mode = "home"

    def start_phase(self, phase_number):
        self.phase_number = phase_number
        if phase_number == FINAL_PHASE:
            self.player = Player(80, GROUND_Y - 70, FINAL_PHASE)
            self.level = BossArena(self.audio.boss_intro_duration_ms())
        else:
            self.player = Player(120, 500, phase_number)
            self.level = Level(phase_number)

        self.victory = False
        self.game_over = False
        self.enemies_hit_this_attack.clear()
        self.screen_mode = "playing"
        if phase_number == FINAL_PHASE and not self.on_web:
            self.audio.start_boss_intro()

    def request_phase(self, phase_number):
        if self.on_web:
            self.pending_phase = phase_number
        else:
            self.start_phase(phase_number)

    async def load_requested_phase(self):
        self.view.draw_loading()
        pygame.display.flip()
        await self.audio.fade_for_phase_change()
        await asyncio.sleep(0)

        self.start_phase(self.pending_phase)
        self.pending_phase = None
        self.draw()
        pygame.display.flip()
        await asyncio.sleep(0)

        if self.phase_number == FINAL_PHASE:
            self.audio.start_boss_intro()
        else:
            self.update_music()

    async def run(self, *, on_web=False):
        self.on_web = on_web
        controls = None
        if on_web:
            from platform import window

            controls = window.riffRunControls
        screenshot_path = os.environ.get("RIFF_RUN_SCREENSHOT")
        pending_time = 1000
        simulation_ticks = 0
        last_draw_tick = -2
        while self.running:
            # No navegador, dormir aqui bloqueia a thread do áudio e do desenho.
            frame_ms = self.clock.tick(0 if on_web else FPS)
            for event in pygame.event.get():
                if controls and event.type == pygame.MOUSEBUTTONDOWN and getattr(event, "touch", False):
                    continue
                self.handle_event(event)

            if controls:
                self.read_web_controls(controls)

            if self.pending_phase is not None and self.running:
                if controls:
                    controls.poll("loading")
                await self.load_requested_phase()
                self.clock.tick()
                pending_time = 1000
                continue

            if on_web:
                # Limita a recuperação após uma pausa longa ou troca de aba.
                pending_time = min(pending_time + frame_ms * FPS, 3000)
                steps, pending_time = divmod(pending_time, 1000)
                if not steps:
                    await asyncio.sleep(0)
                    continue
                for _ in range(steps):
                    previous_ms = simulation_ticks * 1000 // FPS
                    simulation_ticks += 1
                    self.update(simulation_ticks * 1000 // FPS - previous_ms)
            else:
                self.update(frame_ms)

            self.update_music()
            if self.mobile_web and simulation_ticks - last_draw_tick < 2:
                await asyncio.sleep(0)
                continue
            self.draw()
            pygame.display.flip()
            last_draw_tick = simulation_ticks

            if screenshot_path:
                pygame.image.save(self.screen, screenshot_path)
                self.running = False

            await asyncio.sleep(0)

    def read_web_controls(self, controls):
        mode = self.screen_mode
        if self.pending_phase is not None:
            mode = "loading"
        elif mode == "playing":
            if self.victory:
                mode = "victory"
            elif self.game_over:
                mode = "defeat"

        self.player.touch_input, actions, self.mobile_web = json.loads(controls.poll(mode))
        keys = {"back": pygame.K_ESCAPE, "retry": pygame.K_r, "next": pygame.K_RETURN,
                "mute": pygame.K_v}
        for action, x, y in actions:
            if action in ("attack", "select"):
                self.handle_event(pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, button=1,
                    pos=(int(x * self.screen.get_width()), int(y * self.screen.get_height())),
                ))
            else:
                self.handle_event(pygame.event.Event(pygame.KEYDOWN, key=keys[action]))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return
        if self.audio.handle_music_event(event):
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            self.audio.toggle_mute()
            return

        if self.pending_phase is not None:
            return

        if self.screen_mode == "home":
            self.handle_home_event(event)
        elif self.screen_mode in ("options", "credits"):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.screen_mode = "home"
        elif self.screen_mode == "menu":
            self.handle_menu_event(event)
        elif self.screen_mode == "playing":
            self.handle_playing_event(event)

    def handle_home_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.screen_mode = "menu"
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for action, rect in home_button_rects().items():
                if not rect.collidepoint(event.pos):
                    continue
                self.audio.play_sfx("menu_click")
                if action == "quit":
                    pygame.time.wait(60)
                    self.running = False
                else:
                    self.screen_mode = "menu" if action == "play" else action
                break

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.request_phase(FINAL_PHASE)
            elif event.key == pygame.K_ESCAPE:
                self.screen_mode = "home"
            elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
                self.selected_phase = (self.selected_phase - 1) % CAMPAIGN_PHASES
            elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT, pygame.K_d):
                self.selected_phase = (self.selected_phase + 1) % CAMPAIGN_PHASES
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.selected_phase < self.unlocked_phases:
                    self.request_phase(self.selected_phase + 1)
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                requested_phase = event.key - pygame.K_0
                if requested_phase <= self.unlocked_phases:
                    self.selected_phase = requested_phase - 1
                    self.request_phase(requested_phase)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, rect in enumerate(menu_card_rects()):
                if rect.collidepoint(event.pos):
                    self.audio.play_sfx("menu_click")
                    self.selected_phase = index
                    if index < self.unlocked_phases:
                        self.request_phase(index + 1)
                    break

    def handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.return_to_menu()
            elif (self.victory or self.game_over) and event.key == pygame.K_r:
                self.request_phase(self.phase_number)
            elif self.victory and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.audio.play_sfx("menu_click")
                if self.phase_number < FINAL_PHASE:
                    self.selected_phase = min(self.phase_number, CAMPAIGN_PHASES - 1)
                    self.request_phase(self.phase_number + 1)
                else:
                    self.return_to_menu()
            elif self.victory and event.key == pygame.K_m:
                self.return_to_menu(after_victory=True)
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
              and not self.victory and not self.game_over
              and not self.boss_intro_active and self.player.start_attack()):
            self.enemies_hit_this_attack.clear()
            self.audio.play_sfx("attack")

    def return_to_menu(self, *, after_victory=False):
        self.screen_mode = "menu"
        phase_index = self.phase_number if after_victory else self.phase_number - 1
        self.selected_phase = min(phase_index, CAMPAIGN_PHASES - 1)

    @property
    def boss_intro_active(self):
        return self.phase_number == FINAL_PHASE and self.level.boss.intro_timer > 0

    def update(self, frame_ms):
        if self.screen_mode != "playing":
            return
        if self.game_over:
            self.player.update_death(self.level.platforms)
            return
        if self.victory:
            return

        player, level = self.player, self.level
        if self.boss_intro_active:
            player.vel.update(0, 0)
            player.on_ground = True
            player.update_animation()
        else:
            level.run_score.advance(frame_ms)
            player.update(level.platforms, play_sfx=self.audio.play_sfx)

        if self.phase_number == FINAL_PHASE:
            level.update(player, intro_elapsed_ms=self.audio.boss_intro_elapsed_ms(),
                         play_sfx=self.audio.play_sfx)
        else:
            level.update(player, play_sfx=self.audio.play_sfx)

        hazard_sound = level.handle_hazards(player)
        if hazard_sound and player.health > 0:
            self.audio.play_sfx(hazard_sound)

        for guitar in level.guitars:
            if not guitar.collected and player.rect.colliderect(guitar.rect):
                guitar.collected = True
                player.score += 1
                self.audio.play_sfx("collect")

        self.resolve_player_attack()
        self.resolve_enemy_attacks()
        self.check_outcome()

        if self.game_over:
            player.update_death(level.platforms)

    def resolve_player_attack(self):
        attack_rect = self.player.get_attack_rect()
        if attack_rect is None:
            return

        hit_sounds = {}
        for enemy in self.level.enemies:
            if (not enemy.alive or enemy in self.enemies_hit_this_attack
                    or not attack_rect.colliderect(enemy.rect)):
                continue

            self.enemies_hit_this_attack.add(enemy)
            previous_health = getattr(enemy, "health", None)
            if hasattr(enemy, "take_hit"):
                enemy.take_hit()
            else:
                enemy.alive = False

            health = getattr(enemy, "health", None)
            if not enemy.alive:
                sound = "boss_death" if self.phase_number == FINAL_PHASE else "enemy_death"
                hit_sounds[sound] = None
            elif health != previous_health:
                hit_sounds["enemy_hit"] = None

        for sound in hit_sounds:
            self.audio.play_sfx(sound)

    def resolve_enemy_attacks(self):
        player = self.player
        for enemy in self.level.enemies:
            if not enemy.alive:
                continue
            for projectile in getattr(enemy, "projectiles", ())[:]:
                if player.rect.colliderect(projectile["rect"]):
                    self.damage_player()
                    if hasattr(enemy, "on_projectile_hit"):
                        enemy.on_projectile_hit(projectile)
                    enemy.projectiles.remove(projectile)

        for enemy in self.level.enemies:
            if not enemy.alive or not getattr(enemy, "can_damage", True):
                continue
            attack_rect = enemy.get_attack_rect() if hasattr(enemy, "get_attack_rect") else None
            if (player.rect.colliderect(enemy.rect)
                    or (attack_rect is not None and player.rect.colliderect(attack_rect))):
                self.damage_player()

    def damage_player(self):
        health_before = self.player.health
        self.player.take_damage()
        if 0 < self.player.health < health_before:
            self.audio.play_sfx("hurt")

    def check_outcome(self):
        player, level = self.player, self.level
        if player.rect.top > HEIGHT + 100:
            player.take_damage()
            if player.health > 0:
                self.audio.play_sfx("fall")
            player.pos.update(120, 500)
            player.rect.topleft = player.pos
            player.vel.update(0, 0)

        if player.health <= 0:
            self.audio.play_sfx("hurt")
            self.audio.play_sfx("defeat")
            self.game_over = True
            level.run_score.finish(player.score, completed=False)
            return

        if self.phase_number == FINAL_PHASE:
            reached_goal = not level.boss.alive and level.boss.death_timer <= 0
        else:
            reached_goal = player.rect.colliderect(level.goal.rect)

        if reached_goal:
            self.audio.play_sfx("victory")
            level.run_score.finish(player.score)
            self.victory = True
            self.unlocked_phases = max(
                self.unlocked_phases, min(CAMPAIGN_PHASES, self.phase_number + 1)
            )
            save_unlocked_phases(self.unlocked_phases)
            self.selected_phase = min(self.unlocked_phases - 1, CAMPAIGN_PHASES - 1)

    def update_music(self):
        if self.screen_mode != "playing":
            self.audio.set_phase("menu")
        elif self.victory and self.phase_number == FINAL_PHASE:
            self.audio.set_phase("ending")
        elif self.victory or self.game_over:
            self.audio.set_phase(None)
        elif self.phase_number == FINAL_PHASE:
            if not self.boss_intro_active:
                self.audio.finish_boss_intro()
            self.audio.set_phase("boss_intro" if self.boss_intro_active else FINAL_PHASE)
        else:
            self.audio.set_phase(self.phase_number)

    def draw(self):
        if self.screen_mode == "home":
            self.view.draw_home()
        elif self.screen_mode == "options":
            self.view.draw_info_panel("OPCOES", ["V - ATIVAR/DESATIVAR SOM", "ESC - VOLTAR"])
        elif self.screen_mode == "credits":
            self.view.draw_info_panel("CREDITOS", [
                "RIFF RUN",
                "Desenvolvimento: Equipe Riff Run",
                "Projeto academico",
                "Programacao para Jogos",
            ])
        elif self.screen_mode == "menu":
            self.view.draw_map_menu(self.selected_phase, self.unlocked_phases)
        elif self.screen_mode == "playing":
            self.view.draw_playing(
                self.player, self.level, self.phase_number, self.victory, self.game_over,
            )
