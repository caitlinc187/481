import pygame
from typing import Tuple, Optional

#Initialize pygame
pygame.init()

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BACKGROUND = (240, 240, 240)
HIGHLIGHT = (255, 255, 150)

#Screen dimensions
WIDTH, HEIGHT = 600, 650
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 9
BOARD_CELL_SIZE = BOARD_SIZE // 3
INFO_HEIGHT = 50

class GUI:
    def __init__(self, game_logic):
        self.game = game_logic
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ultimate Tic Tac Toe")
        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 22)
        self.running = True
        self.mouse_pos = (0, 0)
        self.hover_cell = None
        self.message = ""
        self.ai_thinking = False
        
        #Set up a clock for consistent frame rate
        self.clock = pygame.time.Clock()
        
    def draw_board(self):
        self.screen.fill(BACKGROUND)
        
        #Highlight the available board(s)
        valid_moves = self.game.get_valid_moves()
        valid_boards = set()
        for move in valid_moves:
            valid_boards.add((move[0], move[1]))
        
        for board_row, board_col in valid_boards:
            rect = pygame.Rect(
                board_col * BOARD_CELL_SIZE, 
                board_row * BOARD_CELL_SIZE,
                BOARD_CELL_SIZE, 
                BOARD_CELL_SIZE
            )
            pygame.draw.rect(self.screen, LIGHT_GRAY, rect)
        
        #Highlight the next board if specified
        if self.game.next_board:
            next_row, next_col = self.game.next_board
            if (self.game.meta_board[next_row][next_col] == '' and 
                not self.game.boards[next_row][next_col].is_full()):
                rect = pygame.Rect(
                    next_col * BOARD_CELL_SIZE, 
                    next_row * BOARD_CELL_SIZE,
                    BOARD_CELL_SIZE, 
                    BOARD_CELL_SIZE
                )
                pygame.draw.rect(self.screen, HIGHLIGHT, rect)
        
        #Drawing all grid lines
        for board_row in range(3):
            for board_col in range(3):
                board_x = board_col * BOARD_CELL_SIZE
                board_y = board_row * BOARD_CELL_SIZE
                
                #Internal grid lines for each small board
                for i in range(1, 3):
                    pygame.draw.line(
                        self.screen, GRAY,
                        (board_x + i * CELL_SIZE, board_y),
                        (board_x + i * CELL_SIZE, board_y + BOARD_CELL_SIZE),
                        1
                    )
                    
                    pygame.draw.line(
                        self.screen, GRAY,
                        (board_x, board_y + i * CELL_SIZE),
                        (board_x + BOARD_CELL_SIZE, board_y + i * CELL_SIZE),
                        1
                    )
        
        #Drawing the big grid lines on top
        for i in range(4):
            pygame.draw.line(
                self.screen, BLACK,
                (i * BOARD_CELL_SIZE, 0),
                (i * BOARD_CELL_SIZE, BOARD_SIZE),
                3 if 0 < i < 3 else 2
            )
   
            pygame.draw.line(
                self.screen, BLACK,
                (0, i * BOARD_CELL_SIZE),
                (BOARD_SIZE, i * BOARD_CELL_SIZE),
                3 if 0 < i < 3 else 2
            )
        
        #Draw X's and O's for each cell
        for board_row in range(3):
            for board_col in range(3):
                board = self.game.boards[board_row][board_col]
                for cell_row in range(3):
                    for cell_col in range(3):
                        x = board_col * BOARD_CELL_SIZE + cell_col * CELL_SIZE
                        y = board_row * BOARD_CELL_SIZE + cell_row * CELL_SIZE
                        
                        #Draw the cell content
                        cell_content = board.board[cell_row][cell_col]
                        if cell_content:
                            if cell_content == 'X':
                                self.draw_x(x, y)
                            else:
                                self.draw_o(x, y)
        
        #Draw small board winners
        for board_row in range(3):
            for board_col in range(3):
                winner = self.game.meta_board[board_row][board_col]
                if winner:
                    x = board_col * BOARD_CELL_SIZE
                    y = board_row * BOARD_CELL_SIZE
                    if winner == 'X':
                        self.draw_big_x(x, y)
                    elif winner == 'O':
                        self.draw_big_o(x, y)
                    elif winner == 'D':
                        self.draw_big_d(x, y)
        
        #Information text at the bottom
        status_rect = pygame.Rect(0, BOARD_SIZE, WIDTH, INFO_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, status_rect)
        pygame.draw.line(self.screen, BLACK, (0, BOARD_SIZE), (WIDTH, BOARD_SIZE), 2)
        
        if self.message:
            text = self.font.render(self.message, True, BLACK)
            self.screen.blit(text, (10, BOARD_SIZE + 15))
        elif self.game.winner:
            if self.game.winner == 'D':
                text = self.font.render("Game Over! It's a Draw!", True, BLACK)
            else:
                text = self.font.render(f"Game Over! Player {self.game.winner} wins!", True, 
                                    BLUE if self.game.winner == 'O' else RED)
            self.screen.blit(text, (10, BOARD_SIZE + 15))
        else:
            text = self.font.render(f"Player {self.game.current_player}'s turn", True, 
                                  BLUE if self.game.current_player == 'O' else RED)
            self.screen.blit(text, (10, BOARD_SIZE + 15))
            
            help_text = self.small_font.render("Click on a valid cell to make a move", True, GRAY)
            self.screen.blit(help_text, (WIDTH - 250, BOARD_SIZE + 15))
        
        #Hover highlights available cell in green
        if self.hover_cell and not self.game.winner and not self.ai_thinking:
            board_row, board_col, cell_row, cell_col = self.hover_cell
            if (board_row, board_col, cell_row, cell_col) in self.game.get_valid_moves():
                x = board_col * BOARD_CELL_SIZE + cell_col * CELL_SIZE
                y = board_row * BOARD_CELL_SIZE + cell_row * CELL_SIZE
                hover_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                hover_surface.fill((0, 200, 0, 80))
                self.screen.blit(hover_surface, (x, y))
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GREEN, rect, 2)
    
    #Draw X's and O's for moves
    def draw_x(self, x, y):
        margin = CELL_SIZE // 4
        pygame.draw.line(self.screen, RED, 
                        (x + margin, y + margin), 
                        (x + CELL_SIZE - margin, y + CELL_SIZE - margin), 
                        3)
        pygame.draw.line(self.screen, RED, 
                        (x + CELL_SIZE - margin, y + margin), 
                        (x + margin, y + CELL_SIZE - margin), 
                        3)
    
    def draw_o(self, x, y):
        margin = CELL_SIZE // 4
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - margin
        pygame.draw.circle(self.screen, BLUE, center, radius, 3)

    #Draw result of small grid (X's and O's and D's)
    def draw_big_x(self, x, y):
        margin = BOARD_CELL_SIZE // 6
        pygame.draw.line(self.screen, RED, 
                        (x + margin, y + margin), 
                        (x + BOARD_CELL_SIZE - margin, y + BOARD_CELL_SIZE - margin), 
                        8)
        pygame.draw.line(self.screen, RED, 
                        (x + BOARD_CELL_SIZE - margin, y + margin), 
                        (x + margin, y + BOARD_CELL_SIZE - margin), 
                        8)
        overlay = pygame.Surface((BOARD_CELL_SIZE, BOARD_CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((255, 200, 200, 100))
        self.screen.blit(overlay, (x, y))
    
    def draw_big_o(self, x, y):
        margin = BOARD_CELL_SIZE // 6
        center = (x + BOARD_CELL_SIZE // 2, y + BOARD_CELL_SIZE // 2)
        radius = BOARD_CELL_SIZE // 2 - margin
        pygame.draw.circle(self.screen, BLUE, center, radius, 8)
        overlay = pygame.Surface((BOARD_CELL_SIZE, BOARD_CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((200, 200, 255, 100))
        self.screen.blit(overlay, (x, y))
    
    def draw_big_d(self, x, y):
        margin = BOARD_CELL_SIZE // 6
        rect_left = x + margin
        rect_top = y + margin
        rect_width = BOARD_CELL_SIZE - 2 * margin
        rect_height = BOARD_CELL_SIZE - 2 * margin
        pygame.draw.line(
            self.screen, GRAY,
            (rect_left, rect_top),
            (rect_left, rect_top + rect_height),
            8
        )
        pygame.draw.line(
            self.screen, GRAY,
            (rect_left, rect_top),
            (rect_left + rect_width * 0.6, rect_top),
            8
        )
        pygame.draw.line(
            self.screen, GRAY,
            (rect_left, rect_top + rect_height),
            (rect_left + rect_width * 0.6, rect_top + rect_height),
            8
        )
        pygame.draw.arc(
            self.screen, GRAY,
            (rect_left + rect_width * 0.2, rect_top, rect_width * 0.8, rect_height),
            -1.57,
            1.57,
            8
        )
        overlay = pygame.Surface((BOARD_CELL_SIZE, BOARD_CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((200, 200, 200, 100))
        self.screen.blit(overlay, (x, y))
            
    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int, int, int]]:
        x, y = pos
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            return None
        
        board_col = x // BOARD_CELL_SIZE
        board_row = y // BOARD_CELL_SIZE
        
        cell_col = (x % BOARD_CELL_SIZE) // CELL_SIZE
        cell_row = (y % BOARD_CELL_SIZE) // CELL_SIZE
        
        return (board_row, board_col, cell_row, cell_col)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                self.hover_cell = self.get_cell_from_pos(self.mouse_pos)
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.ai_thinking:
                    continue
                    
                if self.game.winner:
                    #Game is over, reset when clicked
                    self.message = "Game is over. Close the window to exit."
                    continue
                
                cell = self.get_cell_from_pos(event.pos)
                if cell:
                    board_row, board_col, cell_row, cell_col = cell
                    if (board_row, board_col, cell_row, cell_col) in self.game.get_valid_moves():
                        self.game.make_move(board_row, board_col, cell_row, cell_col)
                    else:
                        self.message = "Invalid move! Try again."
                        pygame.time.set_timer(pygame.USEREVENT, 1500)  #Clear message after 1.5 seconds
            
            if event.type == pygame.USEREVENT:
                self.message = ""  #Clear the temporary message
                pygame.time.set_timer(pygame.USEREVENT, 0)  #Disable the timer
                
    def run(self):
        while self.running:
            self.handle_events()
            self.draw_board()
            pygame.display.flip()
            
            #Maintain consistent frame rate
            self.clock.tick(60)
            
            #Check if the big game is a draw
            if not self.game.winner:
                #Check if all boards are filled or won
                all_boards_completed = True
                for board_row in range(3):
                    for board_col in range(3):
                        if self.game.meta_board[board_row][board_col] == '':
                            if not self.game.boards[board_row][board_col].is_full():
                                all_boards_completed = False
                                break
                    if not all_boards_completed:
                        break
                #If all small boards are completed and there's no winner, it's a draw
                if all_boards_completed:
                    self.game.winner = 'D'

            #AI's turn
            if not self.game.winner and self.game.current_player == 'O' and not self.ai_thinking:
                self.ai_thinking = True
                self.message = "AI is thinking..."
                pygame.display.flip()
                
                #Run AI move in a slight delay
                pygame.time.delay(200)
                _, move = self.game.minimax(depth=3, alpha=-float('inf'), beta=float('inf'), 
                                           maximizing=True, player='O')
                
                if move:
                    self.game.make_move(*move)
                
                self.message = ""
                self.ai_thinking = False
            
        pygame.quit()