import os, random, copy
import pygame

class Map():
    def read_levels_file(self,filename):
        """Read data from text file"""

        assert os.path.exists(filename), 'Cann\'t find the levels file: %s' % (filename)
        with open(filename, 'r') as file:
            content = file.readlines() + ['\r\n']
        
        levels = [] # a list contain data of each level read from files
        lines_for_single_level = [] # contains the lines for a single level's map.
        object = [] # object read from the data in lines_for_single_level

        for line in content:
            line = line.rstrip('\r\n')

            # Each level must end with a blank line
            # ;   @ - The starting position of the player.
            # ;   $ - The starting position for a pushable star.
            # ;   . - A goal where a star needs to be pushed.
            # ;   + - Player & goal
            # ;   * - Star & goal
            # ;  (space) - an empty open space.
            # ;   # - A wall.
            # line = ';   @ - The starting position of the player.'

            if ';' in line:
                # Ignore the ; lines, they're comments in the level file.
                line = ''

            if line != '':
                # This line is part of the map.
                lines_for_single_level.append(line)
    
            # A blank line indicates the end of a level's map in the file.
            elif line == '' and len(lines_for_single_level) > 0:
                # Find the longest row in the map.
                max_width = -1
                for i in lines_for_single_level:
                    if len(i) > max_width:
                        max_width = len(i)

                # Add spaces to the ends of the shorter rows. This ensures the map will be rectangular.
                for i in range(len(lines_for_single_level)):
                    lines_for_single_level[i] += ' ' * (max_width - len(lines_for_single_level[i]))

                # Convert to a list object.
                for x in range(max_width):
                    object.append([])
                for y in range(len(lines_for_single_level)):
                    for x in range(max_width):
                        object[x].append(lines_for_single_level[y][x])

                # The x and y for the player's starting position
                start_x = None 
                start_y = None
                goals = [] # list of (x, y) tuples for each goal.
                dragon_ball = [] # list of (x, y) for each dragon ball's starting position.

                # find the @, ., and $ characters for the starting game state.
                for x in range(max_width):
                    for y in range(len(object[x])):
                        if object[x][y] in ('@'):
                            # '@' is player, '+' is player & goal
                            start_x = x
                            start_y = y
                        if object[x][y] in ('.', '*'):
                            # '.' is goal, '*' is dragon ball & goal
                            goals.append((x, y))
                        if object[x][y] in ('$', '*'):
                            # '$' is dragon ball
                            dragon_ball.append((x, y))        

                # Create level object and starting game state object.
                game_state_obj = {'player': (start_x, start_y),
                                'step_counter': 0,
                                'dragon_ball': dragon_ball}
                level_obj = {'width': max_width,
                            'height': len(object),
                            'object': object,
                            'goals': goals,
                            'start_state': game_state_obj}

                levels.append(level_obj)

                # Reset the variables for reading the next map.
                lines_for_single_level = []
                object = []
                game_state_obj = {}
                
        return levels
    
    def draw_map(self, object, game_state_obj, goals, main):
        """Draws the map to a Surface object, including the player and dragon ball. 
        Return the map_surf"""


        # The width and height must be calculated.
        map_surf_width = len(object) * main.settings.TILE_WIDTH
        map_surf_height = (len(object[0]) - 1) * main.settings.TILE_FLOOR_HEIGHT + main.settings.TILE_HEIGHT
        map_surf = pygame.Surface((map_surf_width, map_surf_height))
        map_surf.fill(main.settings.BGCOLOR) # start with a bg color on the surface.

        # Draw the tile sprites onto this surface.
        for x in range(len(object)):
            for y in range(len(object[x])):
                # space for each tile
                space_rect = pygame.Rect((x * main.settings.TILE_WIDTH, y * main.settings.TILE_FLOOR_HEIGHT,
                    main.settings.TILE_WIDTH, main.settings.TILE_HEIGHT))

                if object[x][y] in main.images.TILE_MAPPING:
                    base_tile = main.images.TILE_MAPPING[object[x][y]]
                elif object[x][y] in main.images.OUTSIDE_DECOMAPPING:
                    base_tile = main.images.TILE_MAPPING[' ']

                # First draw the base ground/wall tile.
                map_surf.blit(base_tile, space_rect)

                if object[x][y] in main.images.OUTSIDE_DECOMAPPING:
                    # Draw any tree/rock decorations that are on this tile.
                    map_surf.blit(main.images.OUTSIDE_DECOMAPPING[object[x][y]], space_rect)
                elif (x, y) in game_state_obj['dragon_ball']:
                    if (x, y) in goals:
                        # A goal & dragon ball are on this space, draw goal first.
                        map_surf.blit(main.images.IMAGES_DICT['covered goal'], space_rect)
                    # Then draw the dragon ball.
                    map_surf.blit(main.images.IMAGES_DICT['dragon_ball'], space_rect)
                elif (x, y) in goals:
                    # Draw a goal without a dragon ball on it.
                    map_surf.blit(main.images.IMAGES_DICT['uncovered goal'], space_rect)

                # Last draw the player
                if (x, y) == game_state_obj['player']:
                    map_surf.blit(main.images.PLAYER_IMAGES[main.images.current_image], space_rect)

        return map_surf
    
    def decorate_map(self, map_obj, start_xy, main):
        """Makes a copy of the given map object and modifies it.
        Here is what is done to it:
            * Walls that are corners are turned into corner pieces.
            * The outside/inside floor tile distinction is made.
            * Tree/rock decorations are randomly added to the outside tiles.
        Returns the decorated map object."""

        start_x, start_y = start_xy # Syntactic sugar

        # Copy the map object so we don't modify the original passed
        map_obj_copy = copy.deepcopy(map_obj)

        # Remove the non-wall characters from the map data
        for x in range(len(map_obj_copy)):
            for y in range(len(map_obj_copy[0])):
                if map_obj_copy[x][y] in ('$', '.', '@', '+', '*'):
                    map_obj_copy[x][y] = ' '

        # Flood fill to determine inside/outside floor tiles.
        self.flood_fill(map_obj_copy, start_x, start_y, ' ', 'o')

        # Convert the adjoined walls into corner tiles.
        for x in range(len(map_obj_copy)):
            for y in range(len(map_obj_copy[0])):

                if map_obj_copy[x][y] == '#':
                    if (self.is_wall(map_obj_copy, x, y-1) and self.is_wall(map_obj_copy, x+1, y)) or \
                    (self.is_wall(map_obj_copy, x+1, y) and self.is_wall(map_obj_copy, x, y+1)) or \
                    (self.is_wall(map_obj_copy, x, y+1) and self.is_wall(map_obj_copy, x-1, y)) or \
                    (self.is_wall(map_obj_copy, x-1, y) and self.is_wall(map_obj_copy, x, y-1)):
                        map_obj_copy[x][y] = 'x'

                elif map_obj_copy[x][y] == ' ' and random.randint(0, 99) < main.settings.OUTSIDE_DECORATION_PCT:
                    map_obj_copy[x][y] = random.choice(list(main.images.OUTSIDE_DECOMAPPING.keys()))

        return map_obj_copy

    def flood_fill(self, map_obj, x, y, old_character, new_character):
        """Changes any values matching oldCharacter on the map object to
        newCharacter at the (x, y) position, and does the same for the
        positions to the left, right, down, and up of (x, y), recursively."""

        if map_obj[x][y] == old_character:
            map_obj[x][y] = new_character

        if x < len(map_obj) - 1 and map_obj[x+1][y] == old_character:
            self.flood_fill(map_obj, x+1, y, old_character, new_character) # call right
        if x > 0 and map_obj[x-1][y] == old_character:
            self.flood_fill(map_obj, x-1, y, old_character, new_character) # call left
        if y < len(map_obj[x]) - 1 and map_obj[x][y+1] == old_character:
            self.flood_fill(map_obj, x, y+1, old_character, new_character) # call down
        if y > 0 and map_obj[x][y-1] == old_character:
            self.flood_fill(map_obj, x, y-1, old_character, new_character) # call up

    def is_wall(self, map_obj, x, y):
        """Returns True if the (x, y) position on
        the map is a wall, otherwise return False."""
        if x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):
            return False # x and y aren't actually on the map.
        elif map_obj[x][y] in ('#', 'x'):
            return True # wall is blocking
        return False

    def is_blocked(self, map_obj, game_state_obj, x, y):
        """Returns True if the (x, y) position on the map is
        blocked by a wall or star, otherwise return False."""

        if self.is_wall(map_obj, x, y):
            return True

        elif x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):
            return True # x and y aren't actually on the map.

        elif (x, y) in game_state_obj['dragon_ball']:
            return True # a star is blocking

        return False