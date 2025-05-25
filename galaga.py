import pygame
import sys

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = -7
ENEMY_SPEED = 2
STARTING_LIVES = 3

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

    # Lives setup
    lives = STARTING_LIVES
    life_image = pygame.transform.scale(player_image, (30, 22))

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

        # Check for collisions between enemies and the player
        for enemy in enemies:
            if enemy.colliderect(player_rect):
                lives -= 1
                player_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
                if lives <= 0:
                    running = False
                break

        # Render
        screen.fill((0, 0, 0))
        screen.blit(player_image, player_rect)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)

        # Draw remaining lives (excluding the active ship)
        for i in range(lives - 1):
            rect = life_image.get_rect()
            rect.bottomleft = (10 + i * (rect.width + 10), SCREEN_HEIGHT - 10)
            screen.blit(life_image, rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
