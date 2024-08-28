# Python Tip Calculator
# (c) 2024 Graeme Kieran
# MIT License

# (NOTE): I'm using a Wayland based WM, and tkinter appears to not really work so I'm using GTK
# This program does the following:
# Provides a GUI with bill amount, tipping options, and number of people present
# Uses above to calculate total bill, tip amount, and splits them among all people present
# Shows the results to the user

# TODO: use CellRenderer table thing for results/fake receipt

# Import and set up necessary libraries
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class TipCalculator(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Tip Calculator")

        # vertical box to hold all the widgets
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # title
        self.title_label = Gtk.Label()
        self.title_label.set_markup('<big><b>Tip Calculator</b></big>')
        self.box.add(self.title_label)

        # grid to organize input widgets
        self.grid = Gtk.Grid()
        self.box.pack_start(self.grid, True, True, 0)

        # bill amount
        self.bill_label = Gtk.Label(label="Bill Amount:")
        self.grid.attach(self.bill_label, 0, 0, 1, 1)
        self.bill_label.set_margin_bottom(10)
        self.bill_label.set_margin_top(10)

        self.bill_entry = Gtk.Entry()
        self.bill_entry.set_placeholder_text("Enter bill amount")
        self.grid.attach(self.bill_entry, 1, 0, 1, 1)
        self.bill_entry.set_margin_bottom(10)

        # tip percentage
        self.tip_label = Gtk.Label(label="Tip Percentage:")
        self.grid.attach(self.tip_label, 0, 1, 1, 1)
        self.tip_label.set_margin_bottom(10)

        self.tip_buttons_box = Gtk.Box(spacing=6)
        self.grid.attach(self.tip_buttons_box, 1, 1, 2, 1)

        self.tip_percentages = [10, 15, 18, 20] # length of this array determines how many tip options there are
        self.tip_buttons = []

        # custom tip percentage input
        self.custom_tip_entry = Gtk.Entry()
        self.custom_tip_entry.set_placeholder_text("Custom Tip %")

        for percentage in self.tip_percentages:
            button = Gtk.Button(label=f"{percentage}%")
            button.connect("clicked", self.on_tip_button_clicked, percentage)
            self.tip_buttons_box.pack_start(button, False, False, 0)
            button.set_margin_bottom(10)
            self.tip_buttons.append(button)

        self.tip_buttons_box.pack_start(self.custom_tip_entry, False, False, 0)
        self.custom_tip_entry.set_margin_bottom(10)

        # number of people
        self.people_label = Gtk.Label(label="Number of People:")
        self.grid.attach(self.people_label, 0, 2, 1, 1)
        self.people_label.set_margin_bottom(10)

        self.people_entry = Gtk.Entry()
        self.people_entry.set_placeholder_text("Enter number of people")
        self.grid.attach(self.people_entry, 1, 2, 1, 1)
        self.people_entry.set_margin_bottom(10)

        # calculate button
        self.calculate_button = Gtk.Button(label="Calculate")
        self.calculate_button.connect("clicked", self.calculate_tip)
        self.grid.attach(self.calculate_button, 1, 3, 1, 1)
        self.calculate_button.set_margin_bottom(10)

        # results label
        self.result_label = Gtk.Label(label="")
        self.box.pack_start(self.result_label, False, False, 0)
        
        # back button (remove results, go back to original input ui)
        self.back_button = Gtk.Button(label="Back")
        self.back_button.connect("clicked", self.show_original_ui)
        self.back_button.set_margin_top(10)
        self.box.pack_end(self.back_button, False, False, 0)
        self.back_button.set_visible(False)

        # show original UI
        self.show_original_ui()

    def on_tip_button_clicked(self, widget, percentage):
        self.custom_tip_entry.set_text("")
        self.selected_tip_percentage = percentage

    def calculate_tip(self, widget):
        try:
            bill_amount = float(self.bill_entry.get_text())
            number_of_people = int(self.people_entry.get_text())
            custom_tip = self.custom_tip_entry.get_text()
            if custom_tip:
                self.selected_tip_percentage = float(custom_tip)
            else:
                self.selected_tip_percentage = self.selected_tip_percentage
        except ValueError:
            self.show_error("Invalid input. Please enter numeric values.")
            return

        if number_of_people <= 0:
            self.show_error("Number of people must be greater than zero.")
            return

        # calculate values
        tip_percentage = self.selected_tip_percentage
        tip_amount = bill_amount * tip_percentage / 100 # tip amount
        total_bill_with_tip = bill_amount + tip_amount # bill + tip
        total_tip_split = tip_amount / number_of_people # split tip
        total_bill_split = total_bill_with_tip / number_of_people # split total bill

        formatted_results = (
        f"Total Bill + Tip: <b>${total_bill_with_tip:.2f}</b>\n"
        f"Total Tip Amount: <b>${tip_amount:.2f}</b>\n"
        f"Total Bill + Tip Split Among All People: <b>${total_bill_split:.2f}</b>\n"
        f"Total Tip Split Among All People: <b>${total_tip_split:.2f}</b>"
        )
        self.show_results(formatted_results)

    def show_original_ui(self, widget=None):
        # show the original UI and hide the back button
        self.result_label.set_text("")
        self.back_button.set_visible(False)

        self.grid.show_all()

    def show_results(self, results):
        self.grid.hide()

        # Display results and back button
        self.result_label.set_markup(results)
        self.back_button.set_visible(True)

    def show_error(self, message):
        self.grid.hide()
        
        # Display error message and back button
        self.result_label.set_text(message)
        self.back_button.set_visible(True)

win = TipCalculator()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
