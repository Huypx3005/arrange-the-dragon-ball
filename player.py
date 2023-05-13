class Player():
    def make_move(self, map_obj, game_state_obj, direction, map):
        """Returns True if the player moved, otherwise False"""

        player_x, player_y = game_state_obj['player']
        dragon_balls = game_state_obj['dragon_ball']

        if direction == "up":
            x_set = 0
            y_set = -1
        elif direction == "right":
            x_set = 1
            y_set = 0
        elif direction == "down":
            x_set = 0
            y_set = 1
        elif direction == "left":
            x_set = -1
            y_set = 0

        # See if the player can move in that direction.
        if map.is_wall(map_obj, player_x + x_set, player_y + y_set):
            return False
        else:
            # There is a dragon ball in the way, see if the player can push it.
            if (player_x + x_set, player_y + y_set) in dragon_balls:
                if not map.is_blocked(map_obj, game_state_obj, player_x + (x_set*2), player_y + (y_set*2)):
                    # Move the star.
                    ind = dragon_balls.index((player_x + x_set, player_y + y_set))
                    dragon_balls[ind] = (dragon_balls[ind][0] + x_set, dragon_balls[ind][1] + y_set)
                else:
                    return False
            # Set new position for player
            game_state_obj['player'] = (player_x + x_set, player_y + y_set)
            return True
