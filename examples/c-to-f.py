import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TempConverter(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Temperature Converter - floatme")

        self.set_border_width(10)
        self.set_default_size(300, 200)

        # Create a vertical box layout
        box = Gtk.VBox(spacing=10)
        self.add(box)

        # Create an entry widget for temperature input
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter temperature")
        box.pack_start(self.entry, True, True, 0)

        # Create a ComboBox for selecting the conversion type
        self.combo = Gtk.ComboBoxText()
        self.combo.append_text("Celsius to Fahrenheit")
        self.combo.append_text("Fahrenheit to Celsius")
        self.combo.set_active(0)
        box.pack_start(self.combo, True, True, 0)

        # Create a button to perform the conversion
        self.convert_button = Gtk.Button(label="Convert")
        self.convert_button.connect("clicked", self.on_convert_clicked)
        box.pack_start(self.convert_button, True, True, 0)

        # Create a label to display the result
        self.result_label = Gtk.Label()
        box.pack_start(self.result_label, True, True, 0)

    def on_convert_clicked(self, widget):
        temp_input = self.entry.get_text()
        if not temp_input:
            self.result_label.set_text("Please enter a temperature.")
            return

        try:
            temp = float(temp_input)
        except ValueError:
            self.result_label.set_text("Invalid temperature value.")
            return

        conversion_type = self.combo.get_active_text()

        if conversion_type == "Celsius to Fahrenheit":
            result = self.celsius_to_fahrenheit(temp)
            self.result_label.set_text(f"{temp}°C is equal to {result:.2f}°F")
        elif conversion_type == "Fahrenheit to Celsius":
            result = self.fahrenheit_to_celsius(temp)
            self.result_label.set_text(f"{temp}°F is equal to {result:.2f}°C")

    def celsius_to_fahrenheit(self, celsius):
        return (celsius * 9/5) + 32

    def fahrenheit_to_celsius(self, fahrenheit):
        return (fahrenheit - 32) * 5/9

# Create and run the application
win = TempConverter()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
