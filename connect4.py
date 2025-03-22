import random
import copy


class Connect4:
    
    def __init__(self):
        self.board = [['0' for i in range(7)] for j in range(6)]


    def update_board(self, symbol, i , j):
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

class Connect4_bot:
    def __init__(self, level, connect4_game, symbol):
        self.level = level
        self.connect4_game = connect4_game
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
            move = self.minimax(self.connect4_game.board)

        self.connect4_game.board[move[0]][move[1]] = self.symbol
        return move
    
    def random(self): 
        empty_indexes = Connect4_bot.get_empty_indexes(self.connect4_game.board)

        if empty_indexes:
            random_index = random.choice(empty_indexes)
            print("Random empty index:", random_index)
        else:
            print("No empty spaces left.")

        return random_index

            
    def rule_based(self):
        empty_indexes = Connect4_bot.get_empty_indexes(self.connect4_game.board)

        for index in empty_indexes:
            board_copy = copy.deepcopy(self.connect4_game.board)
            board_copy[index[0]][index[1]] = self.apponent_symbol
            
            if Connect4.check_winner(board_copy) == self.apponent_symbol:
                print(f"found : {index}")
                return index
        
        random_index = random.choice(empty_indexes)
        print(f"random : {random_index}")
        return random_index
        

    def minimax(self, board):
        best_score = -float("inf")
        best_move = None

        for index in Connect4_bot.get_empty_indexes(board):
            board_copy = copy.deepcopy(board)
            board_copy[index[0]][index[1]] = self.symbol  # AI's move

            score = self.get_best_score(board_copy, self.apponent_symbol, -float("inf"), float("inf"))

            if score > best_score:
                best_score = score
                best_move = index

        return best_move

    def get_best_score(self, board, symbol, alpha, beta):
        # Check if the current board has a winner or is a draw
        winner = Connect4.check_winner(board)
        if winner == self.symbol:  
            return 1
        elif winner == self.apponent_symbol:  
            return -1
        elif not Connect4_bot.get_empty_indexes(board):  
            return 0  # Draw (no more moves)

        empty_indexes = Connect4_bot.get_empty_indexes(board)

        if symbol == self.symbol:  # Maximizing player (AI)
            best_score = -float("inf")
            for index in empty_indexes:
                board_copy = copy.deepcopy(board)
                board_copy[index[0]][index[1]] = symbol  # Make the move

                score = self.get_best_score(board_copy, "X" if symbol == "O" else "O", alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:  # Prune the search
                    break

            return best_score

        else:  # Minimizing player (Opponent)
            best_score = float("inf")
            for index in empty_indexes:
                board_copy = copy.deepcopy(board)
                board_copy[index[0]][index[1]] = symbol  # Make the move

                score = self.get_best_score(board_copy, "X" if symbol == "O" else "O", alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:  # Prune the search
                    break

            return best_score



connect4 = Connect4()

connect4.board = [['0', '0', '0', '0', '0', 'X', 'X'], 
                  ['X', '0', '0', 'X', '0', '0', '0'], 
                  ['X', '0', '0', 'X', 'X', '0', 'X'], 
                  ['0', 'X', 'X', '0', '0', 'X', 'X'], 
                  ['0', '0', 'X', '0', '0', '0', '0'], 
                  ['X', '0', '0', 'X', 'X', '0', 'X']]

print(Connect4.check_winner(connect4.board))