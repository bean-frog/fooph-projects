import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import pygame
import numpy as np
import sys
import math

pygame.display.init()

class ShapeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="shapes - floatme")

        #vertical box layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        #user input section
        self.create_input_section(vbox)

        #drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(400, 300)
        vbox.pack_start(self.drawing_area, True, True, 0)

        self.drawing_area.connect("draw", self.on_draw)

        # pygame default init
        self.color = (255, 0, 0) 
        self.side_thickness = 2
        self.side_length = 100
        self.shape_type = "Polygon"
        self.num_sides = 3

        self.pygame_surface = pygame.Surface((400, 300))

        GLib.timeout_add(100, self.refresh_drawing_area)

        self.show_all()

    def create_input_section(self, vbox):
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        vbox.pack_start(grid, False, False, 10)

        # color input (hex code)
        grid.attach(Gtk.Label(label="Line Color (hex):"), 0, 0, 1, 1)
        self.color_entry = Gtk.Entry()
        self.color_entry.set_text("#FF0000")  # Default red
        grid.attach(self.color_entry, 1, 0, 1, 1)

        # side thickness
        grid.attach(Gtk.Label(label="Side Thickness:"), 0, 1, 1, 1)
        self.thickness_spin = Gtk.SpinButton.new_with_range(1, 10, 1) # min 1, max 10, step 1
        self.thickness_spin.set_value(2)
        grid.attach(self.thickness_spin, 1, 1, 1, 1)

        # side length
        grid.attach(Gtk.Label(label="Side Length:"), 0, 2, 1, 1)
        self.length_spin = Gtk.SpinButton.new_with_range(50, 300, 1) # min 50, max 300, step 1
        self.length_spin.set_value(100)
        grid.attach(self.length_spin, 1, 2, 1, 1)

        # number of sides
        grid.attach(Gtk.Label(label="Number of Sides:"), 0, 3, 1, 1)
        self.sides_spin = Gtk.SpinButton.new_with_range(3, 20, 1) # min 3, max 20, step 1
        self.sides_spin.set_value(6)
        grid.attach(self.sides_spin, 1, 3, 1, 1)

        # shape
        grid.attach(Gtk.Label(label="Shape Type:"), 0, 4, 1, 1)
        self.shape_combo = Gtk.ComboBoxText()
        self.shape_combo.append_text("Polygon")
        self.shape_combo.append_text("Pinwheel")
        self.shape_combo.append_text("Asterisk")
        self.shape_combo.set_active(0)
        grid.attach(self.shape_combo, 1, 4, 1, 1)

        # submit
        self.submit_button = Gtk.Button(label="Draw Shape")
        self.submit_button.connect("clicked", self.on_submit)
        grid.attach(self.submit_button, 0, 5, 2, 1)

    def on_submit(self, widget):
        color_hex = self.color_entry.get_text()
        try:
            self.color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
        except ValueError:
            print("invalid hex code supplied. using default #FF0000 (red)")
            self.color = (255, 0, 0)

        self.side_thickness = int(self.thickness_spin.get_value())
        self.side_length = int(self.length_spin.get_value())
        self.num_sides = int(self.sides_spin.get_value())
        self.shape_type = self.shape_combo.get_active_text()
        self.draw_shape()

    def refresh_drawing_area(self):
        self.drawing_area.queue_draw()
        return True

    def on_draw(self, widget, cr):
        pixel_data = pygame.image.tostring(self.pygame_surface, 'RGB')

        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            pixel_data,
            GdkPixbuf.Colorspace.RGB,
            False,  # No alpha
            8,      # Bits per channel
            self.pygame_surface.get_width(),
            self.pygame_surface.get_height(),
            self.pygame_surface.get_width() * 3
        )

        # draw pixbuf
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()

    def draw_shape(self):
        screen = self.pygame_surface
        screen.fill((0, 0, 0))  # drawing area background

        # center coordinates
        width, height = screen.get_size()
        center_x, center_y = width // 2, height // 2

        # calculate points (i hate this)
        angle_step = 360 / self.num_sides
        points = []
        for i in range(self.num_sides):
            angle = math.radians(i * angle_step) 
            x = center_x + self.side_length * math.cos(angle)
            y = center_y - self.side_length * math.sin(angle)
            points.append((x, y))

        # draw shape
        if self.shape_type == "Polygon":
            pygame.draw.polygon(screen, self.color, points, self.side_thickness)
        elif self.shape_type == "Pinwheel":
            self.draw_pinwheel(points, screen)
        elif self.shape_type == "Asterisk":
            self.draw_asterisk(points, screen)

    
    def draw_pinwheel(self, points, screen):
        num_points = len(points)
        for i in range(num_points):
            current_point = points[i]
            next_point = points[(i + 1) % num_points]
        
            # vector between current and next point
            vector_x = next_point[0] - current_point[0]
            vector_y = next_point[1] - current_point[1]

            # length of the side using vectors
            side_length = math.sqrt(vector_x**2 + vector_y**2)

            unit_vector_x = vector_x / side_length
            unit_vector_y = vector_y / side_length

            # shift the point so that it doesnt overlap (hacky fix but it works)
            shift_x = unit_vector_y * (side_length / 2)
            shift_y = -unit_vector_x * (side_length / 2)

            # new shifted point
            shifted_point = (current_point[0] + shift_x, current_point[1] + shift_y)

            # midpoint of current side
            mid_x = (shifted_point[0] + next_point[0]) / 2
            mid_y = (shifted_point[1] + next_point[1]) / 2
            midpoint = (mid_x, mid_y)
        
            # endpoint of the line (next vertex)
            next_vertex = points[(i+2) % num_points] 
        
            # after all that, draw the line
            pygame.draw.line(screen, self.color, midpoint, next_vertex, self.side_thickness)

    def draw_asterisk(self, points, screen):
        # center coordinates
        width, height = screen.get_size()
        center_x, center_y = width // 2, height // 2
        center = (center_x, center_y)

         # lines from the center to each vertex
        for point in points:
            pygame.draw.line(screen, self.color, center, point, self.side_thickness)
    
    
#run
win = ShapeWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
