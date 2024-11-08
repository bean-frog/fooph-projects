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

        # layout box
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
        for item in ["jack", "king", "queen", "ace", "2", "3", "4", "5", "6", "7", "8", "9", "1"]:
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

        # flowbox to hold the hand
        self.hand_frame = Gtk.FlowBox()
        
        # calculate button
        self.calculate_button = Gtk.Button(label="Calculate Score")
        self.calculate_button.connect("clicked", lambda widget, hand=hand: self.calculate_hand(hand))
        
        # result label
        self.result_label = Gtk.Label()
        
        # add stuff to main vbox
        vbox.pack_start(self.face_num_box, False, False, 0)
        vbox.pack_start(self.of_label, False, False, 0)
        vbox.pack_start(self.suits_box, False, False, 0)
        vbox.pack_end(self.result_label, False, False, 0)
        vbox.pack_end(self.calculate_button, True, False, 0)
        vbox.pack_end(self.hand_frame, True, True, 0)
        
        self.stack.add_titled(vbox, "input", "Input Hand")

    # Selection handlers
    def select_face(self, face):
        self.selected_face = face
        self.check_selection()

    def select_suit(self, suit):
        self.selected_suit = suit
        self.check_selection()

    # Make sure one of each is selected and add it to the grid
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
        button_label = Gtk.Label()
        button_label.set_markup(f"<span size='40pt'>{self.card_to_unicode((face, suit))}</span>")

        button = Gtk.Button()
        button.add(button_label)
        button.connect("clicked", lambda widget, card=card: self.remove_card(card, widget))
        self.hand_frame.add(button)
        print(hand)
        self.hand_frame.show_all()

    # card removal
    def remove_card(self, card, button):
        if card in hand:
            hand.remove(card) 
            self.hand_frame.remove(button)  
            print(hand)
            self.hand_frame.show_all() 

    # convert card text to the unicode character - https://en.wikipedia.org/wiki/Playing_cards_in_Unicode
    def card_to_unicode(self, card):
        face, suit = card
        suit_unicode_bases = {
            'spades': '1F0A',
            'hearts': '1F0B',
            'diamonds': '1F0C',
            'clubs': '1F0D'
        }
    
        face_unicode_additions = {
            'ace': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
            '10': 'A',
            'jack': 'B',
            'queen': 'D',
            'king': 'E'
        }
    
        base = suit_unicode_bases.get(suit.lower())
        addition = face_unicode_additions.get(face.lower())
        unicode_code_point = base + addition 
        unicode_char = chr(int(unicode_code_point, 16)) #ngl had to ask chatgpt how to make it actually display the character instead of just \U000XXXXX  
        
        return unicode_char

    # calculate points
    def calculate_hand(self, hand):
        if len(hand) != 13:
            self.result_label.set_markup("<span size='20pt'>Please ensure the hand contains 13 cards</span>")
        else:
            face_card_points = {
                'ace': 4,
                'king': 3,
                'queen': 2,
                'jack': 1
            }
            total_points = 0

            suit_count = {
                'hearts': 0,
                'diamonds': 0,
                'clubs': 0,
                'spades': 0
            }
    
            for card, suit in hand:
                if card in face_card_points:
                    total_points += face_card_points[card]
                suit_count[suit] += 1
    
            # distribution points
            for count in suit_count.values():
                if count == 2:
                    total_points += 1
                elif count == 1:
                    total_points += 2
                elif count == 0:
                    total_points += 3
            self.result_label.set_markup(f"<span size='20pt'>Your hand is worth <b>{total_points}</b> points.</span>")

# run
win = BridgeCounter()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
