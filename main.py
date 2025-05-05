import pygame
from ultimate_tic_tac_toe import UltimateBoard
from gui import GUI

def main():
    #Initialize the game logic
    game = UltimateBoard()
    
    #Initialize the GUI
    gui = GUI(game)
    
    #Set up the game window
    pygame.init()
    pygame.display.set_caption("Ultimate Tic Tac Toe")
    
    #Run the game
    print("Starting Ultimate Tic Tac Toe...")
    print("Player X: Human")
    print("Player O: AI")
    print("Click on a cell to make a move!")
    
    gui.run()
    
    print("Game ended. Thank you for playing!")

if __name__ == "__main__":
    main()