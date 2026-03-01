import serial
import pygame
import math
import time

# ----------------- CONFIG -----------------
PORT = "/dev/ttyUSB0"  # your Nano port
BAUD = 115200
MAX_DISTANCE = 200      # cm, for scaling
RADAR_RADIUS = 250      # pixels
SWEEP_SPEED = 2         # degrees per frame
# ------------------------------------------

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"[INFO] Connected to Arduino on {PORT}")
except Exception as e:
    print(f"[ERROR] Cannot open Serial port {PORT}: {e}")
    exit(1)

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radar UI")
CENTER = (WIDTH // 2, HEIGHT // 2)

points = []
sweep_angle = 0  # degrees

# ----------------- FUNCTIONS -----------------
def draw_radar():
    global sweep_angle
    screen.fill((0,0,0))

    # Draw radar circles
    for r in range(50, RADAR_RADIUS+1, 50):
        pygame.draw.circle(screen, (0,255,0), CENTER, r, 1)

    # Draw sweep line
    rad_sweep = math.radians(sweep_angle)
    x = CENTER[0] + RADAR_RADIUS * math.cos(rad_sweep)
    y = CENTER[1] + RADAR_RADIUS * math.sin(rad_sweep)
    pygame.draw.line(screen, (0,255,0), CENTER, (x, y), 2)

    # Draw points
    for angle, dist in points:
        if dist < 0:
            continue
        r = min(dist / MAX_DISTANCE * RADAR_RADIUS, RADAR_RADIUS)
        rad = math.radians(angle)
        px = CENTER[0] + r * math.cos(rad)
        py = CENTER[1] + r * math.sin(rad)
        pygame.draw.circle(screen, (0,255,0), (int(px), int(py)), 4)

    sweep_angle = (sweep_angle + SWEEP_SPEED) % 360

def read_serial():
    try:
        line = ser.readline().decode().strip()
        if not line:
            return
        if "," in line:
            angle_str, dist_str = line.split(",")
            angle = int(angle_str)
            distance = float(dist_str)
            points.append((angle, distance))
            if len(points) > 200:
                points.pop(0)
            print(f"[DATA] Angle: {angle}, Distance: {distance}")  # LOG
    except Exception as e:
        print(f"[ERROR] {e}")

# ----------------- MAIN LOOP -----------------
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    read_serial()
    draw_radar()
    pygame.display.flip()
    clock.tick(60)  # limit to 60 FPS

pygame.quit()