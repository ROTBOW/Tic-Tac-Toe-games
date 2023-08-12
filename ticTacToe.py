'''
Just your basic tic tac toe game

Going to add this to a repo of just cli games, that would be cool.
'''
from os import system

from numpy import transpose as trans  # type: ignore

# constants
clear = lambda: system('clear')
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'

class Game:

    def __reset(self) -> None:
        """
        The function resets the board and sets the turn to True, which would be X's turn.
        """
        self.board = [list(['_']*3) for _ in range(3)]
        self.turn = True

    def __vaild(self, pos: list[int]) -> bool:
        """
        The function checks if a given position on a 3x3 board is valid, meaning it is within the board
        boundaries and the position is empty.
        
        :param pos: The `pos` parameter is a list of two integers representing the position on the
        board. The first integer represents the row number and the second integer represents the column
        number
        :type pos: list[int]
        :return: a boolean value. It returns True if the position is valid (within the range of the
        board and the cell is empty), and False otherwise.
        """
        row, col = pos
        if not 0 <= row < 3 or not 0 <= col < 3:
            return False

        if self.board[row][col] != '_':
            return False

        return True

    def __vert_check(self) -> bool:
        """
        The function __vert_check checks if the transpose of the board is a valid vertical
        configuration.
        :return: the result of calling the `__hori_check` method with the transposed version of the
        `self.board` list.
        """
        return self.__hori_check(trans([x.copy() for x in self.board]))  # type: ignore

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

    def __dia_check(self) -> bool:
        """
        The function `__dia_check` checks if there is a winning diagonal line in a tic-tac-toe board.
        :return: a boolean value. It returns True if there is a diagonal win in the tic-tac-toe board,
        and False otherwise.
        """
        left = list(map(
            lambda x: self.board[x[0]][x[1]],
            [[0, 0], [1, 1], [2, 2]]
        ))
        right = list(map(
            lambda x: self.board[x[0]][x[1]],
            [[0,2], [1, 1], [2, 0]]
        ))
        if left[0] == '_' or right[0] == '_':
            return False

        if len(set(left)) == 1 or len(set(right)) == 1:
            return True
        return False
        

    def __init__(self) -> None:
        self.__reset()
        self.place_token = lambda: f'{RED}X{END}' if self.turn else f'{GREEN}O{END}'

    def show(self) -> None:
        """
        The function "show" clears the console, prints the current state of a board game, and adds row
        and column numbers for reference.
        """
        clear()
        print('       1 2 3')
        for i in range(len(self.board)):
            print('    ', i+1, ' '.join(self.board[i]))
        print()

    def move(self) -> None:
        """
        The function "move" prompts the user to enter a move, validates the input, and updates the game
        board accordingly.
        """
        ans = ''
        print(f'{self.place_token()} Enter a move ( ie 1,1 )')
        while True:
            ans = input('-> ')
            ans = [int(x.strip())-1 for x in ans.split(',') if x.strip().isdigit()]
            if len(ans) == 2 and self.__vaild(ans):
                break
            print('that wasn\'t right')
        self.board[ans[0]][ans[1]] = self.place_token()
        self.turn = not self.turn

    def check_win(self) -> bool:
        """
        The function checks if there is a win condition in the game board.
        :return: a boolean value.
        """
        return any([
            self.__hori_check(self.board),
            self.__vert_check(),
            self.__dia_check()
        ])

    def game_over(self) -> bool:
        """
        The function "game_over" prints the game over message, asks the player if they want to play
        again, and returns True if the player does not want to play again.
        :return: a boolean value. If the player chooses to play again, the function returns False. If
        the player chooses not to play again, the function returns True.
        """
        self.turn = not self.turn
        print('GAME OVER')
        print(f'Player {self.place_token()} won!')
        print('would you like to play again?')
        ans = ''
        while True:
            ans = input('-> ')
            if ans.lower() in ('yes', 'y', 'no', 'n'):
                break
            print('That isn\'t right')
        if ans.lower() in ('yes', 'y'):
            self.__reset()
            return False
        return True
    

    def play(self) -> None:
        """
        The "play" function is a loop that asks for user input, displays the game board, makes a move,
        checks for a win, and ends the game if it is over.
        """
        while True:
            self.show()
            self.move()


            if self.check_win():
                clear()
                self.show()
                if self.game_over():
                    break

            


if __name__ == '__main__':
    game = Game()
    game.play()

