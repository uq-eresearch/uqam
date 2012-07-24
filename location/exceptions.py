

class IllegalMove(Exception):
    """
    Illegal attempt to restructure the tree
    """
    pass


class SameLevelMove(IllegalMove):
    """
    Cannot move to a parent at the same level of the tree
    """
    pass


class WrongLevelMove(IllegalMove):
    """
    Can only move to a valid new parent
    """
    pass
