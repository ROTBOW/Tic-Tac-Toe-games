'''
Made 3d tic tac toe bc its fun
It was also written with typing throughout.

I wrote this code like 4-7 months ago I forgor how half of it works
'''
from os import system
from typing import Callable

from numpy import transpose as trans  # type: ignore

# constants
clear = lambda: system('clear')
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'

class Game:

    def __reset(self) -> None:
        gen_board = lambda: [["_"]*3 for _ in range(3)]
        self.level1: list[list[str]] = gen_board()
        self.level2: list[list[str]] = gen_board()
        self.level3: list[list[str]] = gen_board()
        self.levels = [self.level1, self.level2, self.level3]
        self.turn = True
        
        
    def vaild_ans(self, ans:str) -> list[bool|list[str|int]]:
        res: list[bool|list[str|int]] = [False, [], []]
        ans_list = ans.strip().split()
        
        if len(ans_list) != 3:
            res[1].append('Incorrect count of inputs!')  # type: ignore
        
        get_title: Callable[[int], str] = lambda x: {0: 'Level', 1: 'Row', 2: 'Col'}[x]
        for idx, num in enumerate(ans_list):
            n = num.strip()
            if not n.isdigit():
                res[1].append(f'{get_title(idx)} {num} is not a number!') # type: ignore
                continue
            if not 0 <= int(n)-1 < 3:
                res[1].append(f'{get_title(idx)} {n} is not on the board!') # type: ignore
            
        if len(res[1]) > 0: # type: ignore
            return res
        if self.__get_at(*[int(x)-1 for x in ans_list]) != '_':
            res[1].append('That spot is taken!') # type: ignore
            return res
            
        
        res[0] = True
        res[2] = [int(x)-1 for x in ans_list] # type: ignore
        return res
    
    
    def place_at(self, lvl: int, row: int, col: int) -> None:
        level = {0: self.level1, 1: self.level2, 2: self.level3}[lvl]
        level[row][col] = self.place_token()
       
        
    def __get_at(self, lvl: int, row: int, col: int) -> str:
        level = {0: self.level1, 1: self.level2, 2: self.level3}[lvl]
        return level[row][col]
    
    
    def __vert_check(self, board: list[list[str]]) -> bool:
        return self.__hori_check(trans([x.copy() for x in board]))  # type: ignore
    
    
    def __hori_check(self, board: list[list[str]]) -> bool:
        return any(map(
            lambda x: len(set(x)) == 1 and x[0] != '_',
            board
        ))
        
        
    def __dia_check(self, board: list[list[str]]) -> bool:
        left = list(map(
            lambda x: board[x[0]][x[1]],
            [[0, 0], [1, 1], [2, 2]]
        ))
        right = list(map(
            lambda x: board[x[0]][x[1]],
            [[0,2], [1, 1], [2, 0]]
        ))
        if left[0] == '_' or right[0] == '_':
            return False

        if len(set(left)) == 1 or len(set(right)) == 1:
            return True
        return False


    def __init__(self) -> None:
        self.place_token = lambda: RED+'X'+END if self.turn else GREEN+'O'+END
        self.__reset()


    def show(self) -> None:
        clear()
        print('      1  2  3')
        for level_idx, level in enumerate(self.levels):
            for row_idx, row in enumerate(level):
                print('    ', end='')
                for col_idx, col in enumerate(row):
                    row_str = f'{row_idx+1}' if level_idx == 0 and col_idx == 0 else ' '
                    print(' '*(row_idx)+row_str, col, end='')
                level_str = f'--------LEVEL {level_idx+1}'
                print(f'{level_str if row_idx == 0 else ""}')
            print()
            
            
    def move(self) -> None:
        print(f'Your turn {self.place_token()}!')
        print('enter your move as: level row col\nUse Spaces to separate them!')
        while True:
            ans = input('-> ')
            status, err, new_ans = self.vaild_ans(ans)
            if status:
                break
            print('\n'.join(err))       # type: ignore
        level, row, col = new_ans        # type: ignore
        self.place_at(level, row, col) # type: ignore
        self.turn = not self.turn
        
        
    def level_check(self, lvl: list[list[str]]) -> bool:
        return any([
            self.__hori_check(lvl),
            self.__vert_check(lvl),
            self.__dia_check(lvl)
        ])
        
    def vert_level_win(self) -> bool:
        for row in range(3):
            for col in range(3):
                test: set[str] = set()
                for lvl in range(3):
                    test.add(self.levels[lvl][row][col])
                if '_' not in test and len(test) == 1:
                    return True
        
        return False
    
    def dia_level_win(self) -> bool:
        lleft: list[list[int]] = [[0, 0], [1, 1], [2, 2]] # lvl, row
        lright: list[list[int]] = [[0, 2], [1, 1], [2, 0]]
        
        for suit in [lleft, lright]:
            for col in range(3):
                test: set[str] = set()
                for lvl, row in suit:
                    test.add(self.levels[lvl][row][col])
                if '_' not in test and len(test) == 1:
                    return True
                
        rleft: list[list[int]] = [[0, 0], [1, 1], [2, 2]] # lvl, col
        rright: list[list[int]] = [[0, 2], [1, 1], [2, 0]]
        for suit in [rright, rleft]:
            for row in range(3):
                test: set[str] = set()
                for lvl, col in suit:
                    test.add(self.levels[lvl][row][col])
                if '_' not in test and len(test) == 1:
                    return True
        
        lcorner: list[list[int]] = [[0, 0, 0], [2, 2, 2]]
        rcorner: list[list[int]] = [[0, 0, 2], [2, 2, 0]]
        llcorner: list[list[int]] = [[0, 2, 0], [2, 0, 2]]
        rrcorner: list[list[int]] = [[0, 2, 2], [2, 0, 0]]
        for suit in [lcorner, rcorner, rrcorner, llcorner]:
            test: set[str] = set([self.levels[1][1][1]])
            for lvl, row, col in suit:
                test.add(self.levels[lvl][row][col])
            if '_' not in test and len(test) == 1:
                return True
        
        return False
        
        
    def over(self) -> bool:
        if any([ self.level_check(level) for level in self.levels ]):
            return True
        
        if self.vert_level_win():
            return True
        
        if self.dia_level_win():
            return True
        
        return False
    
    
    def game_over(self) -> bool:
        self.turn = not self.turn
        print(RED+'GAME OVER'+END)
        print(f'Player {self.place_token()} won!')
        print('Would you like to play again?')
        while True:
            ans = input('-> ')
            if ans.lower() in ('yes', 'y'):
                return False
            if ans.lower() in ('no', 'n'):
                return True
            print('That isn\'t right...')
     
        
    def play(self) -> None:
        while True:
            if self.over():
                self.show()
                if self.game_over():
                    return
                self.__reset()
                
            game.show()
            game.move()
         
              
                
                
if __name__ == '__main__':
    game = Game()
    game.play()
