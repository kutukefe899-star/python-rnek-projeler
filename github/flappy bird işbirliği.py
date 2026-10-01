import pygame
import sys
import random
import time
import math

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Flappy Bird - WhiteHacker Edition")
clock = pygame.time.Clock()

SCALE = WIDTH / 360.0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (113, 197, 207)
YELLOW = (250, 210, 40)
ORANGE = (245, 120, 20)
RED = (235, 20, 20)
DARK_RED = (140, 0, 0)
GLOW_RED = (255, 90, 90)
GRAY = (60, 60, 60)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (30, 30, 30)
MATRIX_GREEN = (0, 255, 65)

PIPE_BODY_BASE = (115, 190, 45)
PIPE_BODY_LIGHT = (170, 230, 80)
PIPE_BODY_DARK = (70, 135, 25)
PIPE_BODY_SHADOW = (40, 85, 15)

MATRIX_BG = (5, 15, 5)
MATRIX_PIPE_BASE = (0, 180, 40)
MATRIX_PIPE_LIGHT = (50, 255, 100)
MATRIX_PIPE_DARK = (0, 90, 20)
MATRIX_PIPE_SHADOW = (0, 40, 10)
MATRIX_GROUND = (10, 30, 10)
MATRIX_GROUND_TOP = (0, 200, 50)

font_title = pygame.font.SysFont("arial", int(22 * SCALE), bold=True)
font_main = pygame.font.SysFont("arial", int(17 * SCALE), bold=True)
font_small = pygame.font.SysFont("arial", int(12 * SCALE), bold=True)
font_matrix = pygame.font.SysFont("consolas", int(14 * SCALE), bold=True)

keyboard_overlay = pygame.Surface((WIDTH, HEIGHT))
keyboard_overlay.fill((10, 10, 15))

STATE_START = 0
STATE_PLAYING = 1
STATE_BOSS_FIGHT = 2
STATE_GAME_OVER = 3
STATE_ADMIN_KEYBOARD = 4
STATE_ADMIN_MENU = 5
STATE_MATRIX_ENDING = 7
STATE_BOSS_VICTORY = 8
STATE_DEV_INFO = 9

current_state = STATE_START

bird_x = int(WIDTH * 0.22)
bird_y = int(HEIGHT * 0.4)
bird_radius = int(16 * SCALE)
bird_vel = 0
gravity = 0.38 * SCALE
jump_strength = -5.8 * SCALE
bird_angle = 0
hover_counter = 0

no_pipes_mode = False
god_mode = False
auto_score_timer = 0
is_matrix_mode = False
matrix_start_time = 0

class MatrixRain:
    def __init__(self):
        self.columns = max(1, int(WIDTH / (16 * SCALE)))
        self.drops = [random.randint(-20, 0) for _ in range(self.columns)]

    def draw(self):
        for i in range(len(self.drops)):
            char = str(random.randint(0, 1))
            x = i * int(16 * SCALE)
            y = self.drops[i] * int(18 * SCALE)
            txt = font_matrix.render(char, True, MATRIX_GREEN)
            screen.blit(txt, (x, y))
            if y > HEIGHT or random.random() > 0.975:
                self.drops[i] = 0
            self.drops[i] += 1

matrix_rain = MatrixRain()

blood_particles = []
bullets = []
muzzle_flash_timer = 0

ground_height = int(HEIGHT * 0.12)
pipe_width = int(58 * SCALE)
pipe_gap = int(145 * SCALE)
pipe_speed = 3.2 * SCALE
pipes = []
spawn_pipe_timer = 0

score = 0
score_rect = pygame.Rect(int(10 * SCALE), int(10 * SCALE), int(120 * SCALE), int(40 * SCALE))
score_click_count = 0
last_score_click_time = 0

admin_btn_rect = pygame.Rect(WIDTH - int(105 * SCALE), int(12 * SCALE), int(95 * SCALE), int(32 * SCALE))
back_btn_rect = pygame.Rect(int(15 * SCALE), int(12 * SCALE), int(80 * SCALE), int(32 * SCALE))

play_btn_rect = pygame.Rect(WIDTH // 2 - int(70 * SCALE), HEIGHT // 2 - int(20 * SCALE), int(140 * SCALE), int(48 * SCALE))
dev_btn_rect = pygame.Rect(WIDTH // 2 - int(100 * SCALE), HEIGHT - ground_height - int(52 * SCALE), int(200 * SCALE), int(38 * SCALE))

entered_password = ""
pressed_key_symbol = None
pressed_key_time = 0

KEY_ROWS = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'SIL', 'OK']
]

def trigger_matrix_easter_egg():
    global is_matrix_mode, matrix_start_time, current_state
    is_matrix_mode = True
    matrix_start_time = time.time()
    current_state = STATE_PLAYING

def reset_game():
    global bird_x, bird_y, bird_vel, score, pipes, current_state, bird_angle
    global death_reason, no_pipes_mode, auto_score_timer, blood_particles, is_matrix_mode, god_mode
    global boss_hp, player_hp, bullets, indicator_pos, indicator_speed, indicator_dir, entered_password

    bird_x = int(WIDTH * 0.22)
    bird_y = int(HEIGHT * 0.4)
    bird_vel = 0
    bird_angle = 0
    blood_particles.clear()
    bullets.clear()
    score = 0
    pipes = []
    no_pipes_mode = False
    god_mode = False
    is_matrix_mode = False
    auto_score_timer = 0
    boss_hp = 5
    player_hp = 3
    indicator_pos = 0.0
    indicator_dir = 1
    indicator_speed = base_indicator_speed
    entered_password = ""
    current_state = STATE_START
    death_reason = ""

monster_x = WIDTH - int(100 * SCALE)
monster_y = HEIGHT // 2 - int(70 * SCALE)
boss_hp = 5
player_hp = 3
boss_hover = 0
boss_hit_anim = 0
boss_attack_anim = 0

bar_w = int(WIDTH * 0.8)
bar_h = int(26 * SCALE)
bar_x = (WIDTH - bar_w) // 2
bar_y = HEIGHT - ground_height - int(60 * SCALE)

indicator_pos = 0.0
indicator_dir = 1
base_indicator_speed = 0.024
indicator_speed = base_indicator_speed

target_start = 0.35
target_width = 0.15

death_reason = ""

def randomize_target():
    global target_start, target_width, indicator_speed, indicator_pos, indicator_dir
    target_width = random.uniform(0.12, 0.18)
    target_start = random.uniform(0.08, 0.92 - target_width)
    indicator_speed = base_indicator_speed + (5 - boss_hp) * 0.003
    indicator_pos = 0.0
    indicator_dir = 1

def spawn_pipe():
    min_h = int(60 * SCALE)
    max_h = HEIGHT - ground_height - pipe_gap - min_h
    top_h = random.randint(min_h, max(min_h + 10, max_h))
    bottom_h = HEIGHT - ground_height - top_h - pipe_gap
    pipes.append({'x': WIDTH, 'top': top_h, 'bottom': bottom_h, 'passed': False})

def create_blood(x, y, count=35):
    global blood_particles
    for _ in range(count):
        blood_particles.append({
            'x': x,
            'y': y,
            'vx': random.uniform(-9, 9) * SCALE,
            'vy': random.uniform(-11, 3) * SCALE,
            'size': random.uniform(3, 8) * SCALE,
            'color': random.choice([RED, DARK_RED, (180, 0, 0)])
        })

def update_and_draw_blood():
    global blood_particles
    for p in blood_particles[:]:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['vy'] += 0.4 * SCALE
        p['size'] = max(0, p['size'] - 0.1)
        pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), int(p['size']))
        if p['y'] >= HEIGHT - ground_height or p['size'] <= 0:
            if p in blood_particles:
                blood_particles.remove(p)

def draw_realistic_pipe_part(rect, is_cap=False):
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    if h <= 0: return

    c_base = MATRIX_PIPE_BASE if is_matrix_mode else PIPE_BODY_BASE
    c_light = MATRIX_PIPE_LIGHT if is_matrix_mode else PIPE_BODY_LIGHT
    c_dark = MATRIX_PIPE_DARK if is_matrix_mode else PIPE_BODY_DARK
    c_shadow = MATRIX_PIPE_SHADOW if is_matrix_mode else PIPE_BODY_SHADOW

    pygame.draw.rect(screen, c_base, (x, y, w, h))
    light_w = int(w * 0.22)
    pygame.draw.rect(screen, c_light, (x + int(w * 0.12), y, light_w, h))
    dark_w = int(w * 0.25)
    shadow_w = int(w * 0.1)
    pygame.draw.rect(screen, c_dark, (x + w - dark_w, y, dark_w, h))
    pygame.draw.rect(screen, c_shadow, (x + w - shadow_w, y, shadow_w, h))
    pygame.draw.rect(screen, MATRIX_GREEN if is_matrix_mode else BLACK, (x, y, w, h), int(2 * SCALE))

def draw_pipes():
    cap_h = int(24 * SCALE)
    cap_overhang = int(4 * SCALE)
    for pipe in pipes:
        px = pipe['x']
        top_body_h = max(0, pipe['top'] - cap_h)
        if top_body_h > 0:
            draw_realistic_pipe_part(pygame.Rect(px, 0, pipe_width, top_body_h))
        draw_realistic_pipe_part(pygame.Rect(px - cap_overhang, top_body_h, pipe_width + cap_overhang * 2, cap_h), is_cap=True)

        bot_y = HEIGHT - ground_height - pipe['bottom']
        draw_realistic_pipe_part(pygame.Rect(px - cap_overhang, bot_y, pipe_width + cap_overhang * 2, cap_h), is_cap=True)
        bot_body_h = max(0, pipe['bottom'] - cap_h)
        if bot_body_h > 0:
            draw_realistic_pipe_part(pygame.Rect(px, bot_y + cap_h, pipe_width, bot_body_h))

def draw_bird(x, y, angle):
    bird_surf = pygame.Surface((bird_radius * 3.5, bird_radius * 3.5), pygame.SRCALPHA)
    cx, cy = bird_radius * 1.75, bird_radius * 1.75

    body_color = MATRIX_GREEN if is_matrix_mode else YELLOW
    wing_color = (0, 100, 20) if is_matrix_mode else WHITE
    beak_color = (0, 200, 80) if is_matrix_mode else ORANGE
    line_color = MATRIX_GREEN if is_matrix_mode else BLACK

    pygame.draw.polygon(bird_surf, beak_color, [
        (cx - bird_radius * 0.9, cy - bird_radius * 0.2),
        (cx - bird_radius * 1.3, cy - bird_radius * 0.5),
        (cx - bird_radius * 1.2, cy + bird_radius * 0.2)
    ])
    pygame.draw.circle(bird_surf, body_color, (int(cx), int(cy)), bird_radius)
    pygame.draw.circle(bird_surf, line_color, (int(cx), int(cy)), bird_radius, 2)

    beak_pts = [
        (cx + bird_radius * 0.5, cy - bird_radius * 0.25),
        (cx + bird_radius * 1.35, cy + bird_radius * 0.1),
        (cx + bird_radius * 0.5, cy + bird_radius * 0.45)
    ]
    pygame.draw.polygon(bird_surf, beak_color, beak_pts)
    pygame.draw.polygon(bird_surf, line_color, beak_pts, 2)

    eye_x, eye_y, eye_r = cx + bird_radius * 0.35, cy - bird_radius * 0.35, bird_radius * 0.42
    pygame.draw.circle(bird_surf, WHITE if not is_matrix_mode else BLACK, (int(eye_x), int(eye_y)), int(eye_r))
    pygame.draw.circle(bird_surf, line_color, (int(eye_x), int(eye_y)), int(eye_r), 2)
    pygame.draw.circle(bird_surf, MATRIX_GREEN if is_matrix_mode else BLACK, (int(eye_x + eye_r * 0.3), int(eye_y)), int(eye_r * 0.45))

    wing_rect = pygame.Rect(cx - bird_radius * 0.7, cy - bird_radius * 0.1, bird_radius * 0.85, bird_radius * 0.55)
    pygame.draw.ellipse(bird_surf, wing_color, wing_rect)
    pygame.draw.ellipse(bird_surf, line_color, wing_rect, 2)

    if current_state == STATE_BOSS_FIGHT:
        pygame.draw.rect(bird_surf, DARK_RED if is_matrix_mode else GRAY, (cx + bird_radius * 0.3, cy, int(18 * SCALE), int(7 * SCALE)))
        pygame.draw.rect(bird_surf, BLACK, (cx + bird_radius * 0.3, cy + int(4*SCALE), int(6 * SCALE), int(7 * SCALE)))
        if muzzle_flash_timer > 0:
            pygame.draw.circle(bird_surf, YELLOW, (int(cx + bird_radius * 1.5), int(cy + int(3.5*SCALE))), int(8 * SCALE))
            pygame.draw.circle(bird_surf, ORANGE, (int(cx + bird_radius * 1.5), int(cy + int(3.5*SCALE))), int(4 * SCALE))

    rotated_surf = pygame.transform.rotate(bird_surf, -angle)
    new_rect = rotated_surf.get_rect(center=(int(x), int(y)))
    screen.blit(rotated_surf, new_rect.topleft)

def draw_monster(x, y, is_attacking=False, is_hit=False):
    head_r = int(34 * SCALE)
    px, py = x, y + int(140 * SCALE)
    hx, hy = px, py - int(160 * SCALE)

    body_color = RED if is_hit else BLACK
    pygame.draw.circle(screen, body_color, (hx, hy), head_r)

    pygame.draw.polygon(screen, body_color, [(hx - 15, hy - 25), (hx - 35, hy - 55), (hx - 5, hy - 35)])
    pygame.draw.polygon(screen, body_color, [(hx + 15, hy - 25), (hx + 35, hy - 55), (hx + 5, hy - 35)])

    eye_col = GLOW_RED if not is_hit else WHITE
    pygame.draw.circle(screen, eye_col, (hx - int(10*SCALE), hy - int(3*SCALE)), int(9 * SCALE))
    pygame.draw.circle(screen, eye_col, (hx + int(10*SCALE), hy - int(3*SCALE)), int(9 * SCALE))

    pygame.draw.line(screen, body_color, (hx, hy + head_r), (px, py), int(18 * SCALE))

    if is_attacking:
        pygame.draw.line(screen, RED, (px - int(10*SCALE), py - int(80*SCALE)), (bird_x + int(50*SCALE), bird_y), int(12 * SCALE))
        pygame.draw.line(screen, DARK_RED, (px - int(10*SCALE), py - int(110*SCALE)), (bird_x + int(40*SCALE), bird_y + int(20*SCALE)), int(10 * SCALE))
    else:
        pygame.draw.line(screen, body_color, (px - int(20*SCALE), py - int(80*SCALE)), (px - int(45*SCALE), py - int(50*SCALE)), int(12 * SCALE))

def draw_animated_keyboard():
    global pressed_key_symbol

    if time.time() - pressed_key_time > 0.1:
        pressed_key_symbol = None

    screen.blit(keyboard_overlay, (0, 0))

    t_title = font_title.render("ADMIN GİRİŞİ", True, MATRIX_GREEN)
    screen.blit(t_title, (WIDTH // 2 - t_title.get_width() // 2, int(40 * SCALE)))

    input_box = pygame.Rect(int(30 * SCALE), int(85 * SCALE), WIDTH - int(60 * SCALE), int(42 * SCALE))
    pygame.draw.rect(screen, DARK_GRAY, input_box, border_radius=8)
    pygame.draw.rect(screen, MATRIX_GREEN, input_box, int(2 * SCALE), border_radius=8)

    txt_surf = font_title.render(entered_password, True, WHITE)
    screen.blit(txt_surf, (input_box.x + int(15 * SCALE), input_box.y + int(8 * SCALE)))

    start_y = int(150 * SCALE)
    key_h = int(45 * SCALE)
    margin = int(4 * SCALE)

    for row_idx, row in enumerate(KEY_ROWS):
        total_keys = len(row)
        key_w = (WIDTH - int(30 * SCALE) - (total_keys * margin)) // total_keys
        start_x = int(15 * SCALE)
        for col_idx, key in enumerate(row):
            kx = start_x + col_idx * (key_w + margin)
            ky = start_y + row_idx * (key_h + margin)

            kw = key_w + (int(6 * SCALE) if key in ['SIL', 'OK'] else 0)
            key_rect = pygame.Rect(kx, ky, kw, key_h)

            is_pressed = (pressed_key_symbol == key)

            if is_pressed:
                draw_rect = key_rect.inflate(int(-6 * SCALE), int(-6 * SCALE))
                bg_col = MATRIX_GREEN
                txt_col = BLACK
            else:
                draw_rect = key_rect
                bg_col = GRAY if key not in ['SIL', 'OK'] else DARK_RED if key == 'SIL' else (0, 150, 50)
                txt_col = WHITE

            pygame.draw.rect(screen, bg_col, draw_rect, border_radius=6)
            pygame.draw.rect(screen, WHITE if is_pressed else BLACK, draw_rect, int(1.5 * SCALE), border_radius=6)

            k_txt = font_small.render(key, True, txt_col)
            screen.blit(k_txt, (draw_rect.centerx - k_txt.get_width() // 2, draw_rect.centery - k_txt.get_height() // 2))

    pygame.draw.rect(screen, RED, back_btn_rect, border_radius=6)
    screen.blit(font_small.render("< İptal", True, WHITE), (back_btn_rect.x + int(12*SCALE), back_btn_rect.y + int(7*SCALE)))

def handle_keyboard_click(mx, my):
    global entered_password, current_state, pressed_key_symbol, pressed_key_time

    if back_btn_rect.collidepoint(mx, my):
        current_state = STATE_PLAYING if score > 0 else STATE_START
        return

    start_y = int(150 * SCALE)
    key_h = int(45 * SCALE)
    margin = int(4 * SCALE)

    for row_idx, row in enumerate(KEY_ROWS):
        total_keys = len(row)
        key_w = (WIDTH - int(30 * SCALE) - (total_keys * margin)) // total_keys
        start_x = int(15 * SCALE)

        for col_idx, key in enumerate(row):
            kx = start_x + col_idx * (key_w + margin)
            ky = start_y + row_idx * (key_h + margin)
            kw = key_w + (int(6 * SCALE) if key in ['SIL', 'OK'] else 0)

            key_rect = pygame.Rect(kx, ky, kw, key_h)
            if key_rect.collidepoint(mx, my):
                pressed_key_symbol = key
                pressed_key_time = time.time()

                if key == 'SIL':
                    entered_password = entered_password[:-1]
                elif key == 'OK':
                    pw = entered_password.lower()
                    if len(pw) == 11 and sum(ord(c) * (i + 2) for i, c in enumerate(pw)) == 8100 and ord(pw[0]) == 119 and ord(pw[-1]) == 114:
                        current_state = STATE_ADMIN_MENU
                        entered_password = ""
                    else:
                        entered_password = ""
                else:
                    if len(entered_password) < 15:
                        entered_password += key.lower()
running = True

while running:
    clock.tick(60)

    if muzzle_flash_timer > 0:
        muzzle_flash_timer -= 1

    bg_color = MATRIX_BG if is_matrix_mode else SKY_BLUE
    screen.fill(bg_color)

    if current_state != STATE_ADMIN_KEYBOARD:
        if is_matrix_mode and current_state != STATE_MATRIX_ENDING:
            matrix_rain.draw()

        if is_matrix_mode and current_state == STATE_PLAYING:
            if time.time() - matrix_start_time >= 6.0:
                current_state = STATE_MATRIX_ENDING

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if current_state == STATE_ADMIN_KEYBOARD:
                handle_keyboard_click(mx, my)
                continue

            if admin_btn_rect.collidepoint(mx, my) and current_state in [STATE_PLAYING, STATE_START]:
                current_state = STATE_ADMIN_KEYBOARD
                entered_password = ""
                continue

            if current_state == STATE_ADMIN_MENU and back_btn_rect.collidepoint(mx, my):
                current_state = STATE_PLAYING if score > 0 else STATE_START
                continue

            if current_state == STATE_DEV_INFO:
                current_state = STATE_START
                continue

            if current_state in [STATE_START, STATE_PLAYING] and score_rect.collidepoint(mx, my):
                now = time.time()
                if now - last_score_click_time < 0.8:
                    score_click_count += 1
                else:
                    score_click_count = 1
                last_score_click_time = now
                if score_click_count >= 5:
                    trigger_matrix_easter_egg()
                    score_click_count = 0
                continue

            if current_state == STATE_START:
                if play_btn_rect.collidepoint(mx, my):
                    current_state = STATE_PLAYING
                    bird_vel = jump_strength
                elif dev_btn_rect.collidepoint(mx, my):
                    current_state = STATE_DEV_INFO
                continue

            elif current_state == STATE_PLAYING:
                bird_vel = jump_strength

            elif current_state == STATE_BOSS_FIGHT:
                if target_start <= indicator_pos <= (target_start + target_width):
                    bullets.append({'x': bird_x + int(25 * SCALE), 'y': bird_y})
                    muzzle_flash_timer = 5
                    boss_hp -= 1
                    boss_hit_anim = 12
                    randomize_target()

                    if boss_hp <= 0:
                        create_blood(monster_x, monster_y, 80)
                        current_state = STATE_BOSS_VICTORY
                else:
                    player_hp -= 1
                    boss_attack_anim = 22
                    create_blood(bird_x, bird_y, 30)
                    randomize_target()

                    if player_hp <= 0:
                        death_reason = "Boss Seni Pençeleriyle Parçaladı!"
                        current_state = STATE_GAME_OVER

            elif current_state in [STATE_GAME_OVER, STATE_MATRIX_ENDING, STATE_BOSS_VICTORY]:
                reset_game()

            elif current_state == STATE_ADMIN_MENU:
                btn1 = pygame.Rect(30 * SCALE, 140 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
                btn2 = pygame.Rect(30 * SCALE, 190 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
                btn3 = pygame.Rect(30 * SCALE, 240 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
                btn4 = pygame.Rect(30 * SCALE, 290 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
                btn5 = pygame.Rect(30 * SCALE, 340 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)

                if btn1.collidepoint(mx, my):
                    pipes.clear()
                    no_pipes_mode = True
                    current_state = STATE_PLAYING
                elif btn2.collidepoint(mx, my):
                    score = 50
                    current_state = STATE_BOSS_FIGHT
                    randomize_target()
                elif btn3.collidepoint(mx, my):
                    create_blood(monster_x, monster_y, 80)
                    current_state = STATE_BOSS_VICTORY
                elif btn4.collidepoint(mx, my):
                    god_mode = not god_mode
                elif btn5.collidepoint(mx, my):
                    trigger_matrix_easter_egg()

    g_base = MATRIX_GROUND if is_matrix_mode else (222, 216, 149)
    g_top = MATRIX_GROUND_TOP if is_matrix_mode else (75, 195, 50)
    pygame.draw.rect(screen, g_base, (0, HEIGHT - ground_height, WIDTH, ground_height))
    pygame.draw.rect(screen, g_top, (0, HEIGHT - ground_height, WIDTH, int(14 * SCALE)))

    if current_state == STATE_START:
        hover_counter += 0.08
        bird_y = int(HEIGHT * 0.4) + math.sin(hover_counter) * 10
        bird_angle = 0

    elif current_state == STATE_PLAYING:
        bird_vel += gravity
        bird_y += bird_vel
        bird_angle = max(-30, min(bird_vel * 4, 70))

        if bird_y - bird_radius <= 0:
            bird_y = bird_radius
            bird_vel = 0

        if no_pipes_mode:
            auto_score_timer += 1
            if auto_score_timer >= 60:
                score += 1
                auto_score_timer = 0
                if score >= 50:
                    current_state = STATE_BOSS_FIGHT
                    randomize_target()
        else:
            spawn_pipe_timer += 1
            if spawn_pipe_timer > 85:
                spawn_pipe()
                spawn_pipe_timer = 0

            for pipe in pipes[:]:
                pipe['x'] -= pipe_speed
                if not pipe['passed'] and pipe['x'] < bird_x:
                    pipe['passed'] = True
                    score += 1
                    if score >= 50:
                        current_state = STATE_BOSS_FIGHT
                        randomize_target()

                top_rect = pygame.Rect(pipe['x'], 0, pipe_width, pipe['top'])
                bottom_rect = pygame.Rect(pipe['x'], HEIGHT - ground_height - pipe['bottom'], pipe_width, pipe['bottom'])
                bird_rect = pygame.Rect(bird_x - bird_radius + 4, bird_y - bird_radius + 4, bird_radius*2 - 8, bird_radius*2 - 8)

                if not god_mode:
                    if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                        death_reason = "Boruya Çarptın!"
                        current_state = STATE_GAME_OVER

                if pipe['x'] < -pipe_width - int(10 * SCALE):
                    pipes.remove(pipe)

        if bird_y >= HEIGHT - ground_height - bird_radius:
            bird_y = HEIGHT - ground_height - bird_radius
            if not god_mode:
                death_reason = "Yere Düşüp Öldün!"
                current_state = STATE_GAME_OVER

    elif current_state == STATE_BOSS_FIGHT:
        bird_y = HEIGHT // 2
        bird_angle = 0

        boss_hover += 0.05
        cur_monster_y = monster_y + math.sin(boss_hover) * 12

        indicator_pos += indicator_speed * indicator_dir
        if indicator_pos >= 1.0:
            indicator_pos = 1.0
            indicator_dir = -1
        elif indicator_pos <= 0.0:
            indicator_pos = 0.0
            indicator_dir = 1

        for bullet in bullets[:]:
            bullet['x'] += 15 * SCALE
            pygame.draw.rect(screen, YELLOW, (int(bullet['x']), int(bullet['y'] - 3), int(12 * SCALE), int(6 * SCALE)))
            if bullet['x'] >= monster_x:
                create_blood(monster_x, cur_monster_y, 20)
                bullets.remove(bullet)

        if boss_attack_anim > 0:
            boss_attack_anim -= 1

        if boss_hit_anim > 0:
            boss_hit_anim -= 1

        draw_monster(monster_x, cur_monster_y, is_attacking=(boss_attack_anim > 0), is_hit=(boss_hit_anim > 0))

        pygame.draw.rect(screen, BLACK, (bar_x - 3, bar_y - 3, bar_w + 6, bar_h + 6), border_radius=8)
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_w, bar_h), border_radius=6)

        t_x = bar_x + int(bar_w * target_start)
        t_w = int(bar_w * target_width)
        pygame.draw.rect(screen, MATRIX_GREEN, (t_x, bar_y, t_w, bar_h), border_radius=4)

        ind_x = bar_x + int(bar_w * indicator_pos)
        pygame.draw.line(screen, RED, (ind_x, bar_y - 5), (ind_x, bar_y + bar_h + 5), int(5 * SCALE))

        txt_b = font_small.render(f"BOSS HP: {'♥' * boss_hp}", True, RED)
        txt_p = font_small.render(f"CANIN: {'♥' * player_hp}", True, MATRIX_GREEN)
        screen.blit(txt_b, (WIDTH - int(120 * SCALE), bar_y - int(25 * SCALE)))
        screen.blit(txt_p, (bar_x, bar_y - int(25 * SCALE)))

    if not no_pipes_mode and current_state in [STATE_PLAYING, STATE_START]:
        draw_pipes()

    update_and_draw_blood()
    draw_bird(bird_x, bird_y, bird_angle)

    score_txt = font_main.render(f"Skor: {score}", True, MATRIX_GREEN if is_matrix_mode else BLACK)
    screen.blit(score_txt, (15 * SCALE, 15 * SCALE))

    pygame.draw.rect(screen, GRAY, admin_btn_rect, border_radius=6)
    btn_txt = font_small.render("Admin Panel", True, WHITE)
    screen.blit(btn_txt, (admin_btn_rect.x + int(10*SCALE), admin_btn_rect.y + int(7*SCALE)))

    if current_state == STATE_START:
        box_w = WIDTH - int(30 * SCALE)
        box_h = int(105 * SCALE)
        box_x = int(15 * SCALE)
        box_y = int(55 * SCALE)

        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((0, 0, 0, 160))
        screen.blit(box_surf, (box_x, box_y))
        pygame.draw.rect(screen, MATRIX_GREEN if is_matrix_mode else WHITE, (box_x, box_y, box_w, box_h), int(2 * SCALE), border_radius=8)

        t_err_title = font_small.render("Oyundan Kaldırılan Hatalar:", True, MATRIX_GREEN if is_matrix_mode else YELLOW)
        e1 = font_small.render("1) Boruların üstünden geçme kaldırıldı", True, WHITE)
        e2 = font_small.render("2) Boss savaşında çubuk takılması kaldırıldı", True, WHITE)
        e3 = font_small.render("3) Admin paneli klavye gecikmesi kaldırıldı", True, WHITE)

        screen.blit(t_err_title, (box_x + int(10 * SCALE), box_y + int(8 * SCALE)))
        screen.blit(e1, (box_x + int(10 * SCALE), box_y + int(30 * SCALE)))
        screen.blit(e2, (box_x + int(10 * SCALE), box_y + int(52 * SCALE)))
        screen.blit(e3, (box_x + int(10 * SCALE), box_y + int(74 * SCALE)))

        pygame.draw.rect(screen, (0, 180, 70), play_btn_rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, play_btn_rect, int(2.5 * SCALE), border_radius=12)
        txt_play = font_title.render("OYNA", True, WHITE)
        screen.blit(txt_play, (play_btn_rect.centerx - txt_play.get_width() // 2, play_btn_rect.centery - txt_play.get_height() // 2))

        pygame.draw.rect(screen, DARK_GRAY, dev_btn_rect, border_radius=8)
        pygame.draw.rect(screen, LIGHT_GRAY, dev_btn_rect, int(1.5 * SCALE), border_radius=8)
        txt_dev = font_small.render("Oyun Yapımcısı (Tıkla)", True, WHITE)
        screen.blit(txt_dev, (dev_btn_rect.centerx - txt_dev.get_width() // 2, dev_btn_rect.centery - txt_dev.get_height() // 2))

    elif current_state == STATE_DEV_INFO:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 15, 235))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, RED, back_btn_rect, border_radius=6)
        screen.blit(font_small.render("< Geri", True, WHITE), (back_btn_rect.x + int(15*SCALE), back_btn_rect.y + int(7*SCALE)))

        yt_w, yt_h = int(70 * SCALE), int(48 * SCALE)
        yt_x, yt_y = WIDTH // 2 - yt_w // 2, HEIGHT // 2 - int(60 * SCALE)

        pygame.draw.rect(screen, RED, (yt_x, yt_y, yt_w, yt_h), border_radius=12)
        tri_pts = [
            (yt_x + int(26 * SCALE), yt_y + int(13 * SCALE)),
            (yt_x + int(26 * SCALE), yt_y + int(35 * SCALE)),
            (yt_x + int(48 * SCALE), yt_y + int(24 * SCALE))
        ]
        pygame.draw.polygon(screen, WHITE, tri_pts)

        txt_yt = font_title.render("YouTube", True, WHITE)
        screen.blit(txt_yt, (WIDTH // 2 - txt_yt.get_width() // 2, yt_y + yt_h + int(15 * SCALE)))

        txt_channel = font_title.render("muhammet efe & oyuncanavarı", True, MATRIX_GREEN)
        screen.blit(txt_channel, (WIDTH // 2 - txt_channel.get_width() // 2, yt_y + yt_h + int(50 * SCALE)))

    elif current_state == STATE_GAME_OVER:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        t1 = font_title.render("OYUN BİTTİ", True, RED)
        t2 = font_main.render(f"{death_reason}", True, WHITE)
        t3 = font_small.render("Yeniden Başlamak için Dokun", True, LIGHT_GRAY)

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, int(180 * SCALE)))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, int(230 * SCALE)))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, int(290 * SCALE)))

    elif current_state == STATE_BOSS_VICTORY:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))

        t1 = font_title.render("EFSANEVİ ZAFER!", True, MATRIX_GREEN)
        t2 = font_main.render("Boss'u 5 Kurşunla Yok Ettin!", True, WHITE)
        t3 = font_small.render("Yeniden Başlamak için Dokun", True, LIGHT_GRAY)

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - int(40 * SCALE)))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2 + int(5 * SCALE)))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, HEIGHT//2 + int(50 * SCALE)))

    elif current_state == STATE_ADMIN_KEYBOARD:
        draw_animated_keyboard()

    elif current_state == STATE_ADMIN_MENU:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 235))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, RED, back_btn_rect, border_radius=6)
        screen.blit(font_small.render("< Geri", True, WHITE), (back_btn_rect.x + int(15*SCALE), back_btn_rect.y + int(7*SCALE)))

        t1 = font_title.render("ADMIN PANELİ", True, MATRIX_GREEN)
        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, int(85 * SCALE)))

        btn1 = pygame.Rect(30 * SCALE, 140 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
        btn2 = pygame.Rect(30 * SCALE, 190 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
        btn3 = pygame.Rect(30 * SCALE, 240 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
        btn4 = pygame.Rect(30 * SCALE, 290 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)
        btn5 = pygame.Rect(30 * SCALE, 340 * SCALE, WIDTH - 60 * SCALE, 40 * SCALE)

        for b in [btn1, btn2, btn3, btn4, btn5]:
            pygame.draw.rect(screen, GRAY, b, border_radius=8)

        god_str = "AÇIK" if god_mode else "KAPALI"
        screen.blit(font_small.render("1) Tüm boruları yok et", True, WHITE), (btn1.x + 15 * SCALE, btn1.y + 10 * SCALE))
        screen.blit(font_small.render("2) Boss Savaşını Başlat", True, WHITE), (btn2.x + 15 * SCALE, btn2.y + 10 * SCALE))
        screen.blit(font_small.render("3) Yaratığı Yok Et (Direkt Öldür)", True, RED), (btn3.x + 15 * SCALE, btn3.y + 10 * SCALE))
        screen.blit(font_small.render(f"4) Ölümsüzlük Modu ({god_str})", True, WHITE), (btn4.x + 15 * SCALE, btn4.y + 10 * SCALE))
        screen.blit(font_small.render("5) Matrix Modunu Aç", True, MATRIX_GREEN), (btn5.x + 15 * SCALE, btn5.y + 10 * SCALE))

    elif current_state == STATE_MATRIX_ENDING:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        screen.blit(overlay, (0, 0))
        matrix_rain.draw()

        t1 = font_title.render("MATRIX SONU EASTEREGG", True, MATRIX_GREEN)
        t2 = font_main.render("Sistemi Ele Geçirdin!", True, WHITE)
        t3 = font_small.render("Yeniden Başlamak için Dokun", True, LIGHT_GRAY)

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - int(40 * SCALE)))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2 + int(5 * SCALE)))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, HEIGHT//2 + int(50 * SCALE)))

    pygame.display.flip()

pygame.quit()
sys.exit()