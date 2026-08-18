import random
import tkinter as tk
from tkinter import ttk

# Stuff from my other files that this page needs
from constants import (
    FIGHT_LOSS_PURSE,
    FIGHT_WIN_PURSE,
    LOSSES_BEFORE_RELEASE,
    SCOUTING_GROUP_SIZE,
    STARTING_MONEY,
    STAT_KEYS,
    TRAINING_COST,
    WINS_TO_BECOME_CHAMPION,
)
from generation import generate_fighter, generate_scouting_group


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("MMA Agent - Version 4")
        self.geometry("440x950")

        # Main game variables
        self.scouted_fighters = generate_scouting_group(SCOUTING_GROUP_SIZE)
        self.current_fighter_number = 0
        self.shortlist = []
        self.stat_labels = {}

        self.money = STARTING_MONEY
        self.week = 1
        self.signed_fighter = None
        self.trained_this_week = False

        # Fight night variables
        self.wins = 0
        self.losses = 0
        self.fought_this_week = False

        # Top information
        self.agency_label = ttk.Label(self, text="")
        self.agency_label.pack(pady=(16, 4))

        heading = ttk.Label(self, text="Scouting Report")
        heading.pack(pady=(8, 4))

        self.fighter_number_label = ttk.Label(self, text="")
        self.fighter_number_label.pack()

        self.name_label = ttk.Label(self, text="")
        self.name_label.pack(pady=(8, 0))

        self.info_label = ttk.Label(self, text="")
        self.info_label.pack(pady=(0, 14))

        # Box that shows all of the stats
        stats_frame = ttk.LabelFrame(self, text="Stats", padding=12)
        stats_frame.pack(fill="x", padx=24)

        for stat_name in STAT_KEYS:
            row = ttk.Frame(stats_frame)
            row.pack(fill="x", pady=2)

            name_text = ttk.Label(row, text=stat_name.capitalize(), width=12)
            name_text.pack(side="left")

            number_text = ttk.Label(row, text="0")
            number_text.pack(side="left")

            # Saving the label means I can change the number later
            self.stat_labels[stat_name] = number_text

        self.overall_label = ttk.Label(self, text="Overall Rating: 0")
        self.overall_label.pack(pady=(14, 3))

        self.potential_label = ttk.Label(self, text="Potential: 0")
        self.potential_label.pack(pady=3)

        self.value_label = ttk.Label(self, text="Estimated Value: $0")
        self.value_label.pack(pady=(3, 10))

        # Previous and next buttons go on the same row
        browse_buttons = ttk.Frame(self)
        browse_buttons.pack(pady=3)

        previous_button = ttk.Button(
            browse_buttons, text="Previous", command=self.previous_fighter
        )
        previous_button.pack(side="left", padx=5)

        next_button = ttk.Button(browse_buttons, text="Next", command=self.next_fighter)
        next_button.pack(side="left", padx=5)

        add_button = ttk.Button(
            self, text="Add to Shortlist", command=self.add_to_shortlist
        )
        add_button.pack(pady=3)

        shortlist_button = ttk.Button(
            self, text="View Shortlist", command=self.open_shortlist_window
        )
        shortlist_button.pack(pady=3)

        scout_button = ttk.Button(
            self, text="Scout New Group", command=self.scout_new_group
        )
        scout_button.pack(pady=3)

        sign_button = ttk.Button(
            self, text="Sign Current Fighter", command=self.sign_fighter
        )
        sign_button.pack(pady=(3, 12))

        # Agency section near the bottom
        agency_frame = ttk.LabelFrame(self, text="Your Agency", padding=12)
        agency_frame.pack(fill="x", padx=24)

        self.signed_fighter_label = ttk.Label(
            agency_frame, text="No fighter signed yet."
        )
        self.signed_fighter_label.pack(pady=3)

        self.record_label = ttk.Label(agency_frame, text="")
        self.record_label.pack(pady=(0, 3))

        training_text = "Train Fighter ($" + format(TRAINING_COST, ",") + ")"
        train_button = ttk.Button(
            agency_frame, text=training_text, command=self.train_fighter
        )
        train_button.pack(pady=4)

        fight_button = ttk.Button(
            agency_frame, text="Book a Fight", command=self.book_fight
        )
        fight_button.pack(pady=4)

        next_week_button = ttk.Button(
            agency_frame, text="Advance Week", command=self.advance_week
        )
        next_week_button.pack(pady=4)

        self.message_label = ttk.Label(self, text="", wraplength=390)
        self.message_label.pack(pady=12)

        # Put the first fighter and agency details onto the screen
        self.update_fighter_display()
        self.update_agency_display()

    def get_current_fighter(self):
        fighter = self.scouted_fighters[self.current_fighter_number]
        return fighter

    def update_fighter_display(self):
        fighter = self.get_current_fighter()

        current_number = self.current_fighter_number + 1
        total_fighters = len(self.scouted_fighters)

        number_message = "Fighter " + str(current_number)
        number_message = number_message + " of " + str(total_fighters)
        self.fighter_number_label.config(text=number_message)

        self.name_label.config(text=fighter.name)

        info = "Age " + str(fighter.age)
        info = info + " | " + fighter.weight_class
        info = info + " | " + fighter.archetype
        self.info_label.config(text=info)

        for stat_name in STAT_KEYS:
            score = fighter.stats[stat_name]
            label_to_change = self.stat_labels[stat_name]
            label_to_change.config(text=str(score))

        overall = fighter.get_overall()
        value = fighter.get_value()

        self.overall_label.config(text="Overall Rating: " + str(overall))
        self.potential_label.config(text="Potential: " + str(fighter.potential))
        self.value_label.config(text="Estimated Value: $" + format(value, ","))

    def update_agency_display(self):
        money_text = format(self.money, ",")
        top_text = "Week " + str(self.week) + " | Money: $" + money_text
        self.agency_label.config(text=top_text)

        if self.signed_fighter is None:
            self.signed_fighter_label.config(text="No fighter signed yet.")
            self.record_label.config(text="")
        else:
            fighter = self.signed_fighter

            signed_text = fighter.name
            signed_text = signed_text + " | Overall " + str(fighter.get_overall())
            signed_text = signed_text + " | " + fighter.weight_class

            self.signed_fighter_label.config(text=signed_text)

            record_text = "Record: " + str(self.wins) + "-" + str(self.losses)
            self.record_label.config(text=record_text)

    def previous_fighter(self):
        self.current_fighter_number = self.current_fighter_number - 1

        # Go back to the end if the player goes past the first fighter
        if self.current_fighter_number < 0:
            self.current_fighter_number = len(self.scouted_fighters) - 1

        self.message_label.config(text="")
        self.update_fighter_display()

    def next_fighter(self):
        self.current_fighter_number = self.current_fighter_number + 1

        # Go back to fighter 1 after reaching the end
        if self.current_fighter_number >= len(self.scouted_fighters):
            self.current_fighter_number = 0

        self.message_label.config(text="")
        self.update_fighter_display()

    def add_to_shortlist(self):
        fighter = self.get_current_fighter()

        if fighter in self.shortlist:
            message = fighter.name + " is already shortlisted."
            self.message_label.config(text=message)
        else:
            self.shortlist.append(fighter)
            message = fighter.name + " added to shortlist."
            self.message_label.config(text=message)

    def scout_new_group(self):
        new_fighters = generate_scouting_group(SCOUTING_GROUP_SIZE)
        self.scouted_fighters = new_fighters
        self.current_fighter_number = 0

        self.message_label.config(text="A new group of fighters has been scouted.")
        self.update_fighter_display()

    def sign_fighter(self):
        fighter = self.get_current_fighter()
        cost = fighter.get_value()

        if self.signed_fighter is not None:
            self.message_label.config(text="You already have a signed fighter.")
            return

        if self.money < cost:
            self.message_label.config(text="You do not have enough money.")
            return

        self.signed_fighter = fighter
        self.money = self.money - cost

        message = fighter.name + " has joined your agency."
        self.message_label.config(text=message)
        self.update_agency_display()

    def train_fighter(self):
        if self.signed_fighter is None:
            self.message_label.config(text="You need to sign a fighter first.")
            return

        if self.trained_this_week == True:
            self.message_label.config(
                text="Your fighter has already trained this week."
            )
            return

        if self.money < TRAINING_COST:
            self.message_label.config(text="You do not have enough money for training.")
            return

        # Start by acting like the first stat is the lowest
        lowest_stat = STAT_KEYS[0]

        # Check every stat and replace it when a lower one is found
        for stat_name in STAT_KEYS:
            current_score = self.signed_fighter.stats[stat_name]
            lowest_score = self.signed_fighter.stats[lowest_stat]

            if current_score < lowest_score:
                lowest_stat = stat_name

        old_score = self.signed_fighter.stats[lowest_stat]
        self.signed_fighter.stats[lowest_stat] = old_score + 1

        self.money = self.money - TRAINING_COST
        self.trained_this_week = True

        message = self.signed_fighter.name + " improved "
        message = message + lowest_stat + " by 1 point."
        self.message_label.config(text=message)

        self.update_fighter_display()
        self.update_agency_display()

    def book_fight(self):
        if self.signed_fighter is None:
            self.message_label.config(text="You need to sign a fighter first.")
            return

        if self.fought_this_week == True:
            self.message_label.config(text="Your fighter already fought this week.")
            return

        # Make a random opponent just for this fight, they don't need to be saved anywhere
        opponent = generate_fighter()

        # Add some randomness on top of the overall rating so favourites can still lose
        fighter_score = self.signed_fighter.get_overall() + random.randint(-10, 10)
        opponent_score = opponent.get_overall() + random.randint(-10, 10)

        self.fought_this_week = True

        if fighter_score >= opponent_score:
            self.wins = self.wins + 1
            self.money = self.money + FIGHT_WIN_PURSE

            message = self.signed_fighter.name + " beat " + opponent.name
            message = message + " and earned $" + format(FIGHT_WIN_PURSE, ",") + "."

            # Check for the win condition
            if self.wins >= WINS_TO_BECOME_CHAMPION:
                message = self.signed_fighter.name
                message = message + " just became the CHAMPION! You win the game!"

        else:
            self.losses = self.losses + 1
            self.money = self.money + FIGHT_LOSS_PURSE

            message = self.signed_fighter.name + " lost to " + opponent.name
            message = message + " but still made $" + format(FIGHT_LOSS_PURSE, ",")
            message = message + " in show money."

            # Too many losses and the fighter gets cut from the agency
            if self.losses >= LOSSES_BEFORE_RELEASE:
                released_name = self.signed_fighter.name

                self.signed_fighter = None
                self.wins = 0
                self.losses = 0

                message = (
                    released_name + " was cut from the agency after too many losses."
                )

        self.message_label.config(text=message)
        self.update_agency_display()

    def advance_week(self):
        self.week = self.week + 1
        self.trained_this_week = False
        self.fought_this_week = False

        self.message_label.config(
            text="Week advanced. Your fighter can train and fight again."
        )
        self.update_agency_display()

    def open_shortlist_window(self):
        shortlist_window = tk.Toplevel(self)
        shortlist_window.title("Fighter Shortlist")
        shortlist_window.geometry("420x300")

        heading = ttk.Label(shortlist_window, text="Your Shortlist")
        heading.pack(pady=(16, 8))

        shortlist_box = tk.Listbox(shortlist_window, width=58, height=9)
        shortlist_box.pack(padx=16, pady=5)

        for fighter in self.shortlist:
            fighter_text = fighter.name
            fighter_text = fighter_text + " | OVR " + str(fighter.get_overall())
            fighter_text = fighter_text + " | POT " + str(fighter.potential)
            fighter_text = fighter_text + " | $" + format(fighter.get_value(), ",")

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
        selected = shortlist_box.curselection()

        if len(selected) == 0:
            return

        selected_number = selected[0]

        if len(self.shortlist) == 0:
            return

        removed_fighter = self.shortlist.pop(selected_number)
        shortlist_box.delete(selected_number)

        message = removed_fighter.name + " removed from shortlist."
        self.message_label.config(text=message)
