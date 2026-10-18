import re

def remove_banner(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to remove the banner
    banner_pattern = r'<!-- =+\s*⚡ 원클릭 1초 전자동 담기 히어로 배너 \(딸깍 모드\)[\s\S]*?</div>\s*</div>\s*</div>'
    if re.search(banner_pattern, content):
        content = re.sub(banner_pattern, '', content)
        print(f"Removed banner by regex from {file_path}")
    else:
        # Fallback search for <div class="auto-engine-hero-banner" ... </div></div></div>
        banner_pattern2 = r'<div class="auto-engine-hero-banner" id="auto-engine-hero-banner">[\s\S]*?</div>\s*</div>\s*</div>'
        if re.search(banner_pattern2, content):
            content = re.sub(banner_pattern2, '', content)
            print(f"Removed banner by fallback from {file_path}")
        else:
            print(f"WARNING: banner not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    remove_banner('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html')
    remove_banner('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html')
