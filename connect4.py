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
    def __init__(self, level, connect4_game, symbol, max_depth=3):
        self.level = level
        self.connect4_game = connect4_game
        self.symbol = symbol
        self.apponent_symbol = 'O' if self.symbol == 'X' else 'X'
        self.max_depth = max_depth


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
        board = self.connect4_game.board

        empty_indexes = Connect4_bot.get_empty_indexes(board)


        for index in empty_indexes:
            board_copy = copy.deepcopy(board)
            board_copy[index[0]][index[1]] = self.symbol
            
            if Connect4.check_winner(board_copy) == self.symbol:
                print(f"found : {index}")
                return index

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  
        for row in range(6):
            for col in range(7):
                if board[row][col] == self.apponent_symbol:
                    for dr, dc in directions:
                        r1, c1 = row + dr, col + dc
                        r2, c2 = row + 2 * dr, col + 2 * dc

                        if 0 <= r1 < 6 and 0 <= c1 < 7 and board[r1][c1] == self.apponent_symbol:
                            if 0 <= r2 < 6 and 0 <= c2 < 7 and board[r2][c2] == '0':
                                return (r2, c2)

        for index in empty_indexes:
            board_copy = copy.deepcopy(board)
            board_copy[index[0]][index[1]] = self.apponent_symbol
            
            if Connect4.check_winner(board_copy) == self.apponent_symbol:
                print(f"found : {index}")
                return index
        
        for index in empty_indexes:
            x = index[0]
            y = index[1]

            adj_cells = [(x,y+1),(x+1,y),(x,y-1),(x-1,y),(x+1,y-1),(x-1,y+1),(x+1,y+1),(x-1,y-1)]

            for cell in adj_cells:
                try:
                    if board[cell[0]][cell[1]] == self.apponent_symbol:
                        return index

                except:
                    continue

        random_index = random.choice(empty_indexes)
        print(f"random : {random_index}")
        return random_index
        
    def evaluate_board(self, board):
        score = 0
        def score_line(line):
            nonlocal score
            line_str = "".join(line)
            
            if "XXXX" in line_str:  
                return 100
            elif "OOOO" in line_str:  
                return -100
            elif "XXX0" in line_str or "0XXX" in line_str or "X0XX" in line_str or "XX0X" in line_str:
                score += 10  
            elif "OOO0" in line_str or "0OOO" in line_str or "O0OO" in line_str or "OO0O" in line_str:
                score -= 10  
            elif "XX00" in line_str or "00XX" in line_str or "X00X" in line_str:
                score += 5
            elif "OO00" in line_str or "00OO" in line_str or "O00O" in line_str:
                score -= 5
        
        for row in board:
            for i in range(4):
                score_line(row[i:i+4])
        
        for col in range(7):
            for row in range(3):
                score_line([board[row + i][col] for i in range(4)])
        
        for row in range(3):
            for col in range(4):
                score_line([board[row + i][col + i] for i in range(4)])

        for row in range(3):
            for col in range(3, 7):
                score_line([board[row + i][col - i] for i in range(4)])

        center_column = [board[row][3] for row in range(6)]
        score += center_column.count(self.symbol) * 3
        score -= center_column.count(self.apponent_symbol) * 3
        
        return score

    def get_best_score(self, board, symbol, alpha, beta, depth):
        winner = Connect4.check_winner(board)
        
        if winner == self.symbol:  
            return 100
        elif winner == self.apponent_symbol:  
            return -100
        elif not Connect4_bot.get_empty_indexes(board):
            return 0
        elif depth == 0:  
            return self.evaluate_board(board)

        empty_indexes = Connect4_bot.get_empty_indexes(board)

        if symbol == self.symbol: 
            best_score = -float("inf")
            for index in empty_indexes:
                board_copy = copy.deepcopy(board)
                board_copy[index[0]][index[1]] = symbol  

                score = self.get_best_score(board_copy, self.apponent_symbol, alpha, beta, depth - 1)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:  
                    break

            return best_score

        else: 
            best_score = float("inf")
            for index in empty_indexes:
                board_copy = copy.deepcopy(board)
                board_copy[index[0]][index[1]] = symbol  

                score = self.get_best_score(board_copy, self.symbol, alpha, beta, depth - 1)
                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:  # Prune
                    break

            return best_score

    def minimax(self, board):
        best_score = -float("inf")
        best_move = None

        for index in Connect4_bot.get_empty_indexes(board):
            board_copy = copy.deepcopy(board)
            board_copy[index[0]][index[1]] = self.symbol  

            score = self.get_best_score(board_copy, self.apponent_symbol, -float("inf"), float("inf"), self.max_depth)

            if score > best_score:
                best_score = score
                best_move = index

        return best_move


connect4 = Connect4()

connect4.board = [['O', 'O', 'X', 'O', 'X', 'O', 'X'],
                  ['0', 'X', 'O', '0', 'X', 'X', 'O'], 
                  ['O', '0', 'X', 'X', 'O', 'X', 'O'], 
                  ['X', '0', 'O', 'X', '0', 'O', 'O'], 
                  ['0', '0', 'X', 'O', 'O', 'X', 'X'], 
                  ['0', 'O', '0', 'X', '0', '0', '0']]
bot = Connect4_bot("minimax", connect4, "O")
print(bot.make_move())
print(Connect4.check_winner(connect4.board))