import pygame.image

class Images():
    """Stora data input from inmages"""
    def __init__(self):
        # Surface objects returned by pygame.image.load().
        self.IMAGES_DICT = {
                        # map object
                        'uncovered goal': pygame.image.load('images/map_obj/RedSelector.png'),
                        'covered goal': pygame.image.load('images/map_obj/Selector.png'),
                        'dragon_ball': pygame.image.load('images/map_obj/dragon_ball.png'),
                        'corner': pygame.image.load('images/map_obj/Wall_Block_Tall.png'),
                        'wall': pygame.image.load('images/map_obj/Wood_Block_Tall.png'),
                        'inside floor': pygame.image.load('images/map_obj/Plain_Block.png'),
                        'outside floor': pygame.image.load('images/map_obj/Grass_Block.png'),
                        
                        # player
                        'broly': pygame.image.load('images/players/broly.png'),
                        'cadiz': pygame.image.load('images/players/cadiz.png'),
                        # 'vegeta': pygame.image.load('images/players/vegeta.png'),
                        # 'goku': pygame.image.load('images/players/goku.png'),
                        'horngirl': pygame.image.load('images/players/horngirl.png'),

                        # decorate object
                        'rock': pygame.image.load('images/decorate_obj/Rock.png'),
                        'short tree': pygame.image.load('images/decorate_obj/Tree_Short.png'),
                        'tall tree': pygame.image.load('images/decorate_obj/Tree_Tall.png'),
                        'ugly tree': pygame.image.load('images/decorate_obj/Tree_Ugly.png'),

                        # button
                        'back_main_button' : pygame.image.load('images/buttons/back_main_button.png'),
                        'button' : pygame.image.load('images/buttons/button.jpg'),
                        
                        # others
                        'background' : pygame.image.load('images/background.jpg'),
                        'game_instruction' : pygame.image.load('images/game_instruction.jpg'),
                        'win': pygame.image.load('images/win.png'),
                        'goku_decorate': pygame.image.load('images/goku_decorate.png')}

        # in the level file to the Surface object it represents.
        self.TILE_MAPPING = {'x': self.IMAGES_DICT['corner'],
                            '#': self.IMAGES_DICT['wall'],
                            'o': self.IMAGES_DICT['inside floor'],
                            ' ': self.IMAGES_DICT['outside floor']}

        self.OUTSIDE_DECOMAPPING = {'1': self.IMAGES_DICT['rock'],
                                    '2': self.IMAGES_DICT['short tree'],
                                    '3': self.IMAGES_DICT['tall tree'],
                                    '4': self.IMAGES_DICT['ugly tree']}

        # currentImage is the index of the player's current player image.
        self.current_image = 0
        self.PLAYER_IMAGES = [self.IMAGES_DICT['broly'],
                            self.IMAGES_DICT['cadiz'],
                            # self.IMAGES_DICT['vegeta'],
                            # self.IMAGES_DICT['goku'],
                            self.IMAGES_DICT['horngirl']]