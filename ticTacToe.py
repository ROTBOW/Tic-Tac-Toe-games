'''
just your basic tic tac toe game
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
        self.board = [list(['_']*3) for _ in range(3)]
        self.turn = True

    def __vaild(self, pos: list[int]) -> bool:
        row, col = pos
        if not 0 <= row < 3 or not 0 <= col < 3:
            return False

        if self.board[row][col] != '_':
            return False

        return True

    def __vert_check(self) -> bool:
        return self.__hori_check(trans([x.copy() for x in self.board]))  # type: ignore

    def __hori_check(self, board: list[list[str]]) -> bool:
        return any(map(
            lambda x: len(set(x)) == 1 and x[0] != '_',
            board
        ))

    def __dia_check(self) -> bool:
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
        clear()
        print('       1 2 3')
        for i in range(len(self.board)):
            print('    ', i+1, ' '.join(self.board[i]))
        print()

    def move(self) -> None:
        ans = ''
        print('Enter a move ( ie 1,1 )')
        while True:
            ans = input('-> ')
            ans = [int(x.strip())-1 for x in ans.split(',') if x.strip().isdigit()]
            if len(ans) == 2 and self.__vaild(ans):
                break
            print('that wasn\'t right')
        self.board[ans[0]][ans[1]] = self.place_token()
        self.turn = not self.turn

    def check_win(self) -> bool:
        return any([
            self.__hori_check(self.board),
            self.__vert_check(),
            self.__dia_check()
        ])

    def game_over(self) -> bool:
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
    
    def ask_for_bot(self) -> None:
        pass

    def play(self) -> None:
        self.ask_for_bot()
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

