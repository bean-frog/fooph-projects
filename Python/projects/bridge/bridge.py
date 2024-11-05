import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class BridgeCounter(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Bridge Hand Calculator - floatme")
        self.set_default_size(400, 600)

        # Title
        self.title = Gtk.Label()
        self.title.set_markup("<big><b>Bridge Hand Calculator</big></b>")

        # stack and swtcher
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(200)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        # content panels
        self.info_panel()
        #self.input_panel()
        #self.result_panel()

        # Box to hpld components
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(10)
        vbox.pack_start(self.title, False, False, 0)
        vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(self.stack, True, True, 0)

        self.add(vbox)

    # Information panel
    def info_panel(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.info_label = Gtk.Label()
        self.info_label.set_markup("""
        <b>How to use this calculator</b>\n
        Using the buttons, select the suit and face/number for each card in your hand.\n
        There are also buttons to remove cards if you've made a mistake.\n
        Press "Calculate" to show your hand's score.\n
        """)
        vbox.pack_start(self.info_label, False, False, 0)
        self.stack.add_titled(vbox, "info", "Info")





#run
win = BridgeCounter()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
