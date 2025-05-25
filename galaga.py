import os
import sys
import pygame
import random

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = -7
ENEMY_SPEED = 2
CAPTURE_SPEED = 2
DIVE_SPEED = 3
DIVE_PROBABILITY = 0.005
ENEMY_BULLET_SPEED = 4

pygame.init()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Galaga")

    clock = pygame.time.Clock()

    def load_sprite(name, width, height):
        """Helper to load and scale images from the sprite folder."""
        path = os.path.join("space_starter_kit", name)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, (width, height))

    # Sprite setup using images
    player_image = load_sprite("starship.svg", 40, 30)
    bullet_image = load_sprite("projectile1.svg", 5, 15)
    enemy_image = load_sprite("ufo.svg", 30, 20)
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
        def __init__(self, pos, is_boss=False):
            super().__init__()
            self.base_image = enemy_image
            self.image = self.base_image
            self.rect = self.image.get_rect(topleft=pos)
            self.start_pos = pygame.Vector2(pos)
            self.is_boss = is_boss
            self.capturing = False
            self.capture_stationary = False
            self.capture_timer = 0
            self.has_player = False
            self.diving = False
            self.dive_dir = 1
            self.angle = 0

        def start_dive(self):
            if not self.capturing and not self.diving:
                self.diving = True
                self.dive_dir = 1 if self.rect.centerx < player.rect.centerx else -1
                self.angle = 0

        def update(self, direction):
            if self.capturing:
                if self.capture_stationary:
                    # stay still while beam is active
                    self.capture_timer += 1
                    if self.capture_timer > 120:
                        self.capturing = False
                        self.capture_stationary = False
                        self.capture_timer = 0
                        if self.rect.y > self.start_pos.y:
                            self.rect.topleft = self.start_pos
                elif self.has_player:
                    # return to start position with captured ship
                    if self.rect.y > self.start_pos.y:
                        self.rect.y -= CAPTURE_SPEED
                    else:
                        self.capturing = False
                else:
                    self.rect.y += CAPTURE_SPEED
            elif self.diving:
                self.rect.x += self.dive_dir * ENEMY_SPEED
                self.rect.y += DIVE_SPEED
                self.angle = (self.angle + 5) % 360
                center = self.rect.center
                self.image = pygame.transform.rotate(self.base_image, self.angle)
                self.rect = self.image.get_rect(center=center)
                if random.random() < 0.02:
                    bullet = EnemyBullet(self.rect.midbottom)
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet)
                if self.has_player and self.rect.y > SCREEN_HEIGHT // 3 and not self.capturing:
                    self.diving = False
                    self.capturing = True
                    self.capture_stationary = True
                    self.angle = 0
                    self.image = self.base_image
                elif self.rect.top > SCREEN_HEIGHT:
                    self.diving = False
                    self.angle = 0
                    self.image = self.base_image
                    self.rect.topleft = self.start_pos
            else:
                self.rect.x += ENEMY_SPEED * direction

    class FreedShip(pygame.sprite.Sprite):
        """Ship released from an enemy after being captured."""
        def __init__(self, pos):
            super().__init__()
            self.image = player_image
            self.rect = self.image.get_rect(midtop=pos)

        def update(self):
            self.rect.y += CAPTURE_SPEED
            if self.rect.bottom >= SCREEN_HEIGHT - 10:
                # Join the player's ship and enable double shooting
                player.double = True
                self.kill()

    # Groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    freed_ships = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # create a simple row of enemies (first enemy acts as a boss)
    for i in range(8):
        enemy = Enemy((80 * i + 50, 50), is_boss=(i == 0))
        enemies.add(enemy)
        all_sprites.add(enemy)

    enemy_direction = 1
    boss = next(e for e in enemies if e.is_boss)
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
        freed_ships.update()

        # Update enemies
        move_down = False
        for enemy in enemies:
            enemy.update(enemy_direction)
            if enemy.rect.right > SCREEN_WIDTH or enemy.rect.left < 0:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                enemy.rect.y += 20

        available = [e for e in enemies if not e.diving and not e.capturing]
        if available and random.random() < DIVE_PROBABILITY:
            random.choice(available).start_dive()

        # Boss capture behaviour when aligned at the top
        if boss.is_boss and not boss.capturing and not boss.has_player:
            if abs(boss.rect.centerx - player.rect.centerx) < 5 and boss.rect.y <= boss.start_pos.y:
                boss.capturing = True

        beam_rects = []
        for enemy in enemies:
            if enemy.capturing:
                beam = pygame.Rect(enemy.rect.centerx - 10, enemy.rect.bottom,
                                   20, SCREEN_HEIGHT - enemy.rect.bottom)
                beam_rects.append(beam)
                if player.alive() and beam.colliderect(player.rect):
                    if not enemy.has_player:
                        enemy.has_player = True
                    lives -= 1
                    all_sprites.remove(player)
                    player.kill()
                    if lives > 0:
                        player = Player()
                        all_sprites.add(player)
                    else:
                        running = False

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

        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for hit_enemy in hits.values():
            for enemy in hit_enemy:
                if enemy.has_player:
                    freed = FreedShip(enemy.rect.midbottom)
                    all_sprites.add(freed)
                    freed_ships.add(freed)
                enemies.remove(enemy)
                all_sprites.remove(enemy)

        # Render
        screen.fill((0, 0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect)

        # Draw captured ship if any
        for enemy in enemies:
            if enemy.has_player:
                captured_pos = (enemy.rect.centerx - player_image.get_width() // 2,
                                enemy.rect.bottom)
                screen.blit(player_image, captured_pos)

        for beam_rect in beam_rects:
            pygame.draw.rect(screen, (0, 255, 255), beam_rect)

        for i in range(lives):
            x = 10 + i * (life_image.get_width() + 10)
            y = SCREEN_HEIGHT - life_image.get_height() - 5
            screen.blit(life_image, (x, y))
        pygame.display.flip()
        clock.tick(60)

    print("Game Over")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
