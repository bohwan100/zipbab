import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove dangling broken bookmarklet snippet between </header> and auto-engine-hero-banner
    # The broken snippet starts with <div class="bm-step-card"> and ends before <!-- ⚡ 원클릭
    # Pattern matching from </header> to <!-- =+ --> ... <!-- ⚡ 원클릭
    pattern_dangling = r'</header>\s*<div class="bm-step-card">.*?<!-- =+\s*-->\s*<!-- ⚡ 원클릭 1초 전자동 담기 히어로 배너 \(딸깍 모드\) -->\s*<!-- =+\s*-->\s*<div class="auto-engine-hero-banner"'
    if re.search(pattern_dangling, content, flags=re.DOTALL):
        content = re.sub(
            pattern_dangling,
            '</header>\n\n    <!-- ==============================================\n    ⚡ 원클릭 1초 전자동 담기 히어로 배너 (딸깍 모드)\n    ============================================== -->\n    <div class="auto-engine-hero-banner"',
            content,
            flags=re.DOTALL
        )
    else:
        # Broader regex
        content = re.sub(
            r'</header>[\s\S]*?<div class="auto-engine-hero-banner"',
            '</header>\n\n    <!-- ==============================================\n    ⚡ 원클릭 1초 전자동 담기 히어로 배너 (딸깍 모드)\n    ============================================== -->\n    <div class="auto-engine-hero-banner"',
            content,
            count=1
        )

    # 2. Fix duplicate `let currentBatchItems = [];` in script
    # Replace the second occurrence: `let currentBatchItems = [];` with `currentBatchItems = [];`
    # Let's find lines with `let currentBatchItems = [];`
    parts = content.split('let currentBatchItems = [];')
    if len(parts) > 2:
        # Keep first, replace subsequent with nothing
        content = parts[0] + 'let currentBatchItems = [];' + 'currentBatchItems = [];'.join(parts[1:])
    elif len(parts) == 2:
        # Only one, good!
        pass

    # 3. Check for any other redeclarations
    # Let's check `let isBatchRunning`
    parts_batch = content.split('let isBatchRunning = false;')
    if len(parts_batch) > 2:
        content = parts_batch[0] + 'let isBatchRunning = false;' + 'isBatchRunning = false;'.join(parts_batch[1:])

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {file_path}")

if __name__ == '__main__':
    fix_file('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html')
    fix_file('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html')
