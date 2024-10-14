import pygame
import random

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Dimensiones de la pantalla
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Naves y Marcianos")

# Fuente para texto (puntuación y vidas)
font = pygame.font.Font(None, 36)

# Cargar imágenes
player_img = pygame.image.load('nave.png')
enemy_img = pygame.image.load('marciano.png')
bullet_img = pygame.image.load('bala.png')

# Clase de la nave
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.lives = 3  # Añadir vidas

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Limitar movimiento dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase del enemigo (marciano)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 3)
            # Si un enemigo llega al fondo, perderás una vida
            player.lives -= 1

# Clase de la bala
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (5, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Función para mostrar texto en pantalla
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Grupo de todos los sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear el jugador
player = Player()
all_sprites.add(player)

# Crear enemigos
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Variables de juego
score = 0  # Añadir puntuación

# Bucle principal del juego
running = True
while running:
    # Mantener el bucle a 60 fps
    pygame.time.Clock().tick(60)

    # Eventos del juego (movimiento, disparo, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Actualizar los sprites
    all_sprites.update()

    # Detectar colisiones entre balas y enemigos
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10  # Sumar puntos al destruir un enemigo
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Verificar si el jugador ha perdido todas sus vidas
    if player.lives <= 0:
        running = False  # Fin del juego si se pierden todas las vidas

    # Dibujar en la pantalla
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Mostrar la puntuación y las vidas
    draw_text(screen, f"Puntuación: {score}", 24, WIDTH // 2, 10, WHITE)
    draw_text(screen, f"Vidas: {player.lives}", 24, WIDTH - 60, 10, RED)

    pygame.display.flip()

pygame.quit()
