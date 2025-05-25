import pygame
import sys
import random

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = -7
ENEMY_SPEED = 2
CAPTURE_FIELD_HEIGHT = 200
CAPTURE_FIELD_WIDTH = 40
CAPTURE_COLOR = (50, 50, 255)

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
    player_lives = 2
    double_ship = False
    captured_ship_rect = None
    captured_falling = False

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
    enemy_home = [e.topleft for e in enemies]
    capture_active = False
    capturing_enemy = None
    capturing_index = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if double_ship and captured_ship_rect is None:
                        rect1 = bullet_image.get_rect()
                        rect2 = bullet_image.get_rect()
                        rect1.midbottom = (player_rect.centerx - 15, player_rect.top)
                        rect2.midbottom = (player_rect.centerx + 15, player_rect.top)
                        bullets.extend([rect1, rect2])
                    else:
                        rect = bullet_image.get_rect()
                        rect.midbottom = player_rect.midtop
                        bullets.append(rect)
                elif event.key == pygame.K_c:
                    if not captured_ship_rect and not capture_active:
                        capture_active = True
                        capturing_enemy = enemies[0]
                        capturing_index = 0

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
                continue
            # bullet hits carrying enemy
            if capturing_enemy and bullet.colliderect(capturing_enemy):
                bullets.remove(bullet)
                enemies.remove(capturing_enemy)
                captured_falling = True
                capturing_enemy = None
                continue
            # bullet hits regular enemy
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break
            # bullet hits captured ship
            if captured_ship_rect and bullet.colliderect(captured_ship_rect):
                bullets.remove(bullet)
                captured_ship_rect = None
                captured_falling = False

        # Capture field logic
        if capture_active and capturing_enemy:
            capture_field_rect = pygame.Rect(
                capturing_enemy.centerx - CAPTURE_FIELD_WIDTH // 2,
                capturing_enemy.bottom,
                CAPTURE_FIELD_WIDTH,
                CAPTURE_FIELD_HEIGHT,
            )
            if player_rect.colliderect(capture_field_rect):
                capture_active = False
                captured_ship_rect = player_rect
                capturing_enemy = enemies[capturing_index]
                player_lives -= 1
                if player_lives <= 0:
                    running = False
                else:
                    player_rect = player_image.get_rect()
                    player_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
        elif captured_ship_rect and capturing_enemy:
            captured_ship_rect.midtop = (capturing_enemy.centerx, capturing_enemy.bottom)
            home_x, home_y = enemy_home[capturing_index]
            if capturing_enemy.y > home_y:
                capturing_enemy.y -= ENEMY_SPEED
            else:
                capturing_enemy.y = home_y
        if captured_falling and captured_ship_rect:
            captured_ship_rect.y += 3
            if captured_ship_rect.colliderect(player_rect):
                captured_falling = False
                captured_ship_rect = None
                double_ship = True
        # Update enemies
        move_down = False
        for idx, enemy in enumerate(enemies):
            if enemy is capturing_enemy and (capture_active or captured_ship_rect):
                continue
            enemy.x += ENEMY_SPEED * enemy_direction
            if enemy.right > SCREEN_WIDTH or enemy.left < 0:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                if enemy is capturing_enemy and (capture_active or captured_ship_rect):
                    continue
                enemy.y += 20

        # Render
        screen.fill((0, 0, 0))
        if double_ship and captured_ship_rect is None:
            left = player_rect.copy(); left.x -= 15
            right = player_rect.copy(); right.x += 15
            screen.blit(player_image, left)
            screen.blit(player_image, right)
        else:
            screen.blit(player_image, player_rect)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        if capture_active and capturing_enemy:
            capture_field_rect = pygame.Rect(
                capturing_enemy.centerx - CAPTURE_FIELD_WIDTH // 2,
                capturing_enemy.bottom,
                CAPTURE_FIELD_WIDTH,
                CAPTURE_FIELD_HEIGHT,
            )
            pygame.draw.rect(screen, CAPTURE_COLOR, capture_field_rect, 2)
        if captured_ship_rect:
            screen.blit(player_image, captured_ship_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
