import random
import copy
import math
import pickle

class Connect4:
    def __init__(self):
        self.board = [['0' for i in range(7)] for j in range(6)]

    def update_board(self, symbol, i , j):
        self.board[i][j] = symbol

    def check_winner(self):
        return self.__class__.check_winner_static(self.board)
    
    @staticmethod
    def check_winner_static(board):        
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

    def get_empty_indexes(self):
        empty_indexes = [
            (i, j) 
            for i, row in enumerate(self.board)  
            for j, e in enumerate(row)  
            if e == '0'  
        ]
        return empty_indexes
    

class Connect4_bot:
    def __init__(self, connect4_game, symbol, max_depth=3):
        self.connect4_game = connect4_game
        self.symbol = symbol
        self.opponent_symbol = 'O' if self.symbol == 'X' else 'X'
        self.max_depth = max_depth

    def evaluate_board(self):
        board = self.connect4_game.board

        # Check for a winner first, return high rewards if found
        winner = self.connect4_game.check_winner()
        if winner == self.symbol:
            return 10000  # RL bot wins
        elif winner == self.opponent_symbol:
            return -10000  # Opponent wins

        score = 0

        def score_line(line):
            nonlocal score
            line_str = "".join(line)

            # Check for a line of four of the same symbol
            if self.symbol * 4 in line_str:
                score += 100  # Favorable to the RL bot
            elif self.opponent_symbol * 4 in line_str:
                score -= 100  # Opponent winning line

            # Check for three in a row with one empty space
            elif self.symbol * 3 + '0' in line_str or '0' + self.symbol * 3 in line_str or self.symbol + '0' + self.symbol * 2 in line_str:
                score += 10  # One move away from winning
            elif self.opponent_symbol * 3 + '0' in line_str or '0' + self.opponent_symbol * 3 in line_str or self.opponent_symbol + '0' + self.opponent_symbol * 2 in line_str:
                score -= 10  # Opponent one move away from winning

            # Check for two in a row with two empty spaces
            elif self.symbol * 2 + '00' in line_str or '00' + self.symbol * 2 in line_str:
                score += 5  # Partial favorable line
            elif self.opponent_symbol * 2 + '00' in line_str or '00' + self.opponent_symbol * 2 in line_str:
                score -= 5  # Opponent partial favorable line

            return 0

        # Score rows
        for row in board:
            for i in range(4):
                score_line(row[i:i+4])

        # Score columns
        for col in range(7):
            for row in range(3):
                score_line([board[row + i][col] for i in range(4)])

        # Score diagonals (bottom-left to top-right)
        for row in range(3):
            for col in range(4):
                score_line([board[row + i][col + i] for i in range(4)])

        # Score diagonals (top-left to bottom-right)
        for row in range(3):
            for col in range(3, 7):
                score_line([board[row + i][col - i] for i in range(4)])

        # Center column preference (strategic advantage)
        center_column = [board[row][3] for row in range(6)]
        score += center_column.count(self.symbol) * 3
        score -= center_column.count(self.opponent_symbol) * 3

        return score


    def update_board(self, move):
        self.connect4_game.board[move[0]][move[1]] = self.symbol
    
    def create_bot(level, connect4_game, symbol):
        if level == "random":
            return Connect4_random_bot(connect4_game, symbol)
        
        if level == "rule based":
            return Connect4_rule_based_bot(connect4_game, symbol)

        if level == "rl":
            return Connect4_rl_bot(connect4_game, symbol)



class Connect4_random_bot(Connect4_bot):
    def make_move(self): 
        
        empty_indexes = self.connect4_game.get_empty_indexes()

        if empty_indexes:
            random_index = random.choice(empty_indexes)
            print("Random empty index:", random_index)
        else:
            print("No empty spaces left.")

        return random_index

class Connect4_rule_based_bot(Connect4_bot):
    def make_move(self):
        board = self.connect4_game.board

        empty_indexes = self.connect4_game.get_empty_indexes()
        
        # print("here", flush=True)

        for index in empty_indexes:
            board_copy = copy.deepcopy(board)
            board_copy[index[0]][index[1]] = self.symbol
            
            if Connect4.check_winner_static(board_copy) == self.symbol:
                # print(f"win found : {index}", flush=True)
                return index
        
        for index in empty_indexes:
            board_copy = copy.deepcopy(board)
            board_copy[index[0]][index[1]] = self.opponent_symbol
            
            if Connect4.check_winner_static(board_copy) == self.opponent_symbol:
                # print(f"win prevention found : {index}", flush=True)
                return index

        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  
        for row in range(6):
            for col in range(7):
                if board[row][col] == self.opponent_symbol:
                    for dr, dc in directions:
                        r1, c1 = row + dr, col + dc
                        r2, c2 = row + 2 * dr, col + 2 * dc

                        if 0 <= r1 < 6 and 0 <= c1 < 7 and board[r1][c1] == self.opponent_symbol:
                            if 0 <= r2 < 6 and 0 <= c2 < 7 and board[r2][c2] == '0':
                                # print("two adj oppnent found", flush=True)
                                return (r2, c2)

        
        for index in empty_indexes:
            x = index[0]
            y = index[1]

            adj_cells = [(x,y+1),(x+1,y),(x,y-1),(x-1,y),(x+1,y-1),(x-1,y+1),(x+1,y+1),(x-1,y-1)]

            for cell in adj_cells:
                try:
                    if board[cell[0]][cell[1]] == self.opponent_symbol:
                        # print("empty adj found", flush=True)
                        return index
                except:
                    continue

        random_index = random.choice(empty_indexes)
        # print(f"random : {random_index}")
        return random_index

class Connect4_minimax_bot(Connect4_bot):
    

    def get_best_score(self, board, symbol, alpha, beta, depth):
        winner = Connect4.check_winner(board)
        if winner == self.symbol:  
            return 100
        elif winner == self.opponent_symbol:  
            return -100
        elif not self.connect4_game.get_empty_indexes():
            return 0
        elif depth == 0:  
            return self.evaluate_board(board)

        empty_indexes = self.connect4_game.get_empty_indexes()

        if symbol == self.symbol: 
            best_score = -float("inf")
            for index in empty_indexes:
                board_copy = copy.deepcopy(board)
                board_copy[index[0]][index[1]] = symbol  

                score = self.get_best_score(board_copy, self.opponent_symbol, alpha, beta, depth - 1)
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

    def make_move(self, board):
        best_score = -float("inf")
        best_move = None

        for index in self.connect4_game.get_empty_indexes():
            board_copy = copy.deepcopy(board)
            board_copy[index[0]][index[1]] = self.symbol  

            score = self.get_best_score(board_copy, self.opponent_symbol, -float("inf"), float("inf"), self.max_depth)

            if score > best_score:
                best_score = score
                best_move = index

        return best_move

class Connect4_rl_bot(Connect4_bot):
    def __init__(self,connect4_game, symbol, learning_rate=0.1, discount_factor=0.5, exploration=0.99, exploration_decay_factor=0.5, epoch=1000):
        super().__init__(connect4_game, symbol)
        self.qtable = {}
        self.load_qtable()
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epoch = epoch
        self.exploration = exploration
        self.exploration_min = 0.01
        self.exploration_max = 1
        self.exploration_decay_factor = exploration_decay_factor

    def load_qtable(self):
        with open('q_table.pkl', 'rb') as file:
            self.qtable = pickle.load(file)
    
    def save_qtable(self):
        with open('q_table.pkl', 'wb') as file:
            pickle.dump(self.qtable, file)
    
    def update_exploration(self, epoch):
        self.exploration = self.exploration_min + (self.exploration_max - self.exploration_min) * math.exp(-self.exploration_decay_factor * epoch)

    def train(self):
        self.qtable = {}

        for i in range(self.epoch+1):
            game = Connect4()
            # print(game.board)

            rule_based_bot = Connect4_rule_based_bot(game, self.opponent_symbol)
            self.connect4_game = game
            
            rl_turn = True
            while True:
                rl_turn = not rl_turn

                empty_indexes = game.get_empty_indexes()

                if rl_turn:

                    if random.random() < self.exploration:
                        move = random.choice(empty_indexes)
                    else:
                        move = self.make_move()

                    current_board = copy.deepcopy(self.connect4_game.board)

                    self.update_exploration(i)
                    self.update_board(move)
                    self.update_qtable(current_board, move)
 
                else:
                    move = rule_based_bot.make_move()
                    rule_based_bot.update_board(move)


                # if i % 10 == 0 :
                #     print(f"\n\n=== EPOCH {i} ===")
                #     if rl_turn:
                #         print("RL BOT : ")
                #     else:
                #         print("RULE BASED BOT : ")   
                #     print(f"MOVE : {move}")
                #     print(game.board)

                if not game.get_empty_indexes():
                    print(f"\n\n{i}. DRAW  : \n{game.board}")
                    break
                else:   
                    winner = game.check_winner()
                    if winner != "0":
                        if winner == self.symbol:
                            print(f"\n\n{i}. {winner} WINS  : \n{game.board}")
                        break
        
        self.save_qtable()

    def update_qtable(self, current_board, move):

        current_state = tuple(tuple(row) for row in current_board)

        current_q = self.qtable.get((current_state, move), 0)

        next_possible_moves = self.connect4_game.get_empty_indexes()

        next_state = tuple(tuple(row) for row in self.connect4_game.board)
        max_next_q = max([self.qtable.get((next_state, next_move), 0) for next_move in next_possible_moves], default=0)
            
        new_q = current_q + self.learning_rate * (self.evaluate_board() + self.discount_factor * max_next_q - current_q)

        self.qtable[(current_state, move)] = new_q


    def make_move(self):
        best_move = None
        best_q_value = -float("inf")

        empty_indexes = self.connect4_game.get_empty_indexes()

        for move in empty_indexes:
            state = tuple(tuple(row) for row in self.connect4_game.board)
            q_value = self.qtable.get((state, move), 0)

            if q_value > best_q_value :
                best_q_value = q_value
                best_move = move

        return best_move


game = Connect4()
# #
rl_bot = Connect4_rl_bot(game, "X", epoch=5000, exploration=0.9, learning_rate=0.2, exploration_decay_factor=0.8, discount_factor=0.9)

# rl_bot.train()
# rl_bot.load_qtable()


print("======\n")
print(rl_bot.qtable)



# connect4.board = [['O', 'O', 'X', 'O', 'X', 'O', 'X'],
#                   ['0', 'X', 'O', '0', 'X', 'X', 'O'], 
#                   ['O', '0', 'X', 'X', 'O', 'X', 'O'], 
#                   ['X', '0', 'O', 'X', '0', 'O', 'O'], 
#                   ['0', '0', 'X', 'O', 'O', 'X', 'X'], 
#                   ['0', 'O', '0', 'X', '0', '0', '0']]
# bot = Connect4_bot("minimax", connect4, "O")
# print(bot.make_move())
# print(Connect4.check_winner(connect4.board))