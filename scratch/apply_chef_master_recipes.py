import re
import sys

with open("generator/recipe_engine.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's inspect where MASTER_RECIPES starts and ends
start_idx = content.find("MASTER_RECIPES = [")
end_marker = "\ndef parse_household_count"
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not locate MASTER_RECIPES markers!")
    sys.exit(1)

print(f"Found MASTER_RECIPES from char {start_idx} to {end_idx}")
