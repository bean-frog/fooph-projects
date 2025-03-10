import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk
import pygame
import sys

from Brick import Brick
from Ball import Ball
from Paddle import Paddle

class BreakoutGame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Breakout - floatme")
        self.set_default_size(640, 480)
        self.set_border_width(10)

        # pygame init
        pygame.init()
        self.game_width = 640
        self.game_height = 400
        self.game_surface = pygame.Surface((self.game_width, self.game_height))

        # page stack
        self.stack = Gtk.Stack()
        self.add(self.stack)

        # homescreen/instructions
        self.page_instructions = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.page_instructions.set_border_width(10)
        instructions = Gtk.Label(label="Welcome to Breakout!\n\n"
                                       "Move the paddle with your mouse.\n"
                                       "Break all the bricks by bouncing the ball off your paddle.\n")
        self.page_instructions.pack_start(instructions, True, True, 0)
        
        # difficulty selector
        diff_label = Gtk.Label(label="Select Difficulty:")
        self.combo_diff = Gtk.ComboBoxText()
        self.combo_diff.append_text("Easy")
        self.combo_diff.append_text("Medium")
        self.combo_diff.append_text("Hard")
        self.combo_diff.set_active(1) 
        self.page_instructions.pack_start(diff_label, False, False, 0)
        self.page_instructions.pack_start(self.combo_diff, False, False, 0)
        
        # number of balls
        ball_label = Gtk.Label(label="Number of Balls (2-9):")
        adjustment_balls = Gtk.Adjustment(1, 1, 9, 1, 1, 0)
        self.spin_balls = Gtk.SpinButton()
        self.spin_balls.set_adjustment(adjustment_balls)
        self.page_instructions.pack_start(ball_label, False, False, 0)
        self.page_instructions.pack_start(self.spin_balls, False, False, 0)
        
        # number of rows
        rows_label = Gtk.Label(label="Number of Rows of Bricks (2-5):")
        adjustment_rows = Gtk.Adjustment(1, 1, 5, 1, 1, 0)
        self.spin_rows = Gtk.SpinButton()
        self.spin_rows.set_adjustment(adjustment_rows)
        self.page_instructions.pack_start(rows_label, False, False, 0)
        self.page_instructions.pack_start(self.spin_rows, False, False, 0)
        
        play_button = Gtk.Button(label="Play")
        play_button.connect("clicked", self.start_game)
        self.page_instructions.pack_start(play_button, False, False, 0)
        self.stack.add_titled(self.page_instructions, "instructions", "Instructions")

        # game page
        self.page_game = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        # gtk drawingarea to hold pygame graphics
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(self.game_width, self.game_height)
        self.drawing_area.connect("draw", self.on_draw)
        self.page_game.pack_start(self.drawing_area, True, True, 0)

        # score/lives
        self.score_label = Gtk.Label(label="Score: 0")
        self.lives_label = Gtk.Label(label="Lives: 0")
        self.page_game.pack_start(self.score_label, False, False, 0)
        self.page_game.pack_start(self.lives_label, False, False, 0)
        
        self.stack.add_titled(self.page_game, "game", "Game")

        # game over page
        self.page_game_over = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.page_game_over.set_border_width(10)
        # win/lose
        self.game_over_label = Gtk.Label(label="")
        self.page_game_over.pack_start(self.game_over_label, True, True, 0)
        #play again/exit
        self.button_box_game_over = Gtk.Box(spacing=5)
        self.play_again_button_go = Gtk.Button(label="Play Again")
        self.play_again_button_go.connect("clicked", self.start_game)
        self.exit_button_go = Gtk.Button(label="Exit")
        self.exit_button_go.connect("clicked", self.on_exit)
        self.button_box_game_over.pack_start(self.play_again_button_go, True, True, 0)
        self.button_box_game_over.pack_start(self.exit_button_go, True, True, 0)
        self.page_game_over.pack_start(self.button_box_game_over, False, False, 0)
        self.stack.add_titled(self.page_game_over, "game_over", "Game Over")

        # gamestate things
        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.paddle = None
        self.score = 0
        self.lives = 0
        self.num_balls = 1  # default, will be overwritten by menu selection
        self.game_over = False
        self.waiting_for_respawn = False

        # score multiplier (decreases by 0.1 each second until 1)
        self.multiplier = 3.0
        self.multiplier_timer = None

        # mouse tracking
        self.drawing_area.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.drawing_area.connect("motion-notify-event", self.on_mouse_motion)

        # GLib timout for game loop stuff
        self.game_loop_id = None

    def start_game(self, widget):
        # clear game state
        self.score = 0
        self.game_over = False
        self.waiting_for_respawn = False
        self.all_sprites.empty()
        self.bricks.empty()
        self.balls.empty()
   
        self.multiplier = 3.0
        if self.multiplier_timer:
            GLib.source_remove(self.multiplier_timer)
        self.multiplier_timer = GLib.timeout_add(1000, self.update_multiplier)

        self.stack.set_visible_child_name("game")
        
        difficulty = self.combo_diff.get_active_text()
        self.num_balls = int(self.spin_balls.get_value())
        num_rows = int(self.spin_rows.get_value())
        
        # set options based on difficulty
        if difficulty == "Easy":
            Ball.VELOCITY = 3
            self.lives = 5
        elif difficulty == "Medium":
            Ball.VELOCITY = 5
            self.lives = 3
        elif difficulty == "Hard":
            Ball.VELOCITY = 7
            self.lives = 1
        self.lives_label.set_text(f"Lives: {self.lives}")
        
        # create paddle
        self.paddle = Paddle(self.game_width // 2, self.game_height - 20)
        self.all_sprites.add(self.paddle)

        # spawn ball(s)
        self.spawn_balls()

        # spawn bricks
        brick_width = 60
        brick_height = 20
        padding = 5
        columns = self.game_width // (brick_width + padding)
        for row in range(num_rows):
            for col in range(columns):
                x = col * (brick_width + padding) + padding
                y = row * (brick_height + padding) + padding
                brick = Brick(x, y, brick_width, brick_height)
                self.bricks.add(brick)
                self.all_sprites.add(brick)

        self.score_label.set_text("Score: 0")

        # clear existing loop and start new one
        if self.game_loop_id:
            GLib.source_remove(self.game_loop_id)
        self.game_loop_id = GLib.timeout_add(16, self.game_loop)

    def update_multiplier(self):
        if self.multiplier > 1:
            self.multiplier = max(1, self.multiplier - 0.1)
            return True  
        else:
            return False

    def spawn_balls(self):
        for i in range(self.num_balls):
            ball = Ball(self.paddle.rect.centerx, self.paddle.rect.top - 10)
            self.balls.add(ball)
            self.all_sprites.add(ball)

    def game_loop(self):
        # clear pygame surface
        self.game_surface.fill((0, 0, 0))

        # update each ball
        for ball in list(self.balls):
            ball.update(self.game_surface.get_rect())
            
            # bounce off paddle
            if pygame.sprite.collide_rect(ball, self.paddle):
                ball.vy = -abs(ball.vy)
            
            # brick collision
            hit_bricks = pygame.sprite.spritecollide(ball, self.bricks, True)
            if hit_bricks:
                ball.vy = -ball.vy
                # point multiplier
                points = int(round(len(hit_bricks) * self.multiplier))
                self.score += points
                self.score_label.set_text(f"Score: {self.score}")
            
            # kill ball if below paddle
            if ball.rect.top > self.paddle.rect.bottom + 10: # small buffer because it was acting weird without
                self.balls.remove(ball)
                self.all_sprites.remove(ball)
        
        # no more balls, -1 life
        if len(self.balls) == 0:
            if not self.waiting_for_respawn:
                self.waiting_for_respawn = True
                self.lives -= 1
                self.lives_label.set_text(f"Lives: {self.lives}")
                if self.lives > 0:
                    GLib.timeout_add(500, self.respawn_balls)
                    return True
                else:
                    self.end_game(win=False)
                    return False
        
        # all bricks cleared?
        if len(self.bricks) == 0:
            self.end_game(win=True)
            return False

        # draw sprites
        self.all_sprites.draw(self.game_surface)
        # gtk drawingarea needs to be redrawn
        self.drawing_area.queue_draw()
        return True

    def respawn_balls(self):
        self.spawn_balls()
        self.waiting_for_respawn = False
        return False 

    def end_game(self, win):
        self.game_over = True
        if self.multiplier_timer:
            GLib.source_remove(self.multiplier_timer)
            self.multiplier_timer = None
        message = "You Win!" if win else "Game Over"
        self.game_over_label.set_text(f"{message}\nFinal Score: {self.score}")
        self.stack.set_visible_child_name("game_over")

# handle drawing to gtk drawingarea from pygame using a pixbuf
    def on_draw(self, widget, cr):
        mode = "RGB"
        width, height = self.game_surface.get_size()
        data = pygame.image.tostring(self.game_surface, mode)
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            data,
            GdkPixbuf.Colorspace.RGB,
            False,
            8,
            width,
            height,
            width * 3
        )
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()

    def on_mouse_motion(self, widget, event):
        if self.paddle and not self.game_over:
            self.paddle.update(int(event.x), self.game_surface.get_rect())

    def on_exit(self, widget):
        Gtk.main_quit()

def main():
    win = BreakoutGame()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
