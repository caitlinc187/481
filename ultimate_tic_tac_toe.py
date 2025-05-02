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
    

class UltimateBoard:
    def __init__(self):
        self.boards = [[SmallBoard() for _ in range(3)] for _ in range(3)]
        self.meta_board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board : Optional[Tuple[int, int]] = None
        self.winner: Optional[str] = None

    def make_move(self,board_row: int, board_col: int, cell_row: int, cell_col: int) -> bool:
        if self.winner:
            return False
        
        if self.next_board and (board_row, board_col) != self.next_board:
            return False
        
        board = self.boards[board_row][board_col]
        if board.make_move(cell_row, cell_col, self.current_player):
            if board.winner and self.meta_board[board_row][board_col] == '':
                self.meta_board[board_row][board_col] = board.winner
                self.check_global_winner()

            if self.boards[cell_row][cell_col].is_full():
                self.next_board = None
            else:
                self.next_board = (cell_row, cell_col)
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_global_winner(self):
        lines = self.meta_board + [list(col) for col in zip(*self.meta_board)]
        lines.append([self.meta_board[i][i] for i in range(3)])
        lines.append([self.meta_board[i][2-i] for i in range(3)])

        for line in lines:
            if line[0] in ('X', 'O') and all(cell == line[0] for cell in line):
                self.winner = 'D'
    
    def get_valid_moves(self) -> List[Tuple[int, int, int, int]]:
        moves = []
        if self.winner:
            return moves
        if self.next_board:
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
        print(f"Next Plaer: {self.current_player}")
        if self.next_board:
            print(f" play in board: {self.next_board}")
        if self.winner:
            print(f"Game over! Winner: {self.winner}")

def play_game():
    game = UltimateBoard()

    while not game.winner:
        game.print_board()
        print("Enteryour move as: board_row board_col cell_row cell_col")
        print("Or type 'q' to quit")
        move = input("> ").strip()

        if move.lower() == 'q':
            print("Quiting game")
            break

        try: 
            br, bc, cr, cc = map(int,move.split())
            if (br,bc,cr,cc) in game.get_valid_moves():
                game.make_move(br,bc,cr,cc)
            else:
                print("invalid move")
        except ValueError:
            print("invalid input")

    if game.winner:
        game.print_board()
        if game.winner == 'D':
            print("There was a draw")
        else:
            print(f"Player {game.winner} won")

if __name__ == "__main__":
    play_game()

