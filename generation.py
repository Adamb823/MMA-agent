import random

from constants import ARCHETYPES, FIRST_NAMES, LAST_NAMES, STAT_KEYS, WEIGHT_CLASSES
from models import Fighter


def generate_fighter():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    full_name = first_name + " " + last_name

    fighter_stats = {}

    for stat in STAT_KEYS:
        fighter_stats[stat] = random.randint(35, 75)

    fighter_age = random.randint(18, 36)
    fighter_weight = random.choice(WEIGHT_CLASSES)
    fighter_style = random.choice(ARCHETYPES)

    new_fighter = Fighter(
        full_name, fighter_age, fighter_weight, fighter_style, fighter_stats
    )

    return new_fighter

