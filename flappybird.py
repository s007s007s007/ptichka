import arcade
import random

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900
SCREEN_TITLE = "kNIGGA"
ESHKERE = 10
GRAVITI = 1


class VLODIMIR(arcade.Sprite):
    i = 0
    popa = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.popa += delta_time
        if self.popa > 0.1:
            self.popa = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)


class PTICHKA(VLODIMIR):
    def __init__(self):
        super().__init__("bird/bluebird-downflap.png", 1)
        self.angle = 0

    def logika_ptichki(self):
        self.center_y += self.change_y
        self.angle += self.change_angle
        self.change_y -= GRAVITI
        self.change_angle -= GRAVITI
        if self.center_y < 150:
            self.center_y = 150
        if self.top >= SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.angle < -45:
            self.angle = -45
        if self.angle > 15:
            self.angle = 15


class PIPEILIDVUSHKA(VLODIMIR):
    def __init__(self, isup):
        super().__init__("pipe.png", 0.3, flipped_vertically=isup)
        self.change_x = -1
        self.isup = isup

    def logika_pipi(self):
        self.center_x += self.change_x
        if self.right < 0:
            self.left = SCREEN_WIDTH
            if self.isup:
                self.center_y = random.randint(800, 900)
            else:
                self.center_y = random.randint(-100, 100)
            self.change_x -= 0.05
            window.b = True
        if self.right < window.ptichka.left and window.b:
            window.b = False
            window.a += 1
            arcade.play_sound(window.ah2)

    def update(self):
        self.logika_pipi()


class OKKOiliOKNO(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("bg.png")
        self.vacok = arcade.load_texture("Image20240723153125.png")
        self.game_over = False
        self.a = 0
        self.ptichka = PTICHKA()
        self.ptichka.append_texture(arcade.load_texture("bird/bluebird-midflap.png"))
        self.ptichka.append_texture(arcade.load_texture("bird/bluebird-upflap.png"))
        self.ptichka.append_texture(arcade.load_texture("bird/redbird-downflap.png"))
        self.ptichka.append_texture(arcade.load_texture("bird/redbird-midflap.png"))
        self.ptichka.append_texture(arcade.load_texture("bird/redbird-upflap.png"))
        self.ptichka.append_texture(arcade.load_texture("bird/yellowbird-downflap.png"))
        self.ptichka.append_texture(arcade.load_texture("bird/yellowbird-midflap.png"))
        self.ptichka.append_texture(arcade.load_texture("bird/yellowbird-upflap.png"))
        self.ah = arcade.load_sound("audio/wing.wav")
        self.ah1 = arcade.load_sound("audio/hit.wav")
        self.ah2 = arcade.load_sound("audio/point.wav")
        self.hihihiha = arcade.SpriteList()
        self.byby = False
        self.b = True

    def spawn(self):
        self.a = 0
        self.hihihiha = arcade.SpriteList()

        self.ptichka.center_y = 500
        self.ptichka.center_x = 400

        self.ptichka.change_y = -12
        for x in range(13):
            pipa = PIPEILIDVUSHKA(False)
            pipa.center_x = 100 * x
            pipa.center_y = random.randint(-100, 100)
            self.hihihiha.append(pipa)
            pip = PIPEILIDVUSHKA(True)
            pip.center_x = 100 * x
            pip.center_y = random.randint(800, 900)
            self.hihihiha.append(pip)

    def on_key_press(self, symbol: int, modifiers: int):
        if not self.game_over:
            if symbol == arcade.key.SPACE:
                self.byby = True

        if not self.game_over:
            if symbol == arcade.key.UP:
                self.ptichka.change_y = ESHKERE
                arcade.play_sound(self.ah)
                self.ptichka.change_angle = 15

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if 1000 <= x <= 1300 and 800 <= y <= 860:
            self.game_over = False
            self.spawn()

    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.ptichka.draw()
        self.hihihiha.draw()
        if not self.game_over:
            arcade.draw_text(self.a, 1000, 800, arcade.color.JET, 52)
        if self.game_over:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.vacok)
            arcade.draw_text("ZANOVO???", 1000, 800, arcade.color.DIAMOND, 52)
            self.start = False
            self.byby = False

    def update(self, delta_time: float):
        if not self.game_over:
            if self.byby:
                self.ptichka.logika_ptichki()
                self.ptichka.update_animation(delta_time)
                self.hihihiha.update()
                gghit = arcade.check_for_collision_with_list(self.ptichka, self.hihihiha)
                if len(gghit) > 0:
                    self.game_over = True
                    arcade.play_sound(self.ah1)


window = OKKOiliOKNO(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
window.spawn()
arcade.run()
