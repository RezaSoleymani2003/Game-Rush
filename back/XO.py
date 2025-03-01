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
            if ''.join(row) == "xxx":
                return 'x'
            
            if ''.join(row) == "ooo":
                return 'o'

        for i in range(3):
            col = [self.board[0][i], self.board[1][i], self.board[2][i]]   

            if ''.join(col) == "xxx":
                return 'x'
            
            if ''.join(col) == "ooo":
                return 'o' 

        main_diagonal = ''.join([self.board[0][0], self.board[1][1], self.board[2][2]])
        secondry_diagonal = ''.join([self.board[0][2], self.board[1][1], self.board[2][0]])

        if main_diagonal == "xxx" or secondry_diagonal == "xxx" :
            return 'x'

        if main_diagonal == "ooo" or secondry_diagonal == "ooo" :
            return 'o'

        return '0'

    

xo = XO()
xo.board = [
    ['x','x','x'],
    ['0','o','o'],
    ['0','0','0'],
]

# xo.update_board('x', 1, 1)
print(xo.check_winner())
print(xo.board)
# a = ['x', 'x', 'x']
# # a = str(a)
# print(''.join(a))