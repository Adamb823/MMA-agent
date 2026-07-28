class Fighter:
    def __init__(self, name, age, weight_class, archetype, stats):
        self.name = name
        self.age = age
        self.weight_class = weight_class
        self.archetype = archetype
        self.stats = stats

    def get_overall(self):
        total = 0

        for stat_name in self.stats:
            total = total + self.stats[stat_name]

        average = total / len(self.stats)

        return round(average)
