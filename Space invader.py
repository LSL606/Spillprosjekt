import pygame
import random

# Initialiser Pygame
pygame.init()

# Definer konstanter
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Sett opp vinduet
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Last inn bilder
background = pygame.image.load("background.jpg")
player_image = pygame.image.load("player.png")
enemy_image = pygame.image.load("enemy.png")
bullet_image = pygame.image.load("bullet.png")

# Skalering av bilder
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (30, 50))  
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Spillerens posisjon
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 70
player_speed = 5

# Fiender
num_enemies = 5
enemies = [{"x": random.randint(0, WIDTH - 50), "y": random.randint(50, 200), "speed": 2, "direction": 1} for _ in range(num_enemies)]

# Skudd
bullets = []
bullet_speed = 15
cooldown = 0  # Kjøletid før neste skudd kan skytes
shoot_key_pressed = False  # Variabel for å spore at mellomromstasten er nylig trykket

# Poengsum
score = 0

# Timer
start_time = pygame.time.get_ticks()
game_duration = 30 * 1000  # 30 sekunder i millisekunder

# Font for tekster
font = pygame.font.Font(None, 36)

# Spillhastighet
clock = pygame.time.Clock()

def reset_game():
    global player_x, player_y, enemies, bullets, score, start_time
    player_x = WIDTH // 2 - 25
    player_y = HEIGHT - 70
    enemies = [{"x": random.randint(0, WIDTH - 50), "y": random.randint(50, 200), "speed": 2, "direction": 1} for _ in range(num_enemies)]
    bullets = []
    score = 0
    start_time = pygame.time.get_ticks()

# Spill-løkke
running = True
while running:
    screen.blit(background, (0, 0))

    # Behandle hendelser
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not shoot_key_pressed:  # Sjekk om mellomromstasten er nylig trykket
                    bullets.append([player_x + 22, player_y])
                    cooldown = 10  # Kjøletid i antall frames før neste skudd kan skytes
                    shoot_key_pressed = True  # Sett til True for å unngå gjentatt skyting
            elif event.key == pygame.K_r and not bullets and len(enemies) == 0:
                reset_game()  # Start spillet på nytt hvis R-tasten trykkes etter at alle fiender er borte

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shoot_key_pressed = False  # Sett til False når mellomromstasten er løslatt

    # Flytt spilleren med piltastene
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed

    # Beveg fiender
    for enemy in enemies:
        enemy["x"] += enemy["speed"] * enemy["direction"]
        if enemy["x"] < 0 or enemy["x"] > WIDTH - 50:
            enemy["direction"] *= -1  # Bytt retning hvis fienden når kanten

    # Skudd
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Kollisjonssjekk mellom skudd og fiender
    for enemy in enemies[:]:  # Kopier listen for å unngå endring under iterasjon
        for bullet in bullets[:]:  # Kopier også skuddlisten
            if (
                enemy["x"] < bullet[0] + 10 < enemy["x"] + 50
                and enemy["y"] < bullet[1] + 30 < enemy["y"] + 50
            ):
                print("Fienden truffet!")
                enemies.remove(enemy)
                bullets.remove(bullet)
                if len(enemies) == 0:  # Hvis alle fiender er borte, start spillet på nytt
                    reset_game()
                else:
                    new_enemy = {"x": random.randint(0, WIDTH - 50), "y": random.randint(50, 200), "speed": 2, "direction": 1}
                    enemies.append(new_enemy)
                score += 1  # Øk poengsummen med 1 for hver truffet fiende

    # Tegn spilleren, fiendene og skuddene
    screen.blit(player_image, (player_x, player_y))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy["x"], enemy["y"]))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))

    # Tegn poengsummen
    score_text = font.render(f"Poeng: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Sjekk om tiden har gått ut
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= game_duration:
        print("Spillet er over! Tiden har gått ut.")
        print(f"Din poengsum ble: {score}")
        print("Trykk R for å starte på nytt eller Q for å avslutte.")
        pygame.display.flip()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        waiting_for_input = False
                    elif event.key == pygame.K_q:
                        running = False
                        waiting_for_input = False

    else:
        # Tegn gjenværende tid øverst til høyre
        remaining_time = (game_duration - elapsed_time) // 1000
        timer_text = font.render(f"Tid: {remaining_time}s", True, WHITE)
        screen.blit(timer_text, (WIDTH - 150, 10))

    # Oppdater skjermen
    pygame.display.flip()

    # Begrens oppdateringshastigheten
    clock.tick(FPS)

    # Reduser kjøletid
    if cooldown > 0:
        cooldown -= 1

# Avslutt Pygame
pygame.quit()
