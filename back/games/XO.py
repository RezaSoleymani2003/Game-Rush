import random
import copy

class XO:
    def __init__(self):
        self.board = [['0', '0', '0'] for i in range(3)]
        self.step = 0
    
    def check_end(self):
        return self.step == 9 or self.check_winner() != '0'
        
    def update_board(self, symbol, i , j):
        self.step += 1
        self.board[i][j] = symbol
    
    def check_winner(board):
        for row in board:
            if ''.join(row) == "XXX":
                return 'X'
            
            if ''.join(row) == "OOO":
                return 'O'

        for i in range(3):
            col = [board[0][i], board[1][i], board[2][i]]   

            if ''.join(col) == "XXX":
                return 'X'
            
            if ''.join(col) == "OOO":
                return 'O' 

        main_diagonal = ''.join([board[0][0], board[1][1], board[2][2]])
        secondry_diagonal = ''.join([board[0][2], board[1][1], board[2][0]])

        if main_diagonal == "XXX" or secondry_diagonal == "XXX" :
            return 'X'

        if main_diagonal == "OOO" or secondry_diagonal == "OOO" :
            return 'O'

        return '0'

class XO_bot:
    def __init__(self, level, xo_game, symbol):
        self.level = level
        self.xo_game = xo_game
        self.symbol = symbol
        self.apponent_symbol = 'O' if self.symbol == 'X' else 'X'


    def get_empty_indexes(board):
        empty_indexes = [
            (i, j) 
            for i, row in enumerate(board)  
            for j, e in enumerate(row)  
            if e == '0'  
        ]
        return empty_indexes

    def make_move(self):
        move = ""
        if self.level == "random":
            move = self.random()

        if self.level == "rule based":
            move = self.rule_based() 

        if self.level == "minimax":
            move = self.minimax(self.xo_game.board, self.symbol)

        self.xo_game.board[move[0]][move[1]] = self.symbol
        return move
    
    def random(self): 
        empty_indexes = XO_bot.get_empty_indexes(self.xo_game.board)

        if empty_indexes:
            random_index = random.choice(empty_indexes)
            print("Random empty index:", random_index)
        else:
            print("No empty spaces left.")

        return random_index

            
    def rule_based(self):
        empty_indexes = XO_bot.get_empty_indexes(self.xo_game.board)


        for index in empty_indexes:
            board_copy = copy.deepcopy(self.xo_game.board)
            board_copy[index[0]][index[1]] = self.apponent_symbol
            
            if XO.check_winner(board_copy) == self.apponent_symbol:
                print(f"found : {index}")
                return index
        
        random_index = random.choice(empty_indexes)
        print(f"random : {random_index}")
        return random_index
        


    def minimax(self, board, symbol):
        empty_indexes = XO_bot.get_empty_indexes(board)
        viewed = {index: False for index in empty_indexes}

        for index in viewed.keys():
            if not viewed[index]:
                board_copy = copy.deepcopy(board)
                board_copy[index[0]][index[1]] = symbol
                viewed[index] = True

                new_symbol = "X" if symbol == "O" else "X"

                if XO.check_winner(board_copy) == self.symbol:
                    return index
                self.minimax(board_copy, new_symbol)
        




xo = XO()
xo.board = [
    ['O','O','X'],
    ['X','O','O'],
    ['0','0','X'],
]

bot = XO_bot("minimax", xo, 'O')

# Xo.update_board('X', 1, 1)
# print(xo.check_winner())
print(xo.board)
print()
bot.make_move()

print(xo.board)

# a = ['X', 'X', 'X']
# a = str(a)
# print(''.join(a))