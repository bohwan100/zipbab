#!/usr/bin/env python3
"""
Restore Golden State Snapshot Script
Executed whenever user asks: "원래 상태로 돌려줘"
"""
import shutil
import os
import subprocess

WORKSPACE_DIR = "/Users/bohwanlee/Desktop/antigravity 폴더"
SNAPSHOT_DIR = os.path.join(WORKSPACE_DIR, "snapshots", "golden_state")
DEPLOY_DIR = "/tmp/zipbab_deploy"

FILES = [
    "cart_dashboard.html",
    "gogaek_cart.html",
    "recipe_viewer.html",
    "gogaek_recipe.html",
    "storage_guide.html",
    "index.html",
    "salad_bmi_challenge.html",
    "salad_mealprep.html",
    "server.py",
    "coupang_engine.py"
]

def restore():
    print("🔄 Restoring golden state snapshot...")
    for f in FILES:
        src = os.path.join(SNAPSHOT_DIR, f)
        dst = os.path.join(WORKSPACE_DIR, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ Restored: {f}")
            if os.path.exists(DEPLOY_DIR):
                shutil.copy2(src, os.path.join(DEPLOY_DIR, f))
    
    # Git sync deploy
    if os.path.exists(DEPLOY_DIR):
        subprocess.run(["git", "-C", DEPLOY_DIR, "commit", "-am", "revert: restore golden-v1.0-clean state"], capture_output=True)
        subprocess.run(["git", "-C", DEPLOY_DIR, "push", "origin", "main"], capture_output=True)
        print("  🚀 GitHub Pages deploy pushed!")

    # Reload Chrome tab if open
    try:
        subprocess.run([
            "osascript", "-e",
            'tell application "Google Chrome" to execute active tab of front window javascript "location.reload(true)"'
        ], capture_output=True)
        print("  🔄 Browser reloaded!")
    except Exception:
        pass

    print("🎉 Golden state successfully restored!")

if __name__ == "__main__":
    restore()
