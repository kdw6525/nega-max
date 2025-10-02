"""
piece.py

Create piece class:
1. id in piece list
2. row in board
3. col in board
4. png for display
5. move generation function
"""

import moves
from typing import List

class Piece:
    # init a piece obj, should mostly stay the same except updates over time
    def __init__(self, id:int, r:int, c:int, color:bool, png, generation, promotion):
        self.id = id
        self.r = r
        self.c = c
        self.color = color
        self.png = png
        self.mv_generation = generation
    
    def update_piece(self, new_png, new_generation):
        self.png = new_png
        self.mv_generation = new_generation
    

