class Connect4:
    
    def __init__(self):
        self.grid = [['0' for i in range(7)] for j in range(6)]


    def update_board(self, symbol, i , j):
        self.step += 1
        self.board[i][j] = symbol

    
    





connect4 = Connect4()

print(connect4.grid)