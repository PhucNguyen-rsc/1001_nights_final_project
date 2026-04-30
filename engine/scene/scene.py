from pygame import SRCALPHA
from pygame.sprite import Sprite
from pygame.surface import Surface


class Scene(Sprite):
    image = None
    battle = None

    def __init__(self):
        from engine.game.game import Game
        self.main_dir = Game.main_dir
        self.data_dir = Game.data_dir
        self.screen_scale = Game.screen_scale
        self.screen_size = Game.screen_size
        self.screen_width = self.screen_size[0]
        self.screen_height = self.screen_size[1]
        self.half_screen = self.screen_width / 2
        self._layer = 0
        Sprite.__init__(self)
        self.data = {}
        self.images = {}
        self.full_scene_image = None
        self.current_scene_image = None
        self.shown_camera_pos = None
        self.camera_left = None
        self.camera_y_shift = None
        self.rect = None

        self.alpha = 0
        self.fade_speed = 1
        self.fade_start = False
        self.fade_in = False
        self.fade_out = False
        self.fade_delay = 0
        self.size_width = self.screen_width
        self.size_height = self.screen_height

        # cross-fade state for bgchange-with-fade
        self.bg_fade_image = None    # snapshot of the OLD full_scene_image
        self.bg_fade_alpha = 0       # 255 = fully showing old, 0 = fully showing new
        self.bg_fade_speed = 600     # alpha units per second

    def setup(self):
        self.full_scene_image = Surface((self.screen_width * len(self.data), self.size_height), SRCALPHA)
        for scene_index, image in self.data.items():
            x = (scene_index - 1) * self.images[image].get_width()
            rect = self.images[image].get_rect(topleft=(x, 0))
            self.full_scene_image.blit(self.images[image], rect)

    def update(self, camera_left, camera_y_shift):
        if self.camera_left != camera_left:
            self.camera_left = camera_left
            self.current_scene_image = Surface.subsurface(self.full_scene_image, (camera_left, 0,
                                                                                  self.size_width, self.size_height))
        if self.camera_y_shift != camera_y_shift:
            self.camera_y_shift = camera_y_shift
            self.rect = self.current_scene_image.get_rect(midtop=(self.current_scene_image.get_width() / 2,
                                                                  camera_y_shift))
        self.image.blit(self.current_scene_image, self.rect)

        # bg cross-fade: blit the OLD bg over the new one with diminishing alpha
        if self.bg_fade_image is not None and self.bg_fade_alpha > 0:
            old_sub = Surface.subsurface(self.bg_fade_image, (self.camera_left, 0,
                                                              self.size_width, self.size_height))
            old_sub.set_alpha(int(self.bg_fade_alpha))
            self.image.blit(old_sub, self.rect)
            self.bg_fade_alpha -= self.bg_fade_speed * self.battle.true_dt
            if self.bg_fade_alpha <= 0:
                self.bg_fade_alpha = 0
                self.bg_fade_image = None

        if self.fade_start:
            if self.fade_in:  # keep fading in
                self.alpha += self.battle.dt * self.fade_speed
                if self.alpha >= 255:
                    self.alpha = 255
                    self.fade_in = False
                self.image.fill((0, 0, 0, self.alpha))
            elif self.fade_out:
                self.alpha -= self.battle.dt * self.fade_speed
                if self.alpha <= 0:
                    self.alpha = 0
                    self.fade_out = False
                self.image.fill((0, 0, 0, self.alpha))

            if self.fade_delay:
                self.fade_delay -= self.battle.dt
                if self.fade_delay < 0:
                    self.fade_delay = 0
            if not self.fade_delay:
                self.fade_start = False


class HalfScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.size_height = self.size_height / 2

    def setup(self):
        self.full_scene_image = Surface((self.screen_width * len(self.data), self.size_height), SRCALPHA)
        for scene_index, image in self.data.items():
            x = (scene_index - 1) * self.images[image].get_width()
            rect = self.images[image].get_rect(topleft=(x, 0))
            self.full_scene_image.blit(self.images[image], rect)
