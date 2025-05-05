from typing import List, Optional, Tuple


class SmallBoard:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.winner: Optional[str] = None
        self.full = False
    
    def make_move(self,row: int, col: int, player: str) -> bool:
        if self.board[row][col] == '' and self.winner is None:
            self.board[row][col] = player
            self.update_state()
            return True
        return False
    
    def update_state(self):
        lines = self.board +[list(col) for col in zip(*self.board)]
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2-i] for i in range(3)])

        for line in lines:
            if line[0] and all(cell == line[0] for cell in line):
                self.winner = line[0]
                return
            
        self.full = all(cell for row in self.board for cell in row)
        if self.full:
            self.winner = 'D'
        
    def is_full(self) -> bool:
        return self.full
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        if self.winner:
            return []
        return [(r,c) for r in range(3) for c in range(3) if self.board[r][c] == '']
    
    def __str__(self):
        return '\n'.join([' '.join([cell if cell else '.' for cell in row]) for row in self.board])
import math
import random    

class UltimateBoard:
    @staticmethod
    def evaluate_small_board(board: SmallBoard, player: str) -> int:
        if board.winner == player:
            return 100
        elif board.winner and board.winner != 'D':
            return -100
        elif board.winner == 'D':
            return 0
        
        score = 0
        lines = board.board + [list(col) for col in zip(*board.board)]
        lines.append([board.board[i][i] for i in range(3)])
        lines.append([board.board[i][2-i] for i in range(3)])

        opponent = 'O' if player == 'X' else 'X'
        for line in lines:
            if opponent not in line:
                score += line.count(player)
        return score
    
    def evaluate(self,player: str)-> int:
        total = 0
        for row in range(3):
            for col in range(3):
                total += self.evaluate_small_board(self.boards[row][col], player)
        return total
    
    def minimax(self, depth: int, alpha: int, beta: int, maximizing: bool, player: str) -> Tuple[int, Optional[Tuple[int, int, int, int]]]:
        if depth == 0 or self.winner:
            return self.evaluate(player), None
        
        valid_moves = self.get_valid_moves()
        random.shuffle(valid_moves)

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                clone = self.clone()
                clone.make_move(*move)
                eval_score, _ = clone.minimax(depth - 1, alpha, beta, False, player)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break 
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in valid_moves:
                clone = self.clone()
                clone.make_move(*move)
                eval_score, _ = clone.minimax(depth - 1, alpha, beta, True, player)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
        
    def clone(self) -> 'UltimateBoard':
        import copy
        new_board = UltimateBoard()
        new_board.boards = [[copy.deepcopy(board) for board in row] for row in self.boards]
        new_board.meta_board = [row[:] for row in self.meta_board]
        new_board.current_player = self.current_player
        new_board.next_board = self.next_board
        new_board.winner = self.winner
        return new_board

    def __init__(self):
        self.boards = [[SmallBoard() for _ in range(3)] for _ in range(3)]
        self.meta_board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board : Optional[Tuple[int, int]] = None
        self.winner: Optional[str] = None

    def make_move(self,board_row: int, board_col: int, cell_row: int, cell_col: int) -> bool:
        if self.winner:
            return False
        
        if self.next_board:
            if self.meta_board[self.next_board[0]][self.next_board[1]] != '' or \
            self.boards[self.next_board[0]][self.next_board[1]].is_full():
                self.next_board = None

            elif (board_row, board_col) != self.next_board:
                return False
        
        board = self.boards[board_row][board_col]
        if board.make_move(cell_row, cell_col, self.current_player):
            if board.winner and self.meta_board[board_row][board_col] == '':
                self.meta_board[board_row][board_col] = board.winner
                self.check_global_winner()

            target_board = self.boards[cell_row][cell_col]
            if target_board.is_full() or target_board.winner:
                self.next_board = None
            else:
                self.next_board = (cell_row, cell_col)
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_global_winner(self):
        lines = self.meta_board + [list(col) for col in zip(*self.meta_board)]
        lines.append([self.meta_board[i][i] for i in range(3)])
        lines.append([self.meta_board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] in ('X', 'O') and all(cell == line[0] for cell in line):
                self.winner = line[0]
    
    def get_valid_moves(self) -> List[Tuple[int, int, int, int]]:
        moves = []
        if self.winner:
            return moves
        if self.next_board and self.meta_board[self.next_board[0]][self.next_board[1]] == '':
            r, c = self.next_board
            for cell in self.boards[r][c].get_available_moves():
                moves.append((r, c, cell[0], cell[1]))

        else: 
            for br in range(3):
                for bc in range(3):
                    if self.meta_board[br][bc] == '':
                        for cell in self.boards[br][bc].get_available_moves():
                            moves.append((br,bc, cell[0], cell[1]))
        return moves
    
    def print_board(self):
        def merge_rows(row_idx):
            lines = []
            for r in range(3):
                line = ''
                for c in range(3):
                    line += ' '.join(self.boards[row_idx][c].board[r][cc] or '.' for cc in range(3)) + ' | '
                lines.append(line.strip(' | '))
            return lines
        
        full = []
        for i in range(3):
            full += merge_rows(i)
            if i < 2:
                full.append('-'* 29)
        print('\n'.join(full))
        print(f"Next Player: {self.current_player}")
        if self.next_board:
            r,c = self.next_board
            if self.meta_board[r][c] == '' and not self.boards[r][c].is_full():
                print(f"Recommended to play in board: {self.next_board}")

        if self.winner:
            print(f"Game over! Winner: {self.winner}")

def play_game():
    game = UltimateBoard()

    while not game.winner:
        game.print_board()

        if game.current_player == 'X':
            print("your turn. Enter: board_row board_col cell_row cell_col")
            move = input("> ").strip()
            if move.lower() in ('exit','quit'):
                print("Exiting game")
                break
            try:
                br, bc, cr, cc = map(int, move.split())
                if (br,bc, cr, cc) in game.get_valid_moves():
                    game.make_move(br, bc, cr, cc)
                else:
                    print("Invalid move")

            except ValueError:
                print("Invalid input")
        else:
            print("AI is thinking")
            _, move = game.minimax(depth = 3, alpha =-math.inf, beta=math.inf , maximizing=True, player='O')
            if move:
                game.make_move(*move)
            else:
                print("No move for AI")
    game.print_board()
    if game.winner == 'D':
        print("Draw")
    else:
        print(f"Player {game.winner} won!")


if __name__ == "__main__":
    play_game()
