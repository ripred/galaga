import os
import sys
import pygame

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = -7
ENEMY_SPEED = 2

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

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = player_image
            self.rect = self.image.get_rect()
            self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)

        def update(self, keys):
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
            self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

        def shoot(self):
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
        def __init__(self, pos):
            super().__init__()
            self.image = enemy_image
            self.rect = self.image.get_rect(topleft=pos)

        def update(self, direction):
            self.rect.x += ENEMY_SPEED * direction

    # Groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # create a simple row of enemies
    for i in range(8):
        enemy = Enemy((80 * i + 50, 50))
        enemies.add(enemy)
        all_sprites.add(enemy)

    enemy_direction = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()

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

        pygame.sprite.groupcollide(bullets, enemies, True, True)

        # Render
        screen.fill((0, 0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
