import os
import glob
import re

TARGET_FILES = [
    "cart_dashboard.html",
    "recipe_viewer.html",
    "storage_guide.html",
    "gogaek_cart.html",
    "gogaek_recipe.html",
    "templates/cart.html",
    "templates/recipes.html",
    "templates/storage.html"
] + glob.glob("clients/*/*.html")

OLD_HOVER_PATTERN = re.compile(
    r'\.nav-btn:hover\s*\{\s*\.nav-btn\.recipe:hover:not\(\.active\)',
    re.MULTILINE
)

CSS_REPLACEMENT = """    .nav-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.25);
    }
    .nav-btn.recipe:hover:not(.active) {
      border-color: rgba(249, 115, 22, 0.5);
      color: #fb923c;
      background: rgba(249, 115, 22, 0.1);
    }
    .nav-btn.cart:hover:not(.active) {
      border-color: rgba(56, 189, 248, 0.5);
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.1);
    }
    .nav-btn.storage:hover:not(.active) {
      border-color: rgba(52, 211, 153, 0.5);
      color: #34d399;
      background: rgba(52, 211, 153, 0.1);
    }
    /* 3대 핵심 서비스 버튼 활성화 (주황색, 파란색, 초록색) */
    .nav-btn.orange.active, .nav-btn.recipe.active {
      background: linear-gradient(135deg, #f97316, #ea580c);
      color: #fff !important;
      border-color: transparent;
      box-shadow: 0 4px 14px rgba(249, 115, 22, 0.45);
    }
    .nav-btn.orange.active:hover, .nav-btn.recipe.active:hover {
      background: linear-gradient(135deg, #ea580c, #c2410c);
      transform: translateY(-1px);
    }
    .nav-btn.blue.active, .nav-btn.cart.active, .nav-btn.cyan.active {
      background: linear-gradient(135deg, #0284c7, #0ea5e9);
      color: #fff !important;
      border-color: transparent;
      box-shadow: 0 4px 14px rgba(14, 165, 233, 0.45);
    }
    .nav-btn.blue.active:hover, .nav-btn.cart.active:hover, .nav-btn.cyan.active:hover {
      background: linear-gradient(135deg, #0369a1, #0284c7);
      transform: translateY(-1px);
    }
    .nav-btn.green.active, .nav-btn.storage.active {
      background: linear-gradient(135deg, #10b981, #059669);
      color: #fff !important;
      border-color: transparent;
      box-shadow: 0 4px 14px rgba(16, 185, 129, 0.45);
    }
    .nav-btn.green.active:hover, .nav-btn.storage.active:hover {
      background: linear-gradient(135deg, #059669, #047857);
      transform: translateY(-1px);
    }"""

fixed_count = 0
for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Fix the broken .nav-btn:hover syntax if present
    if OLD_HOVER_PATTERN.search(content):
        content = OLD_HOVER_PATTERN.sub(
            """.nav-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.25);
    }
    .nav-btn.recipe:hover:not(.active)""",
            content
        )
        modified = True

    # 2. Upgrade the blue active style to vibrant #0284c7 -> #0ea5e9
    if "linear-gradient(135deg, #0284c7, #0369a1)" in content:
        content = content.replace(
            "linear-gradient(135deg, #0284c7, #0369a1)",
            "linear-gradient(135deg, #0284c7, #0ea5e9)"
        )
        content = content.replace(
            "box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4)",
            "box-shadow: 0 4px 14px rgba(14, 165, 233, 0.45)"
        )
        content = content.replace(
            "linear-gradient(135deg, #0369a1, #075985)",
            "linear-gradient(135deg, #0369a1, #0284c7)"
        )
        modified = True

    if modified:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        fixed_count += 1
        print(f"[OK] Fixed CSS in: {fpath}")

print(f"Total files updated: {fixed_count}")
