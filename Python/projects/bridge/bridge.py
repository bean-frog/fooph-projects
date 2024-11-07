import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

# Suits as unicode glyphs
suits = {
    "hearts": "\u2665",         
    "clubs": "\u2663",     
    "spades": "\u2660",
    "diamonds": "\u2666"
}

hand = [] 


class BridgeCounter(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Bridge Hand Calculator - floatme")
        self.set_default_size(400, 600)

        # Title
        self.title = Gtk.Label()
        self.title.set_markup("<big><b>Bridge Hand Calculator</b></big>")

        # Stack and stack switcher
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(200)
        
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        # Initialize panels
        self.info_panel()
        self.input_panel()

        # Main layout box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(10)
        vbox.pack_start(self.title, False, False, 0)
        vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(self.stack, True, True, 0)

        self.add(vbox)

        # state variables
        self.selected_face = None
        self.selected_suit = None

    # Information 
    def info_panel(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.info_label = Gtk.Label()
        self.info_label.set_markup("""
        <b>How to use this calculator</b>\n
        Using the buttons, select the suit and face/number for each card in your hand.\n
        Each card in your hand is represented by buttons,\n which you can click to remove if you made a mistake.\n
        Press "Calculate" to show your hand's score.\n
        """)
        vbox.pack_start(self.info_label, False, False, 0)
        self.stack.add_titled(vbox, "info", "Info")
    
    # Hand input
    def input_panel(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.face_num_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.suits_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        
        self.of_label = Gtk.Label()
        self.of_label.set_markup("<span size='20pt'>of</span>")

        # face selection buttons
        for item in ["jack", "king", "queen", "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            label = Gtk.Label()
            label.set_markup(f"<span size='15pt'>{item}</span>")
            button = Gtk.Button()
            button.add(label)
            button.connect('clicked', lambda widget, item=item: self.select_face(item))
            self.face_num_box.pack_start(button, True, True, 0)

        # suit selection buttons
        for suit in suits:
            label_content = suits[suit]  # get unicode for suit
            label = Gtk.Label()
            label.set_markup(f"<span size='40pt'>{label_content}</span>")
            button = Gtk.Button()
            button.add(label)
            button.connect('clicked', lambda widget, suit=suit: self.select_suit(suit))
            self.suits_box.pack_start(button, True, True, 0)

        # grid to hold the hand
        self.hand_frame = Gtk.Grid()
        
        # add stuff to main vbox
        vbox.pack_start(self.face_num_box, False, False, 0)
        vbox.pack_start(self.of_label, False, False, 0)
        vbox.pack_start(self.suits_box, False, False, 0)
        vbox.pack_end(self.hand_frame, True, True, 0)
        
        self.stack.add_titled(vbox, "input", "Input Hand")

    # selection handlers
    def select_face(self, face):
        self.selected_face = face
        self.check_selection()

    def select_suit(self, suit):
        self.selected_suit = suit
        self.check_selection()

    # make sure one of each is selected and add it to the grid
    def check_selection(self):
        if self.selected_face and self.selected_suit:
            card = (self.selected_face, self.selected_suit)
            hand.append(card)
            self.add_card_button(card)
            # reset state
            self.selected_face = None
            self.selected_suit = None

    def add_card_button(self, card):
        face, suit = card
        suit_symbol = suits[suit]
        button_label = f"{face} of {suit_symbol}"

        button = Gtk.Button(label=button_label)
        button.connect("clicked", lambda widget, card=card: self.remove_card(card, widget))
        self.hand_frame.add(button)
        
        self.hand_frame.show_all()  # Ensure the new button is shown

    # Remove card from hand and button from hand_frame
    def remove_card(self, card, button):
        if card in hand:
            hand.remove(card)  # Remove first occurrence
            self.hand_frame.remove(button)  # Remove the button from the frame
            self.hand_frame.show_all()  # Update display
    
# Run the application
win = BridgeCounter()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
