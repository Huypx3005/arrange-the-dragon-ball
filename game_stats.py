class GameStats:
    def __init__(self):
        self.current_level_index = 0

    def is_level_finished(self, level_obj, game_state_obj):
        """Returns True if all the goals have dragon ball in them."""
        for goal in level_obj['goals']:
            # Found a space with a goal but no dragon ball on it.
            if goal not in game_state_obj['dragon_ball']:
                return False
        return True