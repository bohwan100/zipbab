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
font_timer = get_font(FONT_MONO, 14)
font_climax_title = get_font(FONT_MONO, 24)
font_climax_sub = get_font(FONT_KR, 14)

def draw_capsule_bone(draw, p1, p2, width, fill_col, outline_col=(20, 24, 32), outline_w=2):
    draw.line([p1, p2], fill=outline_col, width=width + outline_w * 2)
    draw.line([p1, p2], fill=fill_col, width=width)
    ro = (width + outline_w * 2) // 2
    ri = width // 2
    for p in (p1, p2):
        draw.ellipse([p[0]-ro, p[1]-ro, p[0]+ro, p[1]+ro], fill=outline_col)
        draw.ellipse([p[0]-ri, p[1]-ri, p[0]+ri, p[1]+ri], fill=fill_col)

def draw_zipbab_head(draw, pos, r=22, eye_dir=1):
    hx, hy = pos
    # Neck
    draw.rectangle([hx - 6, hy + r - 4, hx + 6, hy + r + 10], fill=(255, 220, 192), outline=(20, 24, 32), width=2)
    # Head Base
    draw.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(255, 224, 198), outline=(20, 24, 32), width=3)
    
    # Stylish Hair (Dark Brown / Black modern crop)
    draw.polygon([
        (hx - r - 2, hy - 4),
        (hx - r - 2, hy - r - 6),
        (hx - 8, hy - r - 12),
        (hx + 14, hy - r - 10),
        (hx + r + 2, hy - 6),
        (hx + r, hy - 2),
        (hx + 8, hy - r + 4),
        (hx - 10, hy - r + 4)
    ], fill=(36, 28, 24))
    
    # SIGNATURE SUNGLASSES
    # Frame width and glasses
    gw, gh = 18, 12
    # Left lens
    draw.rectangle([hx - 20, hy - 5, hx - 3, hy + 7], fill=(12, 14, 20), outline=(5, 5, 8), width=2)
    # Right lens
    draw.rectangle([hx + 3, hy - 5, hx + 20, hy + 7], fill=(12, 14, 20), outline=(5, 5, 8), width=2)
    # Bridge
    draw.line([(hx - 3, hy), (hx + 3, hy)], fill=(12, 14, 20), width=3)
    # Specular white gloss slash on both lenses
    draw.line([(hx - 16, hy + 4), (hx - 10, hy - 2)], fill=(255, 255, 255), width=2)
    draw.line([(hx + 7, hy + 4), (hx + 13, hy - 2)], fill=(255, 255, 255), width=2)
    
    # Confident Smile
    draw.arc([hx - 7, hy + 8, hx + 7, hy + 17], start=0, end=180, fill=(185, 60, 60), width=2)

def draw_tired_head(draw, pos, r=21, is_sleeping=False, is_panicked=False):
    hx, hy = pos
    # Neck
    draw.rectangle([hx - 6, hy + r - 4, hx + 6, hy + r + 10], fill=(235, 218, 205), outline=(20, 24, 32), width=2)
    # Head Base (slightly pale/dull)
    draw.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(238, 222, 210), outline=(20, 24, 32), width=3)
    
    # Messy Bedhead Hair
    draw.polygon([
        (hx - r - 2, hy - 2),
        (hx - r - 6, hy - r),
        (hx - 14, hy - r - 10),
        (hx - 4, hy - r - 5),
        (hx + 8, hy - r - 12),
        (hx + r + 4, hy - r + 2),
        (hx + r + 2, hy + 2),
        (hx + 12, hy - r + 6),
        (hx - 8, hy - r + 6)
    ], fill=(68, 62, 58))
    
    if is_sleeping:
        # Closed eyes: simple dash
        draw.line([(hx - 14, hy + 1), (hx - 6, hy + 1)], fill=(40, 40, 45), width=2)
        draw.line([(hx + 6, hy + 1), (hx + 14, hy + 1)], fill=(40, 40, 45), width=2)
        # Sleeping mouth slightly open
        draw.ellipse([hx - 3, hy + 8, hx + 3, hy + 13], fill=(70, 50, 50))
    elif is_panicked:
        # Wide startled eyes!
        draw.ellipse([hx - 16, hy - 4, hx - 6, hy + 6], fill=(255, 255, 255), outline=(20, 20, 25), width=1)
        draw.ellipse([hx - 12, hy - 1, hx - 9, hy + 2], fill=(20, 20, 25))
        draw.ellipse([hx + 6, hy - 4, hx + 16, hy + 6], fill=(255, 255, 255), outline=(20, 20, 25), width=1)
        draw.ellipse([hx + 9, hy - 1, hx + 12, hy + 2], fill=(20, 20, 25))
        # Open screaming mouth
        draw.ellipse([hx - 6, hy + 8, hx + 6, hy + 18], fill=(90, 40, 40), outline=(20, 20, 25), width=2)
        # Sweat droplet
        draw.ellipse([hx + r + 3, hy - 6, hx + r + 8, hy + 1], fill=(56, 189, 248))
    else:
        # Tired eyes with dark circles
        draw.arc([hx - 16, hy, hx - 5, hy + 8], start=0, end=180, fill=(140, 125, 130), width=2)
        draw.line([(hx - 15, hy + 1), (hx - 6, hy + 2)], fill=(30, 30, 35), width=2)
        draw.arc([hx + 5, hy, hx + 16, hy + 8], start=0, end=180, fill=(140, 125, 130), width=2)
        draw.line([(hx + 6, hy + 2), (hx + 15, hy + 1)], fill=(30, 30, 35), width=2)
        # Slumped mouth
        draw.line([(hx - 6, hy + 12), (hx + 6, hy + 11)], fill=(120, 70, 70), width=2)

def draw_timer_badge(draw, cx, cy, time_str, progress_ratio):
    r = 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 14, 20), outline=(255, 255, 255), width=2)
    # Rotating progress arc
    arc_box = [cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3]
    start_angle = -90
    end_angle = -90 + int(progress_ratio * 360)
    if end_angle > start_angle:
        draw.arc(arc_box, start=start_angle, end=end_angle, fill=(245, 158, 11), width=3)
    
    bbox = font_timer.getbbox(time_str)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 1), time_str, fill=(255, 255, 255), font=font_timer)

# --- SCENE RENDERS ---

def render_act1(draw, t):
    # AM 07:00
    # Top: Zipbab Boy waking up, sitting up in bed, stretching arms with sunglasses!
    # Bottom: Regular person dead asleep with snooze.
    
    # TOP SCENE (Sunny bedroom)
    draw.rectangle([0, 100, W, 480], fill=(45, 52, 68))
    # Morning window
    draw.rectangle([60, 140, 170, 240], fill=(25, 30, 42), outline=(15, 18, 26), width=4)
    for wy in range(144, 236):
        ratio = (wy - 144) / 92
        draw.line([(64, wy), (166, wy)], fill=(int(120 + ratio * 120), int(160 + ratio * 80), int(220 - ratio * 40)))
    draw.line([(115, 140), (115, 240)], fill=(15, 18, 26), width=3)
    draw.line([(60, 190), (170, 190)], fill=(15, 18, 26), width=3)
    
    # Bed
    draw.rectangle([180, 290, 440, 390], fill=(30, 38, 52), outline=(45, 56, 76), width=2)
    draw.rectangle([430, 240, 450, 390], fill=(45, 56, 76)) # headboard
    draw.ellipse([370, 275, 425, 310], fill=(245, 245, 250)) # pillow
    
    # Zipbab Boy sitting up, stretching arms high in the air!
    stretch = math.sin(t * 4) * 5
    hip = (320, 350)
    torso_top = (320, 260)
    head_pos = (320, 215)
    
    # Body (wearing crisp white pajama tee)
    draw_capsule_bone(draw, hip, torso_top, width=28, fill_col=(250, 250, 255))
    # Arms stretched up in victory/stretch
    draw_capsule_bone(draw, (308, 265), (285, 205 + int(stretch)), width=12, fill_col=(250, 250, 255)) # left arm up
    draw_capsule_bone(draw, (332, 265), (355, 205 + int(stretch)), width=12, fill_col=(250, 250, 255)) # right arm up
    
    # Head with sunglasses
    draw_zipbab_head(draw, head_pos, r=22)
    
    # Duvet covering legs
    draw.rectangle([210, 340, 410, 395], fill=(234, 88, 12), outline=(194, 65, 12), width=2) # warm orange duvet
    
    draw.text((36, 120), "AM 07:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 148), "WAKE UP & STRETCH", fill=(245, 158, 11), font=font_sub)
    
    # BOTTOM SCENE (Dark sleepy bedroom)
    draw.rectangle([0, 480, W, 860], fill=(12, 16, 26))
    
    # Dark window
    draw.rectangle([340, 520, 450, 620], fill=(6, 9, 16), outline=(15, 20, 32), width=4)
    draw.rectangle([344, 524, 446, 616], fill=(14, 20, 36))
    draw.line([(395, 520), (395, 620)], fill=(15, 20, 32), width=3)
    draw.line([(340, 570), (450, 570)], fill=(15, 20, 32), width=3)
    
    # Bed
    draw.rectangle([60, 680, 380, 780], fill=(18, 24, 38), outline=(28, 38, 58), width=2)
    draw.rectangle([50, 620, 70, 780], fill=(28, 38, 58))
    draw.ellipse([80, 660, 140, 700], fill=(220, 220, 230))
    
    # Sleeping head (under pillow / blanket)
    draw_tired_head(draw, (145, 670), r=20, is_sleeping=True)
    # Dark blue blanket over whole body
    draw.rectangle([165, 665, 375, 775], fill=(30, 58, 138), outline=(24, 46, 110), width=2)
    
    # Clock
    draw.rectangle([80, 610, 135, 635], fill=(12, 16, 24), outline=(30, 40, 60), width=1)
    draw.text((86, 615), "07:00", fill=(239, 68, 68), font=font_sub)
    
    # Z Z Z
    z_off = int((t * 20) % 35)
    draw.text((210, 620 - z_off), "z", fill=(148, 163, 184), font=font_sub)
    draw.text((225, 605 - z_off), "Z", fill=(180, 195, 215), font=font_sub)
    draw.text((240, 590 - z_off), "Z", fill=(220, 230, 245), font=font_title)
    
    draw.text((36, 500), "AM 07:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 528), "DEEP SLEEP · SNOOZE", fill=(148, 163, 184), font=font_sub)

def render_act2(draw, t):
    # AM 07:30
    # Top: Zipbab Boy cooking food in pan and tasting with spoon, wearing apron & sunglasses!
    # Bottom: Regular person in bed, holding phone up above face scrolling.
    
    # TOP SCENE (Kitchen)
    draw.rectangle([0, 100, W, 480], fill=(42, 48, 62))
    # Wall cabinet
    draw.rectangle([100, 140, 240, 205], fill=(30, 36, 48), outline=(20, 24, 34), width=2)
    draw.line([(170, 140), (170, 205)], fill=(20, 24, 34), width=2)
    
    # Kitchen Counter
    draw.rectangle([140, 285, 460, 480], fill=(30, 36, 48))
    draw.rectangle([130, 275, 470, 292], fill=(50, 60, 78))
    
    # Pan with eggs/food
    draw.rectangle([300, 267, 380, 278], fill=(20, 24, 30), outline=(0, 0, 0), width=1)
    draw.line([(380, 273), (420, 273)], fill=(15, 18, 24), width=6)
    draw.ellipse([315, 269, 335, 277], fill=(255, 255, 255))
    draw.ellipse([322, 271, 328, 275], fill=(245, 158, 11))
    draw.ellipse([345, 269, 365, 277], fill=(255, 255, 255))
    draw.ellipse([352, 271, 358, 275], fill=(245, 158, 11))
    
    # Steam
    steam_phase = (t * 6) % 3
    for si in range(3):
        sy = 255 - int(((steam_phase + si) % 3) * 16)
        sx = 330 + si * 14
        draw.arc([sx, sy, sx + 12, sy + 10], start=0, end=180, fill=(255, 255, 255), width=2)
    
    # Zipbab Boy standing at counter with Apron & Sunglasses
    whisk = math.sin(t * 12)
    bob = abs(whisk) * 2
    hip = (250, 295)
    torso_top = (250, 210 + bob)
    head_pos = (250, 168 + bob)
    
    # Legs (navy pants)
    draw_capsule_bone(draw, hip, (240, 360), width=15, fill_col=(30, 41, 59))
    draw_capsule_bone(draw, (240, 360), (235, 430), width=14, fill_col=(30, 41, 59))
    draw_capsule_bone(draw, hip, (260, 360), width=15, fill_col=(30, 41, 59))
    draw_capsule_bone(draw, (260, 360), (265, 430), width=14, fill_col=(30, 41, 59))
    
    # Torso: White tee + Warm Amber Apron!
    draw_capsule_bone(draw, hip, torso_top, width=28, fill_col=(250, 250, 255))
    # Apron over torso
    draw.rectangle([238, 220 + bob, 262, 290], fill=(245, 158, 11), outline=(180, 110, 5), width=2)
    
    # Left arm holding pan handle
    draw_capsule_bone(draw, (240, 220 + bob), (280, 250), width=11, fill_col=(255, 222, 196))
    draw_capsule_bone(draw, (280, 250), (320, 273), width=10, fill_col=(255, 222, 196))
    
    # Right arm bringing tasting spoon to mouth!
    tast_x = 265 + whisk * 10
    tast_y = 205 + whisk * 8
    draw_capsule_bone(draw, (260, 220 + bob), (285, 235), width=11, fill_col=(255, 222, 196))
    draw_capsule_bone(draw, (285, 235), (tast_x, tast_y), width=10, fill_col=(255, 222, 196))
    # Spoon
    draw.line([(tast_x, tast_y), (tast_x - 12, tast_y - 12)], fill=(200, 205, 215), width=3)
    draw.ellipse([tast_x - 18, tast_y - 18, tast_x - 10, tast_y - 10], fill=(200, 205, 215))
    
    draw_zipbab_head(draw, head_pos, r=21)
    
    draw.text((36, 120), "AM 07:30", fill=(255, 255, 255), font=font_title)
    draw.text((36, 148), "COOKING & TASTING", fill=(245, 158, 11), font=font_sub)
    
    # BOTTOM SCENE (Still in bed, scrolling smartphone)
    draw.rectangle([0, 480, W, 860], fill=(12, 16, 26))
    
    # Bed
    draw.rectangle([60, 680, 380, 780], fill=(18, 24, 38), outline=(28, 38, 58), width=2)
    draw.ellipse([80, 660, 140, 700], fill=(220, 220, 230))
    
    # Regular person awake but lying in bed staring at phone
    b_head = (145, 670)
    draw_tired_head(draw, b_head, r=20, is_sleeping=False)
    
    # Arms holding phone above face
    draw_capsule_bone(draw, (155, 680), (180, 645), width=10, fill_col=(235, 218, 205))
    draw_capsule_bone(draw, (180, 645), (195, 630), width=9, fill_col=(235, 218, 205))
    
    # Smartphone with blue glow
    draw.rectangle([190, 615, 205, 640], fill=(20, 24, 32), outline=(0, 0, 0), width=1)
    draw.rectangle([192, 618, 203, 637], fill=(56, 189, 248))
    # Blue beam on face
    draw.polygon([(195, 625), (145, 655), (145, 685)], fill=(20, 38, 62))
    
    # Blanket
    draw.rectangle([165, 670, 375, 775], fill=(30, 58, 138), outline=(24, 46, 110), width=2)
    
    draw.text((36, 500), "AM 07:30", fill=(255, 255, 255), font=font_title)
    draw.text((36, 528), "BED PHONE SCROLLING", fill=(148, 163, 184), font=font_sub)

def render_act3(draw, t):
    # AM 08:00
    # Top: Zipbab Boy enjoying warm healthy breakfast at table with sunglasses!
    # Bottom: Regular person in total panic! Clock says 8:00! Frantically stuffing leftover cold food & rushing out door!
    
    # TOP SCENE (Warm Dining)
    draw.rectangle([0, 100, W, 480], fill=(42, 48, 62))
    # Table
    draw.rectangle([180, 305, 430, 480], fill=(32, 38, 50))
    draw.rectangle([170, 295, 440, 310], fill=(55, 65, 85))
    
    # Warm bowl & steam
    draw.ellipse([270, 280, 330, 300], fill=(240, 240, 245), outline=(0, 0, 0), width=2)
    draw.ellipse([275, 283, 325, 295], fill=(234, 179, 8))
    steam_y = 260 - int(((t * 5) % 2) * 15)
    draw.arc([290, steam_y, 305, steam_y + 15], start=0, end=180, fill=(255, 255, 255), width=2)
    
    # Zipbab Boy seated, spoon in mouth, smiling happily
    hip = (230, 320)
    torso_top = (230, 230)
    head_pos = (230, 188)
    
    # Seated legs
    draw_capsule_bone(draw, hip, (200, 350), width=15, fill_col=(30, 41, 59))
    draw_capsule_bone(draw, (200, 350), (200, 425), width=14, fill_col=(30, 41, 59))
    draw_capsule_bone(draw, hip, torso_top, width=28, fill_col=(250, 250, 255))
    
    # Spoon to mouth
    draw_capsule_bone(draw, (235, 235), (265, 255), width=11, fill_col=(255, 222, 196))
    draw_capsule_bone(draw, (265, 255), (250, 205), width=10, fill_col=(255, 222, 196))
    
    draw_zipbab_head(draw, head_pos, r=21)
    
    draw.text((36, 120), "AM 08:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 148), "HEALTHY BREAKFAST", fill=(245, 158, 11), font=font_sub)
    
    # BOTTOM SCENE (Frantic Rush out the door!)
    draw.rectangle([0, 480, W, 860], fill=(12, 16, 26))
    
    # Exit Doorway on the right
    draw.rectangle([390, 520, 500, 840], fill=(45, 30, 20), outline=(20, 24, 32), width=3) # Door frame
    draw.polygon([(470, 530), (520, 550), (520, 830), (470, 830)], fill=(70, 50, 35)) # open door
    
    # Leftover takeout box on low table
    draw.rectangle([80, 720, 180, 780], fill=(25, 32, 45))
    draw.rectangle([95, 705, 140, 722], fill=(220, 225, 235), outline=(0, 0, 0), width=1) # plastic takeout box
    draw.text((100, 708), "TAKEOUT", fill=(220, 38, 38), font=font_sub)
    
    # Frantic Person running towards door!
    # Torso leaning forward 35 degrees
    run_cycle = math.sin(t * 18)
    run_x = 280 + int(run_cycle * 15)
    f_hip = (run_x, 680)
    f_torso_top = (run_x + 35, 600)
    f_head = (run_x + 50, 565)
    
    # Legs sprinting
    draw_capsule_bone(draw, f_hip, (run_x - 30, 720), width=14, fill_col=(71, 85, 105))
    draw_capsule_bone(draw, (run_x - 30, 720), (run_x - 55, 765), width=13, fill_col=(71, 85, 105))
    draw_capsule_bone(draw, f_hip, (run_x + 40, 715), width=14, fill_col=(71, 85, 105))
    draw_capsule_bone(draw, (run_x + 40, 715), (run_x + 75, 765), width=13, fill_col=(71, 85, 105))
    
    # Torso (rumpled grey tee)
    draw_capsule_bone(draw, f_hip, f_torso_top, width=26, fill_col=(100, 116, 139))
    
    # Left hand grabbing cold leftover pizza/chicken
    draw_capsule_bone(draw, (run_x + 25, 610), (run_x + 10, 650), width=11, fill_col=(235, 218, 205))
    draw_capsule_bone(draw, (run_x + 10, 650), (run_x + 40, 580), width=10, fill_col=(235, 218, 205)) # stuffed to mouth!
    draw.polygon([(run_x + 35, 575), (run_x + 50, 580), (run_x + 45, 565)], fill=(217, 119, 6)) # leftover pizza slice
    
    # Head panicked!
    draw_tired_head(draw, f_head, r=21, is_panicked=True)
    
    # Motion lines behind
    draw.line([(run_x - 60, 640), (run_x - 20, 640)], fill=(200, 210, 225), width=2)
    draw.line([(run_x - 70, 670), (run_x - 30, 670)], fill=(200, 210, 225), width=2)
    
    draw.text((36, 500), "AM 08:00", fill=(255, 255, 255), font=font_title)
    draw.text((36, 528), "LEFTOVER & RUSH OUT", fill=(239, 68, 68), font=font_sub)

def render_act4_commute(img, draw, t):
    # AM 08:30 (Climax Commute)
    # Fullscreen morning street scene!
    # Ahead: Zipbab Boy, sunglasses, bag, proud upright confident stride!
    # Behind: Regular person, slouching, staring at smartphone, squiggly tired lines!
    
    # Sky: Bright crisp morning blue with sunny gradient
    for y in range(0, 560):
        ratio = y / 560
        r = int(70 + ratio * 140)
        g = int(130 + ratio * 100)
        b = int(220 + ratio * 35)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Morning Sun
    draw.ellipse([420, 80, 480, 140], fill=(255, 245, 210))
    
    # Distant modern city buildings
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
    
    # Railing & Trees
    draw.line([(0, 495), (W, 495)], fill=(120, 140, 160), width=3)
    for rx in range(0, W, 40):
        draw.line([(rx, 495), (rx, 530)], fill=(120, 140, 160), width=2)
    
    # Sidewalk ground
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
    
    # Front leg
    knee_f = (lead_x + stride_phase * 18, 625 - bob_lead)
    foot_f = (lead_x + stride_phase * stride_amp, 690)
    # Back leg
    lift_b = max(0, -stride_phase * 18)
    knee_b = (lead_x - stride_phase * 14, 625 - bob_lead - lift_b * 0.5)
    foot_b = (lead_x - stride_phase * stride_amp, 690 - lift_b)
    
    # Draw back leg
    draw_capsule_bone(draw, hip_lead, knee_b, width=15, fill_col=(30, 41, 59))
    draw_capsule_bone(draw, knee_b, foot_b, width=14, fill_col=(30, 41, 59))
    # Shoes (clean white sneakers)
    draw.ellipse([foot_b[0] - 2, foot_b[1] - 4, foot_b[0] + 16, foot_b[1] + 6], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    
    # Torso (Smart stylish jacket / shirt)
    draw_capsule_bone(draw, hip_lead, torso_top_lead, width=28, fill_col=(245, 158, 11))
    
    # Front leg
    draw_capsule_bone(draw, hip_lead, knee_f, width=15, fill_col=(30, 41, 59))
    draw_capsule_bone(draw, knee_f, foot_f, width=14, fill_col=(30, 41, 59))
    draw.ellipse([foot_f[0] - 2, foot_f[1] - 4, foot_f[0] + 16, foot_f[1] + 6], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    
    # Right arm swinging with sleek bag
    shoulder_lead = (lead_x, 490 - bob_lead)
    arm_swing = math.sin(walk_t) * 26
    hand_lead = (lead_x - arm_swing, 555 - bob_lead)
    draw_capsule_bone(draw, shoulder_lead, (lead_x - arm_swing * 0.5, 520 - bob_lead), width=12, fill_col=(255, 222, 196))
    draw_capsule_bone(draw, (lead_x - arm_swing * 0.5, 520 - bob_lead), hand_lead, width=11, fill_col=(255, 222, 196))
    
    # Briefcase
    bc_x, bc_y = hand_lead[0] - 8, hand_lead[1] + 2
    draw.rectangle([bc_x, bc_y, bc_x + 32, bc_y + 24], fill=(120, 80, 50), outline=(0, 0, 0), width=2)
    draw.line([(bc_x + 10, bc_y), (bc_x + 22, bc_y)], fill=(0, 0, 0), width=2)
    
    # Head with sunglasses!
    draw_zipbab_head(draw, head_lead, r=22)
    
    # 2. FOLLOWER (REGULAR TIRED PERSON) - Behind, hunched over, staring at phone
    fol_x = 185
    t_slow = t * 6.5
    bob_fol = abs(math.cos(t_slow)) * 3
    hip_fol = (fol_x, 580 - bob_fol)
    torso_top_fol = (fol_x + 24, 500 - bob_fol) # forward hunch!
    head_fol = (fol_x + 36, 465 - bob_fol)
    
    f_swing = math.sin(t_slow) * 18
    f_knee_b = (fol_x - f_swing * 0.5, 635 - bob_fol)
    f_foot_b = (fol_x - f_swing, 690)
    f_knee_f = (fol_x + f_swing * 0.5, 635 - bob_fol)
    f_foot_f = (fol_x + f_swing, 690)
    
    draw_capsule_bone(draw, hip_fol, f_knee_b, width=14, fill_col=(51, 65, 85))
    draw_capsule_bone(draw, f_knee_b, f_foot_b, width=13, fill_col=(51, 65, 85))
    draw_capsule_bone(draw, hip_fol, torso_top_fol, width=26, fill_col=(100, 116, 139))
    draw_capsule_bone(draw, hip_fol, f_knee_f, width=14, fill_col=(51, 65, 85))
    draw_capsule_bone(draw, f_knee_f, f_foot_f, width=13, fill_col=(51, 65, 85))
    
    # Arms holding glowing smartphone
    shoulder_fol = (fol_x + 20, 515 - bob_fol)
    f_hand = (fol_x + 50, 530 - bob_fol)
    draw_capsule_bone(draw, shoulder_fol, (fol_x + 36, 535 - bob_fol), width=11, fill_col=(235, 218, 205))
    draw_capsule_bone(draw, (fol_x + 36, 535 - bob_fol), f_hand, width=10, fill_col=(235, 218, 205))
    
    draw.rectangle([f_hand[0] - 2, f_hand[1] - 8, f_hand[0] + 6, f_hand[1] + 8], fill=(20, 25, 35), outline=(0, 0, 0), width=1)
    draw.rectangle([f_hand[0], f_hand[1] - 6, f_hand[0] + 4, f_hand[1] + 6], fill=(56, 189, 248))
    
    draw_tired_head(draw, head_fol, r=20, is_sleeping=False)
    
    # Fatigue steam waves (~ ~)
    steam_y = head_fol[1] - 28 - int((t * 18) % 18)
    draw.arc([head_fol[0] - 18, steam_y, head_fol[0], steam_y + 14], start=0, end=180, fill=(140, 150, 170), width=2)
    draw.arc([head_fol[0] - 8, steam_y - 10, head_fol[0] + 10, steam_y + 4], start=180, end=360, fill=(140, 150, 170), width=2)
    
    # Climax Titles
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
            
        # Center seam bar & timer badge
        draw.line([(0, 480), (W, 480)], fill=(0, 0, 0), width=4)
        draw_timer_badge(draw, W // 2, 480, timer_str, progress)
    else:
        render_act4_commute(img, draw, t)
        
    # Watermark
    wm = "ZIPBAB BOY · 집밥보이"
    bbox_wm = font_sub.getbbox(wm)
    draw.text(((W - (bbox_wm[2]-bbox_wm[0])) // 2, 930), wm, fill=(120, 130, 145), font=font_sub)
    
    return img

if __name__ == '__main__':
    os.makedirs('scratch/test_acts_v3', exist_ok=True)
    f1 = render_frame_by_time(1.4)
    f1.save('scratch/test_acts_v3/act1_0700.png')
    f2 = render_frame_by_time(4.2)
    f2.save('scratch/test_acts_v3/act2_0730.png')
    f3 = render_frame_by_time(7.0)
    f3.save('scratch/test_acts_v3/act3_0800.png')
    f4 = render_frame_by_time(9.8)
    f4.save('scratch/test_acts_v3/act4_0830.png')
    print('All 4 acts rendered successfully!')
