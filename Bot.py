import pygame as pg
from helpers import *

class Bot(pg.sprite.Sprite):
    def __init__(self, location_on_scenario, surface, background, player):
        super().__init__()

        # image and rect will be defined according with the animation
        self.image = None
        self.rect = None
        
        # original_image will be used in rotate
        self.original_image = None

        # load all objects necessary for bot interaction
        self.player = player
        self.background = background

        # surface to draw
        self.surface = surface

        # represent the position in relation to map
        # when drawing, this coordinate should be converted to position in screen
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

        # the center of sprite isnt the center of the own image file
        # so, this is needed to find the real center
        self.delta_center_position = pg.math.Vector2((+35.5/2.7,-8/2.7))
        
        # [TODO] sounds should be loaded in Sounds.py
        self.grunt = pg.mixer.Sound('Assets/Sounds/zombie.wav')

        # flag
        self.is_grunting = False

        # load animation
        # [TODO] all animations should be loaded in Animations.py
        self.animation = self.load_animation()

        # index for animations
        self.index_animation_idle = 0
        self.float_index = 0

    def update(self):
        self.choose_animation()
        self.rotate()

        distance_to_player = self.position_on_scenario.distance_to(self.player.position_on_scenario)
        if distance_to_player < 300:
            if not self.is_grunting:
                self.is_grunting = True
                pg.mixer.Channel(3).play(self.grunt, -1)
            self.grunt.set_volume(1-distance_to_player/300)
        else:
            self.grunt.stop()
            self.is_grunting = False

    def rotate(self):
        _, angle = (self.player.position_on_scenario-self.position_on_scenario).as_polar()

        # gira todas as imagens
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)

        # gira em torno do centro real
        # encontra a nova posição do centro do rect
        self.rotated_center = self.delta_center_position.rotate(+angle)
        self.new_rect_center = self.rotated_center + scenario_to_screen(self.position_on_scenario, self.background.rect)

        # atualiza o rect da imagem com o novo centro correto
        self.rect = self.image.get_rect(center=self.new_rect_center)

    def load_animation(self):
        default_directory = 'Assets/Images/zombie/idle/skeleton-idle_'
        extension_file = '.png'
        idle = load_image_list(default_directory, extension_file, 17)
        idle = scale_image_list(idle, 2.7)
        return idle

    def choose_animation(self):
        self.float_index = increment(self.float_index, 0.25, 1)
        self.index_animation_idle = increment(self.index_animation_idle, int(self.float_index), 16)
        self.original_image = self.animation[self.index_animation_idle]

