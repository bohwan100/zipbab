import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Warm, earthy, artistic, Kinfolk vibe)
BG_COLOR = RGBColor(250, 248, 245)      # Warm Cream
CARD_BG = RGBColor(255, 255, 255)       # Pure White
PRIMARY = RGBColor(54, 43, 37)          # Deep Charcoal/Warm Espresso
ACCENT_TERRA = RGBColor(189, 79, 44)    # Warm Terracotta
ACCENT_GREEN = RGBColor(68, 108, 86)    # Sage/Olive Green
TEXT_MUTED = RGBColor(115, 105, 95)     # Muted warm gray
CARD_BORDER = RGBColor(230, 224, 215)   # Subtle border

def set_slide_background(slide, color=BG_COLOR):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="요리의 몰입과 예술 1기 OT"):
    # Category / Breadcrumb
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11), Inches(0.4))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_TERRA
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = PRIMARY

blank_layout = prs.slide_layouts[6]

IMG_HEADER = "/Users/bohwanlee/.gemini/antigravity-ide/brain/9e0c0085-ca5c-46cd-ba5d-af211a1b4cc8/cooking_challenge_header_1789372226048.jpg"
IMG_VERIF = "/Users/bohwanlee/.gemini/antigravity-ide/brain/9e0c0085-ca5c-46cd-ba5d-af211a1b4cc8/cooking_verification_example_1789372243276.jpg"

# -----------------------------------------------------------------------------
# SLIDE 1: COVER
# -----------------------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, BG_COLOR)

# Left image
if os.path.exists(IMG_HEADER):
    s1.shapes.add_picture(IMG_HEADER, Inches(6.8), Inches(0.8), width=Inches(5.7), height=Inches(5.9))

# Text Box Left
tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "4주간의 주방 아틀리에"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(16)

p2 = tf1.add_paragraph()
p2.text = "요리의 몰입과\n예술 1기"
p2.font.size = Pt(40)
p2.font.bold = True
p2.font.color.rgb = PRIMARY
p2.space_after = Pt(20)

p3 = tf1.add_paragraph()
p3.text = "배달앱을 끄고, 내 손으로 감각과 이야기를 짓는 28일간의 여정\n온라인 오리엔테이션 (2026. 09. 16)"
p3.font.size = Pt(15)
p3.font.color.rgb = TEXT_MUTED

# -----------------------------------------------------------------------------
# SLIDE 2: AGENDA (1시간 타임테이블)
# -----------------------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, BG_COLOR)
add_header(s2, "오늘 1시간 동안 함께 나눌 이야기")

agendas = [
    ("01", "왜 '요리의 몰입과 예술'인가?", "15분", "스마트폰 도파민 디톡스, 설명하는 힘, 식재료 낭비 제로"),
    ("02", "4주 커리큘럼 & 진행 방식", "15분", "1주 1재료 3요리 원칙 & 아날로그 레시피북의 비밀"),
    ("03", "인증 룰 & 100% 환급 시스템", "10분", "카톡 인증 가이드 & 완주 페이스메이커 안내"),
    ("04", "준비 주간 미션 & 20인 크루 소개", "15분", "손글씨 노트 준비하기 & 20인의 요리 예술가 한 줄 인사"),
    ("05", "Q&A 및 파이팅 단체 캡처", "5분", "궁금증 해결 및 설레는 4주의 첫 단체 기념사진")
]

top_offset = Inches(1.8)
for i, (num, title, duration, desc) in enumerate(agendas):
    # Card Background
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_offset + Inches(i * 1.0), Inches(11.7), Inches(0.85))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    
    # Card Content
    tb = s2.shapes.add_textbox(Inches(1.0), top_offset + Inches(i * 1.0) + Inches(0.12), Inches(11.3), Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    
    run_num = p.add_run()
    run_num.text = f"{num}  "
    run_num.font.bold = True
    run_num.font.size = Pt(18)
    run_num.font.color.rgb = ACCENT_TERRA
    
    run_title = p.add_run()
    run_title.text = f"{title}   "
    run_title.font.bold = True
    run_title.font.size = Pt(16)
    run_title.font.color.rgb = PRIMARY
    
    run_dur = p.add_run()
    run_dur.text = f"[{duration}]  "
    run_dur.font.size = Pt(13)
    run_dur.font.color.rgb = ACCENT_GREEN
    
    run_desc = p.add_run()
    run_desc.text = f"― {desc}"
    run_desc.font.size = Pt(13)
    run_desc.font.color.rgb = TEXT_MUTED

# -----------------------------------------------------------------------------
# SLIDE 3: PROBLEM & WHY (우리는 왜 여기에 모였을까요?)
# -----------------------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, BG_COLOR)
add_header(s3, "우리는 왜 배달앱을 끄고 칼을 쥐었을까요?", "PART 1. 챌린지의 시작")

points = [
    ("도파민 과부하와 피로", "스마트폰 알림과 숏폼에 하루 종일 노출된 뇌.\n끼니마저 배달앱으로 대충 때우며 감각이 무뎌졌습니다."),
    ("남아서 버려지는 식재료", "자취할 때 요리를 꺼리는 가장 큰 이유는\n'어차피 재료가 남아 썩어 버릴까 봐'였습니다."),
    ("내 삶을 대접하는 감각의 결핍", "남을 위한 일에만 에너지를 쏟고,\n정작 나 자신을 위한 가장 따뜻한 밥 한 끼는 잊고 살았습니다.")
]

for i, (title, desc) in enumerate(points):
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 3.95), Inches(2.0), Inches(3.7), Inches(4.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    
    tb = s3.shapes.add_textbox(Inches(1.0 + i * 3.95), Inches(2.3), Inches(3.3), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"0{i+1}"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TERRA
    p.space_after = Pt(14)
    
    p2 = tf.add_paragraph()
    p2.text = title
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = PRIMARY
    p2.space_after = Pt(16)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED

# -----------------------------------------------------------------------------
# SLIDE 4: CORE VALUE 1 - 요리의 몰입
# -----------------------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, BG_COLOR)
add_header(s4, "가치 1. 요리의 몰입 : 맑은 정신을 회복하는 도파민 디톡스", "CORE PHILOSOPHY")

card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
card.fill.solid()
card.fill.fore_color.rgb = CARD_BG
card.line.color.rgb = CARD_BORDER

tb = s4.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.9), Inches(4.2))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "“사람이라면 매일 먹어야 하는 밥을 내 손으로 짓는 순간, 뇌는 정화됩니다.”"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(20)

items = [
    ("스마트폰을 끄는 시간", "요리하는 동안에는 유튜브나 쇼츠를 끕니다. 오직 칼질 소리, 끓는 냄새, 식재료의 질감에만 오감을 집중합니다."),
    ("주방에서 경험하는 움직이는 명상", "불을 다루고 타이밍을 맞추는 고도의 몰입 속에서 회사나 일상의 복잡한 잡생각이 말끔히 씻겨 나갑니다."),
    ("아날로그 손글씨의 힘", "스마트폰 화면 대신 손때 묻은 종이 노트에 펜으로 레시피를 쓰며 진짜 아날로그 도파민 디톡스를 완성합니다.")
]

for title, desc in items:
    p_item = tf.add_paragraph()
    p_item.text = f"• {title} : "
    p_item.font.bold = True
    p_item.font.size = Pt(15)
    p_item.font.color.rgb = PRIMARY
    
    run = p_item.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = TEXT_MUTED
    p_item.space_after = Pt(14)

# -----------------------------------------------------------------------------
# SLIDE 5: CORE VALUE 2 - 요리의 예술
# -----------------------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, BG_COLOR)
add_header(s5, "가치 2. 요리의 예술 : 내 행동의 가치를 증명하는 '설명하는 힘'", "CORE PHILOSOPHY")

card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
card.fill.solid()
card.fill.fore_color.rgb = CARD_BG
card.line.color.rgb = CARD_BORDER

tb = s5.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.9), Inches(4.2))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "“현대미술도 의도와 설명이 붙을 때 예술이 됩니다. 우리 일과 삶도 똑같습니다.”"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(20)

items5 = [
    ("예술을 완성하는 것은 '설명'이다", "변기 하나를 갖다 놔도 작가의 철학과 설명이 붙으면 수백억의 예술품이 되듯, 요리도 설명이 붙어야 특별해집니다."),
    ("사회생활과 일의 본질도 설명의 힘", "내가 직장이나 비즈니스에서 한 행동도 어떤 맥락과 의도로 설명하느냐에 따라 최고의 성과가 되기도, 헛수고가 되기도 합니다."),
    ("내 요리에 스토리 불어넣기", "'그냥 배고파서 볶은 밥'이 아니라, '이 재료를 고른 이유, 불 앞에 선 생각, 나에게 건네는 위로'를 언어로 훈련합니다.")
]

for title, desc in items5:
    p_item = tf.add_paragraph()
    p_item.text = f"• {title} : "
    p_item.font.bold = True
    p_item.font.size = Pt(15)
    p_item.font.color.rgb = PRIMARY
    
    run = p_item.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = TEXT_MUTED
    p_item.space_after = Pt(14)

# -----------------------------------------------------------------------------
# SLIDE 6: CORE VALUE 3 - 12가지 나만의 레시피
# -----------------------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, BG_COLOR)
add_header(s6, "가치 3. 12가지 나만의 레시피 : 식재료 낭비 제로 & 평생의 자립", "CORE PHILOSOPHY")

card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
card.fill.solid()
card.fill.fore_color.rgb = CARD_BG
card.line.color.rgb = CARD_BORDER

tb = s6.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.9), Inches(4.2))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "“어떤 재료가 남아도 근사한 한 끼로 비워내는 냉장고 파먹기의 무기”"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(20)

items6 = [
    ("자취 요리의 진입장벽 격파", "재료를 사기 꺼려지는 진짜 이유는 '남아서 썩어 버릴까 봐'입니다. 1주 1재료 3요리 훈련은 이 두려움을 완벽히 없앱니다."),
    ("한 재료의 무한한 변주", "양파 하나로 볶음, 수프, 피클까지 만들어보며 식재료를 입체적으로 다루는 감각을 손에 익힙니다."),
    ("평생 써먹는 자립의 기술", "4주 뒤 내 손에는 12가지 검증된 나만의 레시피북이 남습니다. 어떤 재료든 맛있게 요리할 수 있는 평생의 자존감이 생깁니다.")
]

for title, desc in items6:
    p_item = tf.add_paragraph()
    p_item.text = f"• {title} : "
    p_item.font.bold = True
    p_item.font.size = Pt(15)
    p_item.font.color.rgb = PRIMARY
    
    run = p_item.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = TEXT_MUTED
    p_item.space_after = Pt(14)

# -----------------------------------------------------------------------------
# SLIDE 7: 4-WEEK CURRICULUM
# -----------------------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, BG_COLOR)
add_header(s7, "4주 커리큘럼 : 1주 1재료 3요리", "PART 2. 4주간의 여정")

curriculums = [
    ("1주차", "양파 (Onion)", "단단한 껍질을 벗겨내고\n불을 만나 달콤해지는 시간", "양파 카라멜라이징, 양파스프,\n양파피클, 양파덮밥 등"),
    ("2주차", "계란 (Egg)", "가장 단순하지만\n무궁무진한 변주의 미학", "달걀말이, 수란 토스트,\n스페니시 오믈렛, 달걀장 등"),
    ("3주차", "토마토 (Tomato)", "붉은 생명력과 산미,\n깊은 풍미를 끌어내는 몰입", "토마토 마리네이드, 파스타,\n토마토 달걀볶음, 토마토스프 등"),
    ("4주차", "감자 (Potato)", "투박한 흙에서 건져 올린\n든든함과 따뜻한 위로", "감자 뇨끼, 감자채전,\n메쉬드 포테이토, 감자조림 등")
]

for i, (wk, ing, theme, ex) in enumerate(curriculums):
    card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.95), Inches(1.8), Inches(2.8), Inches(4.8))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    
    tb = s7.shapes.add_textbox(Inches(1.0 + i * 2.95), Inches(2.0), Inches(2.4), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = wk
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TERRA
    p.space_after = Pt(8)
    
    p2 = tf.add_paragraph()
    p2.text = ing
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = PRIMARY
    p2.space_after = Pt(14)
    
    p3 = tf.add_paragraph()
    p3.text = theme
    p3.font.size = Pt(13)
    p3.font.color.rgb = ACCENT_GREEN
    p3.space_after = Pt(16)
    
    p4 = tf.add_paragraph()
    p4.text = f"[추천 예시]\n{ex}"
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_MUTED

# -----------------------------------------------------------------------------
# SLIDE 8: RECIPE NOTEBOOK GUIDE
# -----------------------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, BG_COLOR)
add_header(s8, "핵심 도구 : 왜 스마트폰이 아닌 '종이 레시피북'인가?", "PART 2. 4주간의 여정")

# Left text
tb8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.5), Inches(5.0))
tf8 = tb8.text_frame
tf8.word_wrap = True

p = tf8.paragraphs[0]
p.text = "스마트폰을 주방에 들이는 순간, 몰입은 깨집니다."
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(16)

rules8 = [
    ("스마트폰 없는 청정 주방", "유튜브나 릴스를 보며 요리하면 음식에 집중할 수 없습니다. 레시피는 미리 노트에 적어두고 종이만 보고 요리합니다."),
    ("손글씨로 새기는 기억", "직접 펜으로 적어본 레시피는 뇌에 각인되어 온전히 나의 기술이 됩니다."),
    ("나만의 아틀리에 아카이브", "4주가 끝나면 손때 묻고 기름방울이 살짝 튄, 세상에 단 하나뿐인 나만의 보물 레시피북이 탄생합니다.")
]

for title, desc in rules8:
    p_item = tf8.add_paragraph()
    p_item.text = f"✔ {title}\n"
    p_item.font.bold = True
    p_item.font.size = Pt(15)
    p_item.font.color.rgb = PRIMARY
    
    run = p_item.add_run()
    run.text = desc
    run.font.bold = False
    run.font.size = Pt(13)
    run.font.color.rgb = TEXT_MUTED
    p_item.space_after = Pt(14)

# Right Picture
if os.path.exists(IMG_VERIF):
    s8.shapes.add_picture(IMG_VERIF, Inches(7.5), Inches(1.8), width=Inches(5.0), height=Inches(4.8))

# -----------------------------------------------------------------------------
# SLIDE 9: VERIFICATION GUIDE (인증 룰)
# -----------------------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, BG_COLOR)
add_header(s9, "카톡방 인증 가이드 : 사진과 설명의 힘", "PART 3. 실전 룰 & 인증")

steps = [
    ("STEP 1", "주 3회 요리 & 레시피북 작성", "매주 지정 식재료로 3번 요리하고,\n종이 노트에 레시피와 단상을 손글씨로 기록합니다."),
    ("STEP 2", "레시피북 사진 3장 촬영", "직접 쓴 레시피북 페이지를 촬영합니다.\n(요리 완성 사진을 함께 올리면 금상첨화!)"),
    ("STEP 3", "카톡방에 요리 설명 작성 후 인증", "각 요리에 담긴 나의 생각, 의도, 추억을\n언어로 멋지게 풀어내어 카톡방에 공유합니다.")
]

for i, (st, title, desc) in enumerate(steps):
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 3.95), Inches(1.8), Inches(3.7), Inches(2.6))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    
    tb = s9.shapes.add_textbox(Inches(1.0 + i * 3.95), Inches(2.0), Inches(3.3), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = st
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TERRA
    p.space_after = Pt(6)
    
    p2 = tf.add_paragraph()
    p2.text = title
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = PRIMARY
    p2.space_after = Pt(10)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED

# Example Box
box_ex = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.1))
box_ex.fill.solid()
box_ex.fill.fore_color.rgb = RGBColor(243, 239, 233)
box_ex.line.color.rgb = CARD_BORDER

tb_ex = s9.shapes.add_textbox(Inches(1.1), Inches(4.9), Inches(11.1), Inches(1.7))
tf_ex = tb_ex.text_frame
tf_ex.word_wrap = True

pe1 = tf_ex.paragraphs[0]
pe1.text = "💬 [카톡 인증 양식 예시]"
pe1.font.bold = True
pe1.font.size = Pt(14)
pe1.font.color.rgb = ACCENT_TERRA
pe1.space_after = Pt(6)

pe2 = tf_ex.add_paragraph()
pe2.text = "📷 사진 : 이번 주 작성한 레시피북 3페이지 촬영 사진\n✍️ 요리 설명 : \n1. [양파 카라멜라이징 수프] 껍질을 까며 복잡한 생각을 비워내고, 40분 동안 불 앞을 지키며 인내의 단맛을 맛본 요리\n2. [양파 달걀 덮밥] 바쁜 퇴근길, 배달 대신 10분 만에 따뜻하게 나를 위로해 준 든든한 한 끼"
pe2.font.size = Pt(12)
pe2.font.color.rgb = PRIMARY

# -----------------------------------------------------------------------------
# SLIDE 10: REFUND SYSTEM (환급 룰)
# -----------------------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, BG_COLOR)
add_header(s10, "100% 환급 시스템 : 배달비 아끼고 전액 다시 찾아가기!", "PART 3. 실전 룰 & 인증")

refund_cards = [
    ("100% 완주 달성", "12회 완벽 인증", "50,000원", "전액 100% 환급!", ACCENT_TERRA),
    ("90% 이상 달성", "11회 인증", "35,000원", "70% 환급", ACCENT_GREEN),
    ("75% 이상 달성", "10회 인증", "25,000원", "50% 환급", PRIMARY)
]

for i, (title, sub, money, rate, color) in enumerate(refund_cards):
    card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 3.95), Inches(1.8), Inches(3.7), Inches(3.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    
    tb = s10.shapes.add_textbox(Inches(1.0 + i * 3.95), Inches(2.2), Inches(3.3), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(8)
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_after = Pt(20)
    
    p3 = tf.add_paragraph()
    p3.text = money
    p3.font.size = Pt(28)
    p3.font.bold = True
    p3.font.color.rgb = color
    p3.space_after = Pt(6)
    
    p4 = tf.add_paragraph()
    p4.text = rate
    p4.font.size = Pt(15)
    p4.font.bold = True
    p4.font.color.rgb = color

# Bottom Note
tb_note = s10.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.2))
tf_note = tb_note.text_frame
tf_note.word_wrap = True
pn = tf_note.paragraphs[0]
pn.text = "💡 '5만 원'은 비용이 아니라 내 완주 의지를 지키는 '보증금'입니다.\n20명 전원이 100% 환급받아 가실 수 있도록 단톡방에서 함께 응원하고 이끌어드립니다!"
pn.font.size = Pt(14)
pn.font.bold = True
pn.font.color.rgb = ACCENT_TERRA

# -----------------------------------------------------------------------------
# SLIDE 11: PREPARATION WEEK (준비 주간 미션)
# -----------------------------------------------------------------------------
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, BG_COLOR)
add_header(s11, "준비 주간 미션 (9/17 ~ 9/20) : 나만의 도구를 갖추라!", "PART 4. 준비 주간 & 크루 소개")

card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
card.fill.solid()
card.fill.fore_color.rgb = CARD_BG
card.line.color.rgb = CARD_BORDER

tb11 = s11.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.9), Inches(4.2))
tf11 = tb11.text_frame
tf11.word_wrap = True

p = tf11.paragraphs[0]
p.text = "본 챌린지 시작(9/21 월) 전까지 아래 3가지를 완료해 주세요!"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(20)

m_items = [
    ("미션 1. 나만의 '종이 레시피북(노트)' 마련하기", "문구점이나 다이소에서 마음에 드는 무선/유선 노트를 하나 구입하세요. 표지에 [요리의 몰입과 예술 1기 - 나의 이름]을 손글씨로 적어봅니다."),
    ("미션 2. 1주차 식재료 '양파' 장보기", "9/21(월) 첫 요리를 시작하기 전, 신선한 양파 1망을 사서 냉장고나 서늘한 곳에 준비해 둡니다."),
    ("미션 3. 양파로 해보고 싶은 3가지 요리 스케치하기", "노트 첫 페이지에 이번 주에 도전해보고 싶은 3가지 양파 요리 이름을 미리 손으로 적어봅니다.")
]

for title, desc in m_items:
    p_item = tf11.add_paragraph()
    p_item.text = f"✔ {title}\n"
    p_item.font.bold = True
    p_item.font.size = Pt(16)
    p_item.font.color.rgb = PRIMARY
    
    run = p_item.add_run()
    run.text = desc
    run.font.bold = False
    run.font.size = Pt(14)
    run.font.color.rgb = TEXT_MUTED
    p_item.space_after = Pt(14)

# -----------------------------------------------------------------------------
# SLIDE 12: CREW INTRODUCTIONS (20인 자기소개)
# -----------------------------------------------------------------------------
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12, BG_COLOR)
add_header(s12, "20인의 주방 예술가 : 30초 릴레이 자기소개", "PART 4. 준비 주간 & 크루 소개")

card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
card.fill.solid()
card.fill.fore_color.rgb = CARD_BG
card.line.color.rgb = CARD_BORDER

tb12 = s12.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(10.9), Inches(4.0))
tf12 = tb12.text_frame
tf12.word_wrap = True

p = tf12.paragraphs[0]
p.text = "마이크를 켜고, 4주간 함께할 크루들에게 반갑게 인사해주세요!"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(24)

p2 = tf12.add_paragraph()
p2.text = "🎙️ [릴레이 소개 키워드 3가지]\n\n" \
          "1. 닉네임 / 하시는 일 (간단히)\n" \
          "2. 이 챌린지에 신청하게 된 결정적인 계기 (배달앱 끊기, 도파민 디톡스 등)\n" \
          "3. 4주 후 내가 꿈꾸는 나의 변화된 모습 & 각오 한 줄!\n\n" \
          "💡 완주율은 '동료들과 친해질수록' 3배 이상 높아집니다. 편안하게 이야기 나눠요 :)"
p2.font.size = Pt(16)
p2.font.color.rgb = PRIMARY
p2.space_after = Pt(14)

# -----------------------------------------------------------------------------
# SLIDE 13: CLOSING & Q&A
# -----------------------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13, BG_COLOR)
add_header(s13, "주방은 나를 대접하는 가장 작은 아틀리에입니다", "FINISH")

tb13 = s13.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(4.5))
tf13 = tb13.text_frame
tf13.word_wrap = True

p = tf13.paragraphs[0]
p.text = "Q & A 및 단체 캡처 타임"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = ACCENT_TERRA
p.space_after = Pt(20)

p2 = tf13.add_paragraph()
p2.text = "• 궁금하신 점이나 룰 관련 질문을 편하게 남겨주세요.\n" \
          "• 마지막으로 화면을 켜고, 설레는 1기의 출발을 기념하는 단체 캡처 사진을 찍습니다!\n\n" \
          "“우리는 4주 뒤, 12가지 나만의 레시피와 단단해진 자존감을 안고 다시 만납니다.”"
p2.font.size = Pt(17)
p2.font.color.rgb = PRIMARY

output_path = "/Users/bohwanlee/Desktop/antigravity 폴더/요리의_몰입과_예술_1기_OT.pptx"
prs.save(output_path)
print(f"PPTX Successfully created at: {output_path}")
