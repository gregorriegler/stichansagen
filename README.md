# Stiche Ansagen

[Stiche Ansagen](https://de.wikipedia.org/wiki/Stiche-Raten) is a card game.
The goal of this app is to make it as simple as possible to track the progress of a game of Stiche Ansagen.
You can run it from the command line or in the browser.

Try the browser version [here](http://gregorriegler.com/sticheansagen?p=Player1&p=Player2)

## Good to Know

- The url is your savegame. As you track the games progress, the url will change and be saved to your browser history.
- It does not need a server and runs completely in the browser.
- It is unfortunately not possible to call 10 "Stiche". As the number 10 is the only callable number that takes two digits, I sacrificed it for the sake of simple user input. It is highly unlikely for a 10 to be called anyways. 
- The games logic is separated from UI and is well tested. This should make it easy to extend and add functionality.
- The game is written in python and uses pyscript with webassembly to run in the browser.