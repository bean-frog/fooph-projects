import pygame
import gi
import random

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

pygame.display.init()
pygame.font.init()

# Words for the game
words = [
    "python",
    "javascript",
    "erlang",
    "perl",
    "typescript",
    "swift",
    "objective-c",
    "haskell",
    "racket",
    "actionscript",
    "basic",
    "assembly",
    "fortran",
    "elixir",
    "vbscript",
    "kotlin",
    "clojure",
    "julia",
    "dart",
    "nodejs",
    "express",
    "react",
    "gleam",
    "apache",
    "suckless",
    "kernel.org",
    "ocaml",
    "flutter",
    "tailwind"

]

word_cache = []  # stores past words to avoid repeats
part_names = ["head", "armR", "armL", "body", "legL", "legR"]  # valid body part names
used_parts = []  # keep track of which body parts have already been added


class Hangman(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hangman - floatme")
        self.set_default_size(900, 500)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(200)
        self.add(self.stack)

        self.create_start_screen()

        game_screen = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Pygame drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(400, 500)
        game_screen.pack_start(self.drawing_area, True, True, 0)

        self.drawing_area.connect("draw", self.on_draw)

        # word display and keyboard
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        game_screen.pack_start(right_box, True, True, 0)

        # Select  random word
        self.secret_word = self.get_new_word()
        self.displayed_word = self.obfuscate_word(self.secret_word)

        self.word_label = Gtk.Label()
        self.update_displayed_word_label(self.displayed_word)
        right_box.pack_start(self.word_label, False, False, 10)

        # qwerty keypad
        self.letter_buttons = {}
        letters_box = Gtk.Grid()

        letters_box.set_hexpand(True)
        letters_box.set_vexpand(True)

        qwerty_rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for row_index, row in enumerate(qwerty_rows):
            for col_index, letter in enumerate(row):
                button = Gtk.Button(label=letter)
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
                button.set_valign(Gtk.Align.FILL)
                button.connect("clicked", self.on_letter_click, letter)
                letters_box.attach(button, col_index, row_index, 1, 1)
                self.letter_buttons[letter] = button
        right_box.pack_start(letters_box, True, True, 10)


        self.stack.add_named(game_screen, "game_screen")
        self.create_end_screens()
        self.stack.set_visible_child_name("start_screen")
        self.body_parts = []  # initialize state

    
    def create_start_screen(self): 
        start_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        welcome_label = Gtk.Label(label="Welcome to Hangman!")
        welcome_label.set_markup("<big><b>Welcome to Hangman!</b></big>")
        start_box.pack_start(welcome_label, True, True, 10)

        instructions_label = Gtk.Label(
            label="Try to guess the word by selecting letters. Incorrect guesses add parts to the hangman!"
        )
        start_box.pack_start(instructions_label, True, True, 10)

        start_button = Gtk.Button(label="Start Game")
        start_button.connect("clicked", lambda _: self.stack.set_visible_child_name("game_screen"))
        start_box.pack_start(start_button, False, False, 5)

        self.stack.add_named(start_box, "start_screen")

    def create_end_screens(self):
        # Win Screen
        win_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        win_label = Gtk.Label(label="You Won!")
        win_box.pack_start(win_label, True, True, 10)

        new_game_button_win = Gtk.Button(label="New Game")
        new_game_button_win.connect("clicked", self.start_new_game)
        win_box.pack_start(new_game_button_win, False, False, 5)

        exit_button_win = Gtk.Button(label="Exit")
        exit_button_win.connect("clicked", Gtk.main_quit)
        win_box.pack_start(exit_button_win, False, False, 5)

        self.stack.add_named(win_box, "win_screen")

        # Lose Screen
        lose_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        lose_label = Gtk.Label()
        lose_label.set_name("lose_label")  # Name the label for dynamic updating
        lose_box.pack_start(lose_label, True, True, 10)

        new_game_button_lose = Gtk.Button(label="New Game")
        new_game_button_lose.connect("clicked", self.start_new_game)
        lose_box.pack_start(new_game_button_lose, False, False, 5)

        exit_button_lose = Gtk.Button(label="Exit")
        exit_button_lose.connect("clicked", Gtk.main_quit)
        lose_box.pack_start(exit_button_lose, False, False, 5)

        self.stack.add_named(lose_box, "lose_screen")

    def on_draw(self, widget, cr):
        self.draw_hangman(cr)

    def draw_hangman(self, cr):
        width = self.drawing_area.get_allocated_width()
        height = self.drawing_area.get_allocated_height()

        surface = pygame.Surface((width, height))
        surface.fill((255, 255, 255))  # White background

        base_x, base_y = width // 2, height // 4
        part_draw_methods = {
            "head": lambda: pygame.draw.circle(surface, (0, 0, 0), (base_x, base_y), 30, 2),
            "body": lambda: pygame.draw.line(surface, (0, 0, 0), (base_x, base_y + 30), (base_x, base_y + 100), 2),
            "armR": lambda: pygame.draw.line(surface, (0, 0, 0), (base_x, base_y + 50), (base_x + 50, base_y + 80), 2),
            "armL": lambda: pygame.draw.line(surface, (0, 0, 0), (base_x, base_y + 50), (base_x - 50, base_y + 80), 2),
            "legR": lambda: pygame.draw.line(surface, (0, 0, 0), (base_x, base_y + 100), (base_x + 30, base_y + 150), 2),
            "legL": lambda: pygame.draw.line(surface, (0, 0, 0), (base_x, base_y + 100), (base_x - 30, base_y + 150), 2),
        }

        for part in self.body_parts:
            draw_method = part_draw_methods.get(part)
            if draw_method:
                draw_method()

        data = pygame.image.tostring(surface, "RGB", False)
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            data, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width * 3
        )

        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()

    def get_new_word(self):
        available_words = [w for w in words if w not in word_cache]
        if not available_words:
            word_cache.clear()
            available_words = words
        word = random.choice(available_words)
        word_cache.append(word)
        return word

    def obfuscate_word(self, word):
        return ''.join('_' if char.isalpha() else char for char in word)

    def update_displayed_word_label(self, displayed_word):
        spaced_word = " ".join(displayed_word)
        self.word_label.set_markup(f'<span size="15pt" stretch="expanded">{spaced_word}</span>')

    def on_letter_click(self, button, letter):
        button.set_sensitive(False)
        if letter.lower() in self.secret_word.lower():
            self.update_displayed_word(letter)
        else:
            self.add_body_part()
            self.on_draw()

    def update_displayed_word(self, letter):
        updated_word = ''.join(
            letter if letter.lower() == self.secret_word[i].lower() else self.displayed_word[i]
            for i in range(len(self.secret_word))
        )
        self.displayed_word = updated_word
        self.update_displayed_word_label(self.displayed_word)
        if '_' not in self.displayed_word:
            self.show_screen("win_screen")

    def add_body_part(self):
        for part in part_names:
            if part not in used_parts:
                used_parts.append(part)
                self.body_parts.append(part)
                break
        self.drawing_area.queue_draw()
        if len(used_parts) >= len(part_names):
            self.show_screen("lose_screen")

    def show_screen(self, screen_name):
        if screen_name == "lose_screen":
            lose_label = self.stack.get_child_by_name("lose_screen").get_children()[0]
            lose_label.set_text(f"Game Over! The word was '{self.secret_word}'")
        self.stack.set_visible_child_name(screen_name)

    def start_new_game(self, button):
        self.secret_word = self.get_new_word()
        self.displayed_word = self.obfuscate_word(self.secret_word)
        self.update_displayed_word_label(self.displayed_word)
        self.body_parts.clear()
        used_parts.clear()
        for button in self.letter_buttons.values():
            button.set_sensitive(True)
        self.stack.set_visible_child_name("game_screen")


win = Hangman()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
