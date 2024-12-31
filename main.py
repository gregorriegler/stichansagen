from stichansagen import Stichansagen
from js import window, document, location, URLSearchParams
from pyodide.ffi.wrappers import add_event_listener

queryString = URLSearchParams.new(location.search)
players = queryString.getAll("players")
game = Stichansagen(players=players)

def handle_keypress(event):
    game.input(int(event.key))
    draw_game(game)

input_field = document.getElementById("inputs")
add_event_listener(window, "keypress", handle_keypress)

def draw_game(game):
    container = document.getElementById("game")
    table = create_table(game.headers(), game.body())
    container.innerHTML = ""
    container.appendChild(table)

draw_game(game)

def create_table(headers, rows):
    table = document.createElement("table")
    table.style.border = "1px solid black"
    table.style.borderCollapse = "collapse"

    thead = document.createElement("thead")
    header_row = document.createElement("tr")
    for header in headers:
        th = document.createElement("th")
        th.textContent = header
        th.style.border = "1px solid black"
        th.style.padding = "1px"
        header_row.appendChild(th)
    thead.appendChild(header_row)
    table.appendChild(thead)

    tbody = document.createElement("tbody")
    for row in rows:
        tr = document.createElement("tr")
        for cell in row:
            td = document.createElement("td")
            td.textContent = str(cell)
            td.style.border = "1px solid black"
            td.style.padding = "1px"
            tr.appendChild(td)
        tbody.appendChild(tr)
    table.appendChild(tbody)

    return table
