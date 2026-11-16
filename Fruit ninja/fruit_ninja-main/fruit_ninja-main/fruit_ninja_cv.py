import cv2
import mediapipe as mp
import numpy as np
import random
import time
import math
from collections import deque

# -------------------------------------------------------------
# MediaPipe Setup
# -------------------------------------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

WIDTH, HEIGHT = 1280, 720

# -------------------------------------------------------------
# KAWAII CARTOON HELPERS
# -------------------------------------------------------------
def draw_kawaii_face(f, x, y, r, is_sliced=False, angle=0):
    if is_sliced:
        # Dizzy / Dead Face (X_X)
        cv2.line(f, (x - r//3, y - r//4), (x - r//6, y - r//8), (0,0,0), 3)
        cv2.line(f, (x - r//3, y - r//8), (x - r//6, y - r//4), (0,0,0), 3)
        cv2.line(f, (x + r//6, y - r//4), (x + r//3, y - r//8), (0,0,0), 3)
        cv2.line(f, (x + r//6, y - r//8), (x + r//3, y - r//4), (0,0,0), 3)
        cv2.circle(f, (x, y + r//8), r//8, (0,0,0), -1) 
    else:
        # Cute Anime Eyes
        cv2.circle(f, (x - r//4, y - r//6), r//6, (0, 0, 0), -1)
        cv2.circle(f, (x + r//4, y - r//6), r//6, (0, 0, 0), -1)
        # Eye Highlights
        cv2.circle(f, (x - r//4 - 2, y - r//6 - 2), r//12, (255, 255, 255), -1)
        cv2.circle(f, (x + r//4 - 2, y - r//6 - 2), r//12, (255, 255, 255), -1)
        # Pink Blush
        cv2.ellipse(f, (x - r//2, y), (r//6, r//10), 0, 0, 360, (150, 150, 255), -1)
        cv2.ellipse(f, (x + r//2, y), (r//6, r//10), 0, 0, 360, (150, 150, 255), -1)
        # Cute Smile
        cv2.ellipse(f, (x, y - r//8), (r//6, r//6), 0, 0, 180, (0, 0, 0), 2)

def draw_heart(img, x, y, s, c_in, c_out):
    cv2.circle(img, (x - s//2, y), s//2, c_out, 6)
    cv2.circle(img, (x + s//2, y), s//2, c_out, 6)
    pts = np.array([[x - s - 3, y + 2], [x + s + 3, y + 2], [x, y + s + 5]], np.int32)
    cv2.fillPoly(img, [pts], c_out)
    
    cv2.circle(img, (x - s//2, y), s//2, c_in, -1)
    cv2.circle(img, (x + s//2, y), s//2, c_in, -1)
    pts_in = np.array([[x - s, y + 1], [x + s, y + 1], [x, y + s]], np.int32)
    cv2.fillPoly(img, [pts_in], c_in)

# -------------------------------------------------------------
# CUTE CARTOON DRAWING FUNCTIONS 
# -------------------------------------------------------------
def draw_watermelon(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.circle(f, (x, y), r, (0, 0, 0), -1) 
        cv2.circle(f, (x, y), r - 3, (40, 200, 40), -1)
        cv2.circle(f, (x, y), r - 10, (40, 40, 230), -1)
        seeds = [(-r//2, -r//6), (r//2, -r//6), (-r//3, r//3), (r//3, r//3), (0, -r//2)]
        for sx, sy in seeds:
            cv2.circle(f, (x+sx, y+sy), 4, (0,0,0), -1)
        draw_kawaii_face(f, x, y, r)
    else:
        cv2.ellipse(f, (x, y), (r, r), angle, 0, 180, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (r-3, r-3), angle, 0, 180, (40, 200, 40), -1)
        cv2.ellipse(f, (x, y), (r-10, r-10), angle, 0, 180, (40, 40, 230), -1)
        draw_kawaii_face(f, x, y - r//3, r, True)

def draw_orange(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.line(f, (x, y - r + 5), (x, y - r - 15), (0, 0, 0), 8)
        cv2.line(f, (x, y - r + 5), (x, y - r - 15), (40, 80, 130), 4)
        cv2.ellipse(f, (x + 18, y - r - 5), (18, 9), -30, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x + 18, y - r - 5), (15, 6), -30, 0, 360, (40, 200, 40), -1)
        cv2.circle(f, (x, y), r, (0, 0, 0), -1)
        cv2.circle(f, (x, y), r - 3, (0, 140, 255), -1)
        draw_kawaii_face(f, x, y, r)
    else:
        cv2.ellipse(f, (x, y), (r, r), angle, 0, 180, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (r-3, r-3), angle, 0, 180, (0, 140, 255), -1)
        cv2.ellipse(f, (x, y), (r-6, r-6), angle, 0, 180, (255, 255, 255), -1)
        cv2.ellipse(f, (x, y), (r-10, r-10), angle, 0, 180, (0, 165, 255), -1)
        draw_kawaii_face(f, x, y - r//3, r, True)

def draw_apple(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.line(f, (x, y - r + 15), (x + 15, y - r - 20), (0, 0, 0), 8)
        cv2.line(f, (x, y - r + 15), (x + 15, y - r - 20), (40, 80, 130), 4)
        cv2.ellipse(f, (x - 20, y - r + 5), (20, 10), 30, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x - 20, y - r + 5), (17, 7), 30, 0, 360, (40, 200, 40), -1)
        cv2.circle(f, (x-5, y), r-2, (0,0,0), -1)
        cv2.circle(f, (x+5, y), r-2, (0,0,0), -1)
        cv2.circle(f, (x-5, y), r-5, (30, 30, 230), -1)
        cv2.circle(f, (x+5, y), r-5, (30, 30, 230), -1)
        draw_kawaii_face(f, x, y+5, r)
    else:
        cv2.ellipse(f, (x, y), (r, r), angle, 0, 180, (0,0,0), -1)
        cv2.ellipse(f, (x, y), (r-3, r-3), angle, 0, 180, (30, 30, 230), -1)
        cv2.ellipse(f, (x, y), (r-8, r-8), angle, 0, 180, (230, 240, 230), -1)
        draw_kawaii_face(f, x, y - r//3, r, True)

def draw_strawberry(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.ellipse(f, (x, y), (r, int(r*1.1)), 0, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (r-3, int(r*1.1)-3), 0, 0, 360, (40, 40, 230), -1)
        seeds = [(-r//2, -r//6), (r//2, -r//6), (-r//3, r//4), (r//3, r//4), (0, r//2.5), (-r//4, -r//2), (r//4, -r//2)]
        for sx, sy in seeds:
            cv2.ellipse(f, (int(x+sx), int(y+sy)), (2, 4), 0, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y-r+15), (r//2 + 10, r//4), 0, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y-r+15), (r//2 + 6, r//4 - 3), 0, 0, 360, (40, 200, 40), -1)
        cv2.ellipse(f, (x, y-r+5), (r//4, r//3), 0, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y-r+5), (r//4 - 3, r//3 - 3), 0, 0, 360, (40, 200, 40), -1)
        draw_kawaii_face(f, x, y+5, r)
    else:
        cv2.ellipse(f, (x, y), (r, int(r*1.1)), angle, 0, 180, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (r-3, int(r*1.1)-3), angle, 0, 180, (40, 40, 230), -1)
        draw_kawaii_face(f, x, y - r//3, r, True)

def draw_grapes(f, x, y, r, half=False, angle=0):
    grape_positions = [
        (0, int(r*0.7)), (-r//3, r//3), (r//3, r//3), 
        (-r//2, 0), (r//2, 0), (0, -r//3)
    ]
    grape_radius = int(r * 0.45)
    if not half:
        cv2.line(f, (x, y - r//2 + 5), (x, y - r - 20), (0, 0, 0), 8)
        cv2.line(f, (x, y - r//2 + 5), (x, y - r - 20), (40, 80, 130), 4) 
        cv2.ellipse(f, (x + 20, y - r - 15), (20, 10), -30, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x + 20, y - r - 15), (17, 7), -30, 0, 360, (40, 200, 40), -1)
        for ox, oy in grape_positions:
            cv2.circle(f, (int(x + ox), int(y + oy)), grape_radius + 3, (0, 0, 0), -1)
        for ox, oy in grape_positions:
            gx, gy = int(x + ox), int(y + oy)
            cv2.circle(f, (gx, gy), grape_radius, (190, 80, 160), -1)
            cv2.circle(f, (gx - grape_radius//3, gy - grape_radius//3), 4, (255, 255, 255), -1)
        draw_kawaii_face(f, x, y + r//8, r)
    else:
        for ox, oy in grape_positions[3:]: 
            cv2.circle(f, (int(x + ox), int(y + oy)), grape_radius + 3, (0, 0, 0), -1)
            cv2.circle(f, (int(x + ox), int(y + oy)), grape_radius, (190, 80, 160), -1)
        draw_kawaii_face(f, x, y - r//4, r, True)

def draw_avocado(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.ellipse(f, (x, y), (r, int(r*1.2)), 0, 0, 360, (0, 0, 0), -1) 
        cv2.ellipse(f, (x, y), (r-3, int(r*1.2)-3), 0, 0, 360, (20, 100, 20), -1)
        cv2.circle(f, (x, int(y + r//3.5)), r//2 + 3, (0, 0, 0), -1)
        cv2.circle(f, (x, int(y + r//3.5)), r//2, (40, 80, 130), -1) 
        draw_kawaii_face(f, x, y - r//4, r)
    else:
        cv2.ellipse(f, (x, y), (r, int(r*1.2)), angle, 0, 360, (0, 0, 0), -1) 
        cv2.ellipse(f, (x, y), (r-3, int(r*1.2)-3), angle, 0, 360, (140, 220, 140), -1)
        cv2.circle(f, (x, int(y + r//3.5)), r//2 + 3, (0, 0, 0), -1)
        cv2.circle(f, (x, int(y + r//3.5)), r//2, (40, 80, 130), -1) 
        draw_kawaii_face(f, x, y - r//4, r, True)

def draw_pineapple(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.ellipse(f, (x, y), (r, int(r*1.1)), 0, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (r-3, int(r*1.1)-3), 0, 0, 360, (0, 200, 255), -1)
        cv2.line(f, (x-r//2, y-r//2), (x+r//2, y+r//2), (0, 100, 200), 3)
        cv2.line(f, (x-r//2, y+r//2), (x+r//2, y-r//2), (0, 100, 200), 3)
        pts = np.array([[x-25, y-r-20], [x, y-r+10], [x, y-r-30], [x+10, y-r+10], [x+25, y-r-20]], np.int32)
        cv2.polylines(f, [pts], False, (0, 0, 0), 8)
        cv2.polylines(f, [pts], False, (40, 200, 40), 4)
        draw_kawaii_face(f, x, y+10, r)
    else:
        cv2.ellipse(f, (x, y), (r, int(r*1.1)), angle, 0, 180, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (r-3, int(r*1.1)-3), angle, 0, 180, (0, 200, 255), -1)
        draw_kawaii_face(f, x, y - r//4, r, True)

def draw_banana(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.circle(f, (x, y), int(r*0.8) + 3, (0, 0, 0), -1)
        cv2.circle(f, (x, y), int(r*0.8), (0, 220, 255), -1)
        cv2.circle(f, (x, y), int(r*0.8) - 10, (220, 240, 240), -1)
        draw_kawaii_face(f, x, y, r)
    else:
        cv2.circle(f, (x, y), int(r*0.6) + 3, (0, 0, 0), -1)
        cv2.circle(f, (x, y), int(r*0.6), (0, 220, 255), -1)
        cv2.circle(f, (x, y), int(r*0.6) - 6, (220, 240, 240), -1)
        draw_kawaii_face(f, x, y, int(r*0.8), True)

def draw_lemon(f, x, y, r, half=False, angle=0):
    if not half:
        cv2.ellipse(f, (x, y), (int(r*1.1), r), 20, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (int(r*1.1)-3, r-3), 20, 0, 360, (0, 255, 255), -1)
        cv2.ellipse(f, (x + 20, y - r + 10), (25, 12), -40, 0, 360, (0, 0, 0), -1)
        cv2.ellipse(f, (x + 20, y - r + 10), (22, 9), -40, 0, 360, (40, 200, 40), -1)
        draw_kawaii_face(f, x, y, r)
    else:
        cv2.ellipse(f, (x, y), (int(r*1.1), r), angle, 0, 180, (0, 0, 0), -1)
        cv2.ellipse(f, (x, y), (int(r*1.1)-3, r-3), angle, 0, 180, (0, 255, 255), -1)
        cv2.ellipse(f, (x, y), (int(r*1.1)-6, r-6), angle, 0, 180, (200, 255, 255), -1)
        draw_kawaii_face(f, x, y - r//3, r, True)

def draw_bomb(f, x, y, r):
    cv2.circle(f, (x, y), r, (255, 255, 255), -1) 
    cv2.circle(f, (x, y), r-3, (30, 30, 30), -1)
    cv2.rectangle(f, (x-12, y-r-12), (x+12, y-r+2), (0, 0, 0), -1)
    cv2.rectangle(f, (x-10, y-r-10), (x+10, y-r+2), (100, 100, 100), -1)
    sx, sy = x + 20, y - r - 20
    cv2.line(f, (x, y-r-10), (sx, sy), (150, 200, 250), 4)
    cv2.circle(f, (sx + random.randint(-2, 2), sy + random.randint(-2, 2)), 8, (0, 150, 255), -1)
    cv2.line(f, (x-15, y-10), (x-5, y), (255, 255, 255), 3)
    cv2.line(f, (x+15, y-10), (x+5, y), (255, 255, 255), 3)
    cv2.circle(f, (x-10, y+5), 4, (255, 255, 255), -1)
    cv2.circle(f, (x+10, y+5), 4, (255, 255, 255), -1)

# -------------------------------------------------------------
# Game Entities
# -------------------------------------------------------------
class Target:
    def __init__(self):
        self.x, self.y = random.randint(200, WIDTH - 200), HEIGHT
        self.radius = random.randint(50, 65) 
        self.vy, self.vx = random.uniform(-24.0, -34.0), random.uniform(-5.0, 5.0)
        self.gravity = 0.6
        self.t_id = random.choices(range(10), weights=[1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.5, 1.5, 1.5])[0]
        self.active = True

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        if self.y > HEIGHT + self.radius and self.vy > 0: self.active = False

    def draw(self, f):
        ix, iy = int(self.x), int(self.y)
        if self.t_id == 0: draw_watermelon(f, ix, iy, self.radius)
        elif self.t_id == 1: draw_orange(f, ix, iy, self.radius)
        elif self.t_id == 2: draw_apple(f, ix, iy, self.radius)
        elif self.t_id == 3: draw_strawberry(f, ix, iy, self.radius)
        elif self.t_id == 4: draw_grapes(f, ix, iy, self.radius)
        elif self.t_id == 5: draw_avocado(f, ix, iy, self.radius)
        elif self.t_id == 6: draw_pineapple(f, ix, iy, self.radius)
        elif self.t_id == 7: draw_bomb(f, ix, iy, self.radius)
        elif self.t_id == 8: draw_banana(f, ix, iy, self.radius)
        elif self.t_id == 9: draw_lemon(f, ix, iy, self.radius)

class SlicedHalf:
    def __init__(self, x, y, r, t_id, dir_x):
        self.x, self.y, self.radius, self.t_id = x, y, r, t_id
        self.vy, self.vx = random.uniform(-5, -10), dir_x * random.uniform(5, 12)
        self.gravity, self.angle = 0.8, random.randint(0, 360)
        self.rot = dir_x * random.randint(5, 15)

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.angle = (self.angle + self.rot) % 360

    def draw(self, f):
        ix, iy = int(self.x), int(self.y)
        if self.t_id == 0: draw_watermelon(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 1: draw_orange(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 2: draw_apple(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 3: draw_strawberry(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 4: draw_grapes(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 5: draw_avocado(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 6: draw_pineapple(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 8: draw_banana(f, ix, iy, self.radius, True, self.angle)
        elif self.t_id == 9: draw_lemon(f, ix, iy, self.radius, True, self.angle)

class Particle:
    def __init__(self, x, y, t_id):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-15, 15), random.uniform(-15, 15)
        self.gravity, self.life = 0.5, 1.0
        colors = {0:(40,40,220), 1:(0,165,255), 2:(30,30,230), 3:(40,40,230), 
                  4:(190,80,160), 5:(140,220,140), 6:(0,200,255), 7:(0,0,255),
                  8:(0,220,255), 9:(0,255,255)}
        self.c = colors.get(t_id, (255, 255, 255))

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.04

    def draw(self, f):
        if self.life > 0:
            rad = int(max(1, 10 * self.life))
            cv2.circle(f, (int(self.x), int(self.y)), rad + 2, (0,0,0), -1) 
            cv2.circle(f, (int(self.x), int(self.y)), rad, self.c, -1)

# -------------------------------------------------------------
# Collision & Main Logic
# -------------------------------------------------------------
def check_slice(trail, cx, cy, radius):
    if len(trail) < 2: return False
    x1, y1 = trail[-2]
    x2, y2 = trail[-1]
    line_sq = (x2 - x1)**2 + (y2 - y1)**2
    if line_sq == 0: return math.hypot(cx - x1, cy - y1) < radius + 15
    t = max(0, min(1, ((cx - x1) * (x2 - x1) + (cy - y1) * (y2 - y1)) / line_sq))
    return math.hypot(cx - (x1 + t * (x2 - x1)), cy - (y1 + t * (y2 - y1))) < (radius + 20)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    
    # 10 lives means 10 bomb strikes before game over
    score, lives = 0, 10 
    targets, halves, particles = [], [], []
    blade_trail = deque(maxlen=10)
    last_spawn = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        swipe_spd = 0

        if results.multi_hand_landmarks:
            fx = int(results.multi_hand_landmarks[0].landmark[8].x * w)
            fy = int(results.multi_hand_landmarks[0].landmark[8].y * h)
            blade_trail.append((fx, fy))
            if len(blade_trail) > 3:
                swipe_spd = math.hypot(fx - blade_trail[-3][0], fy - blade_trail[-3][1])
            if len(blade_trail) > 1:
                for i in range(1, len(blade_trail)):
                    thk = int(i * 1.5)
                    c_val = int((i / len(blade_trail)) * 255)
                    cv2.line(frame, blade_trail[i-1], blade_trail[i], (0, 200, 255), thk + 6) 
                    cv2.line(frame, blade_trail[i-1], blade_trail[i], (255, 255, 255), thk)
        else:
            blade_trail.clear()

        # Adjusted spawn timer to be balanced and not overwhelming
        if time.time() - last_spawn > max(0.5, 1.5 - (score * 0.01)):
            targets.append(Target())
            last_spawn = time.time()

        for entity_list in (halves, particles, targets):
            for e in entity_list[:]:
                e.update()
                e.draw(frame)
                
                if hasattr(e, 'active') and not e.active:
                    targets.remove(e)
                elif not hasattr(e, 'active'):
                    if (hasattr(e, 'life') and e.life <= 0) or e.y > HEIGHT:
                        entity_list.remove(e)

        for t in targets[:]:
            if swipe_spd > 30 and check_slice(list(blade_trail), t.x, t.y, t.radius):
                if t.t_id == 7: 
                    lives -= 1
                    for _ in range(40): particles.append(Particle(t.x, t.y, 7))
                    cv2.circle(frame, (int(t.x), int(t.y)), 300, (255, 255, 255), 15)
                else:
                    score += 10
                    for _ in range(25): particles.append(Particle(t.x, t.y, t.t_id))
                    halves.extend([SlicedHalf(t.x, t.y, t.radius, t.t_id, -1), 
                                   SlicedHalf(t.x, t.y, t.radius, t.t_id, 1)])
                targets.remove(t)

        cv2.putText(frame, f"SCORE: {score}", (30, 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 8)
        cv2.putText(frame, f"SCORE: {score}", (30, 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, (100, 255, 255), 3)
        
        cv2.putText(frame, "LIVES:", (WIDTH - 330, 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 8)
        cv2.putText(frame, "LIVES:", (WIDTH - 330, 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 255, 255), 3)
        
        # Calculate how many hearts to show based on 2 hits per heart
        active_hearts = (lives + 1) // 2
        for i in range(5):
            c_out = (0, 0, 0)
            c_in = (50, 50, 255) if i < active_hearts else (200, 200, 200)
            draw_heart(frame, WIDTH - 170 + (i*40), 35, 12, c_in, c_out)

        if lives <= 0:
            cv2.putText(frame, "GAME OVER", (WIDTH//2 - 200, HEIGHT//2), cv2.FONT_HERSHEY_DUPLEX, 2.0, (0, 0, 0), 10)
            cv2.putText(frame, "GAME OVER", (WIDTH//2 - 200, HEIGHT//2), cv2.FONT_HERSHEY_DUPLEX, 2.0, (50, 50, 255), 4)
            cv2.putText(frame, "Press 'R' to Restart", (WIDTH//2 - 150, HEIGHT//2 + 60), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0), 6)
            cv2.putText(frame, "Press 'R' to Restart", (WIDTH//2 - 150, HEIGHT//2 + 60), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)

        cv2.imshow("Kawaii Cartoon Fruit Ninja", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27: break
        elif key == ord('r') and lives <= 0:
            lives, score = 10, 0
            targets.clear(); halves.clear(); particles.clear(); blade_trail.clear()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()