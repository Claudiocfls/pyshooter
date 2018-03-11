import os
import sys
import pygame as pg

from Menu import *
from Player import *
from Background import *
from Bot import *
from ExtendedGroup import *
from Statistics import *

import Animation
import Sound

###############################################

class Main:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 800, 600
        self.fps = 60
        self.multiplayer_on = False
    
    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(frequency=44100, size=0, channels=1, buffer=4096) #size - 16, channels 2
        pg.mixer.init()
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()

        # self.resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))

        self.menu = Menu()

        # no final vai ser melhor usar o self.resolution no lugar de self.size e usar o pg.FULLSCREEN
        # mas em desenvolvimento pode ser melhor manter assim para permitir a visualização no console
        self._display_surf = pg.display.set_mode(self.size)
        self.screen = pg.display.get_surface() # repetido?
        
        self.PLAYER_POSITION = (self.width/2, self.height/2)
        
        self.PLAY_IMAGE = pg.image.load("Assets/Images/player3.png")
        self.PLAY_IMAGE = pg.transform.scale(self.PLAY_IMAGE, (75,75))
        self.PLAY_IMAGE_BACK = pg.image.load("Assets/Images/back_player.png")
        self.sz = self.PLAY_IMAGE_BACK.get_rect().size
        self.PLAY_IMAGE_BACK = pg.transform.scale(self.PLAY_IMAGE_BACK, (int(self.sz[0]/2.7),int(self.sz[1]/2.7) ))
        
        self.BOT_IMAGE = pg.image.load("Assets/Images/player2.png")
        self.BOT_IMAGE = pg.transform.scale(self.BOT_IMAGE, (75,75))
        
        self.BACK_IMAGE = pg.image.load("Assets/Images/city1_back.png").convert_alpha()
        self.FRONT_IMAGE = pg.image.load("Assets/Images/city1.jpg").convert_alpha()

        self.CROSS_IMAGE = pg.image.load("Assets/Images/cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        
        self.player_animation = Animation.Player
        self.player_animation.load()
        self.player_sound = Sound.Player 
        self.player_sound.load()

        self.back = Background(self.BACK_IMAGE, self.FRONT_IMAGE)
        self.player = Player(self.PLAY_IMAGE, self.PLAY_IMAGE_BACK, (0,0), self.PLAYER_POSITION, self.player_animation, self.player_sound, self.back)
        self.bot0 = Bot(self.BOT_IMAGE, (200,200), self.screen, self.back, self.player)
        self.stats = Statistics(self.player, self.screen.get_rect().size)
        self.players = ExtendedGroup(self.player)
        self.bots = ExtendedGroup(self.bot0)

        #call menu
        self.menu.intro()

        self.multiplayer_on = self.menu.have_client
        if self.multiplayer_on:
            self.server_client = self.menu.server_client

        pg.mouse.set_visible(0)

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._running = False

        # o grupo deveria chamar esses metodos também
        self.players.handle_event(event)
        
    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        self.clock.tick(self.fps)

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill((0,0,0))
        # sem sprite ainda
        self.back.draw(self.screen, self.player)
        self.players.update()
        self.bots.update()

        if self.multiplayer_on:
            self.server_client.push_player(self.player)
            self.server_client.pull_players()
            player_list = self.server_client.players_info
            for player_name in player_list:
                self.player.draw_multiplayer(self.screen, player_list[player_name]['feet_rect'], player_list[player_name]['rect'])

        else:# como que atualiza todos os grupos?

            self.players.draw(self.screen)
            self.bots.draw(self.screen)
            #print(self.player.feet)



        # acho que não precisa de sprite pra essa
        self.screen.blit(self.CROSS_IMAGE, pg.mouse.get_pos())
        self.stats.draw(self.screen)
        
        self.display_fps()
        pg.display.update()

    def on_execute(self):
        self.on_init()

        while (self._running):
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    Main().on_execute()
