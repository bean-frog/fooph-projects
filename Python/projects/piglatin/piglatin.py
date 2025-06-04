import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class PigLatinTranslator(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pig Latin Translator - floatme")
        self.set_default_size(400, 200)

        # Title 
        self.title = Gtk.Label()
        self.title.set_markup("<big><b>Pig Latin Translator</b></big>")

        # Setup stack and switcher
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(200)
        
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        # English to pig latin
        self.english_to_pig_latin_panel()

        # Pig Latin to english
        self.pig_latin_to_english_panel()

        # place the title, stack, and switcher
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(10)
        vbox.pack_start(self.title, False, False, 0)
        vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(self.stack, True, True, 0)
        
        self.add(vbox)

    def english_to_pig_latin_panel(self):
        # Box to hold elements
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Create and place text entry
        self.entry_en_to_pl = Gtk.Entry()
        self.entry_en_to_pl.set_placeholder_text("Enter text to translate to Pig Latin")
        vbox.pack_start(self.entry_en_to_pl, False, False, 0)

        # Create and place button, and connect it to translation function
        translate_button = Gtk.Button(label="Translate to Pig Latin")
        translate_button.connect("clicked", self.on_translate_to_pig_latin_clicked)
        vbox.pack_start(translate_button, False, False, 0)

        # Create and place output
        self.output_label_en_to_pl = Gtk.Label()
        self.output_label_en_to_pl.set_line_wrap(True)
        vbox.pack_start(self.output_label_en_to_pl, True, True, 0)

        # Add all of this to the stack
        self.stack.add_titled(vbox, "en_to_pl", "English to Pig Latin")

    def pig_latin_to_english_panel(self):
        # This function is exactly the same as the one above, except the button calls a different function
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.entry_pl_to_en = Gtk.Entry()
        self.entry_pl_to_en.set_placeholder_text("Enter text to translate to English")
        vbox.pack_start(self.entry_pl_to_en, False, False, 0)

        translate_button = Gtk.Button(label="Translate to English")
        translate_button.connect("clicked", self.on_translate_to_english_clicked)
        vbox.pack_start(translate_button, False, False, 0)

        self.output_label_pl_to_en = Gtk.Label()
        self.output_label_pl_to_en.set_line_wrap(True)
        vbox.pack_start(self.output_label_pl_to_en, True, True, 0)

        self.stack.add_titled(vbox, "pl_to_en", "Pig Latin to English")

    # Translation handler functions
    def on_translate_to_pig_latin_clicked(self, widget):
        input_text = self.entry_en_to_pl.get_text()
        translated_text = self.translate_to_pig_latin(input_text)
        self.output_label_en_to_pl.set_text(translated_text)

    def on_translate_to_english_clicked(self, widget):
        input_text = self.entry_pl_to_en.get_text()
        translated_text = self.translate_to_english(input_text)
        self.output_label_pl_to_en.set_text(translated_text)

    # Translation logic fucntions
    def translate_to_pig_latin(self, text):
        words = text.split()
        translated_words = []

        for word in words:
            if word[0].lower() in 'aeiou':
                translated_word = word + "way"
            elif len(word) > 1 and word[0].lower() not in 'aeiou' and word[1].lower() not in 'aeiou':
                translated_word = word[2:] + word[:2] + "ay"
            else:
                translated_word = word[1:] + word[0] + "ay"
            translated_words.append(translated_word.capitalize() if word[0].isupper() else translated_word.lower())

        return " ".join(translated_words)

    def translate_to_english(self, text):
        words = text.split()
        translated_words = []
        
        # Dictionary for certain cases that dont translate correctly
        edge_case_dictionary = {
            "orldway": "world",
            "eakspay": "speak",

        }
        for word in words:
            # Check if the word is in the edge case dictionary
            if word in edge_case_dictionary:
                translated_words.append(edge_case_dictionary[word])
                continue

            # General pig latin rules
            if word.endswith("way"):
                translated_word = word[:-3]
            elif word.endswith("ay"):
                translated_word = word[-3] + word[:-3]
            else:
                translated_word = word  # word unchanged if it doesnt follow expected patetrn

            translated_words.append(translated_word.capitalize() if word[0].isupper() else translated_word.lower())

        return " ".join(translated_words)

# Run 
win = PigLatinTranslator()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
