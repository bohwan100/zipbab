import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 540, 960

FONT_MONO = '/System/Library/Fonts/SFNSMono.ttf'
FONT_KR = '/System/Library/Fonts/AppleSDGothicNeo.ttc'

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_title = get_font(FONT_MONO, 21)
font_sub = get_font(FONT_MONO, 12)
font_timer = get_font(FONT_MONO, 13)
font_climax_title = get_font(FONT_MONO, 24)
font_climax_sub = get_font(FONT_KR, 14)
font_digital = get_font(FONT_MONO, 13)

def draw_continuous_limb(draw, pts, width=14, outline_w=3, fill_col=(255, 255, 255), outline_col=(20, 24, 32)):
    total_w = width + outline_w * 2
    total_r = total_w // 2
    inner_r = width // 2
    draw.line(pts, fill=outline_col, width=total_w, joint='curve')
    for p in pts:
        draw.ellipse([p[0]-total_r, p[1]-total_r, p[0]+total_r, p[1]+total_r], fill=outline_col)
    draw.line(pts, fill=fill_col, width=width, joint='curve')
    for p in pts:
        draw.ellipse([p[0]-inner_r, p[1]-inner_r, p[0]+inner_r, p[1]+inner_r], fill=fill_col)

def draw_zipbab_head(draw, pos, r=22, sunglasses_on=True, mouth_type='smile'):
    hx, hy = pos
    draw.rectangle([hx - 6, hy + r - 4, hx + 6, hy + r + 10], fill=(255, 220, 192), outline=(20, 24, 32), width=2)
    draw.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(255, 224, 198), outline=(20, 24, 32), width=3)
    
    # Stylish Hair
    draw.polygon([
        (hx - r - 2, hy - 4), (hx - r - 3, hy - r - 6), (hx - 8, hy - r - 12),
        (hx + 14, hy - r - 10), (hx + r + 2, hy - 6), (hx + r, hy - 2),
        (hx + 8, hy - r + 4), (hx - 10, hy - r + 4)
    ], fill=(36, 28, 24))
    
    if sunglasses_on:
        # Sunglasses
        draw.rectangle([hx - 20, hy - 5, hx - 3, hy + 7], fill=(12, 14, 20), outline=(5, 5, 8), width=2)
        draw.rectangle([hx + 3, hy - 5, hx + 20, hy + 7], fill=(12, 14, 20), outline=(5, 5, 8), width=2)
        draw.line([(hx - 3, hy), (hx + 3, hy)], fill=(12, 14, 20), width=3)
        draw.line([(hx - 16, hy + 4), (hx - 10, hy - 2)], fill=(255, 255, 255), width=2)
        draw.line([(hx + 7, hy + 4), (hx + 13, hy - 2)], fill=(255, 255, 255), width=2)
    else:
        # Awake friendly eyes
        draw.ellipse([hx - 15, hy - 3, hx - 7, hy + 5], fill=(20, 24, 32))
        draw.ellipse([hx + 7, hy - 3, hx + 15, hy + 5], fill=(20, 24, 32))
        
    if mouth_type == 'smile':
        draw.arc([hx - 7, hy + 8, hx + 7, hy + 17], start=0, end=180, fill=(185, 60, 60), width=2)
    elif mouth_type == 'taste':
        draw.ellipse([hx - 4, hy + 9, hx + 4, hy + 15], fill=(185, 60, 60))

def draw_tired_head(draw, pos, r=21, state='sleeping', look_down=False):
    hx, hy = pos
    draw.rectangle([hx - 6, hy + r - 4, hx + 6, hy + r + 10], fill=(235, 218, 205), outline=(20, 24, 32), width=2)
    draw.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(238, 222, 210), outline=(20, 24, 32), width=3)
    
    # Messy Bedhead Hair
    draw.polygon([
        (hx - r - 2, hy - 2), (hx - r - 6, hy - r), (hx - 14, hy - r - 10),
        (hx - 4, hy - r - 5), (hx + 8, hy - r - 12), (hx + r + 4, hy - r + 2),
        (hx + r + 2, hy + 2), (hx + 12, hy - r + 6), (hx - 8, hy - r + 6)
    ], fill=(68, 62, 58))
    
    if state == 'sleeping':
        draw.line([(hx - 14, hy + 1), (hx - 6, hy + 1)], fill=(40, 40, 45), width=2)
        draw.line([(hx + 6, hy + 1), (hx + 14, hy + 1)], fill=(40, 40, 45), width=2)
        draw.ellipse([hx - 3, hy + 8, hx + 3, hy + 13], fill=(70, 50, 50))
    elif state == 'panicked':
        draw.ellipse([hx - 16, hy - 4, hx - 6, hy + 6], fill=(255, 255, 255), outline=(20, 20, 25), width=1)
        draw.ellipse([hx - 12, hy - 1, hx - 9, hy + 2], fill=(20, 20, 25))
        draw.ellipse([hx + 6, hy - 4, hx + 16, hy + 6], fill=(255, 255, 255), outline=(20, 20, 25), width=1)
        draw.ellipse([hx + 9, hy - 1, hx + 12, hy + 2], fill=(20, 20, 25))
        draw.ellipse([hx - 6, hy + 8, hx + 6, hy + 18], fill=(90, 40, 40), outline=(20, 20, 25), width=2)
        draw.ellipse([hx + r + 3, hy - 6, hx + r + 8, hy + 1], fill=(56, 189, 248)) # sweat
    else: # tired / looking at phone
        eye_y = hy + (3 if look_down else 0)
        draw.arc([hx - 16, eye_y - 1, hx - 5, eye_y + 7], start=0, end=180, fill=(140, 125, 130), width=2)
        draw.line([(hx - 15, eye_y + 1), (hx - 6, eye_y + 2)], fill=(30, 30, 35), width=2)
        draw.arc([hx + 5, eye_y - 1, hx + 16, eye_y + 7], start=0, end=180, fill=(140, 125, 130), width=2)
        draw.line([(hx + 6, eye_y + 2), (hx + 15, eye_y + 1)], fill=(30, 30, 35), width=2)
        draw.line([(hx - 6, hy + 12), (hx + 6, hy + 11)], fill=(120, 70, 70), width=2)

def draw_detailed_phone(draw, cx, cy, w=24, h=42, glow=True):
    # Black chassis
    draw.rounded_rectangle([cx - w//2, cy - h//2, cx + w//2, cy + h//2], radius=5, fill=(18, 22, 30), outline=(50, 60, 75), width=2)
    # Vibrant screen
    sw, sh = w - 6, h - 8
    draw.rectangle([cx - sw//2, cy - sh//2, cx + sw//2, cy + sh//2], fill=(56, 189, 248))
    # UI feed cards
    draw.rectangle([cx - sw//2 + 2, cy - sh//2 + 3, cx + sw//2 - 2, cy - sh//2 + 15], fill=(255, 255, 255, 200))
    draw.line([(cx - sw//2 + 2, cy - sh//2 + 19), (cx + sw//2 - 6, cy - sh//2 + 19)], fill=(15, 23, 42), width=2)
    draw.line([(cx - sw//2 + 2, cy - sh//2 + 23), (cx + sw//2 - 4, cy - sh//2 + 23)], fill=(15, 23, 42), width=2)
    # Thumbs holding edges
    draw.ellipse([cx - w//2 - 3, cy - 2, cx - w//2 + 3, cy + 8], fill=(235, 218, 205), outline=(20, 24, 32))
    draw.ellipse([cx + w//2 - 3, cy - 2, cx + w//2 + 3, cy + 8], fill=(235, 218, 205), outline=(20, 24, 32))

def draw_timer_badge(draw, cx, cy, time_str, progress_ratio):
    r = 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 14, 20), outline=(255, 255, 255), width=2)
    arc_box = [cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3]
    start_angle = -90
    end_angle = -90 + int(progress_ratio * 360)
    if end_angle > start_angle:
        draw.arc(arc_box, start=start_angle, end=end_angle, fill=(245, 158, 11), width=3)
    bbox = font_timer.getbbox(time_str)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 1), time_str, fill=(255, 255, 255), font=font_timer)

# --- ACT 1: AM 07:00 ---
def render_act1(draw, t):
    # TOP SCENE (Zipbab Boy wakes up, sits up smoothly, stretches with sunglasses)
    draw.rectangle([0, 100, W, 480], fill=(45, 52, 68))
    # Morning sunlight through window
    draw.rectangle([60, 140, 170, 240], fill=(25, 30, 42), outline=(15, 18, 26), width=4)
    for wy in range(144, 236):
        ratio = (wy - 144) / 92
        draw.line([(64, wy), (166, wy)], fill=(int(120 + ratio * 120), int(160 + ratio * 80), int(220 - ratio * 40)))
    draw.line([(115, 140), (115, 240)], fill=(15, 18, 26), width=3)
    draw.line([(60, 190), (170, 190)], fill=(15, 18, 26), width=3)
    
    # Bed
    draw.rectangle([180, 290, 440, 390], fill=(30, 38, 52), outline=(45, 56, 76), width=2)
    draw.rectangle([430, 240, 450, 390], fill=(45, 56, 76))
    draw.ellipse([370, 275, 425, 310], fill=(245, 245, 250))
    
    # Action progression: 0s~1.2s rising up, 1.2s~2.8s stretch
    rise_progress = min(1.0, max(0.0, (t - 0.4) / 1.0)) # 0 to 1
    # Torso angle and height rise smoothly
    hip = (320, 350)
    torso_y = int(320 - rise_progress * 60)
    torso_top = (320, torso_y)
    head_pos = (320, torso_y - 45)
    
    # Body
    draw_continuous_limb(draw, [hip, torso_top], width=26, fill_col=(250, 250, 255))
    
    # Arms: at start resting, then stretches high up
    arm_y = int(270 - rise_progress * 65 + math.sin(t * 4) * 4)
    draw_continuous_limb(draw, [(308, torso_y + 10), (285, arm_y)], width=12, fill_col=(250, 250, 255))
    draw_continuous_limb(draw, [(332, torso_y + 10), (355, arm_y)], width=12, fill_col=(250, 250, 255))
    
    draw_zipbab_head(draw, head_pos, r=22, sunglasses_on=True)
    
    # Orange Duvet
    draw.rectangle([210, 340, 410, 395], fill=(234, 88, 12), outline=(194, 65, 12), width=2)
    
    draw.text((36, 120), "AM 07:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 148), "WAKE UP & STRETCH", fill=(245, 158, 11), font=font_sub)
    
    # BOTTOM SCENE (Natural reclining body under blanket, breathing, hand smacks snooze)
    draw.rectangle([0, 480, W, 860], fill=(12, 16, 26))
    draw.rectangle([340, 520, 450, 620], fill=(6, 9, 16), outline=(15, 20, 32), width=4)
    draw.rectangle([344, 524, 446, 616], fill=(14, 20, 36))
    draw.line([(395, 520), (395, 620)], fill=(15, 20, 32), width=3)
    draw.line([(340, 570), (450, 570)], fill=(15, 20, 32), width=3)
    
    # Bed Frame & Pillow
    draw.rectangle([60, 640, 440, 800], fill=(22, 28, 42), outline=(35, 45, 65), width=2)
    draw.ellipse([80, 630, 180, 680], fill=(220, 225, 235)) # indented pillow
    
    # Head resting naturally on pillow
    breath = math.sin(t * 3) * 2
    b_head_pos = (130, 645 + int(breath))
    draw_tired_head(draw, b_head_pos, r=20, state='sleeping')
    
    # Visible Shoulders & Chest in grey tee! (Solves "목만 덩그러니" issue!)
    draw.polygon([(140, 665), (230, 665), (240, 725), (140, 725)], fill=(100, 116, 139), outline=(20, 24, 32), width=2)
    
    # Nightstand & vibrating red alarm clock
    draw.rectangle([50, 600, 110, 640], fill=(20, 25, 36), outline=(35, 45, 65), width=2)
    clock_shake = math.sin(t * 30) * 2 if t > 0.8 else 0
    draw.rectangle([55 + clock_shake, 605, 105 + clock_shake, 630], fill=(10, 12, 18), outline=(30, 38, 52), width=1)
    draw.text((60 + clock_shake, 610), "07:00", fill=(239, 68, 68), font=font_digital)
    
    # Arm movement: groggily reaching to snooze clock at t=1.2s ~ 2.2s
    if 1.0 < t < 2.3:
        reach_p = math.sin((t - 1.0) / 1.3 * math.pi)
        arm_hand = (int(160 - reach_p * 75), int(680 - reach_p * 60))
        draw_continuous_limb(draw, [(165, 675), (140, 660), arm_hand], width=11, fill_col=(235, 218, 205))
    else:
        # Arm resting under blanket
        draw_continuous_limb(draw, [(165, 675), (190, 700)], width=11, fill_col=(235, 218, 205))
        
    # Blue Duvet with realistic layered fold covering chest downwards
    draw.polygon([(145, 690), (430, 690), (430, 790), (145, 790)], fill=(30, 58, 138), outline=(24, 46, 110), width=2)
    draw.polygon([(140, 685), (435, 685), (430, 705), (145, 705)], fill=(40, 70, 160)) # fold rim
    
    # Z Z Z
    z_off = int((t * 20) % 35)
    draw.text((210, 615 - z_off), "z", fill=(148, 163, 184), font=font_sub)
    draw.text((225, 600 - z_off), "Z", fill=(180, 195, 215), font=font_sub)
    draw.text((240, 585 - z_off), "Z", fill=(220, 230, 245), font=font_title)
    
    draw.text((36, 500), "AM 07:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 528), "DEEP SLEEP (SNOOZE)", fill=(148, 163, 184), font=font_sub)

# --- ACT 2: AM 07:30 ---
def render_act2(draw, t):
    # TOP SCENE (Zipbab Boy cooking eggs, tasting, nodding)
    draw.rectangle([0, 100, W, 480], fill=(42, 48, 62))
    draw.rectangle([100, 140, 240, 205], fill=(30, 36, 48), outline=(20, 24, 34), width=2)
    draw.line([(170, 140), (170, 205)], fill=(20, 24, 34), width=2)
    
    draw.rectangle([140, 285, 460, 480], fill=(30, 36, 48))
    draw.rectangle([130, 275, 470, 292], fill=(50, 60, 78))
    
    # Stove flame underneath pan
    for fi in range(4):
        fx = 320 + fi * 15
        draw.polygon([(fx, 288), (fx + 5, 280), (fx + 10, 288)], fill=(245, 158, 11))
        draw.polygon([(fx + 2, 288), (fx + 5, 283), (fx + 8, 288)], fill=(56, 189, 248))
        
    # Pan with eggs
    draw.rectangle([300, 267, 380, 278], fill=(20, 24, 30), outline=(0, 0, 0), width=1)
    draw.line([(380, 273), (420, 273)], fill=(15, 18, 24), width=6)
    draw.ellipse([315, 269, 335, 277], fill=(255, 255, 255))
    draw.ellipse([322, 271, 328, 275], fill=(245, 158, 11))
    draw.ellipse([345, 269, 365, 277], fill=(255, 255, 255))
    draw.ellipse([352, 271, 358, 275], fill=(245, 158, 11))
    
    steam_phase = (t * 6) % 3
    for si in range(3):
        sy = 255 - int(((steam_phase + si) % 3) * 16)
        sx = 330 + si * 14
        draw.arc([sx, sy, sx + 12, sy + 10], start=0, end=180, fill=(255, 255, 255), width=2)
    
    # Character action: tasting loop
    taste_cycle = math.sin(t * 4) # natural human pace
    is_at_mouth = taste_cycle > 0.3
    
    hip = (250, 295)
    torso_top = (250, 210)
    head_pos = (250, 168)
    
    draw_continuous_limb(draw, [hip, (240, 360), (235, 430), (220, 430)], width=15, fill_col=(30, 41, 59))
    draw_continuous_limb(draw, [hip, (260, 360), (265, 430), (280, 430)], width=15, fill_col=(30, 41, 59))
    draw_continuous_limb(draw, [hip, torso_top], width=26, fill_col=(250, 250, 255))
    draw.rectangle([238, 220, 262, 290], fill=(245, 158, 11), outline=(180, 110, 5), width=2) # apron
    
    # Left hand steadying pan handle
    draw_continuous_limb(draw, [(240, 220), (280, 250), (320, 273)], width=11, fill_col=(255, 222, 196))
    
    # Right hand scooping from pan then bringing to mouth
    if is_at_mouth:
        spoon_x, spoon_y = 265, 175
        mouth_t = 'taste'
    else:
        spoon_x, spoon_y = 330, 270
        mouth_t = 'smile'
    draw_continuous_limb(draw, [(260, 220), (280, 215 if is_at_mouth else 245), (spoon_x, spoon_y)], width=11, fill_col=(255, 222, 196))
    draw.line([(spoon_x, spoon_y), (spoon_x - 10, spoon_y - 10)], fill=(200, 205, 215), width=3)
    
    draw_zipbab_head(draw, head_pos, r=21, sunglasses_on=True, mouth_type=mouth_t)
    
    draw.text((36, 120), "AM 07:30", fill=(255, 255, 255), font=font_title)
    draw.text((36, 148), "COOKING & TASTING", fill=(245, 158, 11), font=font_sub)
    
    # BOTTOM SCENE (Propped up in bed, holding smartphone with both hands, thumb scrolling)
    draw.rectangle([0, 480, W, 860], fill=(12, 16, 26))
    draw.rectangle([60, 640, 440, 800], fill=(22, 28, 42), outline=(35, 45, 65), width=2)
    # Stacked pillows propping head & back up
    draw.ellipse([80, 610, 170, 670], fill=(210, 215, 225))
    draw.ellipse([100, 630, 190, 680], fill=(225, 230, 240))
    
    # Head propped up, looking down at phone
    b_head_pos = (145, 635)
    draw_tired_head(draw, b_head_pos, r=20, state='awake', look_down=True)
    
    # Upper Torso clearly visible in grey tee!
    draw.polygon([(155, 650), (240, 650), (245, 715), (155, 715)], fill=(100, 116, 139), outline=(20, 24, 32), width=2)
    
    # Both arms bent holding smartphone right in front of chest/eyes!
    draw_continuous_limb(draw, [(170, 660), (200, 640), (215, 625)], width=11, fill_col=(235, 218, 205))
    draw_continuous_limb(draw, [(210, 665), (225, 645), (230, 625)], width=11, fill_col=(235, 218, 205))
    
    # Clearly rendered smartphone with glow!
    draw_detailed_phone(draw, 225, 620, w=22, h=38)
    
    # Blue light glow reflecting on face
    draw.polygon([(215, 620), (145, 630), (145, 655)], fill=(20, 45, 75))
    
    # Blanket covering lower half
    draw.polygon([(160, 690), (430, 690), (430, 790), (160, 790)], fill=(30, 58, 138), outline=(24, 46, 110), width=2)
    draw.polygon([(155, 685), (435, 685), (430, 705), (160, 705)], fill=(40, 70, 160))
    
    draw.text((36, 500), "AM 07:30", fill=(255, 255, 255), font=font_title)
    draw.text((36, 528), "BED PHONE SCROLLING", fill=(148, 163, 184), font=font_sub)

# --- ACT 3: AM 08:00 ---
def render_act3(draw, t):
    # TOP SCENE (Warm healthy breakfast, coffee sip)
    draw.rectangle([0, 100, W, 480], fill=(42, 48, 62))
    draw.rectangle([180, 305, 430, 480], fill=(32, 38, 50))
    draw.rectangle([170, 295, 440, 310], fill=(55, 65, 85))
    
    # Warm bowl of rice/soup
    draw.ellipse([250, 280, 310, 300], fill=(240, 240, 245), outline=(0, 0, 0), width=2)
    draw.ellipse([255, 283, 305, 295], fill=(234, 179, 8))
    # Coffee mug with warm steam
    draw.rectangle([340, 275, 365, 300], fill=(234, 88, 12), outline=(0, 0, 0), width=1)
    draw.arc([355, 280, 372, 295], start=-90, end=90, fill=(234, 88, 12), width=3) # mug handle
    
    steam_y = 255 - int(((t * 5) % 2) * 15)
    draw.arc([270, steam_y, 285, steam_y + 15], start=0, end=180, fill=(255, 255, 255), width=2)
    draw.arc([345, steam_y - 5, 357, steam_y + 8], start=0, end=180, fill=(255, 255, 255), width=2)
    
    hip = (230, 320)
    torso_top = (230, 230)
    head_pos = (230, 188)
    
    draw_continuous_limb(draw, [hip, (200, 350), (200, 425), (215, 425)], width=15, fill_col=(30, 41, 59))
    draw_continuous_limb(draw, [hip, torso_top], width=26, fill_col=(250, 250, 255))
    draw_continuous_limb(draw, [(235, 235), (265, 255), (250, 205)], width=11, fill_col=(255, 222, 196))
    
    draw_zipbab_head(draw, head_pos, r=21, sunglasses_on=True, mouth_type='smile')
    
    draw.text((36, 120), "AM 08:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 148), "HEALTHY BREAKFAST", fill=(245, 158, 11), font=font_sub)
    
    # BOTTOM SCENE (Alarm says 08:00, panicked leap, stuffing cold food, sprinting out open door!)
    draw.rectangle([0, 480, W, 860], fill=(12, 16, 26))
    
    # Open exit doorway with hallway light
    draw.rectangle([390, 520, 500, 840], fill=(45, 30, 20), outline=(20, 24, 32), width=3)
    draw.rectangle([395, 525, 495, 835], fill=(240, 230, 190)) # bright hallway
    draw.polygon([(465, 525), (515, 545), (515, 835), (465, 835)], fill=(70, 50, 35)) # open door
    
    # Leftover takeout box on floor
    draw.rectangle([70, 740, 160, 790], fill=(25, 32, 45))
    draw.rectangle([80, 725, 135, 745], fill=(220, 225, 235), outline=(0, 0, 0), width=1)
    draw.text((85, 728), "TAKEOUT", fill=(220, 38, 38), font=font_sub)
    
    # Alarm clock flashing 08:00 !!
    draw.rectangle([60, 660, 120, 690], fill=(12, 16, 24), outline=(220, 38, 38), width=2)
    draw.text((66, 668), "08:00", fill=(239, 68, 68), font=font_digital)
    
    # Frantic sprint across screen towards open door
    run_cycle = math.sin(t * 18)
    run_x = int(240 + ((t - 5.6) / 2.8) * 120 + run_cycle * 12)
    f_hip = (run_x, 680)
    f_torso_top = (run_x + 35, 600)
    f_head = (run_x + 50, 565)
    
    # Sprinting legs
    draw_continuous_limb(draw, [f_hip, (run_x - 30, 720), (run_x - 55, 765)], width=14, fill_col=(71, 85, 105))
    draw_continuous_limb(draw, [f_hip, (run_x + 40, 715), (run_x + 75, 765)], width=14, fill_col=(71, 85, 105))
    draw_continuous_limb(draw, [f_hip, f_torso_top], width=26, fill_col=(100, 116, 139))
    
    # Hand stuffing cold leftover slice into mouth
    draw_continuous_limb(draw, [(run_x + 25, 610), (run_x + 10, 650), (run_x + 40, 580)], width=11, fill_col=(235, 218, 205))
    draw.polygon([(run_x + 35, 575), (run_x + 50, 580), (run_x + 45, 565)], fill=(217, 119, 6)) # pizza slice
    
    draw_tired_head(draw, f_head, r=21, state='panicked')
    
    # Speed lines
    draw.line([(run_x - 60, 640), (run_x - 20, 640)], fill=(200, 210, 225), width=2)
    draw.line([(run_x - 70, 670), (run_x - 30, 670)], fill=(200, 210, 225), width=2)
    
    draw.text((36, 500), "AM 08:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 528), "LEFTOVER & RUSH OUT", fill=(239, 68, 68), font=font_sub)

# --- ACT 4: AM 08:30 (CLIMAX COMMUTE) ---
def render_act4_commute(img, draw, t):
    # Morning blue sky with warm sunlight
    for y in range(0, 560):
        ratio = y / 560
        r = int(70 + ratio * 140)
        g = int(130 + ratio * 100)
        b = int(220 + ratio * 35)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Morning Sun with layered rays
    draw.ellipse([420, 80, 480, 140], fill=(255, 248, 220))
    sun_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sun_layer)
    for r_s in range(60, 10, -10):
        s_draw.ellipse([450 - r_s, 110 - r_s, 450 + r_s, 110 + r_s], fill=(255, 245, 200, 15))
    img.paste(sun_layer, (0, 0), sun_layer)
    
    # City buildings
    buildings = [
        (0, 200, 55), (45, 260, 45), (85, 210, 50), (130, 280, 45),
        (170, 220, 60), (225, 190, 50), (270, 270, 55), (320, 220, 45),
        (360, 245, 55), (410, 195, 50), (455, 235, 85)
    ]
    for bx, bh, bw in buildings:
        by = 500 - bh
        draw.rectangle([bx, by, bx + bw, 500], fill=(160, 185, 210))
        for wy in range(by + 16, 480, 24):
            for wx in range(bx + 8, bx + bw - 8, 13):
                if (wx * 11 + wy * 17) % 4 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 255, 255))
    
    draw.line([(0, 495), (W, 495)], fill=(120, 140, 160), width=3)
    for rx in range(0, W, 40):
        draw.line([(rx, 495), (rx, 530)], fill=(120, 140, 160), width=2)
    
    draw.rectangle([0, 525, W, 960], fill=(60, 68, 80))
    draw.line([(0, 525), (W, 525)], fill=(140, 155, 175), width=4)
    draw.line([(0, 630), (W, 630)], fill=(50, 56, 68), width=2)
    draw.line([(0, 750), (W, 750)], fill=(45, 50, 60), width=2)
    
    walk_t = t * 7.5
    
    # 1. LEADER (ZIPBAB BOY WITH SUNGLASSES) - Ahead, upright, confident stride!
    lead_x = 365
    bob_lead = abs(math.cos(walk_t)) * 6
    hip_lead = (lead_x, 565 - bob_lead)
    torso_top_lead = (lead_x, 475 - bob_lead)
    head_lead = (lead_x, 435 - bob_lead)
    
    stride_amp = 36
    stride_phase = math.sin(walk_t)
    
    knee_f = (lead_x + stride_phase * 18, 625 - bob_lead)
    foot_f = (lead_x + stride_phase * stride_amp, 690)
    lift_b = max(0, -stride_phase * 18)
    knee_b = (lead_x - stride_phase * 14, 625 - bob_lead - lift_b * 0.5)
    foot_b = (lead_x - stride_phase * stride_amp, 690 - lift_b)
    
    # Back leg
    draw_continuous_limb(draw, [hip_lead, knee_b, foot_b], width=15, fill_col=(30, 41, 59))
    draw.ellipse([foot_b[0] - 2, foot_b[1] - 4, foot_b[0] + 16, foot_b[1] + 6], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    
    # Torso (Smart orange stylish jacket)
    draw_continuous_limb(draw, [hip_lead, torso_top_lead], width=28, fill_col=(245, 158, 11))
    
    # Front leg
    draw_continuous_limb(draw, [hip_lead, knee_f, foot_f], width=15, fill_col=(30, 41, 59))
    draw.ellipse([foot_f[0] - 2, foot_f[1] - 4, foot_f[0] + 16, foot_f[1] + 6], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    
    # Right arm swinging with sleek bag
    shoulder_lead = (lead_x, 490 - bob_lead)
    arm_swing = math.sin(walk_t) * 26
    hand_lead = (lead_x - arm_swing, 555 - bob_lead)
    draw_continuous_limb(draw, [shoulder_lead, (lead_x - arm_swing * 0.5, 520 - bob_lead), hand_lead], width=12, fill_col=(255, 222, 196))
    
    # Briefcase
    bc_x, bc_y = hand_lead[0] - 8, hand_lead[1] + 2
    draw.rectangle([bc_x, bc_y, bc_x + 32, bc_y + 24], fill=(120, 80, 50), outline=(0, 0, 0), width=2)
    draw.line([(bc_x + 10, bc_y), (bc_x + 22, bc_y)], fill=(0, 0, 0), width=2)
    
    draw_zipbab_head(draw, head_lead, r=22, sunglasses_on=True)
    
    # 2. FOLLOWER (REGULAR TIRED PERSON) - CLEARLY HOLDING & STARING AT PHONE!
    fol_x = 185
    t_slow = t * 6.5
    bob_fol = abs(math.cos(t_slow)) * 3
    # Significant 35 degree forward slouch!
    hip_fol = (fol_x, 580 - bob_fol)
    torso_top_fol = (fol_x + 26, 505 - bob_fol)
    head_fol = (fol_x + 38, 470 - bob_fol)
    
    f_swing = math.sin(t_slow) * 18
    f_knee_b = (fol_x - f_swing * 0.5, 635 - bob_fol)
    f_foot_b = (fol_x - f_swing, 690)
    f_knee_f = (fol_x + f_swing * 0.5, 635 - bob_fol)
    f_foot_f = (fol_x + f_swing, 690)
    
    draw_continuous_limb(draw, [hip_fol, f_knee_b, f_foot_b], width=14, fill_col=(51, 65, 85))
    draw_continuous_limb(draw, [hip_fol, torso_top_fol], width=26, fill_col=(100, 116, 139))
    draw_continuous_limb(draw, [hip_fol, f_knee_f, f_foot_f], width=14, fill_col=(51, 65, 85))
    
    # BOTH ARMS BENT FORWARD HOLDING PHONE PROMINENTLY IN FRONT!
    shoulder_fol = (fol_x + 22, 515 - bob_fol)
    phone_cx, phone_cy = fol_x + 58, 525 - bob_fol
    
    # Left & Right arm holding phone
    draw_continuous_limb(draw, [shoulder_fol, (fol_x + 40, 535 - bob_fol), (phone_cx - 8, phone_cy + 5)], width=11, fill_col=(235, 218, 205))
    draw_continuous_limb(draw, [(fol_x + 15, 520 - bob_fol), (fol_x + 36, 545 - bob_fol), (phone_cx + 8, phone_cy + 5)], width=10, fill_col=(235, 218, 205))
    
    # Large, crisp, clearly visible smartphone with blue feed glow!
    draw_detailed_phone(draw, phone_cx, phone_cy, w=24, h=42)
    
    # Glowing beam from phone lighting up chest & face
    glow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    g_draw.polygon([(phone_cx, phone_cy), (head_fol[0] - 10, head_fol[1]), (head_fol[0] + 15, head_fol[1] + 10)], fill=(56, 189, 248, 45))
    img.paste(glow_layer, (0, 0), glow_layer)
    
    # Head tilted down looking directly at phone
    draw_tired_head(draw, head_fol, r=20, state='awake', look_down=True)
    
    # Squiggly tiredness/exhaustion steam waves (~ ~ ~)
    steam_y = head_fol[1] - 30 - int((t * 18) % 18)
    draw.arc([head_fol[0] - 18, steam_y, head_fol[0], steam_y + 14], start=0, end=180, fill=(140, 150, 170), width=2)
    draw.arc([head_fol[0] - 8, steam_y - 10, head_fol[0] + 10, steam_y + 4], start=180, end=360, fill=(140, 150, 170), width=2)
    
    # Headlines
    bbox1 = font_climax_title.getbbox("SAME MORNING.")
    w1 = bbox1[2] - bbox1[0]
    draw.text(((W - w1) // 2, 85), "SAME MORNING.", fill=(255, 255, 255), font=font_climax_title)
    
    bbox2 = font_climax_title.getbbox("DIFFERENT ME.")
    w2 = bbox2[2] - bbox2[0]
    draw.text(((W - w2) // 2, 118), "DIFFERENT ME.", fill=(255, 255, 255), font=font_climax_title)
    
    sub_text = "똑같은 아침 1시간, 전혀 다른 하루의 시작."
    bbox3 = font_climax_sub.getbbox(sub_text)
    w3 = bbox3[2] - bbox3[0]
    draw.text(((W - w3) // 2, 155), sub_text, fill=(245, 158, 11), font=font_climax_sub)

def render_frame_by_time(t):
    img = Image.new('RGB', (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if t < 8.4:
        if t < 2.8:
            render_act1(draw, t)
            timer_str = "07:00"
            progress = (t / 2.8) * 0.25
        elif t < 5.6:
            render_act2(draw, t)
            timer_str = "07:30"
            progress = 0.25 + ((t - 2.8) / 2.8) * 0.25
        else:
            render_act3(draw, t)
            timer_str = "08:00"
            progress = 0.50 + ((t - 5.6) / 2.8) * 0.25
            
        draw.line([(0, 480), (W, 480)], fill=(0, 0, 0), width=4)
        draw_timer_badge(draw, W // 2, 480, timer_str, progress)
    else:
        render_act4_commute(img, draw, t)
        
    wm = "ZIPBAB BOY · 집밥보이"
    bbox_wm = font_sub.getbbox(wm)
    draw.text(((W - (bbox_wm[2]-bbox_wm[0])) // 2, 930), wm, fill=(120, 130, 145), font=font_sub)
    
    return img

if __name__ == '__main__':
    os.makedirs('scratch/test_acts_v4', exist_ok=True)
    f1 = render_frame_by_time(1.4)
    f1.save('scratch/test_acts_v4/act1_v4.png')
    f2 = render_frame_by_time(4.2)
    f2.save('scratch/test_acts_v4/act2_v4.png')
    f3 = render_frame_by_time(7.0)
    f3.save('scratch/test_acts_v4/act3_v4.png')
    f4 = render_frame_by_time(9.8)
    f4.save('scratch/test_acts_v4/act4_v4.png')
    print('All 4 acts v4 rendered successfully!')
