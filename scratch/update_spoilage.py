import re

new_spoilage_map = {
    "손질 깐 대파": "진액 발생, 시큼한 냄새, 잎이 누렇게 물러짐",
    "깐 양파": "속이 검게 변색, 물렁거리며 쉰내 발생",
    "햇 감자": "표면 초록 변색(솔라닌 독소), 싹 자람 및 쭈글거림",
    "국산 찌개용 두부": "표면 미끌거리는 점액질, 시큼한 신맛과 악취",
    "무항생제 신선 대란": "물에 둥둥 뜨거나 노른자가 퍼져 악취 발생",
    "인큐 애호박": "씨 부분이 갈색으로 물러지며 표면 끈적임",
    "신선 양배추": "잎이 검게 변색되고 시큼하고 퀴퀴한 냄새",
    "국산 콩나물": "줄기가 갈색으로 무르고 물 생기며 악취",
    "팽이버섯": "수분이 흥건히 고이고 노랗게 변하며 미끌거림",
    "세척 무 반토막": "스펀지처럼 푸석해지거나 무르고 곰팡이 발생",
    "종가집 맛김치": "두꺼운 흰 골마지, 톡 쏘는 부패성 악취",
    "소고기 국거리 양지": "회갈색 변색, 끈적이는 점액질과 시큼한 냄새",
    "훈제오리 슬라이스": "기름 쩐내, 표면 끈적임 및 시큼한 냄새",
    "풀무원 순두부": "포장 튜브 팽창, 국물 탁해짐 및 시큼한 냄새",
    "돼지 앞다리살 불고기용": "심한 냉동화상(백화 현상), 해동 시 역한 누린내",
    "닭다리 순살 정육": "황색 핏물 발생, 살이 무르고 시큼한 냄새",
    "우삼겹 바로구이용": "지방 누런 변색, 진한 기름 쩐내 및 시큼함",
    "냉동 손질 해물믹스": "심한 비린내, 해동 후 살이 녹아내림",
    "부산 사각어묵": "시큼한 냄새, 표면 끈적이는 점액과 곰팡이",
    "비엔나 소시지": "표면이 미끈거리고 끈적이며 시큼한 냄새",
    "국산 냉동 큐브 다진마늘": "갈색·녹색 심한 변색, 톡 쏘는 쉰내 발생",
    "국산 햅쌀 백미": "바구미 벌레 발생, 쌀알 부서짐 및 곰팡이내",
    "오뚜기 고소한 참기름": "역한 기름 쩐내, 색 탁해짐 및 쓴맛 발생",
    "이금기 치킨파우더 (치킨스톡)": "습기로 딱딱하게 굳거나 곰팡이·변색 발생",
    "이금기 프리미엄 굴소스": "병 입구 흰 곰팡이, 물 분리 및 신 냄새",
    "샘표 진간장 금F": "표면 흰색 막 형성, 퀴퀴한 군내 및 침전물",
    "해찬들 고추장 & 된장": "표면 푸른·검은 곰팡이, 퀴퀴한 변질 냄새",
    "오뚜기 카놀라유/식용유": "끈적거림 심화, 역한 쩐내 및 거품 발생",
    "국산 고춧가루": "검붉은 변색, 덩어리 굳음 및 곰팡이 냄새",
    "백설 설탕 & 청정원 꽃소금": "수분 침투로 굳음, 이물질 및 벌레 유입",
    "스팸 클래식 & 동원 참치캔": "캔 팽창 및 녹 발생, 개봉 시 시큼한 악취",
    "오뚜기 토마토 케첩": "물 분리, 갈색 변색 및 톡 쏘는 신 냄새",
    "오뚜기 카레 & 짜장가루": "습기로 돌처럼 굳음 및 눅눅한 냄새",
    "오뚜기 소면 & 떡볶이 떡 & 사골육수": "떡 표면 곰팡이 발생, 사골팩 팽창 및 악취"
}

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    old_css = """.spoilage-alert {
      font-size: 0.8rem;
      color: #f87171;
      background: rgba(239, 68, 68, 0.08);
      border-radius: 6px;
      padding: 6px 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }"""

    new_css = """.spoilage-alert {
      font-size: 0.78rem;
      color: #f87171;
      background: rgba(239, 68, 68, 0.08);
      border: 1px solid rgba(239, 68, 68, 0.2);
      border-radius: 6px;
      padding: 6px 10px;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .spoilage-alert strong {
      flex-shrink: 0;
      color: #fca5a5;
    }
    .spoilage-alert span.desc {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }"""

    if old_css in content:
        content = content.replace(old_css, new_css)

    # 2. Update HTML rendering
    old_html = """          <div class="spoilage-alert">
            <span>⚠️ 상함 판별:</span> ${item.spoilage}
          </div>"""

    new_html = """          <div class="spoilage-alert" title="상함 판별: ${item.spoilage}">
            <strong>⚠️ 상함 판별:</strong> <span class="desc">${item.spoilage}</span>
          </div>"""

    if old_html in content:
        content = content.replace(old_html, new_html)

    # 3. Update spoilage values
    for name, new_spoil in new_spoilage_map.items():
        pattern = re.compile(rf'(name:\s*"{re.escape(name)}".*?spoilage:\s*")[^"]+(")', re.DOTALL)
        content = pattern.sub(rf'\g<1>{new_spoil}\g<2>', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {path}")

update_file("storage_guide.html")
try:
    update_file("snapshots/golden_state/storage_guide.html")
except Exception as e:
    print(e)
