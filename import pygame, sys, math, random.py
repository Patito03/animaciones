import pygame, sys, math, random

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Configuración de ventana
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("💖 Te quiero niña bonita 💖")

# Cargar música con fade-in
try:
    pygame.mixer.music.load("symphonia_ix.mp3")  # Coloca el archivo mp3 en la misma carpeta
    pygame.mixer.music.set_volume(0.0)
    pygame.mixer.music.play(-1, fade_ms=2000)  # Fade-in de 2 segundos
except:
    print("⚠ No se encontró 'symphonia_ix.mp3'")

# Fuente elegante
font = pygame.font.SysFont("segoescript", 50, bold=True)

# Colores
WHITE = (255, 255, 255)
RED = (255, 50, 120)
YELLOW = (255, 255, 180)
PINK = (255, 150, 200)
BLUE = (120, 200, 255)

clock = pygame.time.Clock()

# Corazones flotantes con física
hearts = []
for i in range(35):
    x = random.randint(100, WIDTH-100)
    y = random.randint(HEIGHT, HEIGHT + 400)
    size = random.randint(20, 50)
    speed = random.uniform(0.5, 2)
    hearts.append([x, y, size, speed, random.randint(100,255), random.uniform(0, math.pi*2), 0, 0])

# Partículas mágicas y destellos
particles = []
sparks = []
waves = []

def draw_background(time):
    """Fondo degradado dinámico con niebla flotante"""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(20 + 50*math.sin(time*0.0007) + 40*ratio)
        g = int(0 + 50*math.cos(time*0.0009) + 30*ratio)
        b = int(60 + 80*math.sin(time*0.0012) + 60*ratio)
        pygame.draw.line(screen, (r,g,b), (0,y), (WIDTH,y))
    # Niebla flotante
    for i in range(100):
        fx = random.randint(0, WIDTH)
        fy = random.randint(0, HEIGHT)
        radius = random.randint(1,3)
        s = pygame.Surface((radius*2,radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255,255,255,10), (radius,radius), radius)
        screen.blit(s, (fx, fy))

def draw_heart(surface, x, y, size, color, glow=False, aura=False):
    """Corazón con glow y aura"""
    points = []
    for t in range(0, 360, 5):
        rad = math.radians(t)
        px = 16 * math.sin(rad)**3
        py = 13 * math.cos(rad) - 5*math.cos(2*rad) - 2*math.cos(3*rad) - math.cos(4*rad)
        points.append((x + size*px/20, y - size*py/20))
    if aura:
        aura_size = size*1.3 + 5*math.sin(pygame.time.get_ticks()*0.01)
        pygame.draw.polygon(surface, (255,150,200,50), [(x + aura_size*px/20, y - aura_size*py/20) for px,py in [(16,13)]*len(points)])
    if glow:
        for i in range(12,0,-3):
            glow_color = (min(color[0]+i*10,255), min(color[1]+i*10,255), min(color[2]+i*10,255))
            pygame.draw.polygon(surface, glow_color, points, 2)
    pygame.draw.polygon(surface, color, points)

def draw_flower(x, y, size, t):
    """Flor animada con pétalos oscilantes"""
    for i in range(8):
        angle = math.radians(i*45)
        px = x + math.cos(angle)*(size + 6*math.sin(t*0.07+i))
        py = y + math.sin(angle)*(size + 6*math.sin(t*0.07+i))
        color = (255, 120+int(50*math.sin(t*0.1+i)), 180)
        pygame.draw.circle(screen, color, (int(px), int(py)), size//2)
    pygame.draw.circle(screen, (255,220,100), (x,y), size//2)

def handle_collision(h1, h2):
    dx = h2[0]-h1[0]
    dy = h2[1]-h1[1]
    dist = math.hypot(dx, dy)
    min_dist = (h1[2]+h2[2])*0.5
    if dist < min_dist and dist != 0:
        overlap = 0.5*(min_dist - dist)
        nx, ny = dx/dist, dy/dist
        h1[0] -= nx*overlap
        h1[1] -= ny*overlap
        h2[0] += nx*overlap
        h2[1] += ny*overlap

time = 0
alpha = 0
fade_in = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Ajustar volumen para fade-in de música
    if pygame.mixer.music.get_busy() and pygame.mixer.music.get_volume() < 0.5:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.001)

    time += 1
    screen.fill((0,0,0))

    draw_background(time)

    # Corazones
    for h in hearts:
        h[5] += 0.05
        h[1] -= h[3]
        if h[1] < -50:
            h[0] = random.randint(50, WIDTH-50)
            h[1] = HEIGHT + random.randint(0,200)
            h[4] = random.randint(100,255)
        size_pulse = h[2]*(1+0.1*math.sin(h[5]))
        draw_heart(screen, h[0], h[1], size_pulse, (255, random.randint(50,150), h[4]), glow=True, aura=True)

    for i in range(len(hearts)):
        for j in range(i+1, len(hearts)):
            handle_collision(hearts[i], hearts[j])

    # Corazón central y ondas
    pulse = 1 + 0.25*math.sin(time*0.1)
    cx, cy = WIDTH//2, HEIGHT//2
    draw_heart(screen, cx, cy, int(160*pulse), RED, glow=True, aura=True)
    if time % 40 == 0:
        waves.append([cx, cy, 50, 2])
    for w in waves[:]:
        pygame.draw.circle(screen, (255,200,255,50), (w[0], w[1]), int(w[2]), 2)
        w[2] += w[3]
        if w[2] > WIDTH:
            waves.remove(w)

    # Flor
    draw_flower(150, HEIGHT-150, 70, time)

    # Partículas
    if random.random() < 0.25:
        particles.append([random.randint(0,WIDTH), HEIGHT, random.uniform(-1,1), -random.uniform(1,3), random.randint(2,6), random.uniform(0,2*math.pi)])
    for p in particles[:]:
        p[0] += p[2]+0.5*math.sin(p[5])
        p[1] += p[3]
        p[4] -= 0.05
        if p[4]<=0 or p[1]<0:
            particles.remove(p)
        else:
            pygame.draw.circle(screen, (255,255,200), (int(p[0]), int(p[1])), int(p[4]))

    # Destellos
    if random.random() < 0.05:
        sparks.append([random.randint(0,WIDTH), random.randint(0,HEIGHT), random.randint(2,5)])
    for s in sparks[:]:
        pygame.draw.circle(screen, (255,255,255), (s[0], s[1]), s[2])
        s[1] -= 1
        if s[1]<0:
            sparks.remove(s)

    # Texto fade-in
    if fade_in and alpha < 255:
        alpha += 2
    text1 = font.render("💖 Te quiero, niña bonita 💖", True, WHITE)
    text2 = font.render("que ama los Braironts", True, WHITE)
    text1.set_alpha(alpha)
    text2.set_alpha(alpha)
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, 60))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 120))

    pygame.display.flip()
    clock.tick(60)
