try:

    import sys, copy, pygame
    from pygame.locals import *
    from game_stats import GameStats

    from map import Map
    from data import Images
    from player import Player
    from settings import Settings

    class Main:
        """Overall class to manage game assets and behavior."""

        def __init__(self):
            pygame.init()

            # background music
            pygame.mixer.init()
            pygame.mixer.music.load("musics/background.mp3")
            pygame.mixer.music.play(-1, 0.0)

            self.images = Images()
            self.game_stats = GameStats()
            self.player = Player()
            self.settings = Settings()
            self.map = Map()

            # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen = pygame.display.set_mode((self.settings.WINWIDTH, self.settings.WINHEIGHT))
            pygame.display.set_caption('Arrange the Dragon Ball')
            self.FONT = pygame.font.Font('freesansbold.ttf', 20)

            self.levels = self.map.read_levels_file('levels.txt')



        def run_game(self):
            """Start the main loop for the game."""

            while self.start_screen() == False:
                self.start_screen()

            while True: # main game loop
                # Run the level to actually start playing the game:
                result = self.run_level(self.levels, self.game_stats.current_level_index)

                if result in ('win', 'next'):
                    # Go to the next level.
                    self.game_stats.current_level_index += 1
                    if self.game_stats.current_level_index >= len(self.levels):
                        # If there are no more levels, go back to the first one.
                        self.game_stats.current_level_index = 0
                elif result == 'back':
                    # Go to the previous level.
                    self.game_stats.current_level_index -= 1
                    if self.game_stats.current_level_index < 0:
                        # If there are no previous levels, go to the last one.
                        self.game_stats.current_level_index = len(self.levels) - 1
                elif result == 'reset':
                    pass # Do nothing. Loop re-calls run_game() to reset the level

        def start_screen(self):
            """Display the start screen until the player presses a key. Returns None."""

            # Draw the background image.
            background_rect = self.images.IMAGES_DICT['background'].get_rect()
            self.screen.blit(self.images.IMAGES_DICT['background'], background_rect)

            # set the position of play button
            play_button_rect = pygame.Surface((90, 50)).get_rect()
            play_button_rect.x = 100
            play_button_rect.y = 150

            # set the position of instruction button
            instruction_button_rect = pygame.Surface((200, 50)).get_rect()
            instruction_button_rect.x = 100
            instruction_button_rect.y = 210

            # set the position of exit button
            exit_button_rect = pygame.Surface((85, 50)).get_rect()
            exit_button_rect.x = 100
            exit_button_rect.y = 270

            while True: # loop for the start screen until player click somethings
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        back_main_button_rect = self.images.IMAGES_DICT['back_main_button'].get_rect()
                        back_main_button_rect.centerx = self.settings.HALF_WINWIDTH 
                        back_main_button_rect.y = self.settings.HALF_WINHEIGHT + 200

                        if play_button_rect.collidepoint(mouse_pos):
                            return True
                        elif exit_button_rect.collidepoint(mouse_pos):
                            self.exit()
                        elif instruction_button_rect.collidepoint(mouse_pos):
                            # de_active other buttons
                            play_button_rect.x = -1000
                            play_button_rect.y = -1000
                            instruction_button_rect.x = -1000
                            instruction_button_rect.y = -1000
                            exit_button_rect.x = -1000
                            exit_button_rect.y = -1000

                            # game_instruction
                            game_instruction_rect = self.images.IMAGES_DICT['game_instruction'].get_rect()
                            self.screen.blit(self.images.IMAGES_DICT['game_instruction'], game_instruction_rect)

                            # back_main button
                            self.screen.blit(self.images.IMAGES_DICT['back_main_button'], back_main_button_rect)
                        
                        if back_main_button_rect.collidepoint(mouse_pos):
                                return False
                
                pygame.display.update()

        def run_level(self, levels, current_level_index):
            button_rect = self.images.IMAGES_DICT['button'].get_rect()

            # Menu button
            menu_button_rect = pygame.Surface((190, 70)).get_rect()
            menu_button_rect.x = 10
            menu_button_rect.y = 15

            # Left button
            left_button_rect = pygame.Surface((70, 70)).get_rect()
            left_button_rect.x = 245
            left_button_rect.y = 15

            # Resart button
            restart_button_rect = pygame.Surface((70, 70)).get_rect()
            restart_button_rect.x = 410
            restart_button_rect.y = 15

            # Right button
            right_button_rect = pygame.Surface((70, 70)).get_rect()
            right_button_rect.x = 560
            right_button_rect.y = 15

            # Change player button
            change_player_button_rect = pygame.Surface((70, 70)).get_rect()
            change_player_button_rect.x = 720
            change_player_button_rect.y = 15
            
            level_obj = levels[current_level_index]
            map_obj = self.map.decorate_map(level_obj['object'], level_obj['start_state']['player'], self)
            game_state_obj = copy.deepcopy(level_obj['start_state'])
            map_need_draw = True # set to True to call draw_map()
            
            level_is_complete = False

            while True: # main game loop
                # Reset these variables:
                direction = None
                key_pressed = False

                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if menu_button_rect.collidepoint(mouse_pos):
                            self.run_game()
                        elif left_button_rect.collidepoint(mouse_pos):
                            return 'back'
                        elif restart_button_rect.collidepoint(mouse_pos):
                            return 'reset'
                        elif right_button_rect.collidepoint(mouse_pos):
                            return 'next'
                        elif change_player_button_rect.collidepoint(mouse_pos):
                            # Change the player image to the next one.
                            self.images.current_image += 1
                            if self.images.current_image >= len(self.images.PLAYER_IMAGES):
                                # After the last player image, use the first one.
                                self.images.current_image = 0
                            map_need_draw = True

                    elif event.type == KEYDOWN:
                        key_pressed = True
                        if event.key == K_LEFT:
                            direction = "left"
                        elif event.key == K_RIGHT:
                            direction = "right"
                        elif event.key == K_UP:
                            direction = "up"
                        elif event.key == K_DOWN:
                            direction = "down"

                        elif event.key == K_n:
                            return 'next'
                        elif event.key == K_b:
                            return 'back'
                        elif event.key == K_BACKSPACE:
                            return 'reset' # Reset the level.
                        elif event.key == K_p:
                            self.images.current_image += 1
                            if self.images.current_image >= len(self.images.PLAYER_IMAGES):
                                self.images.current_image = 0
                            map_need_draw = True

                if direction != None and not level_is_complete:
                    # Make the move and pull the dragon ball
                    moved = self.player.make_move(map_obj, game_state_obj, direction, self.map)

                    if moved:
                        sound = pygame.mixer.Sound('musics/move.wav')
                        sound.play()

                        # increase the step counter.
                        game_state_obj['step_counter'] += 1
                        map_need_draw = True

                    if self.game_stats.is_level_finished(level_obj, game_state_obj):
                        level_is_complete = True
                        key_pressed = False

                self.screen.fill(self.settings.BGCOLOR)

                if map_need_draw:
                    map_surf = self.map.draw_map(map_obj, game_state_obj, level_obj['goals'], self)
                    map_need_draw = False

                # set the position of map
                map_surf_rect = map_surf.get_rect()
                map_surf_rect.center = (self.settings.HALF_WINWIDTH, self.settings.HALF_WINHEIGHT)

                # Draw map and game stats
                self.screen.blit(map_surf, map_surf_rect)

                level_surf = self.FONT.render('Level %s of %s' % (current_level_index + 1, len(levels)), 1, self.settings.TEXTCOLOR)
                level_rect = level_surf.get_rect()
                level_rect.bottomleft = (20, self.settings.WINHEIGHT - 35)
                self.screen.blit(level_surf, level_rect)

                step_surf = self.FONT.render('Steps: %s' % (game_state_obj['step_counter']), 1, self.settings.TEXTCOLOR)
                step_rect = step_surf.get_rect()
                step_rect.bottomleft = (20, self.settings.WINHEIGHT - 10)
                self.screen.blit(step_surf, step_rect)

                # draw button
                self.screen.blit(self.images.IMAGES_DICT['button'], button_rect)

                # decorate
                goku_decorate_rect = self.images.IMAGES_DICT['goku_decorate'].get_rect()
                goku_decorate_rect.x = self.settings.WINWIDTH - 100
                goku_decorate_rect.y = self.settings.WINHEIGHT - 100
                self.screen.blit(self.images.IMAGES_DICT['goku_decorate'], goku_decorate_rect)

                if level_is_complete:
                    # show the "win" image until the player has pressed a key.
                    win_rect = self.images.IMAGES_DICT['win'].get_rect()
                    win_rect.center = (self.settings.HALF_WINWIDTH, self.settings.HALF_WINHEIGHT)
                    self.screen.blit(self.images.IMAGES_DICT['win'], win_rect)
                    if key_pressed:
                        return 'win'

                pygame.display.update() # draw screen to the screen.
        
        def exit(self):
            pygame.quit()
            sys.exit()
        
    if __name__ == '__main__':
        # Make a game instance, and run the game.
        game = Main()
        game.run_game()
except Exception as bug:
    print(bug)

input()