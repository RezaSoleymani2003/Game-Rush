class Connect4:
    
    def __init__(self):
        self.board = [['0' for i in range(7)] for j in range(6)]


    def update_board(self, symbol, i , j):
        self.step += 1
        self.board[i][j] = symbol

    def check_winner(board):
        get_winner = {"XXXX" : "X", "OOOO" : "O"}

        for i in range(6):
            for j in range(4):
                line = ''.join([board[i][j], board[i][j+1], board[i][j+2], board[i][j+3]])

                val = get_winner.get(line)
                if val != None:
                    return val

        for j in range(7):
            for i in range(3):
                line = ''.join([board[i][j], board[i+1][j], board[i+2][j], board[i+3][j]])

                val = get_winner.get(line)
                if val != None:
                    return val

        for i in range(3):
            for j in range(4):
                line = ''.join([board[i][j], board[i+1][j+1], board[i+2][j+2], board[i+3][j+3]])

                val = get_winner.get(line)
                if val != None:
                    return val

        for i in range(0,3):
            for j in range(3,7):
                line = ''.join([board[i][j], board[i+1][j-1], board[i+2][j-2], board[i+3][j-3]])

                val = get_winner.get(line)
                if val != None:
                    return val
              
        return "0"





connect4 = Connect4()

connect4.board = [['0', '0', '0', '0', '0', 'X', 'X'], 
                  ['X', '0', '0', 'X', '0', '0', '0'], 
                  ['X', '0', '0', 'X', 'X', '0', 'X'], 
                  ['0', 'X', 'X', '0', '0', 'X', 'X'], 
                  ['0', '0', 'X', '0', '0', '0', '0'], 
                  ['X', '0', '0', 'X', 'X', '0', 'X']]

print(Connect4.check_winner(connect4.board))