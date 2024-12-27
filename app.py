import os
import sys
from stichansagen import Stichansagen

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def redraw_screen(game):
    clear_screen()
    print(game)

def getchar():
    """Read a single character from user input."""
    if os.name == 'nt':  # For Windows
        import msvcrt
        return msvcrt.getch().decode()
    else:  # For Unix-like systems
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

def main():    
    game = Stichansagen()
    game.add_player("Max")
    game.add_player("Ingeborg")
    game.add_player("Christina")
    game.add_player("Gregor")
    game.start()

    try:
        while True:
            redraw_screen(game)
            char = getchar()
            game.input(int(char))
    except KeyboardInterrupt:
        clear_screen()
        print("\nExiting... Goodbye!")

if __name__ == "__main__":
    main()



