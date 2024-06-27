import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_size = 50
player_speed = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - player_size - 10, player_size, player_size)

enemies = []

score = 0
time_elapsed = 0

font = pygame.font.Font(None, 36)

start_text = font.render("Drücke Enter zum Starten", True, WHITE)
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

game_over_text = font.render("Spiel vorbei - Drücke Enter für Neustart", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

highscore_file = "highscore.txt"

def draw_player():
    pygame.draw.rect(screen, WHITE, player)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

def draw_score():
    score_text = font.render(f"Punkte: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_highscore():
    highscore_text = font.render(f"Highscore: {get_highscore()}", True, WHITE)
    screen.blit(highscore_text, (10, 50))

def get_highscore():
    try:
        with open(highscore_file, "r") as file:
            highscore = int(file.read())
    except FileNotFoundError:
        highscore = 0
    return highscore

def set_highscore(new_highscore):
    with open(highscore_file, "w") as file:
        file.write(str(new_highscore))

def game_over():
    global score
    highscore = get_highscore()
    if score > highscore:
        set_highscore(score)
    score = 0
    return f"Highscore: {highscore} - Neustart"

def reset_game():
    global time_elapsed, score, player, enemies
    time_elapsed = 0
    score = 0
    player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - player_size - 10, player_size, player_size)
    enemies = []

running = True
game_active = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not game_active:
                    game_active = True
                    reset_game()

    if game_active:
        keys = pygame.key.get_pressed()
        player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed

        
        player.x = max(0, min(WIDTH - player_size, player.x))

        
        if random.randint(1, 30) <= 5:
            enemy = pygame.Rect(random.randint(0, WIDTH - 20), 20, 20, 20)
            enemies.append(enemy)

        
        for enemy in enemies:
            enemy.y += 5
            if enemy.colliderect(player):
                game_active = False
                highscore_text = game_over()
                print(highscore_text)
                break

        
        enemies = [enemy for enemy in enemies if enemy.y < HEIGHT]

        
        score += len(enemies)

        # Zeichne alles
        screen.fill((0, 0, 0))
        draw_player()
        draw_enemies()
        draw_score()
        draw_highscore()

    else:
        
        screen.fill((0, 0, 0))
        if highscore := get_highscore():
            highscore_text = font.render(f"Aktueller Highscore: {highscore}", True, WHITE)
            screen.blit(highscore_text, (WIDTH // 2 - 200, HEIGHT // 2 - 150))

        if game_active:
            screen.blit(start_text, start_rect)
        else:
            screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

