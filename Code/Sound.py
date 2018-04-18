import pygame as pg

class Player:
    @classmethod
    def load(cls):
        # if len(cls.move) == 0:
        cls.shoot = pg.mixer.Sound('Assets/Sounds/ak47_shoot2.wav')
        cls.reload = pg.mixer.Sound('Assets/Sounds/ak47_reload.wav')
        cls.shotgun_shoot = pg.mixer.Sound('Assets/Sounds/shotgun_shoot.wav')
        cls.shotgun_reload = pg.mixer.Sound('Assets/Sounds/shotgun_reload.wav')
        cls.meleeattack = pg.mixer.Sound('Assets/Sounds/meleeattack.wav')
        cls.footstep = pg.mixer.Sound('Assets/Sounds/footstep.wav')
        cls.empty = pg.mixer.Sound('Assets/Sounds/empty.wav')

    @classmethod
    def play(cls):
        cls.shoot.play()

    @classmethod
    def stop(cls):
        cls.shoot.stop()

class Bot:
    grunt = None
    # @staticmethod
    @classmethod
    def load(cls):
        # if len(cls.move) == 0:
        cls.grunt = pg.mixer.Sound('Assets/Sounds/zombie.wav')