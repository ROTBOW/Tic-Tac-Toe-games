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
        """
        The function initializes a Tic-Tac-Toe game board with three levels, each containing a
        3x3 grid of empty spaces represented by underscores, and sets the initial turn to be True, True being X's turn.
        """
        gen_board = lambda: [["_"]*3 for _ in range(3)]
        self.level1: list[list[str]] = gen_board()
        self.level2: list[list[str]] = gen_board()
        self.level3: list[list[str]] = gen_board()
        self.levels = [self.level1, self.level2, self.level3]
        self.turn = True
        
        
    def vaild_ans(self, ans:str) -> list[bool|list[str|int]]:
        """
        The function takes a string input and checks if it is a valid answer for a game. It
        returns a list with three elements: a boolean indicating if the answer is valid, a list of error
        messages if the answer is invalid, and a list of the parsed answer values if the answer is
        valid.
        
        :param ans: The `ans` parameter is a string that represents the user's answer. It is expected to
        be in the format of three space-separated numbers, where each number represents the level, row,
        and column of a spot on a board
        :type ans: str
        :return: The function `valid_ans` returns a list with three elements. The first element is a
        boolean value indicating whether the answer is valid or not. The second element is a list of
        strings, which contains any error messages or notifications about the invalidity of the answer.
        The third element is a list of integers, which represents the parsed and validated answer.
        """
        res: list[bool|list[str|int]] = [False, [], []]
        ans_list = ans.strip().split()
        
        if len(ans_list) != 3:
            res[1].append('Incorrect count of inputs!')  # type: ignore
        
        get_title: Callable[[int], str] = lambda x: {0: 'Level', 1: 'Row', 2: 'Col'}[x] # why did this need to be a lambda? couldn't it have just been a dict?
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
        """
        The function takes in a level number, row number, and column number, and places a
        token at the specified position in the corresponding level of a game.
        
        :param lvl: The `lvl` parameter is an integer that represents the level of the game. It is used
        to determine which level to access from the `level` dictionary
        :type lvl: int
        :param row: The `row` parameter represents the row index of the 2D grid where you want to place
        the token
        :type row: int
        :param col: The `col` parameter represents the column index where the token should be placed in
        the `level` grid
        :type col: int
        """
        level = {0: self.level1, 1: self.level2, 2: self.level3}[lvl]
        level[row][col] = self.place_token()
       
        
    def __get_at(self, lvl: int, row: int, col: int) -> str:
        """
        The function __get_at returns a string value from a specific position in a nested list based on
        the given level, row, and column.
        
        :param lvl: The `lvl` parameter is an integer that represents the level of the game. It is used
        to determine which level's data to access
        :type lvl: int
        :param row: The `row` parameter represents the row index of the desired element in the specified
        level of the object
        :type row: int
        :param col: The `col` parameter represents the column index of the element you want to retrieve
        from the specified level, row, and column
        :type col: int
        :return: a string.
        """
        level = {0: self.level1, 1: self.level2, 2: self.level3}[lvl]
        return level[row][col]
    
    
    def __vert_check(self, board: list[list[str]]) -> bool:
        """
        The function __vert_check checks if there is a vertical win in a given board.
        
        :param board: The parameter `board` is a 2-dimensional list of strings. It represents a game
        board where each element in the list represents a row, and each character in the row represents
        a cell on the board
        :type board: list[list[str]]
        :return: the result of calling the private method `__hori_check` with the transposed board as an
        argument.
        """
        return self.__hori_check(trans([x.copy() for x in board]))  # type: ignore
    
    
    def __hori_check(self, board: list[list[str]]) -> bool:
        """
        The function checks if there is a horizontal line of identical non-empty elements in a given
        board.
        
        :param board: The `board` parameter is a 2-dimensional list of strings. It represents a game
        board where each element in the list represents a row on the board. Each row is a list of
        strings, where each string represents a cell on the board
        :type board: list[list[str]]
        :return: a boolean value.
        """
        return any(map(
            lambda x: len(set(x)) == 1 and x[0] != '_',
            board
        ))
        
        
    def __dia_check(self, board: list[list[str]]) -> bool:
        """
        The function checks if there is a winning diagonal line in a tic-tac-toe board.
        
        :param board: The "board" parameter is a 2-dimensional list of strings. It represents a
        tic-tac-toe board, where each element in the list represents a cell on the board. The board is a
        3x3 grid, and each cell can contain one of three values: 'X',
        :type board: list[list[str]]
        :return: a boolean value.
        """
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
        """
        The function "show" prints a representation of a game board with multiple levels.
        It creates a 3d-ish illustration, there was an attempt.
        """
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
        """
        The function prompts the user for their move in a game, validates the input, and updates the
        game state accordingly.
        """
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
        """
        The function `level_check` checks if there is a winning combination in a given level of a game
        board.
        
        :param lvl: The `lvl` parameter is a 2-dimensional list of strings. It represents a level or
        grid of some sort, where each string represents a cell in the grid
        :type lvl: list[list[str]]
        :return: a boolean value.
        """
        return any([
            self.__hori_check(lvl),
            self.__vert_check(lvl),
            self.__dia_check(lvl)
        ])
        
    def vert_level_win(self) -> bool:
        """
        The function checks if there is a vertical win in a 3D tic-tac-toe game.
        :return: a boolean value. It returns True if there is a vertical win in the game, and False
        otherwise.
        """
        for row in range(3):
            for col in range(3):
                test: set[str] = set()
                for lvl in range(3):
                    test.add(self.levels[lvl][row][col])
                if '_' not in test and len(test) == 1:
                    return True
        
        return False
    
    def dia_level_win(self) -> bool:
        """
        The function `dia_level_win` checks if there is a diagonal or level win in a game.
        :return: The function `dia_level_win` returns a boolean value. It returns `True` if there is a
        diagonal or level win in the game, and `False` otherwise.
        
        oh gosh, this hurts to look at. its pretty hardcoded...
        """
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
        """
        The function checks if there is a win condition in a game by checking the levels, vertical
        levels, and diagonal levels.
        :return: a boolean value. It returns True if any of the conditions in the if statements are
        true, and False otherwise.
        """
        if any([ self.level_check(level) for level in self.levels ]):
            return True
        
        if self.vert_level_win():
            return True
        
        if self.dia_level_win():
            return True
        
        return False
    
    
    def game_over(self) -> bool:
        """
        The function "game_over" checks if the game is over, prints the game over message, asks the
        player if they want to play again, and returns True if they don't want to play again and False
        if they do.
        :return: The function `game_over` returns a boolean value. It returns `False` if the player
        wants to play again and `True` if the player does not want to play again.
        """
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
        """
        The function "play" is a loop that checks if the game is over, shows the current state of the
        game, and resets the game if necessary.
        :return: The `play` method does not explicitly return anything.
        """
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
