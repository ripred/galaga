import os
import sys
import pygame

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = -7
ENEMY_SPEED = 2
CAPTURE_SPEED = 2

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

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, pos, is_boss=False):
            super().__init__()
            self.image = enemy_image
            self.rect = self.image.get_rect(topleft=pos)
            self.start_pos = pygame.Vector2(pos)
            self.is_boss = is_boss
            self.capturing = False
            self.has_player = False

        def update(self, direction):
            if self.capturing:
                if self.has_player:
                    # return to start position with captured ship
                    if self.rect.y > self.start_pos.y:
                        self.rect.y -= CAPTURE_SPEED
                    else:
                        self.capturing = False
                else:
                    self.rect.y += CAPTURE_SPEED
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

        # Boss capture behaviour
        if boss.is_boss and not boss.capturing and not boss.has_player:
            if abs(boss.rect.centerx - player.rect.centerx) < 5 and boss.rect.y <= boss.start_pos.y:
                boss.capturing = True

        beam_rect = None
        if boss.capturing and not boss.has_player:
            beam_rect = pygame.Rect(boss.rect.centerx - 10, boss.rect.bottom,
                                    20, SCREEN_HEIGHT - boss.rect.bottom)
            if player.alive() and beam_rect.colliderect(player.rect):
                boss.has_player = True
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

        if beam_rect:
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
