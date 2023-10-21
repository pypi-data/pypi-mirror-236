from .team import Team
from functools import cached_property


class Match(object):
    def __init__(self, 
                 radiant: Team, 
                 dire: Team, 
                 *, 
                 map: int=None, 
                 championship: str=None, 
                 id: int=None) -> None:
        self.radiant = radiant
        self.dire = dire
        self.map = map
        self.championship = championship
        self.id = id
    
    @cached_property
    def winner(self):
        if self.radiant.is_winner:
            return self.radiant
        if self.dire.is_winner:
            return self.dire
        return None

    @cached_property
    def loser(self):
        if self.winner is self.radiant:
            return self.dire
        if self.winner is self.dire:
            return self.radiant
        return None
    
    @cached_property
    def heroes(self):
        _heroes = self.radiant.heroes + self.dire.heroes
        return _heroes