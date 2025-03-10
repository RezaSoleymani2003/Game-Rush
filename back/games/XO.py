class XO:
    def __init__(self):
        self.board = [['0', '0', '0'] for i in range(3)]
        self.step = 0

    def check_end(self):
        return self.step == 9 or self.check_winner() != '0'
        
    def update_board(self, symbol, i , j):
        self.step += 1
        self.board[i][j] = symbol
    
    def check_winner(self):
        for row in self.board:
            if ''.join(row) == "XXX":
                return 'X'
            
            if ''.join(row) == "OOO":
                return 'O'

        for i in range(3):
            col = [self.board[0][i], self.board[1][i], self.board[2][i]]   

            if ''.join(col) == "XXX":
                return 'X'
            
            if ''.join(col) == "OOO":
                return 'O' 

        main_diagonal = ''.join([self.board[0][0], self.board[1][1], self.board[2][2]])
        secondry_diagonal = ''.join([self.board[0][2], self.board[1][1], self.board[2][0]])

        if main_diagonal == "XXX" or secondry_diagonal == "XXX" :
            return 'X'

        if main_diagonal == "OOO" or secondry_diagonal == "OOO" :
            return 'O'

        return '0'

    
# Xo = XO()
# Xo.board = [
#     ['X','X','X'],
#     ['0','O','O'],
#     ['0','0','0'],
# ]

# # Xo.update_board('X', 1, 1)
# print(Xo.check_winner())
# print(Xo.board)
# # a = ['X', 'X', 'X']
# # a = str(a)
# print(''.join(a))