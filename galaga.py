#!/usr/bin/env python3
import os
import sys
import pygame
import random
import math

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = -7
ENEMY_SPEED = 2
MAX_ENEMY_SPEED = 5
DIVE_SPEED = 3
DIVE_PROBABILITY = 0.005
ENEMY_BULLET_SPEED = 4

pygame.init()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Galaga")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    score = 0

    def load_sprite(name, width, height):
        """Helper to load and scale an image from the starter kit."""
        path = os.path.join("space_starter_kit", name)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, (width, height))


    def load_pack_sprite(fname, width, height):
        """Load a spaceship sprite from the AntuZ pack."""
        path = os.path.join("SpaceShipsPack-AntuZ", "SpaceShips", fname)
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (width, height))

    # Sprite setup using images
    player_image = load_sprite("starship.svg", 40, 30)
    bullet_image = load_sprite("projectile1.svg", 5, 15)
    enemy_image = load_sprite("ufo.svg", 30, 20)
    enemy_images = {
        "shooter": load_pack_sprite("A-10.png", 30, 20),
        "diver": load_pack_sprite("B-08.png", 30, 20),
        "zigzag": load_pack_sprite("C-07.png", 30, 20),
    }
    enemy_bullet_image = load_sprite("projectile2.svg", 5, 15)
    life_image = load_sprite("starship.svg", 30, 20)

    class Player(pygame.sprite.Sprite):
        def __init__(self, double=False):
            super().__init__()
            self.image = player_image
            self.rect = self.image.get_rect()
            self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
            self.double = double

        def update(self, keys):
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
            self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

        def shoot(self):
            if self.double:
                left = self.rect.midtop[0] - 10
                right = self.rect.midtop[0] + 10
                for x in (left, right):
                    bullet = Bullet((x, self.rect.top))
                    all_sprites.add(bullet)
                    bullets.add(bullet)
            else:
                bullet = Bullet(self.rect.midtop)
                all_sprites.add(bullet)
                bullets.add(bullet)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = bullet_image
            self.rect = self.image.get_rect(midbottom=pos)

        def update(self):
            self.rect.y += BULLET_SPEED
            if self.rect.bottom < 0:
                self.kill()

    class EnemyBullet(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = enemy_bullet_image
            self.rect = self.image.get_rect(midtop=pos)

        def update(self):
            self.rect.y += ENEMY_BULLET_SPEED
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, pos, image, enemy_type="shooter", speed=ENEMY_SPEED, shoot_factor=1.0):
            super().__init__()
            self.base_image = image
            self.image = self.base_image
            self.rect = self.image.get_rect(topleft=pos)
            self.start_pos = pygame.Vector2(pos)
            self.enemy_type = enemy_type
            self.speed = min(speed, MAX_ENEMY_SPEED)
            self.diving = False
            self.dive_dir = 1
            self.angle = 0
            self.sine_phase = random.random() * 2 * math.pi
            base_probs = {"shooter": 0.01, "diver": 0.02, "zigzag": 0.015}
            self.shoot_prob = base_probs.get(enemy_type, 0.01) * shoot_factor

        def start_dive(self):
            if self.enemy_type == "diver" and not self.diving:
                self.diving = True
                self.dive_dir = 1 if self.rect.centerx < player.rect.centerx else -1
                self.angle = 0

        def update(self, direction):
            if self.diving:
                self.rect.x += self.dive_dir * self.speed
                self.rect.y += DIVE_SPEED
                self.angle = (self.angle + 5) % 360
                center = self.rect.center
                self.image = pygame.transform.rotate(self.base_image, self.angle)
                self.rect = self.image.get_rect(center=center)
                if random.random() < self.shoot_prob:
                    bullet = EnemyBullet(self.rect.midbottom)
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet)
                if self.rect.top > SCREEN_HEIGHT:
                    self.diving = False
                    self.angle = 0
                    self.image = self.base_image
                    self.rect.topleft = self.start_pos
            else:
                self.rect.x += self.speed * direction
                if self.enemy_type == "zigzag":
                    t = pygame.time.get_ticks() / 200 + self.sine_phase
                    self.rect.y = self.start_pos.y + 20 * math.sin(t)
                # Enemies in formation should not shoot; only those that have
                # left formation (diving/attacking) can fire at the player.


    # Groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    enemy_direction = 1
    wave = 1
    current_dive_prob = DIVE_PROBABILITY

    def spawn_wave(num):
        nonlocal current_dive_prob, enemy_direction
        for e in enemies:
            e.kill()
        current_dive_prob = DIVE_PROBABILITY + (num - 1) * 0.002
        enemy_direction = 1
        rows = 2 if num == 1 else 3
        spacing = 80
        start_x = (SCREEN_WIDTH - spacing * 8) // 2
        speed = min(ENEMY_SPEED + (num - 1) * 0.5, MAX_ENEMY_SPEED)
        shoot_factor = 1 + (num - 1) * 0.25
        for row in range(rows):
            y = 50 + row * 40
            for i in range(8):
                etype = random.choice(list(enemy_images.keys()))
                sprite = enemy_images.get(etype, enemy_image)
                enemy = Enemy((start_x + i * spacing, y), sprite,
                              enemy_type=etype, speed=speed,
                              shoot_factor=shoot_factor)
                enemies.add(enemy)
                all_sprites.add(enemy)

    spawn_wave(wave)
    lives = 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()

        keys = pygame.key.get_pressed()
        if player.alive():
            player.update(keys)
        bullets.update()
        enemy_bullets.update()

        # Update enemies
        move_down = False
        for enemy in enemies:
            enemy.update(enemy_direction)
            if not enemy.diving and enemy.rect.top > SCREEN_HEIGHT:
                enemy.rect.topleft = enemy.start_pos
                continue
            if enemy.rect.right > SCREEN_WIDTH or enemy.rect.left < 0:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                enemy.rect.y += 20

        available = [
            e for e in enemies
            if e.enemy_type == "diver" and not e.diving
        ]
        if available and random.random() < current_dive_prob:
            random.choice(available).start_dive()

        if player.alive():
            if pygame.sprite.spritecollide(player, enemy_bullets, True):
                lives -= 1
                all_sprites.remove(player)
                player.kill()
                if lives > 0:
                    player = Player()
                    all_sprites.add(player)
                else:
                    running = False

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        score += len(hits) * 10
        if not enemies:
            wave += 1
            spawn_wave(wave)

        # Render
        screen.fill((0, 0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect)

        for i in range(lives):
            x = 10 + i * (life_image.get_width() + 10)
            y = SCREEN_HEIGHT - life_image.get_height() - 5
            screen.blit(life_image, (x, y))
        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
        wave_surf = font.render(f"Wave: {wave}", True, (255, 255, 255))
        screen.blit(wave_surf, (SCREEN_WIDTH - wave_surf.get_width() - 10, 10))
        pygame.display.flip()
        clock.tick(60)

    print(f"Game Over! Final score: {score}")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
