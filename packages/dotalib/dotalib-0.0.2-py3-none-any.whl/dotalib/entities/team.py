from typing import Literal
from .hero import Hero, HeroSet
from enum import Enum
from ..exceptions import NumberOfPlayersError, HeroRepeatError


DEFAULT_NUMBER_OF_PLAYERS = 5


class Side(str, Enum):
    RADIANT = "radiant"
    DIRE = "dire"


class Team(object):
    def __init__(self, 
                 heroes: list[Hero], 
                 *,
                 side: Literal[Side.RADIANT, Side.DIRE]=None,
                 name: str=None, 
                 is_winner: bool=None,
                 no_repeat: bool=True,
                 five_players: bool=True) -> None:
        self.heroes = HeroSet(heroes)
        self.side = side
        self.name = name
        self.is_winner = is_winner
        if five_players and len(heroes) != DEFAULT_NUMBER_OF_PLAYERS:
            raise NumberOfPlayersError()
        if no_repeat and len(set(heroes)) != len(heroes):
            raise HeroRepeatError()


class Radiant(Team):
    def __init__(self, 
                 heroes: list[Hero], 
                 *,
                 name: str = None, 
                 is_winner: bool = None, 
                 no_repeat: bool=True,
                 five_players: bool=True) -> None:
        super().__init__(heroes, 
                         side=Side.RADIANT, 
                         name=name, 
                         is_winner=is_winner, 
                         no_repeat=no_repeat,
                         five_players=five_players)
    

class Dire(Team):
    def __init__(self, 
                 heroes: list[Hero], 
                 *,
                 name: str = None, 
                 is_winner: bool = None, 
                 no_repeat: bool=True,
                 five_players: bool=True) -> None:
        super().__init__(heroes, 
                         side=Side.DIRE, 
                         name=name, 
                         is_winner=is_winner, 
                         no_repeat=no_repeat,
                         five_players=five_players)