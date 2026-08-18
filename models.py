class Fighter:
    def __init__(self, name, age, weight_class, archetype, stats, potential):
        self.name = name
        self.age = age
        self.weight_class = weight_class
        self.archetype = archetype
        self.stats = stats
        self.potential = potential

        # V6 stuff. Each fighter needs their own record now because the player can own 3
        self.wins = 0
        self.losses = 0
        self.trained_this_week = False
        self.fought_this_week = False

    def get_overall(self):
        total = 0

        for stat_name in self.stats:
            total = total + self.stats[stat_name]

        average = total / len(self.stats)

        return round(average)

    def get_value(self):
        overall = self.get_overall()

        value = overall * 1200
        value = value + self.potential * 500

        if self.age <= 23:
            value = value + 10000

        return value
