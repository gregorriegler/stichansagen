import os
import sys
from stichansagen import Stichansagen
from tabulate import tabulate

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def redraw_screen(game):
    clear_screen()
    print(game_as_string(game))

def game_as_string(game):
    return table(game) + "\n" + game.info()

def table(game):
    return tabulate(game.body(), game.headers())
    
def getkey():
    """Read a single character from user input."""
    if os.name == 'nt':  # For Windows
        try:
            import msvcrt
            char = msvcrt.getch()
            if char == b'\x08':
                return 'BACKSPACE'
            return char.decode()
        except UnicodeDecodeError:
            return getkey()
    else:  # For Unix-like systems
        print(unix)
        exit
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
    game.add_player("Gregor")
    game.add_player("Ingeborg")
    game.add_player("Christina")
    
    try:
        while True:
            redraw_screen(game)
            key = getkey()
            if(key == 'BACKSPACE'):
                game.undo()
            elif(key.isdigit()):
                game.input(int(key))
            elif(key == 'q'):
                print("\nExiting... Goodbye!")
                exit()
            savegame = "".join(map(str, game.inputs))
            with open("game.txt", "w") as file:
                file.write(savegame)
    except KeyboardInterrupt:
        clear_screen()
        print("\nExiting... Goodbye!")

if __name__ == "__main__":
    main()



