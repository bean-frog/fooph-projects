import gi
import pygame
import random
import time
from threading import Thread

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

pygame.display.init()
pygame.font.init()
responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt",
    "Yes, definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "Outlook not so good.",
    "Very Doubtful"
]

class EightBall(Gtk.Window):
    def __init__(self):
        super().__init__(title="Magic Eight Ball - floatme")
        self.set_default_size(400, 500)
        
        # layout container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        
        # pygame drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(400, 400)
        vbox.pack_start(self.drawing_area, True, True, 0)
        
        # button
        self.button = Gtk.Button(label="Ask the Magic 8-Ball")
        self.button.set_size_request(400, 50)
        vbox.pack_start(self.button, False, False, 0)
        
        # pygame init
        self.screen = pygame.Surface((400, 400))
        self.draw_8_ball()
        
        # signals
        self.drawing_area.connect("draw", self.on_draw)
        self.button.connect("clicked", self.on_button_clicked)
        
    def draw_8_ball(self, message=None):
        self.screen.fill((50, 50, 50)) #background color
        pygame.draw.circle(self.screen, (0, 0, 0), (200, 200), 180)  # black outer circle
        pygame.draw.circle(self.screen, (255, 255, 255), (200, 200), 100)  # white inner circle
        
        # center "8"
        font = pygame.font.Font(None, 100)
        text = font.render("8", True, (0, 0, 0))
        text_rect = text.get_rect(center=(200, 200))
        self.screen.blit(text, text_rect)
        
        # if there is message, draw that too
        if message:
            font = pygame.font.Font(None, 30)
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(200, 320))
            self.screen.blit(text, text_rect)
        
        self.drawing_area.queue_draw()  # redraw
        
    def on_draw(self, widget, cr):
        # pygame surface --> GDK PixBuf
        w, h = self.screen.get_size()
        data = pygame.image.tostring(self.screen, "RGB")
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(data, GdkPixbuf.Colorspace.RGB, False, 8, w, h, w * 3)
        
        # render pixbuf
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        
    def on_button_clicked(self, button):
        time.sleep(0.5) #dramatic delay
        response = random.choice(responses)
        GLib.idle_add(self.draw_8_ball, response) 

win = EightBall()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
