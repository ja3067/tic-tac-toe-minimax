import numpy as np
import re

n, m = 0, 0

class Board:
    def __init__(self, verbose = False):
        self.state = [['', '', ''], ['','',''], ['','','']]
        self.xwins = 0
        self.owins = 0
        self.draws = 0
        self._num_games = 0
        self.verbose = verbose

    def __getitem__(self, n):
        return self.state[n]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __str__(self):
        flat = [x for sublist in self.state for x in sublist]
        return "----------\n| {0} | {1} | {2} |\n|---------\n| {3} | {4} | {5} |\n|---------\n| {6} | {7} | {8} |\n---------".format(*flat)

    def num_games(self):
        self._num_games=self.xwins + self.owins + self.draws
        return self._num_games

    def getstate(self):
        return tuple(tuple(a) for a in self.state)

    def reset(self):
        self.state = [['', '', ''], ['','',''], ['','','']]
        self.gameover = False

    def check_win(self, player):
        return (any(all(self.state[i][j] == player for j in range(3)) for i in range(3)) or
                any(all(self.state[i][j] == player for i in range(3)) for j in range(3)) or
                all(self.state[i][i] == player for i in range(3)) or
                all(self.state[i][2 - i] == player for i in range(3)))

    def check_draw(self):
        return all(self.state[i][j] != '' for i in range(3) for j in range(3))

    def check_gameover(self):
        if self.check_win('o'):
            if self.verbose:
                print("o wins!")
            self.owins += 1
            return True
        if self.check_win('x'):
            if self.verbose:
                print("x wins!")
            self.xwins += 1
            return True
        if self.check_draw():
            if self.verbose:
                print("Draw!")
            self.draws += 1
            return True
        return False

def minimax(board, player, players, max):
    global m,n # number of complete tree searches, number of pruned trees

    if players[0] == player:
        other_player = players[1]
    else:
        other_player = players[0]

    if board.check_win(player):
        return 1
    if board.check_draw():
        return 0
    if board.check_win(other_player):
        return -1

    best_score = -2

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                if best_score >= max:
                    n +=1
                    return best_score
                board[i][j] = player
                subscore = - minimax(board, other_player, players, - best_score)
                board[i][j] = ''
                if subscore > best_score:
                    best_score = subscore

    m +=1

    if m % 100 == 0:
        print("number of complete searchs: {}, number of pruned branches: {}".format(m, n))
    return best_score

def find_move(board, player, players):


    if players[0] == player:
        other_player = players[1]
    else:
        other_player = players[0]

    best_score, index = -2, (0, 0)

    values = []
    for j in range(3):
        for i in range(3):
            if board[i][j] == '':
                board[i][j] = player
                subscore = - minimax(board, other_player, players, - best_score)
                values.append(subscore)
                board[i][j] = ''
                if subscore > best_score:
                    index = (i, j)
                    best_score = subscore
            else: values.append(-10)

    return index, values

def make_move(board, player, players):
    if board.check_gameover():
        return -1
    move, values = find_move(board, player, players)
    board[move[0]][move[1]] = player

    print("----------\n| {0} | {3} | {6} |\n|---------\n| {1} | {4} | {7} |\n|---------\n| {2} | {5} | {8} |\n---------".format(
        *values))

    return 0

def play_game():
    players = ['x', 'o']

    board = Board(verbose=True)

    while True:
        print(board)

        print("Play move:")

        move = input()
        moves = list(map(int, re.findall('\d+', move)))
        board[moves[0]][moves[1]] = 'o'
        print(board)

        if make_move(board, 'x', players) == -1:
            break

        print(board)

        if board.check_gameover() == True:
            break


if __name__ == "__main__":
    while True:
        play_game()
        print("To quit, press q. To play again, press any key.")
        if input() == 'q':
            break