"""
zobrist_hashing.py
Implement zobrist hashing:

Usage: python3 zobrist_hashing.py [-g]
test functions implemented in the file
-g: checks if tt (transposition table) file or zobrist file exists, 
    if one exists we do nothing, if not we generate them

Max hash value is the max num of np.uint32

Value (evaluation heuristic? Or even if it is a win?) (10 bit)
Type of value (flag, exact val, lower bound, upper bound) (2 bits)
Best move/action (rs, cs, re, ce) (max val is 7) so we just need (3 bits each) (12) or just move class?
Search depth (how far we went past this to verify how good it was) (4 bits)
Identification of the position (the hashing) <= zobrist hashing, do XOR on all the positions of the pieces. Make a random number for every position a piece can be in. This means 6 pieces, 40 spots… 6 * 40 = 240 random numbers (not so bad)

32 + 4 + 12 + 2 + 10 = 60 bit for each entry (fits in a 64 bit int)
"""

import numpy as np
import struct
from moves import Move

TT_LEN = 5000000 # 2 million takes 50 mbs, 5 million takes 127 mbs (this is acceptable for me)

class TT_Entry:
    # entry to the table, storing elements described above
    def __init__(self, value:np.int16, depth:np.uint8, flag:np.uint8, best_move: Move):
        self.value = value # heuristic found for this state
        self.depth = depth # the depth where we found this 
        self.flag = flag # 0 = exact, 1 = lower, 2 = upper
        self.best_move = best_move # simply the best move, we will need to update the piece references after verifying
    

def tt_store(tt:np.typing.ArrayLike, key: np.uint32, value:int, depth:int, flag:int, best_move: Move):
    i = key % len(tt)
    tt[i] = TT_Entry(value=value, depth=depth, flag=flag, best_move=best_move)
        
def tt_lookup(tt:np.typing.ArrayLike, key: int) -> TT_Entry:
    i = key % len(tt)
    return tt[i]

def tt_write(tt:np.typing.ArrayLike, fname='tt'):
    # save current tt file
    np.save(fname, tt)

def tt_load(fname='tt.npy') -> np.typing.ArrayLike:
    return np.load(fname, allow_pickle=True)

def zobrist_make(fname='zb'):
    # ran only if zobrist file is not found when running this file
    zobrist = np.random.randint(low=0, high=4294967295, size=(6, 40), dtype=np.uint32)
    np.save(fname, zobrist)

def zobrist_load(fname='zb.npy') -> np.typing.ArrayLike:
    # read zobrist file and return the loaded array
    return np.load(fname, allow_pickle=False)


def main():
    import sys  
    from os.path import isfile

    if len(sys.argv) == 1:
        print('-g to generate a zobrist random number and tt storage file')
        print('-t to test zobrist hashing functions')
        print('-n remove the current zb.npy & tt.npy files and regenerate them')

    if sys.argv[-1] == "-g":
        if not isfile('tt.bin'):
            tt = np.empty(shape=TT_LEN, dtype=object)
            tt_write(tt=tt)
        if not isfile('zb.npy'):
            zobrist_make()
    
    if sys.argv[-1] == "-n":
        tt = np.empty(shape=TT_LEN, dtype=object)
        tt_write(tt=tt)
        zobrist_make()

    if sys.argv[-1] == "-t":
        from piece import Piece, white_pawn_evaluation, black_pawn_evaluation
        from moves import white_pawn_moves, black_pawn_moves

        tt = tt_load()
        tt_test = np.copy(tt)
        zb = zobrist_load()
        p1 = Piece(0, 3, 1, True, 'wp', white_pawn_moves, white_pawn_evaluation)
        p2 = Piece(1, 2, 2, False, 'bp', black_pawn_moves, black_pawn_evaluation)

        test_mv = Move(piece=p1, rs=p1.r, cs=p1.c, re=2, ce=1, capture=None, promotion=False, enpassant=False, enpassant_cap=False)
        for k in range(len(tt_test)):
            tt_store(tt=tt_test, key=k, value=34, depth=5, flag=0, best_move=test_mv)

        entry = tt_lookup(tt=tt_test, key=0)
        print(entry.best_move)

        tt_write(tt=tt_test, fname='tt_test')

        tt_test_reload = tt_load(fname='tt_test.npy')
        entry_reload = tt_lookup(tt=tt_test_reload, key=0)
        print(entry_reload.best_move)

        print(entry.best_move is entry_reload.best_move)



    # zb = load_zobrist()
    # print(zb)
        
    return

if __name__ == "__main__":
    main()