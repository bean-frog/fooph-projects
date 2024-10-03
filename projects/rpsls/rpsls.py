# Rock Paper Scissors Lizard Spock 
# (c) 2024 Graeme Kieran
# MIT License

# description:
# This program allows the user to play a continuation of Rock Paper Scissors that includes two new moves
# The program has a GUI created with GTK that will match the user's selected GTK3 theme.
# The normal gamemode has buttons to select a move
# There is a harder gamemode that requires the user to write code in an esoteric language to play


import gi
import random

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Pango

# map numbers to names for future reference
moves = {
    1: "rock",
    2: "spock",
    3: "paper",
    4: "lizard",
    5: "scissors"
}
# I had this idea at 1 AM and i can't decide if it's genius or incredibly dumb
moves_bf_translations = {
    "rock": "++++++++++[>+++++++++++>+++++++++++>++++++++++>+++++++++++<<<<-]>++++.>+.>-.>---.",
    "spock": "++++++++++[>++++++++++++>+++++++++++>+++++++++++>++++++++++>+++++++++++<<<<<-]>-----.>++.>+.>-.>---.",
    "paper": "++++++++++[>+++++++++++>++++++++++>+++++++++++>++++++++++>+++++++++++<<<<<-]>++.>---.>++.>+.>++++.",
    "lizard": "++++++++++[>+++++++++++>+++++++++++>++++++++++++>++++++++++>+++++++++++>++++++++++<<<<<<-]>--.>-----.>++.>---.>++++.>.",
    "scissors": "++++++++++[>++++++++++++>++++++++++>+++++++++++>++++++++++++>+++++++++++>+++++++++++>++++++++++++<<<<<<<-]>-----.>-.>-----.>-----..>+.>++++.>-----."
}

# function to calculate the result
def calculate_win(pMove, cMove):
    return ((pMove - cMove) + 5) % 5

class GameWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="RPSLS - floatme")
        self.set_default_size(400, 600)
        self.set_border_width(10)

        # stuff to keep track of
        self.player_score = 0
        self.computer_score = 0
        self.is_brainfuck_mode = False  

        # stack stores all screens
        self.stack = Gtk.Stack()
        self.add(self.stack)

        # start screen
        self.start_box = Gtk.VBox(spacing=10)
        self.start_label = Gtk.Label()
        self.start_label.set_markup(
            "<b><big>Welcome to Rock-Paper-Scissors-Lizard-Spock!</big></b>\n\n"
            "<big><b>Rules:</b></big>\n"
            "<b>Rock</b> crushes <b>Scissors</b>, <b>Scissors</b> cuts <b>Paper</b>,\n"
            "<b>Paper</b> covers <b>Rock</b>, <b>Rock</b> crushes <b>Lizard</b>,\n"
            "<b>Lizard</b> poisons <b>Spock</b>, <b>Spock</b> smashes <b>Scissors</b>,\n"
            "<b>Scissors</b> decapitates <b>Lizard</b>, <b>Lizard</b> eats <b>Paper</b>,\n"
            "<b>Paper</b> disproves <b>Spock</b>, <b>Spock</b> vaporizes <b>Rock</b>.\n\n"
            "<big><b>How to play (normal mode):</b></big>\n"
            "You'll see text that says 'Rock, Paper, Scissors, SHOOT', and some buttons for each move.\n"
            "The buttons will become pressable when the above text reaches 'SHOOT'\n\n"
            "<big><b>How to play (hard mode):\n</b></big>"
            "Rather than buttons for selecting a move, you'll have to write a valid program in the esoteric programming language Brainf**k. This program must return one of the following: 'rock', 'paper', 'scissors', 'lizard', or 'spock'.\n"
            "<a href='https://brainfuck.org/brainfuck.html'>here</a> is the documentation for Brainf**k.\n"
            "if you want to cheat, use <a href='https://md5decrypt.net/en/Brainfuck-translator/'>this</a>\n"
            "Good luck!"
        )
        self.start_label.set_line_wrap(True)

        self.start_box.pack_start(self.start_label, True, True, 0)

        self.start_button = Gtk.Button(label="Start Game (Normal)")
        self.start_button.set_size_request(150, 50)  
        self.start_button.connect("clicked", self.on_start_button_clicked)
        self.start_box.pack_start(self.start_button, False, False, 0)

        self.start_button_bf = Gtk.Button(label="Start Game (Hard)")
        self.start_button_bf.set_size_request(150, 50) 
        self.start_button_bf.connect("clicked", self.on_bf_start_button_clicked)
        self.start_box.pack_start(self.start_button_bf, False, False, 0)

        

        # game screen (normal mode)
        self.game_box = Gtk.VBox(spacing=10)

        # score label 
        self.score_label = Gtk.Label()
        self.update_score_label()  # Initialize the score label with 0:0
        self.score_label.set_justify(Gtk.Justification.CENTER)
        self.score_label.set_halign(Gtk.Align.CENTER) 
        self.game_box.pack_start(self.score_label, False, False, 0)

        self.countdown_label = Gtk.Label(label="")
        self.countdown_label.modify_font(Pango.FontDescription("Sans 30"))  # this method is deprecated but its easy and it works
        self.game_box.pack_start(self.countdown_label, True, True, 0)

        # buttons to select move
        self.button_box = Gtk.HBox(spacing=10)
        self.buttons = {}
        for i in range(1, 6):
            button = Gtk.Button(label=moves[i].capitalize())
            button.set_size_request(80, 40) 
            button.connect("clicked", self.on_move_button_clicked, i)
            button.set_sensitive(False)  # disable buttons
            self.buttons[i] = button
            self.button_box.pack_start(button, True, True, 0)

        self.game_box.pack_start(self.button_box, False, False, 0)

        # game screen (Brainf**k Mode)
        self.bf_game_box = Gtk.VBox(spacing=10)

        self.bf_instructions = Gtk.Label(label="Enter a Brainf**k program to select your move.")
        self.bf_game_box.pack_start(self.bf_instructions, False, False, 0)

        self.bf_entry = Gtk.Entry()
        self.bf_game_box.pack_start(self.bf_entry, False, False, 0)

        self.bf_submit_button = Gtk.Button(label="Submit")
        self.bf_submit_button.connect("clicked", self.on_bf_submit_clicked)
        self.bf_game_box.pack_start(self.bf_submit_button, False, False, 0)

        # invalid bf code label
        self.bf_error_label = Gtk.Label(label="")
        self.bf_error_label.set_no_show_all(True)
        self.bf_game_box.pack_start(self.bf_error_label, False, False, 0)

        # result screen 
        self.result_box = Gtk.VBox(spacing=10)
        self.result_label = Gtk.Label(label="")
        self.result_box.pack_start(self.result_label, True, True, 0)

        # box to hold menu/quit buttons
        self.result_button_box = Gtk.HBox(spacing=10)

        # menu button
        self.main_menu_button = Gtk.Button(label="Main Menu")
        self.main_menu_button.set_size_request(150, 50) 
        self.main_menu_button.connect("clicked", self.on_main_menu_button_clicked)
        self.result_button_box.pack_start(self.main_menu_button, True, True, 0)

        # quit button
        self.exit_button = Gtk.Button(label="Quit")
        self.exit_button.set_size_request(150, 50)  
        self.exit_button.connect("clicked", self.on_exit_button_clicked)
        self.result_button_box.pack_start(self.exit_button, True, True, 0)

        self.result_box.pack_start(self.result_button_box, False, False, 0)

        # play again button
        self.play_again_button = Gtk.Button(label="Play Again")
        self.play_again_button.set_size_request(150, 50)  
        self.play_again_button.connect("clicked", self.on_play_again_button_clicked)
        self.result_box.pack_start(self.play_again_button, False, False, 0)

        # add all screens to stack
        self.stack.add_titled(self.start_box, "start", "Start Screen")
        self.stack.add_titled(self.game_box, "game", "Game Screen")
        self.stack.add_titled(self.bf_game_box, "bf_game", "Brainf**k Game Screen")
        self.stack.add_titled(self.result_box, "result", "Result Screen")

        # show starting screen
        self.stack.set_visible_child(self.start_box)

    # re-renders score label when called
    def update_score_label(self):
        score_text = f"[You] <span size='20000'>{self.player_score}:{self.computer_score}</span> [Computer]"
        self.score_label.set_markup(score_text)

    def on_start_button_clicked(self, widget):
        # switch to game screen and start the countdown sequence
        self.is_brainfuck_mode = False # force reset game
        self.stack.set_visible_child(self.game_box)
        GLib.timeout_add(500, self.show_countdown, ["rock", "paper", "scissors", "SHOOT!"]) 

    def on_bf_start_button_clicked(self, widget):
        # switch mode
        self.is_brainfuck_mode = True
        self.stack.set_visible_child(self.bf_game_box)

    def show_countdown(self, countdown_steps):
        if countdown_steps:
            self.countdown_label.set_text(countdown_steps.pop(0))
            return True
        else:
            # countdown done, clear the label and enable the move buttons
            self.countdown_label.set_text("")
            self.button_box.show_all()
            for button in self.buttons.values():
                button.set_sensitive(True)
            return False

    # [[[GAME LOGIC IS HERE!!! (normal mode)]]]
    def on_move_button_clicked(self, widget, player_move):
        # hide buttons
        self.button_box.hide()

        # randomly choose a move for computer
        computer_move = random.randint(1, 5)

        # get result from the magic algorithm
        result = calculate_win(player_move, computer_move)

        if result == 0:
            result_text = "It's a tie!"
        elif result in [1, 2]:
            result_text = "You win! You chose {} and the computer chose {}.".format(
                moves[player_move], moves[computer_move]
            )
            self.player_score += 1 
        else:
            result_text = "You lose! You chose {} and the computer chose {}.".format(
                moves[player_move], moves[computer_move]
            )
            self.computer_score += 1

        # update score
        self.update_score_label()

        # show result screen
        self.result_label.set_text(result_text)
        self.stack.set_visible_child(self.result_box) # side note I absolutely LOVE that gtk lets you put a bunch of screens in a stack and have just 1 function to switch

    # [[[GAME LOGIC IS HERE!!!!! (brainfk mode)]]]
    def on_bf_submit_clicked(self, widget):
        bf_code = self.bf_entry.get_text()
        player_move = None

        # check user's code 
        # i thought about writing an actual interpreter and then I remembered that it's 1:30 AM and i need sleep
        for move, bf_translation in moves_bf_translations.items():
            if bf_code == bf_translation:
                player_move = list(moves.keys())[list(moves.values()).index(move)]
                break

        if player_move:
            # computer move
            computer_move = random.randint(1, 5)

            # consult magic algorithm genie once more
            result = calculate_win(player_move, computer_move)

            if result == 0:
                result_text = "It's a tie!"
            elif result in [1, 3]:
                result_text = "You win! You chose {} and the computer chose {}.".format(
                    moves[player_move], moves[computer_move]
                )
                self.player_score += 1 
            else:
                result_text = "You lose! You chose {} and the computer chose {}.".format(
                    moves[player_move], moves[computer_move]
                )
                self.computer_score += 1 

            # update score label
            self.update_score_label()

            # show result screen
            self.result_label.set_text(result_text)
            self.stack.set_visible_child(self.result_box)
        else:
            # invalid/non matching brainfk code
            self.bf_error_label.set_text("Invalid Brainf**k code! Please try again.")
            self.bf_error_label.show()

    def on_play_again_button_clicked(self, widget):
        # reset game
        if self.is_brainfuck_mode:
            self.bf_entry.set_text("")  # clear brainfk entry field
            self.bf_error_label.hide()  # hide error label
            self.stack.set_visible_child(self.bf_game_box) # ensure correct mode is showing
        else:
            self.button_box.show_all()  # show regular mode buttons
            for button in self.buttons.values():
                button.set_sensitive(False)  # disable buttons
            self.stack.set_visible_child(self.game_box)  # ensure correct mode is showing
            GLib.timeout_add(500, self.show_countdown, ["rock", "paper", "scissors", "SHOOT!"])
    def on_main_menu_button_clicked(self, widget):
    # back to main menu
        self.stack.set_visible_child(self.start_box)

    def on_exit_button_clicked(self, widget):
        Gtk.main_quit()

win = GameWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
