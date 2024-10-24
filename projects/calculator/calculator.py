# YACA - Yet Another (gtk) Calculator App
# (c) 2024 Graeme Kieran

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango
import math
from sympy import sympify, Symbol

class Calculator(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Calculator - floatme") # floatme is specific to my Hyprland config
        self.set_default_size(400, 600)
        self.set_border_width(10)

        # vertical box to arrange the stack switcher and label
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        
        # create a frame (for the cool outline) and put a label in it
        self.input_frame = Gtk.Frame()

        self.display = Gtk.Label(label="")
        self.display.set_xalign(1)  # Right align text
        self.display.modify_font(Pango.FontDescription('20'))
        self.display.set_hexpand(True)
        self.display.set_vexpand(False)
        
        self.input_frame.add(self.display)

        vbox.pack_start(self.input_frame, False, False, 0)

        # Stack/StackSwitcher for different displays (basic/advanced/info)
        self.stack_switcher = Gtk.StackSwitcher()
        vbox.pack_start(self.stack_switcher, False, False, 0)

        self.stack = Gtk.Stack()
        self.stack_switcher.set_stack(self.stack)
        vbox.pack_start(self.stack, True, True, 0)

         # create and populate info panel
        self.info_frame = Gtk.Frame()

        self.info_label = Gtk.Label()
        self.info_label.set_markup(
            "<b>Calculator App</b>\n\n"
            "Use the tabs to switch between basic and advanced modes.\n"
            "Advanced mode enables trigonometric functions, square root (√), \n"
            "permutations (nPr), and combinations (nCr).\n\n"
            "<b>For permutations (nPr) and combinations (nCr):</b>\n"
            "Enter n, press nPr or nCr, enter r.\n"
            "Example: 5P3 will calculate 5 permute 3.\n\n"
            "<b>For trig functions and square roots:</b> \n"
            "Press the function you wish to use, then in parentheses enter the number.\n"
            "For example: sin(10) or √(4)\n"
            "The calculator will automatically add the opening parenthesis '(',\n but you need to remember to close it."
        )
        self.info_label.set_justify(Gtk.Justification.CENTER)
        self.info_label.set_margin_top(10)
        self.info_label.set_margin_bottom(10)
        self.info_label.set_margin_start(10)
        self.info_label.set_margin_end(10)

        self.info_frame.add(self.info_label)

        # grids with buttons. tuple format: (label, x, y)
        self.basic_grid = self.create_grid([
            ('C', 0, 3),  
            ('(', 0, 0), (')', 0, 1), 
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), 
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), 
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), 
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 3), ('=', 4, 2)
        ], spacing=10)

        self.advanced_grid = self.create_grid([
            ('C', 0, 3), 
            ('(', 0, 0), (')', 0, 1), ('del', 0, 2),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 3), ('=', 4, 2),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2),
            ('nPr', 6, 0), ('nCr', 6, 1), ('√', 6, 2)
        ], spacing=10)

        # add grids to the stack
        self.stack.add_titled(self.info_frame, "info", "Info") # moved this here so that Info is the default view
        self.stack.add_titled(self.basic_grid, "basic", "Basic")
        self.stack.add_titled(self.advanced_grid, "advanced", "Advanced")
        
        # variables to keep track of operations and expression
        self.current_expression = ""
        self.last_operator = ""  
        self.last_number = ""  # hold the last number (for nPr and nCr)

    # iterates through array of tuples and adds them to a Gtk.Grid
    def create_grid(self, button_layout, spacing=0):
        grid = Gtk.Grid()
        grid.set_row_spacing(spacing)  # spacing between rows
        grid.set_column_spacing(spacing)  # spacing between columns
        for (label, row, col) in button_layout:
            button = Gtk.Button(label=label)
            button.modify_font(Pango.FontDescription('bold 20')) # deprecated but it works and its easy
            button.set_hexpand(True)
            button.set_vexpand(True)
            button.connect("clicked", self.on_button_clicked)
            grid.attach(button, col, row, 1, 1)
        return grid

    def on_button_clicked(self, button):
        label = button.get_label()

        if label == 'C':
            self.current_expression = ""
            self.last_number = ""
            self.last_operator = ""
        elif label == '=':
            try:
                expr = self.current_expression.replace('sin', 'sin').replace('cos', 'cos').replace('tan', 'tan').replace('√', 'sqrt')

                # Hanhandledle permutations and combinations
                if self.last_operator == 'P':
                    n, r = map(int, self.current_expression.split('P'))
                    result = math.perm(n, r)
                elif self.last_operator == 'C':
                    n, r = map(int, self.current_expression.split('C'))
                    result = math.comb(n, r)
                else:
                    # evaluate with sympy
                    sympy_expr = sympify(expr)
                    result = sympy_expr.evalf()

                self.current_expression = str(result)
            except Exception as e:
                self.current_expression = "Error"
        # special operators
        elif label == 'nPr':
            self.last_operator = 'P'
            self.current_expression += 'P'
        elif label == 'nCr':
            self.last_operator = 'C'
            self.current_expression += 'C'
        elif label == '√':
            self.current_expression += "√("
        elif label == "sin" or label == "cos" or label == "tan":
            self.current_expression += label + "("

            # TODO HOW THE FUCK DO YOU GET TEH LNGTH OF A STRINGGGGG
        elif label == 'del' and self.current_expression.length() > 0:
            exp_len = self.current_expression.length()
            print(exp_len)

        else:
            if self.current_expression == "Error":
                self.current_expression = ""
            self.current_expression += label

        # update the display
        self.display.set_text(self.current_expression)

# init and run
win = Calculator()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
