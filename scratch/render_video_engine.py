import math
import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (9:16 vertical reels)
W, H = 540, 960

FONT_MONO = '/System/Library/Fonts/SFNSMono.ttf'
FONT_SANS = '/System/Library/Fonts/SFNS.ttf'
FONT_KR = '/System/Library/Fonts/AppleSDGothicNeo.ttc'

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_title = get_font(FONT_MONO, 22)
font_sub = get_font(FONT_MONO, 13)
font_timer = get_font(FONT_MONO, 14)
font_climax_title = get_font(FONT_MONO, 24)
font_climax_sub = get_font(FONT_KR, 14)

def draw_continuous_limb(draw, pts, width=14, outline_w=3, fill_col=(255, 255, 255), outline_col=(0, 0, 0)):
    total_w = width + outline_w * 2
    total_r = total_w // 2
    inner_r = width // 2
    
    # Outer black silhouette
    draw.line(pts, fill=outline_col, width=total_w, joint='curve')
    for p in pts:
        draw.ellipse([p[0]-total_r, p[1]-total_r, p[0]+total_r, p[1]+total_r], fill=outline_col)
    
    # Inner solid color
    draw.line(pts, fill=fill_col, width=width, joint='curve')
    for p in pts:
        draw.ellipse([p[0]-inner_r, p[1]-inner_r, p[0]+inner_r, p[1]+inner_r], fill=fill_col)

def draw_head(draw, pos, r=22, outline_w=4, fill_col=(255, 255, 255), outline_col=(0, 0, 0)):
    x, y = pos
    draw.ellipse([x - r - outline_w, y - r - outline_w, x + r + outline_w, y + r + outline_w], fill=outline_col)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=fill_col)

def draw_timer_badge(draw, cx, cy, radius, time_str, progress_ratio):
    # Circular badge background
    r = radius
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 12, 16), outline=(255, 255, 255), width=2)
    
    # Arc progress
    arc_box = [cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3]
    start_angle = -90
    end_angle = -90 + (progress_ratio * 360)
    if end_angle > start_angle:
        draw.arc(arc_box, start=start_angle, end=end_angle, fill=(255, 255, 255), width=3)
    
    # Center text
    bbox = font_timer.getbbox(time_str)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 1), time_str, fill=(255, 255, 255), font=font_timer)

def render_act1(draw, t):
    # Act 1 (0.0s ~ 3.0s):
    # Top: Cooking Prep (Chopping) / Bottom: In bed scrolling phone
    
    # --- TOP SCENE (Kitchen) ---
    # Wall background
    draw.rectangle([0, 100, W, 480], fill=(42, 48, 62))
    
    # Soft ceiling light glow
    draw.polygon([(270, 100), (140, 480), (400, 480)], fill=(48, 55, 72))
    draw.rectangle([250, 100, 290, 112], fill=(22, 26, 34)) # lamp fixture
    draw.ellipse([258, 108, 282, 118], fill=(255, 245, 200)) # bulb
    
    # Window with sunrise
    draw.rectangle([60, 140, 170, 240], fill=(25, 30, 42), outline=(15, 18, 26), width=4)
    # Sunset gradient in window
    for wy in range(144, 236):
        ratio = (wy - 144) / 92
        r = int(70 + ratio * 150)
        g = int(60 + ratio * 90)
        b = int(120 - ratio * 40)
        draw.line([(64, wy), (166, wy)], fill=(r, g, b))
    draw.line([(115, 140), (115, 240)], fill=(15, 18, 26), width=3)
    draw.line([(60, 190), (170, 190)], fill=(15, 18, 26), width=3)
    
    # Kitchen counter & cutting board
    draw.rectangle([220, 310, 480, 480], fill=(28, 34, 46))
    draw.rectangle([210, 300, 490, 316], fill=(50, 58, 76)) # counter top
    draw.rectangle([270, 292, 350, 302], fill=(180, 140, 90), outline=(120, 90, 50), width=1) # wood board
    
    # Chopped veggies
    draw.ellipse([285, 290, 297, 296], fill=(46, 204, 113)) # green
    draw.ellipse([305, 290, 317, 296], fill=(230, 126, 34)) # carrot
    
    # Active Chopping Stickman
    # Head & Torso
    chop_cycle = math.sin(t * 18) # fast chopping
    bob = abs(chop_cycle) * 3
    
    torso_top = (235, 215 + bob)
    hip = (235, 310)
    head_pos = (235, 175 + bob)
    
    # Legs (standing)
    draw_continuous_limb(draw, [hip, (225, 380), (220, 460), (205, 460)], width=14, outline_w=3, fill_col=(160, 170, 185))
    draw_continuous_limb(draw, [hip, torso_top], width=20, outline_w=4, fill_col=(255, 255, 255))
    draw_continuous_limb(draw, [hip, (245, 380), (250, 460), (265, 460)], width=14, outline_w=3, fill_col=(255, 255, 255))
    
    # Left arm holding board
    shoulder = (235, 225 + bob)
    draw_continuous_limb(draw, [shoulder, (270, 265), (285, 295)], width=12, outline_w=3, fill_col=(180, 190, 205))
    
    # Right arm holding knife, chopping up and down
    knife_y = 288 + chop_cycle * 12
    draw_continuous_limb(draw, [shoulder, (265, 240 + chop_cycle * 6), (300, knife_y)], width=12, outline_w=3, fill_col=(255, 255, 255))
    # Knife blade
    draw.polygon([(300, knife_y - 2), (325, knife_y - 4), (325, knife_y + 2), (300, knife_y + 4)], fill=(220, 225, 235), outline=(0, 0, 0))
    
    draw_head(draw, head_pos, r=22, outline_w=4)
    
    # Text Hud Top
    draw.text((36, 120), "15 MINUTES", fill=(255, 255, 255), font=font_title)
    draw.text((36, 148), "COOKING · FRESH PREP", fill=(148, 163, 184), font=font_sub)
    
    # --- BOTTOM SCENE (Dark Bedroom) ---
    draw.rectangle([0, 480, W, 860], fill=(10, 14, 24))
    
    # Night window
    draw.rectangle([340, 520, 450, 620], fill=(6, 9, 16), outline=(15, 20, 32), width=4)
    draw.rectangle([344, 524, 446, 616], fill=(14, 20, 36))
    draw.ellipse([410, 540, 432, 562], fill=(230, 240, 255)) # moon
    draw.line([(395, 520), (395, 620)], fill=(15, 20, 32), width=3)
    draw.line([(340, 570), (450, 570)], fill=(15, 20, 32), width=3)
    
    # Bed
    draw.rectangle([60, 680, 380, 780], fill=(18, 24, 38), outline=(28, 38, 58), width=2)
    draw.rectangle([50, 620, 70, 780], fill=(28, 38, 58)) # headboard
    draw.ellipse([80, 660, 140, 700], fill=(240, 240, 245)) # pillow
    
    # Stickman lying in bed with phone
    b_breath = math.sin(t * 3) * 2
    b_head = (145, 670 + b_breath)
    b_hip = (280, 690)
    b_shoulder = (175, 680 + b_breath)
    
    # Body under duvet
    draw_continuous_limb(draw, [b_shoulder, b_hip], width=18, outline_w=3, fill_col=(255, 255, 255))
    draw_head(draw, b_head, r=20, outline_w=3)
    
    # Arm holding glowing phone
    phone_x, phone_y = 190, 645
    draw_continuous_limb(draw, [b_shoulder, (170, 655), (phone_x, phone_y)], width=11, outline_w=3, fill_col=(255, 255, 255))
    
    # Phone & cyan screen glow
    draw.rectangle([phone_x - 3, phone_y - 12, phone_x + 9, phone_y + 12], fill=(20, 25, 35), outline=(0, 0, 0), width=1)
    draw.rectangle([phone_x - 1, phone_y - 10, phone_x + 7, phone_y + 10], fill=(56, 189, 248))
    # Glow polygon onto face
    draw.polygon([(phone_x, phone_y), (b_head[0] + 10, b_head[1] - 15), (b_head[0] + 15, b_head[1] + 15)], fill=(18, 35, 55))
    
    # Blue duvet covering lower half
    draw.rectangle([180, 675, 375, 775], fill=(30, 58, 138), outline=(24, 46, 110), width=2)
    
    # Digital clock
    draw.rectangle([80, 610, 130, 635], fill=(12, 16, 24), outline=(30, 40, 60), width=1)
    draw.text((88, 615), "19:00", fill=(239, 68, 68), font=font_sub)
    
    # Text Hud Bottom
    draw.text((36, 500), "45 MINUTES", fill=(255, 255, 255), font=font_title)
    draw.text((36, 528), "SOFA · INFINITE SCROLL", fill=(148, 163, 184), font=font_sub)

def render_act4_climax(draw, t):
    # Act 4 (8.2s ~ 11.0s):
    # Fullscreen Convergence: Sunset street walk comparison!
    
    # Twilight sunset sky gradient
    for y in range(0, 620):
        ratio = y / 620
        if ratio < 0.5:
            # Navy to deep purple
            sub = ratio / 0.5
            r = int(12 + sub * 50)
            g = int(18 + sub * 20)
            b = int(38 + sub * 30)
        else:
            # Purple to sunset amber
            sub = (ratio - 0.5) / 0.5
            r = int(62 + sub * 180)
            g = int(38 + sub * 85)
            b = int(68 - sub * 40)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Distant skyscraper silhouettes
    buildings = [
        (0, 180, 60), (50, 240, 45), (90, 190, 55), (140, 270, 40),
        (175, 210, 65), (235, 170, 50), (280, 250, 55), (330, 200, 45),
        (370, 230, 60), (425, 180, 55), (475, 220, 65)
    ]
    for bx, bh, bw in buildings:
        by = 520 - bh
        draw.rectangle([bx, by, bx + bw, 520], fill=(16, 20, 32))
        # Window dots
        for wy in range(by + 15, 500, 24):
            for wx in range(bx + 8, bx + bw - 8, 14):
                if (wx * 7 + wy * 13) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(254, 240, 138, 180))
    
    # Railing
    draw.line([(0, 510), (W, 510)], fill=(45, 52, 68), width=3)
    for rx in range(0, W, 45):
        draw.line([(rx, 510), (rx, 545)], fill=(45, 52, 68), width=2)
    
    # Sidewalk ground
    draw.rectangle([0, 540, W, 960], fill=(30, 36, 48))
    draw.line([(0, 540), (W, 540)], fill=(70, 80, 102), width=4) # curb highlight
    draw.line([(0, 640), (W, 640)], fill=(24, 28, 38), width=2)
    draw.line([(0, 760), (W, 760)], fill=(20, 24, 32), width=2)
    
    # Street lamp post
    lamp_x = 180
    draw.line([(lamp_x, 220), (lamp_x, 540)], fill=(50, 58, 72), width=5)
    draw.line([(lamp_x, 220), (lamp_x + 35, 220)], fill=(50, 58, 72), width=4)
    draw.rectangle([lamp_x + 30, 220, lamp_x + 46, 228], fill=(30, 36, 46))
    # Downward soft light cone
    draw.polygon([(lamp_x + 38, 228), (lamp_x - 30, 540), (lamp_x + 130, 540)], fill=(255, 230, 160, 40))
    
    # --- CHARACTERS WALKING ---
    walk_t = t * 7.5
    
    # 1. LEADER (COOKING / VITALITY) - Ahead, pure white, upright, confident
    lead_x = 360
    bob_lead = abs(math.cos(walk_t)) * 6
    hip_lead = (lead_x, 580 - bob_lead)
    torso_top_lead = (lead_x, 485 - bob_lead)
    head_lead = (lead_x, 442 - bob_lead)
    
    leg_swing = math.sin(walk_t) * 35
    knee_b_lead = (lead_x - leg_swing * 0.6, 640 - bob_lead)
    foot_b_lead = (lead_x - leg_swing, 705)
    knee_f_lead = (lead_x + leg_swing * 0.6, 640 - bob_lead)
    foot_f_lead = (lead_x + leg_swing, 705)
    
    # Back leg
    draw_continuous_limb(draw, [hip_lead, knee_b_lead, foot_b_lead, (foot_b_lead[0] + 14, foot_b_lead[1])], width=16, outline_w=4, fill_col=(160, 175, 195))
    # Torso
    draw_continuous_limb(draw, [hip_lead, torso_top_lead], width=22, outline_w=4, fill_col=(255, 255, 255))
    # Front leg
    draw_continuous_limb(draw, [hip_lead, knee_f_lead, foot_f_lead, (foot_f_lead[0] + 16, foot_f_lead[1])], width=16, outline_w=4, fill_col=(255, 255, 255))
    
    # Arms & Briefcase
    shoulder_lead = (lead_x, 500 - bob_lead)
    arm_swing = math.sin(walk_t) * 28
    hand_f_lead = (lead_x - arm_swing, 570 - bob_lead)
    draw_continuous_limb(draw, [shoulder_lead, (lead_x - arm_swing * 0.5, 535 - bob_lead), hand_f_lead], width=13, outline_w=3, fill_col=(255, 255, 255))
    # Briefcase
    bc_x, bc_y = hand_f_lead[0] - 6, hand_f_lead[1] + 2
    draw.rectangle([bc_x, bc_y, bc_x + 32, bc_y + 24], fill=(120, 80, 50), outline=(0, 0, 0), width=2)
    draw.line([(bc_x + 10, bc_y), (bc_x + 22, bc_y)], fill=(0, 0, 0), width=2)
    
    draw_head(draw, head_lead, r=24, outline_w=4, fill_col=(255, 255, 255))
    
    # 2. FOLLOWER (DELIVERY / EXHAUSTED) - Behind, grey, hunched, phone
    fol_x = 190
    t_slow = t * 6.5
    bob_fol = abs(math.cos(t_slow)) * 3
    # Hunched spine: torso tilts forward
    hip_fol = (fol_x, 595 - bob_fol)
    torso_top_fol = (fol_x + 24, 515 - bob_fol) # tilted 24px right
    head_fol = (fol_x + 36, 480 - bob_fol) # drooped forward
    
    f_swing = math.sin(t_slow) * 20 # small shuffle stride
    f_knee_b = (fol_x - f_swing * 0.5, 650 - bob_fol)
    f_foot_b = (fol_x - f_swing, 705)
    f_knee_f = (fol_x + f_swing * 0.5, 650 - bob_fol)
    f_foot_f = (fol_x + f_swing, 705)
    
    # Back leg
    draw_continuous_limb(draw, [hip_fol, f_knee_b, f_foot_b, (f_foot_b[0] + 10, f_foot_b[1])], width=15, outline_w=3, fill_col=(85, 95, 110))
    # Torso
    draw_continuous_limb(draw, [hip_fol, torso_top_fol], width=20, outline_w=4, fill_col=(115, 125, 140))
    # Front leg
    draw_continuous_limb(draw, [hip_fol, f_knee_f, f_foot_f, (f_foot_f[0] + 12, f_foot_f[1])], width=15, outline_w=3, fill_col=(115, 125, 140))
    
    # Both arms held up holding glowing phone
    shoulder_fol = (fol_x + 20, 530 - bob_fol)
    f_hand = (fol_x + 52, 545 - bob_fol)
    draw_continuous_limb(draw, [shoulder_fol, (fol_x + 38, 550 - bob_fol), f_hand], width=12, outline_w=3, fill_col=(115, 125, 140))
    # Phone
    draw.rectangle([f_hand[0] - 2, f_hand[1] - 8, f_hand[0] + 6, f_hand[1] + 8], fill=(20, 25, 35), outline=(0, 0, 0), width=1)
    draw.rectangle([f_hand[0], f_hand[1] - 6, f_hand[0] + 4, f_hand[1] + 6], fill=(56, 189, 248))
    
    # Head drooped
    draw_head(draw, head_fol, r=22, outline_w=3, fill_col=(115, 125, 140))
    
    # Fatigue steam waves (~ ~)
    steam_y = head_fol[1] - 30 - int((t * 20) % 20)
    draw.arc([head_fol[0] - 20, steam_y, head_fol[0], steam_y + 15], start=0, end=180, fill=(180, 190, 205), width=2)
    draw.arc([head_fol[0] - 10, steam_y - 12, head_fol[0] + 10, steam_y + 3], start=180, end=360, fill=(180, 190, 205), width=2)
    
    # Center Top Climax Title
    bbox1 = font_climax_title.getbbox("SAME 1 HOUR.")
    w1 = bbox1[2] - bbox1[0]
    draw.text(((W - w1) // 2, 85), "SAME 1 HOUR.", fill=(255, 255, 255), font=font_climax_title)
    
    bbox2 = font_climax_title.getbbox("DIFFERENT ME.")
    w2 = bbox2[2] - bbox2[0]
    draw.text(((W - w2) // 2, 118), "DIFFERENT ME.", fill=(255, 255, 255), font=font_climax_title)
    
    sub_text = "같은 1시간이지만, 내일의 내가 완전히 다릅니다."
    bbox3 = font_climax_sub.getbbox(sub_text)
    w3 = bbox3[2] - bbox3[0]
    draw.text(((W - w3) // 2, 155), sub_text, fill=(245, 158, 11), font=font_climax_sub)

def render_frame_by_time(t):
    img = Image.new('RGB', (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if t < 8.2:
        # Split screen acts
        render_act1(draw, t) # currently testing
        
        # Center seam bar & timer
        draw.line([(0, 480), (W, 480)], fill=(0, 0, 0), width=4)
        progress = min(1.0, t / 8.2)
        if t < 3.0:
            timer_str = "19:00"
        elif t < 6.0:
            timer_str = "19:15"
        else:
            timer_str = "19:30"
        draw_timer_badge(draw, W // 2, 480, 32, timer_str, progress)
    else:
        # Climax
        render_act4_climax(draw, t)
        
    # Subtle Watermark
    wm = "ZIPBAB VISUALS"
    bbox_wm = font_sub.getbbox(wm)
    draw.text(((W - (bbox_wm[2]-bbox_wm[0])) // 2, 930), wm, fill=(75, 85, 99), font=font_sub)
    
    return img

if __name__ == '__main__':
    os.makedirs('scratch/test_renders', exist_ok=True)
    f1 = render_frame_by_time(1.5)
    f1.save('scratch/test_renders/frame_act1.png')
    
    f4 = render_frame_by_time(9.5)
    f4.save('scratch/test_renders/frame_act4.png')
    print('Sample frames rendered successfully!')
