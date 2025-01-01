from stichansagen import Stichansagen
from js import window, document, location, URLSearchParams
from pyodide.ffi.wrappers import add_event_listener


input_field = document.getElementById("inputs")
output = document.getElementById("output")
game_container = document.getElementById("game")

queryString = URLSearchParams.new(location.search)
players = queryString.getAll("p")
game = Stichansagen(players=players)
if(queryString.get("inputs")):
    game.load([int(char) for char in queryString.get("inputs")])
    input_field.value = "".join(str(i) for i in game.inputs)

def create_table(headers, rows):
    table = document.createElement("table")
    table.style.borderCollapse = "collapse"

    thead = document.createElement("thead")
    header_row = document.createElement("tr")
    for header in headers:
        th = document.createElement("th")
        th.textContent = header
        header_row.appendChild(th)
    thead.appendChild(header_row)
    table.appendChild(thead)

    tbody = document.createElement("tbody")
    for row in rows:
        tr = document.createElement("tr")
        for cell in row:
            td = document.createElement("td")
            if("?" in str(cell)):
                td.innerHTML = cell.replace("?", "<span class=\"dran\">█</span>")
            else:
                td.innerHTML = str(cell)
            tr.appendChild(td)
        tbody.appendChild(tr)
    table.appendChild(tbody)

    return table

def draw_game(game):
    table = create_table(game.headers(), game.body())
    game_container.innerHTML = ""
    game_container.appendChild(table)
    output.innerHTML = game.info()

def handle_keypress(_):
    game.reset()
    input_field.value = ''.join(char for char in input_field.value if char.isdigit())
    game.load([int(char) for char in input_field.value])
        
    inputs_as_string = "".join(str(i) for i in game.inputs)
    queryString.set("inputs", inputs_as_string)
    window.history.pushState(None, None, f"?{queryString}")
    draw_game(game)

draw_game(game)

add_event_listener(input_field, "input", handle_keypress)

