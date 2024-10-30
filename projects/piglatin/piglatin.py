import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class PigLatin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pig Latin Translator - floatme")
        self.set_default_size(400, 200)

        # Vertical Box to arrange widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(10)
        self.add(vbox)

        # Input text entry
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter text to translate to Pig Latin")
        vbox.pack_start(self.entry, False, False, 0)

        # Translate button
        self.translate_button = Gtk.Button(label="Translate")
        self.translate_button.connect("clicked", self.on_translate_clicked)
        vbox.pack_start(self.translate_button, False, False, 0)

        # Frame for output
        self.output_label = Gtk.Label()
        self.output_label.set_line_wrap(True)
        self.output_label.set_ellipsize(Pango.EllipsizeMode.END)
        vbox.pack_start(self.output_label, True, True, 0)

    def on_translate_clicked(self, widget):
        input_text = self.entry.get_text()
        translated_text = self.translate_to_pig_latin(input_text)
        self.output_label.set_text(translated_text)

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

#run
win = PigLatin()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
