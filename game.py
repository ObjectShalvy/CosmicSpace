#Juego basado en una nave que dispara a un boss 
#Realizado por @Salvador Sanchez Luengas
import pygame
import random
import math
import os
pygame.init()
pygame.mixer.init()
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space piu piu ")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
game_folder = os.path.join(desktop, "game")
background = pygame.image.load(os.path.join(game_folder, "fondo.jpg"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
start_screen = pygame.image.load(os.path.join(game_folder, "pantalla.png"))
start_screen = pygame.transform.scale(start_screen, (WIDTH, HEIGHT))
shoot_sound = pygame.mixer.Sound(os.path.join(game_folder, "bala.mp3"))
start_music = pygame.mixer.Sound(os.path.join(game_folder, "inicio.mp3"))
game_music = pygame.mixer.Sound(os.path.join(game_folder, "boss.mp3"))
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file, size, health):
        super().__init__()
        original_image = pygame.image.load(os.path.join(game_folder, image_file))
        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.health = health

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if not screen.get_rect().contains(self.rect):
            self.kill()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
def game():
    start_music.stop()
    game_music.play(-1)  

    player = Player(WIDTH // 2, HEIGHT - 100, "me.gif", (30, 30), 10)
    enemy = Player(WIDTH // 2, 50, "enemy.gif", (50, 50), 50)

    all_sprites = pygame.sprite.Group(player, enemy)
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    enemy_shoot_delay = 500  

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_music.stop()
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    bullet = Bullet(player.rect.centerx, player.rect.top, 0, -1)
                    player_bullets.add(bullet)
                    all_sprites.add(bullet)
                    shoot_sound.play() 

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        player.move(dx, dy)

        enemy.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

        current_time = pygame.time.get_ticks()
        if current_time - start_time > enemy_shoot_delay:
            for _ in range(8):
                angle = math.radians(_ * 45)
                dx = math.cos(angle)
                dy = math.sin(angle)
                bullet = Bullet(enemy.rect.centerx, enemy.rect.bottom, dx, dy)
                enemy_bullets.add(bullet)
                all_sprites.add(bullet)
            start_time = current_time
        if current_time // 20000 > (current_time - enemy_shoot_delay) // 20000:
            enemy_shoot_delay = max(100, enemy_shoot_delay - 50)

        all_sprites.update()

        for bullet in player_bullets:
            if pygame.sprite.collide_rect(bullet, enemy):
                bullet.kill()
                enemy.health -= 1
        
        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(bullet, player):
                bullet.kill()
                player.health -= 1

        if enemy.health <= 0 or player.health <= 0:
            running = False

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        
        draw_text(f"spaceX: {player.health}", font, BLUE, 70, 20)
        draw_text(f"DarkZ: {enemy.health}", font, RED, WIDTH - 70, 20)
        
        pygame.display.flip()

        clock.tick(60)
    game_music.stop()

    if enemy.health <= 0:
        result = "WIN"
    else:
        result = "LOSE"
    
    return result

def start_screen_func():
    start_music.play(-1)  
    while True:
        screen.blit(start_screen, (0, 0))
        draw_text("Presiona K para iniciar", pygame.font.Font(None, 36), WHITE, WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_music.stop()
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    start_music.stop()
                    return "START"
def main():
    while True:
        game_state = start_screen_func()
        if game_state == "QUIT":
            break
        elif game_state == "START":
            result = game()
            if result == "QUIT":
                break
            else:
                screen.fill((0, 0, 0))
                draw_text(result, pygame.font.Font(None, 72), WHITE if result == "WIN" else RED, WIDTH // 2, HEIGHT // 2)
                draw_text("Presiona [k] para volver al inicio", pygame.font.Font(None, 36), WHITE, WIDTH // 2, HEIGHT - 50)
                pygame.display.flip()
                
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_k:
                                waiting = False

    pygame.quit()

if __name__ == "__main__":
    main()