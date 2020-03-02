from dataclasses import dataclass

@dataclass
class Player:
    index : int
    name : str
    score : int
    duration : int
