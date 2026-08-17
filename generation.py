import random

from constants import ARCHETYPES, FIRST_NAMES, LAST_NAMES, STAT_KEYS, WEIGHT_CLASSES
from models import Fighter


def generate_fighter():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    full_name = first_name + " " + last_name

    fighter_age = random.randint(18, 36)
    fighter_weight = random.choice(WEIGHT_CLASSES)
    fighter_style = random.choice(ARCHETYPES)

    fighter_stats = {}

    for stat in STAT_KEYS:
        fighter_stats[stat] = random.randint(10, 50)

    improve_archetype_stats(fighter_stats, fighter_style)

    fighter_potential = generate_potential(fighter_age)

    new_fighter = Fighter(
        full_name,
        fighter_age,
        fighter_weight,
        fighter_style,
        fighter_stats,
        fighter_potential,
    )

    return new_fighter


def improve_archetype_stats(fighter_stats, fighter_style):
    if fighter_style == "Striker":
        fighter_stats["striking"] = fighter_stats["striking"] + 10
        fighter_stats["power"] = fighter_stats["power"] + 5

    elif fighter_style == "Wrestler":
        fighter_stats["wrestling"] = fighter_stats["wrestling"] + 10
        fighter_stats["cardio"] = fighter_stats["cardio"] + 5

    elif fighter_style == "Grappler":
        fighter_stats["grappling"] = fighter_stats["grappling"] + 10
        fighter_stats["chin"] = fighter_stats["chin"] + 5

    else:
        for stat in fighter_stats:
            fighter_stats[stat] = fighter_stats[stat] + 3

    for stat in fighter_stats:
        fighter_stats[stat] = min(fighter_stats[stat], 50)


def generate_potential(fighter_age):
    if fighter_age <= 22:
        return random.randint(70, 95)

    if fighter_age <= 28:
        return random.randint(55, 85)

    return random.randint(40, 70)


def generate_scouting_group(group_size):
    fighters = []

    for number in range(group_size):
        fighter = generate_fighter()
        fighters.append(fighter)

    return fighters
