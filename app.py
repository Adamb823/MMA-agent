import random
import tkinter as tk

# Stuff from my other files that this page needs
from constants import (
    FIGHT_LOSS_PURSE,
    FIGHT_WIN_PURSE,
    SCOUTING_GROUP_SIZE,
    STARTING_MONEY,
    STAT_KEYS,
    TRAINING_COST,
    WINS_TO_BECOME_CHAMPION,
)
from generation import generate_fighter, generate_scouting_group


class App(tk.Tk):
    def __init__(self):
        """sets up the main game window, game data and the interface widgets."""
        tk.Tk.__init__(self)

        self.title("MMA Agent - Version 6")
        self.geometry("520x950")
        self.configure(bg="#202124")
        self.resizable(False, False)

        # Colours for the game
        # I kept them here because it was easier to change them while testing
        dark_colour = "#202124"
        panel_colour = "#2b2d31"
        red_colour = "#b52b2b"
        light_colour = "#eeeeee"
        grey_colour = "#b7b7b7"

        # Main game variables
        self.scouted_fighters = generate_scouting_group(SCOUTING_GROUP_SIZE)
        self.current_fighter_number = 0
        self.shortlist = []
        self.stat_labels = {}

        self.money = STARTING_MONEY
        self.week = 1

        # V6 lets you have 3 fighters instead of only 1
        self.signed_fighters = []
        self.active_fighter = None

        # Header at the top
        top_frame = tk.Frame(self, bg="#151515", height=65)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)

        game_title = tk.Label(
            top_frame,
            text="MMA AGENT",
            bg="#151515",
            fg="white",
            font=("Arial", 20, "bold"),
        )
        game_title.pack(side="left", padx=18, pady=15)

        self.agency_label = tk.Label(
            top_frame,
            text="",
            bg="#151515",
            fg="#dddddd",
            font=("Arial", 10),
        )
        self.agency_label.pack(side="right", padx=18)

        # Main scouting area
        scouting_frame = tk.Frame(self, bg=dark_colour)
        scouting_frame.pack(fill="x", padx=18, pady=(13, 5))

        heading = tk.Label(
            scouting_frame,
            text="SCOUTING REPORT",
            bg=dark_colour,
            fg=light_colour,
            font=("Arial", 14, "bold"),
        )
        heading.pack(anchor="w")

        self.fighter_number_label = tk.Label(
            scouting_frame,
            text="",
            bg=dark_colour,
            fg=grey_colour,
            font=("Arial", 9),
        )
        self.fighter_number_label.pack(anchor="w", pady=(1, 6))

        # Fighter card
        fighter_card = tk.Frame(
            self,
            bg=panel_colour,
            highlightbackground="#444444",
            highlightthickness=1,
        )
        fighter_card.pack(fill="x", padx=18)

        self.name_label = tk.Label(
            fighter_card,
            text="",
            bg=panel_colour,
            fg="white",
            font=("Arial", 18, "bold"),
        )
        self.name_label.pack(pady=(11, 2))

        self.info_label = tk.Label(
            fighter_card,
            text="",
            bg=panel_colour,
            fg="#c7c7c7",
            font=("Arial", 10),
        )
        self.info_label.pack(pady=(0, 8))

        line = tk.Frame(fighter_card, bg="#484848", height=1)
        line.pack(fill="x", padx=16, pady=(0, 7))

        # Box that shows all of the stats
        stats_frame = tk.Frame(fighter_card, bg=panel_colour)
        stats_frame.pack(fill="x", padx=22)

        for stat_name in STAT_KEYS:
            row = tk.Frame(stats_frame, bg=panel_colour)
            row.pack(fill="x", pady=2)

            name_text = tk.Label(
                row,
                text=stat_name.capitalize(),
                width=14,
                anchor="w",
                bg=panel_colour,
                fg="#dddddd",
                font=("Arial", 10),
            )
            name_text.pack(side="left")

            number_text = tk.Label(
                row,
                text="0",
                width=4,
                bg="#18191b",
                fg="white",
                font=("Arial", 10, "bold"),
            )
            number_text.pack(side="right")

            # Saving the label means I can change the number later
            self.stat_labels[stat_name] = number_text

        rating_frame = tk.Frame(fighter_card, bg="#242529")
        rating_frame.pack(fill="x", padx=16, pady=(9, 8))

        self.overall_label = tk.Label(
            rating_frame,
            text="Overall Rating: 0",
            bg="#242529",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.overall_label.pack(side="left", padx=10, pady=7)

        self.potential_label = tk.Label(
            rating_frame,
            text="Potential: 0",
            bg="#242529",
            fg="#dddddd",
            font=("Arial", 10),
        )
        self.potential_label.pack(side="left", padx=8)

        self.value_label = tk.Label(
            fighter_card,
            text="Estimated Value: $0",
            bg=panel_colour,
            fg="#efc65a",
            font=("Arial", 11, "bold"),
        )
        self.value_label.pack(pady=(0, 9))

        # Previous and next buttons go on the same row
        browse_buttons = tk.Frame(self, bg=dark_colour)
        browse_buttons.pack(pady=(8, 3))

        previous_button = tk.Button(
            browse_buttons,
            text="< Previous",
            width=12,
            command=self.previous_fighter,
            bg="#3c3f44",
            fg="white",
            activebackground="#4a4d52",
            activeforeground="white",
            relief="flat",
        )
        previous_button.pack(side="left", padx=5)

        next_button = tk.Button(
            browse_buttons,
            text="Next >",
            width=12,
            command=self.next_fighter,
            bg="#3c3f44",
            fg="white",
            activebackground="#4a4d52",
            activeforeground="white",
            relief="flat",
        )
        next_button.pack(side="left", padx=5)

        # Scout buttons
        scout_actions = tk.Frame(self, bg=dark_colour)
        scout_actions.pack(pady=3)

        add_button = tk.Button(
            scout_actions,
            text="Add to Shortlist",
            width=16,
            command=self.add_to_shortlist,
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        add_button.pack(side="left", padx=4)

        shortlist_button = tk.Button(
            scout_actions,
            text="View Shortlist",
            width=16,
            command=self.open_shortlist_window,
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        shortlist_button.pack(side="left", padx=4)

        bottom_scout_actions = tk.Frame(self, bg=dark_colour)
        bottom_scout_actions.pack(pady=(1, 8))

        scout_button = tk.Button(
            bottom_scout_actions,
            text="Scout New Group",
            width=16,
            command=self.scout_new_group,
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        scout_button.pack(side="left", padx=4)

        sign_button = tk.Button(
            bottom_scout_actions,
            text="Sign Fighter",
            width=16,
            command=self.sign_fighter,
            bg=red_colour,
            fg="white",
            activebackground="#8f2323",
            activeforeground="white",
            relief="flat",
        )
        sign_button.pack(side="left", padx=4)

        # Agency section near the bottom
        agency_frame = tk.Frame(
            self,
            bg=panel_colour,
            highlightbackground="#444444",
            highlightthickness=1,
        )
        agency_frame.pack(fill="x", padx=18, pady=(0, 6))

        agency_heading = tk.Label(
            agency_frame,
            text="YOUR AGENCY",
            bg=panel_colour,
            fg="white",
            font=("Arial", 12, "bold"),
        )
        agency_heading.pack(anchor="w", padx=14, pady=(9, 2))

        self.roster_count_label = tk.Label(
            agency_frame,
            text="Roster: 0/3",
            bg=panel_colour,
            fg="#aaaaaa",
            font=("Arial", 9),
        )
        self.roster_count_label.pack(anchor="w", padx=14)

        self.signed_fighter_label = tk.Label(
            agency_frame,
            text="No active fighter.",
            bg=panel_colour,
            fg="#dddddd",
            font=("Arial", 10),
        )
        self.signed_fighter_label.pack(anchor="w", padx=14, pady=(3, 1))

        self.record_label = tk.Label(
            agency_frame,
            text="",
            bg=panel_colour,
            fg="#aaaaaa",
            font=("Arial", 9),
        )
        self.record_label.pack(anchor="w", padx=14, pady=(0, 5))

        # The roster button is how you swap which signed fighter you are using
        roster_button = tk.Button(
            agency_frame,
            text="View Roster / Change Fighter",
            width=25,
            command=self.open_roster_window,
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        roster_button.pack(pady=(1, 6))

        training_title = tk.Label(
            agency_frame,
            text="TRAINING",
            bg=panel_colour,
            fg="#dddddd",
            font=("Arial", 9, "bold"),
        )
        training_title.pack()

        # V6 has 3 simple training choices instead of one automatic button
        training_buttons = tk.Frame(agency_frame, bg=panel_colour)
        training_buttons.pack(pady=(3, 5))

        striking_button = tk.Button(
            training_buttons,
            text="Striking",
            width=10,
            command=lambda: self.train_fighter("striking"),
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        striking_button.pack(side="left", padx=2)

        grappling_button = tk.Button(
            training_buttons,
            text="Grappling",
            width=10,
            command=lambda: self.train_fighter("grappling"),
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        grappling_button.pack(side="left", padx=2)

        conditioning_button = tk.Button(
            training_buttons,
            text="Conditioning",
            width=10,
            command=lambda: self.train_fighter("conditioning"),
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        conditioning_button.pack(side="left", padx=2)

        training_cost_label = tk.Label(
            agency_frame,
            text="$" + format(TRAINING_COST, ",") + " per training session",
            bg=panel_colour,
            fg="#888888",
            font=("Arial", 8),
        )
        training_cost_label.pack(pady=(0, 4))

        agency_buttons = tk.Frame(agency_frame, bg=panel_colour)
        agency_buttons.pack(pady=(1, 9))

        fight_button = tk.Button(
            agency_buttons,
            text="Book Fight",
            width=14,
            command=self.book_fight,
            bg=red_colour,
            fg="white",
            activebackground="#8f2323",
            activeforeground="white",
            relief="flat",
        )
        fight_button.pack(side="left", padx=3)

        next_week_button = tk.Button(
            agency_buttons,
            text="Next Week",
            width=14,
            command=self.advance_week,
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        next_week_button.pack(side="left", padx=3)

        # Message area so the player can see what just happened
        self.message_label = tk.Label(
            self,
            text="",
            wraplength=450,
            bg=dark_colour,
            fg="#e6e6e6",
            font=("Arial", 9),
        )
        self.message_label.pack(pady=(3, 5))

        # Put the first fighter and agency details onto the screen
        self.update_fighter_display()
        self.update_agency_display()

    def get_current_fighter(self):
        """return the fighter currently being viewed in the scouting list"""
        fighter = self.scouted_fighters[self.current_fighter_number]
        return fighter

    def update_fighter_display(self):
        """update the scouting display with the current fighter information"""
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
        """uppdates the agencys display with money, roster, and active fighter details"""
        money_text = format(self.money, ",")
        top_text = "Week " + str(self.week) + " | Money: $" + money_text
        self.agency_label.config(text=top_text)

        roster_text = "Roster: " + str(len(self.signed_fighters)) + "/3"
        self.roster_count_label.config(text=roster_text)

        if self.active_fighter is None:
            self.signed_fighter_label.config(text="No active fighter.")
            self.record_label.config(text="Open the roster after signing a fighter.")
        else:
            fighter = self.active_fighter

            signed_text = "Active: " + fighter.name
            signed_text = signed_text + " | Overall " + str(fighter.get_overall())
            signed_text = signed_text + " | " + fighter.weight_class

            self.signed_fighter_label.config(text=signed_text)

            record_text = "Record: " + str(fighter.wins) + "-" + str(fighter.losses)

            if fighter.trained_this_week == True:
                record_text = record_text + " | Trained"

            if fighter.fought_this_week == True:
                record_text = record_text + " | Fought"

            self.record_label.config(text=record_text)

    def previous_fighter(self):
        """move to the previous scouted fighter and update the display"""
        self.current_fighter_number = self.current_fighter_number - 1

        # Go back to the end if the player goes past the first fighter
        if self.current_fighter_number < 0:
            self.current_fighter_number = len(self.scouted_fighters) - 1

        self.message_label.config(text="")
        self.update_fighter_display()

    def next_fighter(self):
        """move to the next scouted fighter and update the display"""
        self.current_fighter_number = self.current_fighter_number + 1

        # Go back to fighter 1 after reaching the end
        if self.current_fighter_number >= len(self.scouted_fighters):
            self.current_fighter_number = 0

        self.message_label.config(text="")
        self.update_fighter_display()

    def add_to_shortlist(self):
        """add the current fighter to the shortlist if they are not already there"""
        fighter = self.get_current_fighter()

        if fighter in self.shortlist:
            message = fighter.name + " is already shortlisted."
            self.message_label.config(text=message)
        else:
            self.shortlist.append(fighter)
            message = fighter.name + " added to shortlist."
            self.message_label.config(text=message)

    def scout_new_group(self):
        """generate a new group of fighters for the user to scout"""
        new_fighters = generate_scouting_group(SCOUTING_GROUP_SIZE)
        self.scouted_fighters = new_fighters
        self.current_fighter_number = 0

        self.message_label.config(text="A new group of fighters has been scouted.")
        self.update_fighter_display()

    def sign_fighter(self):
        """sign yhe current fighter if roster space and enough money are avalable """
        fighter = self.get_current_fighter()
        cost = fighter.get_value()

        if len(self.signed_fighters) >= 3:
            self.message_label.config(
                text="Your roster is full. You can only have 3 fighters."
            )
            return

        if fighter in self.signed_fighters:
            self.message_label.config(text="You already signed this fighter.")
            return

        if self.money < cost:
            self.message_label.config(text="You do not have enough money.")
            return

        self.signed_fighters.append(fighter)
        self.money = self.money - cost

        # First fighter signed becomes the active one automatically
        if self.active_fighter is None:
            self.active_fighter = fighter

        message = fighter.name + " has joined your agency."
        self.message_label.config(text=message)
        self.update_agency_display()

    def train_fighter(self, training_type):
        """train the current fighter in the selected training category once per week"""
        if self.active_fighter is None:
            self.message_label.config(
                text="You need to sign or select a fighter first."
            )
            return

        fighter = self.active_fighter

        if fighter.trained_this_week == True:
            self.message_label.config(text=fighter.name + " already trained this week.")
            return

        if self.money < TRAINING_COST:
            self.message_label.config(text="You do not have enough money for training.")
            return

        # Each type has 2 stats it might improve
        # I used random choice so the same training is not exactly the same every time
        if training_type == "striking":
            stat_to_train = random.choice(["striking", "power"])
        elif training_type == "grappling":
            stat_to_train = random.choice(["grappling", "wrestling"])
        else:
            stat_to_train = random.choice(["cardio", "chin"])

        improvement = 1

        # Potential now has an actual use. Better prospects have more chance of +2
        chance = random.randint(1, 100)

        if (
            fighter.potential >= 80
            and chance <= 40
            or fighter.potential >= 65
            and chance <= 25
            or fighter.potential >= 50
            and chance <= 10
        ):
            improvement = 2

        old_score = fighter.stats[stat_to_train]
        new_score = old_score + improvement

        # Stats were originally made with 50 as the max so I kept that limit
        new_score = min(new_score, 50)

        fighter.stats[stat_to_train] = new_score
        actual_improvement = new_score - old_score

        self.money = self.money - TRAINING_COST
        fighter.trained_this_week = True

        message = fighter.name + " improved " + stat_to_train
        message = message + " by " + str(actual_improvement) + " point"

        if actual_improvement != 1:
            message = message + "s"

        message = message + "."
        self.message_label.config(text=message)

        self.update_fighter_display()
        self.update_agency_display()

    def book_fight(self):
        """Book a fight for the current fighter and also uodate their record and agency money"""
        if self.active_fighter is None:
            self.message_label.config(
                text="You need to sign or select a fighter first."
            )
            return

        fighter = self.active_fighter

        if fighter.fought_this_week == True:
            self.message_label.config(text=fighter.name + " already fought this week.")
            return

        # Make a random opponent just for this fight, they don't need to be saved anywhere
        opponent = generate_fighter()

        # Add some randomness on top of the overall rating so favourites can still lose
        fighter_score = fighter.get_overall() + random.randint(-10, 10)
        opponent_score = opponent.get_overall() + random.randint(-10, 10)

        fighter.fought_this_week = True

        if fighter_score >= opponent_score:
            fighter.wins = fighter.wins + 1
            self.money = self.money + FIGHT_WIN_PURSE

            message = fighter.name + " beat " + opponent.name
            message = message + " and earned $" + format(FIGHT_WIN_PURSE, ",") + "."

            # Check for the win condition
            if fighter.wins >= WINS_TO_BECOME_CHAMPION:
                message = fighter.name
                message = message + " just became the CHAMPION! You win the game!"

        else:
            fighter.losses = fighter.losses + 1
            self.money = self.money + FIGHT_LOSS_PURSE

            message = fighter.name + " lost to " + opponent.name
            message = message + " but still made $" + format(FIGHT_LOSS_PURSE, ",")
            message = message + " in show money."

        # Fighters do not get automatically released anymore in V6
        self.message_label.config(text=message)
        self.update_agency_display()

    def advance_week(self):
        """advance a week in the game and reset weekly fighter actions """
        self.week = self.week + 1

        # Every fighter gets their training and fight back for the new week
        for fighter in self.signed_fighters:
            fighter.trained_this_week = False
            fighter.fought_this_week = False

        self.message_label.config(
            text="Week advanced. Your fighters can train and fight again."
        )
        self.update_agency_display()

    def open_roster_window(self):
        """Open a window showing all signed fighters in the agencys roster"""
        roster_window = tk.Toplevel(self)
        roster_window.title("Agency Roster")
        roster_window.geometry("480x350")
        roster_window.configure(bg="#202124")
        roster_window.resizable(False, False)

        heading = tk.Label(
            roster_window,
            text="YOUR FIGHTERS",
            bg="#202124",
            fg="white",
            font=("Arial", 14, "bold"),
        )
        heading.pack(pady=(15, 4))

        help_text = tk.Label(
            roster_window,
            text="Select a fighter to manage them, or release them from your agency.",
            bg="#202124",
            fg="#aaaaaa",
            font=("Arial", 9),
        )
        help_text.pack(pady=(0, 8))

        roster_box = tk.Listbox(
            roster_window,
            width=61,
            height=9,
            bg="#2b2d31",
            fg="white",
            selectbackground="#b52b2b",
            selectforeground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#444444",
        )
        roster_box.pack(padx=14, pady=4)

        for fighter in self.signed_fighters:
            fighter_text = fighter.name
            fighter_text = fighter_text + " | OVR " + str(fighter.get_overall())
            fighter_text = (
                fighter_text + " | " + str(fighter.wins) + "-" + str(fighter.losses)
            )
            fighter_text = fighter_text + " | " + fighter.weight_class

            if fighter == self.active_fighter:
                fighter_text = fighter_text + "  [ACTIVE]"

            roster_box.insert(tk.END, fighter_text)

        if len(self.signed_fighters) == 0:
            roster_box.insert(tk.END, "No fighters signed yet.")

        buttons = tk.Frame(roster_window, bg="#202124")
        buttons.pack(pady=10)

        select_button = tk.Button(
            buttons,
            text="Use Selected Fighter",
            width=18,
            command=lambda: self.select_roster_fighter(roster_box, roster_window),
            bg="#3c3f44",
            fg="white",
            relief="flat",
        )
        select_button.pack(side="left", padx=4)

        release_button = tk.Button(
            buttons,
            text="Release Fighter",
            width=15,
            command=lambda: self.release_fighter(roster_box, roster_window),
            bg="#b52b2b",
            fg="white",
            activebackground="#8f2323",
            activeforeground="white",
            relief="flat",
        )
        release_button.pack(side="left", padx=4)

    def select_roster_fighter(self, roster_box, roster_window):
        """set the selected roster fighter as the active fighter"""
        selected = roster_box.curselection()

        if len(selected) == 0:
            return

        selected_number = selected[0]

        if len(self.signed_fighters) == 0:
            return

        self.active_fighter = self.signed_fighters[selected_number]
        self.message_label.config(
            text=self.active_fighter.name + " is now your active fighter."
        )
        self.update_agency_display()
        roster_window.destroy()

    def release_fighter(self, roster_box, roster_window):
        """remove selected fighter from the agencys roster"""
        selected = roster_box.curselection()

        if len(selected) == 0:
            return

        selected_number = selected[0]

        if len(self.signed_fighters) == 0:
            return

        fighter = self.signed_fighters[selected_number]
        released_name = fighter.name
        self.signed_fighters.pop(selected_number)

        # If you released the active fighter just use the first fighter left
        if fighter == self.active_fighter:
            if len(self.signed_fighters) > 0:
                self.active_fighter = self.signed_fighters[0]
            else:
                self.active_fighter = None

        self.message_label.config(
            text=released_name + " was released from your agency."
        )
        self.update_agency_display()
        roster_window.destroy()

    def open_shortlist_window(self):
        """open a window showing all fighters currently shortlisted"""
        shortlist_window = tk.Toplevel(self)
        shortlist_window.title("Fighter Shortlist")
        shortlist_window.geometry("460x330")
        shortlist_window.configure(bg="#202124")
        shortlist_window.resizable(False, False)

        heading = tk.Label(
            shortlist_window,
            text="YOUR SHORTLIST",
            bg="#202124",
            fg="white",
            font=("Arial", 14, "bold"),
        )
        heading.pack(pady=(16, 8))

        shortlist_box = tk.Listbox(
            shortlist_window,
            width=58,
            height=10,
            bg="#2b2d31",
            fg="white",
            selectbackground="#b52b2b",
            selectforeground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#444444",
        )
        shortlist_box.pack(padx=16, pady=5)

        for fighter in self.shortlist:
            fighter_text = fighter.name
            fighter_text = fighter_text + " | OVR " + str(fighter.get_overall())
            fighter_text = fighter_text + " | POT " + str(fighter.potential)
            fighter_text = fighter_text + " | $" + format(fighter.get_value(), ",")

            shortlist_box.insert(tk.END, fighter_text)

        if len(self.shortlist) == 0:
            shortlist_box.insert(tk.END, "No fighters have been shortlisted yet.")

        remove_button = tk.Button(
            shortlist_window,
            text="Remove Selected Fighter",
            command=lambda: self.remove_shortlisted_fighter(shortlist_box),
            bg="#b52b2b",
            fg="white",
            activebackground="#8f2323",
            activeforeground="white",
            relief="flat",
        )
        remove_button.pack(pady=10)

    def remove_shortlisted_fighter(self, shortlist_box):
        """remove the selected fighter from the shorlist"""
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
