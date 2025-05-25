import pygame
import sys

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

    # Player setup
    player_image = pygame.Surface((40, 30))
    player_image.fill((0, 255, 0))
    player_rect = player_image.get_rect()
    player_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)

    bullet_image = pygame.Surface((5, 15))
    bullet_image.fill((255, 255, 0))
    bullets = []

    enemy_image = pygame.Surface((30, 20))
    enemy_image.fill((255, 0, 0))
    enemies = []

    # create a simple row of enemies
    for i in range(8):
        rect = enemy_image.get_rect()
        rect.topleft = (80 * i + 50, 50)
        enemies.append(rect)

    enemy_direction = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rect = bullet_image.get_rect()
                    rect.midbottom = player_rect.midtop
                    bullets.append(rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_rect.x += PLAYER_SPEED

        player_rect.x = max(0, min(SCREEN_WIDTH - player_rect.width, player_rect.x))

        # Update bullets
        for bullet in bullets[:]:
            bullet.y += BULLET_SPEED
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Update enemies
        move_down = False
        for enemy in enemies:
            enemy.x += ENEMY_SPEED * enemy_direction
            if enemy.right > SCREEN_WIDTH or enemy.left < 0:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                enemy.y += 20

        # Render
        screen.fill((0, 0, 0))
        screen.blit(player_image, player_rect)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
