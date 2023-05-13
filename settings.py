class Settings:
    """A class to store all settings for game."""

    def __init__(self):

        # self.BGCOLOR = (168, 160, 160) 
        self.BGCOLOR = (80, 120, 160) 
        # self.TEXTCOLOR = (38, 38, 38) 
        self.TEXTCOLOR = (255, 255, 255) 
 
        self.WINWIDTH = 800
        self.WINHEIGHT = 600
        self.HALF_WINWIDTH = int(self.WINWIDTH / 2)
        self.HALF_WINHEIGHT = int(self.WINHEIGHT / 2)

        # The total width and height of each tile in pixels.
        self.TILE_WIDTH = 50
        self.TILE_HEIGHT = 85
        self.TILE_FLOOR_HEIGHT = 40

        # decoration on them, such as a tree or rock.
        self.OUTSIDE_DECORATION_PCT = 20