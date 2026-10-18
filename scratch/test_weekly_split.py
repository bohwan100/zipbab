import sys
sys.path.insert(0, 'generator')
import recipe_engine

plan = recipe_engine.generate_personalized_plan(
    client_name='앙기모',
    household='1명',
    budget=500000,
    cuisine='중식'
)

print("Plan total spent:", plan["total_spent"])
print("Week totals:", plan["week_totals"])
