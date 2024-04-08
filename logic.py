from PyQt6.QtWidgets import *
from gui import *
import random as rnd
import csv


class Logic(QMainWindow, Ui_montyHallGame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stats = {}
        self.users = []
        self.current_user = "not logged in"
        self.player_choice = 0
        self.correct_door = 0

        self.get_information()

        self.tab_current.setCurrentIndex(0)
        self.label.setText("")

        self.button_login.clicked.connect(lambda: self.login())
        self.button_register.clicked.connect(lambda: self.register())
        self.button_moveToGame.clicked.connect(lambda: self.change_to_game())
        self.button_game_next.clicked.connect(lambda: self.change_to_stats())
        self.button_game_back.clicked.connect(lambda: self.change_to_main())
        self.button_stats_back.clicked.connect(lambda: self.change_to_game())
        self.button_submit.clicked.connect(lambda: self.get_door())
        self.button_stay.clicked.connect(lambda: self.stay_resolve())
        self.button_Switch.clicked.connect(lambda: self.switch_resolve())

        self.button_stay.hide()
        self.button_Switch.hide()

    def get_information(self):
        self.stats = {}
        with open("stats.csv", "r") as stats_file:
            first_line = True
            for line in stats_file:
                if first_line:
                    first_line = False
                else:
                    line = line.strip().split(",")
                    self.stats[line[0]] = [line[1], line[2], line[3]]
                    self.users.append(line[0])

    def login(self):
        self.label_login_status.clear()
        username = self.entry_username.text()
        if username == "":
            self.label_login_status.setText(f"Please enter a username to continue")
        elif username in self.users:
            self.current_user = username
            self.label_login_status.setText(f"You have successfully logged in as {username}.")
        else:
            self.label_login_status.setText(f"If you are a new user, click Register\n"
                                            f"If you are returning, make sure you "
                                            f"are using the same username as last time")

    def register(self):
        username = self.entry_username.text()
        if username == "":
            self.label_login_status.setText(f"Please enter a username to continue")
        elif username == "anonymous":
            self.label_login_status.setText(f"This username is reserved for those who want to play anonymously")
        elif username not in self.users:
            self.current_user = username
            self.label_login_status.setText(f"You have successfully registered the username {username}."
                                            f"\nYou may not press the play button to continue on.")
        else:
            self.label_login_status.setText(f"This user is already registered."
                                            f"\nTry using a different name or adding numbers to the end of yours")

    def change_to_main(self):
        self.tab_current.setCurrentIndex(0)

    def change_to_game(self):
        self.tab_current.setCurrentIndex(1)

    def change_to_stats(self):
        self.tab_current.setCurrentIndex(2)

    def get_door(self):
        if self.radioButton_door_1.isChecked():
            self.player_choice = 1
            self.play_game()
        elif self.radioButton_door_2.isChecked():
            self.player_choice = 2
            self.play_game()
        elif self.radioButton_door_3.isChecked():
            self.player_choice = 3
            self.play_game()
        else:
            self.label.setText("Chose a door")

    def play_game(self):
        self.correct_door = rnd.randint(1, 3)
        open_door = [1, 2, 3]
        open_door.remove(self.correct_door)

        if self.player_choice in open_door:  # Player did not choose winning door
            open_door.remove(self.player_choice)
            opened_door = open_door[0]
        elif self.player_choice not in open_door:
            opened_door = open_door[rnd.randint(0, 1)]

        self.label.setText(f"Door {opened_door} is now opened and does not contain the prize"
                           f"\nWould you like to stay on your current selection or switch doors?")
        self.button_stay.show()
        self.button_Switch.show()

    def stay_resolve(self):
        self.button_stay.hide()
        self.button_Switch.hide()

        if self.correct_door == 0:
            self.get_door()
        elif self.correct_door == self.player_choice:
            self.stats[self.current_user][0] += 1
            self.stats[self.current_user][1] += 1
            self.button_clear()
        elif self.correct_door != self.player_choice:
            self.stats[self.current_user][0] += 1
            self.button_clear()

        self.textbrowser_stats.setText(self.stats)


    def switch_resolve(self):
        self.button_stay.hide()
        self.button_Switch.hide()

        if self.correct_door == 0:
            self.get_door()
        elif self.correct_door != self.player_choice:
            self.stats[self.current_user][0] += 1
            self.stats[self.current_user][2] += 1
            self.button_clear()
        elif self.correct_door == self.player_choice:
            self.stats[self.current_user][0] += 1
            self.button_clear()

        self.textbrowser_stats.setText(self.stats)

    def button_clear(self):
        if self.radioButton_door_1.isChecked():
            self.radioButton_door_1.nextCheckState()
            self.label.setText("")
        elif self.radioButton_door_2.isChecked():
            self.radioButton_door_2.nextCheckState()
            self.label.setText("")
        elif self.radioButton_door_3.isChecked():
            self.radioButton_door_3.nextCheckState()
            self.label.setText("")

#
# def read_stats():
#     stats = {}
#     with open("stats.csv", "r") as stats_file:
#         for line in stats_file:
#             line = line.strip()
#             stats[line[0]] = [line[1], line[2], line[3]]
#     return stats
#
# def write_stats(stats_dict):
#     with open("stats.csv", "w") as stats_file:
#         content = csv.writer(stats_file)
#         content.writerow(['User', 'Total Games Played', 'Stay Wins', 'Switch Wins'])
#         for user, stats in stats_dict.items:
#             content.writerow([user, stats[0], stats[1], stats[3]])
