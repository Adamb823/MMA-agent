import tkinter as tk
from tkinter import ttk

from constants import SCOUTING_GROUP_SIZE, STAT_KEYS
from generation import generate_scouting_group


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("MMA Agent - Version 2")
        self.geometry("420x650")

        self.scouted_fighters = generate_scouting_group(SCOUTING_GROUP_SIZE)
        self.current_fighter_number = 0
        self.shortlist = []
        self.stat_labels = {}

        title_label = ttk.Label(self, text="Scouting Report")
        title_label.pack(pady=(18, 4))

        self.fighter_number_label = ttk.Label(self, text="")
        self.fighter_number_label.pack()

        self.name_label = ttk.Label(self, text="")
        self.name_label.pack(pady=(8, 0))

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
        self.overall_label.pack(pady=(16, 3))

        self.potential_label = ttk.Label(self, text="Potential: 0")
        self.potential_label.pack(pady=3)

        self.value_label = ttk.Label(self, text="Estimated Value: $0")
        self.value_label.pack(pady=(3, 14))

        browse_frame = ttk.Frame(self)
        browse_frame.pack(pady=5)

        previous_button = ttk.Button(
            browse_frame, text="Previous", command=self.previous_fighter
        )
        previous_button.pack(side="left", padx=5)

        next_button = ttk.Button(browse_frame, text="Next", command=self.next_fighter)
        next_button.pack(side="left", padx=5)

        shortlist_button = ttk.Button(
            self, text="Add to Shortlist", command=self.add_to_shortlist
        )
        shortlist_button.pack(pady=5)

        view_shortlist_button = ttk.Button(
            self, text="View Shortlist", command=self.open_shortlist_window
        )
        view_shortlist_button.pack(pady=5)

        new_group_button = ttk.Button(
            self, text="Scout New Group", command=self.scout_new_group
        )
        new_group_button.pack(pady=5)

        self.message_label = ttk.Label(self, text="")
        self.message_label.pack(pady=10)

        self.update_fighter_display()

    def get_current_fighter(self):
        return self.scouted_fighters[self.current_fighter_number]

    def update_fighter_display(self):
        fighter = self.get_current_fighter()

        fighter_position = self.current_fighter_number + 1
        fighter_total = len(self.scouted_fighters)

        self.fighter_number_label.config(
            text="Fighter " + str(fighter_position) + " of " + str(fighter_total)
        )

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
        fighter_value = fighter.get_value()

        self.overall_label.config(text="Overall Rating: " + str(overall_score))
        self.potential_label.config(text="Potential: " + str(fighter.potential))
        self.value_label.config(text="Estimated Value: $" + format(fighter_value, ","))

    def previous_fighter(self):
        self.current_fighter_number = self.current_fighter_number - 1

        if self.current_fighter_number < 0:
            self.current_fighter_number = len(self.scouted_fighters) - 1

        self.message_label.config(text="")
        self.update_fighter_display()

    def next_fighter(self):
        self.current_fighter_number = self.current_fighter_number + 1

        if self.current_fighter_number >= len(self.scouted_fighters):
            self.current_fighter_number = 0

        self.message_label.config(text="")
        self.update_fighter_display()

    def add_to_shortlist(self):
        fighter = self.get_current_fighter()

        if fighter in self.shortlist:
            self.message_label.config(text=fighter.name + " is already shortlisted.")
        else:
            self.shortlist.append(fighter)
            self.message_label.config(text=fighter.name + " added to shortlist.")

    def scout_new_group(self):
        self.scouted_fighters = generate_scouting_group(SCOUTING_GROUP_SIZE)
        self.current_fighter_number = 0

        self.message_label.config(text="A new group of fighters has been scouted.")
        self.update_fighter_display()

    def open_shortlist_window(self):
        shortlist_window = tk.Toplevel(self)
        shortlist_window.title("Fighter Shortlist")
        shortlist_window.geometry("420x300")

        title_label = ttk.Label(shortlist_window, text="Your Shortlist")
        title_label.pack(pady=(16, 8))

        shortlist_box = tk.Listbox(shortlist_window, width=58, height=9)
        shortlist_box.pack(padx=16, pady=5)

        for fighter in self.shortlist:
            fighter_text = (
                fighter.name
                + " | OVR "
                + str(fighter.get_overall())
                + " | POT "
                + str(fighter.potential)
                + " | $"
                + format(fighter.get_value(), ",")
            )

            shortlist_box.insert(tk.END, fighter_text)

        if len(self.shortlist) == 0:
            shortlist_box.insert(tk.END, "No fighters have been shortlisted yet.")

        remove_button = ttk.Button(
            shortlist_window,
            text="Remove Selected Fighter",
            command=lambda: self.remove_shortlisted_fighter(shortlist_box),
        )
        remove_button.pack(pady=8)

    def remove_shortlisted_fighter(self, shortlist_box):
        selected_fighters = shortlist_box.curselection()

        if len(selected_fighters) == 0:
            return

        selected_number = selected_fighters[0]

        if len(self.shortlist) == 0:
            return

        removed_fighter = self.shortlist.pop(selected_number)
        shortlist_box.delete(selected_number)

        self.message_label.config(
            text=removed_fighter.name + " removed from shortlist."
        )
