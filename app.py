import tkinter as tk
from tkinter import ttk

from constants import STAT_KEYS
from generation import generate_fighter


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("MMA Agent")
        self.geometry("360x440")

        self.current_fighter = generate_fighter()
        self.stat_labels = {}

        title_label = ttk.Label(self, text="Your Fighter")
        title_label.pack(pady=(18, 4))

        self.name_label = ttk.Label(self, text="")
        self.name_label.pack()

        self.info_label = ttk.Label(self, text="")
        self.info_label.pack(pady=(0, 14))

        stats_box = ttk.LabelFrame(self, text="Stats", padding=12)
        stats_box.pack(fill="x", padx=24)

        for stat in STAT_KEYS:
            stat_row = ttk.Frame(stats_box)
            stat_row.pack(fill="x", pady=2)

            stat_name_label = ttk.Label(stat_row, text=stat.capitalize(), width=12)
            stat_name_label.pack(side="left")

            stat_number_label = ttk.Label(stat_row, text="0")
            stat_number_label.pack(side="left")

            self.stat_labels[stat] = stat_number_label

        self.overall_label = ttk.Label(self, text="Overall Rating: 0")
        self.overall_label.pack(pady=16)

        scout_button = ttk.Button(
            self, text="Scout New Fighter", command=self.scout_new_fighter
        )
        scout_button.pack(pady=6)

        self.update_fighter_display()

    def update_fighter_display(self):
        fighter = self.current_fighter

        self.name_label.config(text=fighter.name)

        fighter_info = (
            "Age "
            + str(fighter.age)
            + " | "
            + fighter.weight_class
            + " | "
            + fighter.archetype
        )

        self.info_label.config(text=fighter_info)

        for stat in STAT_KEYS:
            stat_score = fighter.stats[stat]

            self.stat_labels[stat].config(text=str(stat_score))

        overall_score = fighter.get_overall()

        self.overall_label.config(text="Overall Rating: " + str(overall_score))

    def scout_new_fighter(self):
        self.current_fighter = generate_fighter()
        self.update_fighter_display()
