from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import json
# -------------------------
#          LOGIC  
# -------------------------

rows = 6
colums = 6

def creat():
    return [[" " for c in range(colums)] for r in range(rows)]

def play(col, piece):
    for r in range(rows - 1, -1, -1):
        if bord[r][col] == " ":
            bord[r][col] = piece
            return True
    return False

def check_colums(pieces):
    for c in range(colums):
        for r in range(rows - 3):
            if (
                bord[r][c] == pieces and
                bord[r+1][c] == pieces and
                bord[r+2][c] == pieces and
                bord[r+3][c] == pieces
            ):
                return True
    return False

def check_rows(pieces):
    for r in range(rows):
        for c in range(colums - 3):
            if (
                bord[r][c] == pieces and
                bord[r][c+1] == pieces and
                bord[r][c+2] == pieces and
                bord[r][c+3] == pieces
            ):
                return True
    return False

def check_diagonally(pieces):
    # \
    for r in range(rows - 3):
        for c in range(colums - 3):
            if (
                bord[r][c] == pieces and
                bord[r+1][c+1] == pieces and
                bord[r+2][c+2] == pieces and
                bord[r+3][c+3] == pieces
            ):
                return True

    # /
    for r in range(3, rows):
        for c in range(colums - 3):
            if (
                bord[r][c] == pieces and
                bord[r-1][c+1] == pieces and
                bord[r-2][c+2] == pieces and
                bord[r-3][c+3] == pieces
            ):
                return True

    return False

def win(piece):
    return check_colums(piece) or check_rows(piece) or check_diagonally(piece)


    return True
def early_draw():
    def possible(window):
        return not ("X" in window and "O" in window)

    # افقی
    for r in range(rows):
        for c in range(colums - 3):
            window = [bord[r][c+i] for i in range(4)]
            if possible(window):
                return False

    # عمودی
    for c in range(colums):
        for r in range(rows - 3):
            window = [bord[r+i][c] for i in range(4)]
            if possible(window):
                return False

    #  \️
    for r in range(rows - 3):
        for c in range(colums - 3):
            window = [bord[r+i][c+i] for i in range(4)]
            if possible(window):
                return False

    #  /️ 
    for r in range(3, rows):
        for c in range(colums - 3):
            window = [bord[r-i][c+i] for i in range(4)]
            if possible(window):
                return False

    return True

def draw():
    for r in range(rows):
        for c in range(colums):
            if bord[r][c] == " ":
                return False

#-------------------------
#        single play
#-------------------------

def can_win_next_move(piece):
    
    for col in range(colums):
        temp = [row[:] for row in bord]
        if play(col, piece):
            if win(piece):
                for r in range(rows):
                    bord[r] = temp[r][:]
                return col
        for r in range(rows):
            bord[r] = temp[r][:]
    return None


def ai_best_move():
    
    # 1) اگه بتونه ببره همون ستون 
    col = can_win_next_move("O")
    if col is not None:
        return col

    # 2)اگه بازيکن بتونه ببره جلوش رو بگيره
    col = can_win_next_move("X")
    if col is not None:
        return col

    # 3) در غير اين صورت بهترين انتخاب از مرکزه
    priority = [2, 3, 1, 4, 0, 5]
    for col in priority:
        if bord[0][col] == " ":
            return col

    # اگه راهي نباشه
    for col in range(colums):
        if bord[0][col] == " ":
            return col

    return None

# -------------------------
#           GUI 
# -------------------------

cell_size = 70
mood="two"
turn = 0  # 0 = X , 1 = O
root =Tk()
root.title("Connect Four")
root.geometry('600x600')
root.configure(bg="turquoise")
Label(root,text="Connect Four",bg="turquoise",fg="darkviolet",
            font=("Arial", 32,"bold")).pack(pady=(5, 5))

canvas = Canvas(root, width=colums * cell_size,
                   height=rows * cell_size, bg="violet")
canvas.pack(padx=5 , pady=50)

#-------mood-------#

def set_two_player():
    global mood
    mood = "two"
    reset_game()


def set_single_player():
    global mood
    mood = "one"
    reset_game()


def draw_board():
    canvas.delete("all")
    for r in range(rows):
        for c in range(colums):
            x1 = c * cell_size
            y1 = r * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white")

            if bord[r][c] == "X":
                canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="crimson")
            elif bord[r][c] == "O":
                canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="gold")

def reset_game():
    global bord, turn
    bord = creat()
    turn = 0
    draw_board()

def end(msg):
    response = messagebox.askyesno( " ",msg + "\n\n Do you want to play again?")
    if response:
        reset_game()
    else:
        root.destroy()


# ----------saving the game---------- #

def save_game():
    data = {
        "board": bord,
        "turn": turn,
        "mood": mood
    }
    file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("Game Save", "*.json")])
    if not file_path:
        return

    with open(file_path, "w") as f:
        json.dump(data, f)

    messagebox.showinfo( " ","Game saved succesfully!")
    root.destroy()

# ----------loeding new game----------#

def load_game():
    global bord, turn,mood

    file_path = filedialog.askopenfilename(filetypes=[("Game Save", "*.json")])
    if not file_path:
        return

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except:
        messagebox.showerror( " ","This file is not valid!")
        return

    bord = data["board"]
    turn = data["turn"]
    mood = data["mood"]

    draw_board()
    messagebox.showinfo(" ","Game loaded succefully!")
    
#--------about game----------#    
def rules():
    top = Toplevel()
    top.title('About the Game')
    top.geometry('800x500')
    top.configure(bg="mediumpurple")
    
    Label( top, text="Connect Four", bg="mediumpurple",
        fg="darkviolet",font=("Arial", 32, "bold")).pack(pady=(0, 25))

    # ---game rules---#
    rules_text = [
        "- Connect Four is a two‑player strategy game played on a 7‑column × 6‑row board.",
        "- Players take turns dropping one piece into any of the columns.",
        "- The piece falls to the lowest empty space within that column.",
        "- The first player to form a line of four pieces horizontally, vertically, or diagonally wins.",
        "- If the board fills up and no player connects four, the game ends in a draw."
    ]

    for rule in rules_text:
        Label(top,text=rule,bg="mediumpurple",fg="black",
            font=("Arial", 16),anchor="w",justify="left"
              ).pack(fill="x", pady=5)

    # ---close button---#
    Button(top,text="Close",command=top.destroy,
           font=("Arial", 16, "bold"),bg="darkviolet",fg="white",
        relief="raised",padx=15,pady=5).pack(pady=25)
    
#-----------اجرا بازي--------------#
    
    
def click(event):
    global turn

    col = event.x // cell_size
    if col < 0 or col >= colums:
        return

    if turn==0:
        piece="X"
    else:
        piece="O"

    if not play(col, piece):
        messagebox.showerror( " ","This column is full!")
        return

    draw_board()

    if win(piece):
        end(f"player {turn+1} wins!")
        return
    if early_draw():
        end("It's a draw!")
        return
    if draw():
        end("No empty spaces left.\n It's draw!")
        return
    turn = 1 - turn
    
    if mood == "one" and turn == 1:
        root.after(400, ai_move)  # کمی تأخیر برای طبیعی‌تر شدن بازی


def ai_move():
    global turn

    col = ai_best_move()
    if col is None:
        return

    play(col, "O")
    draw_board()

    if win("O"):
        end("You lose!")
        return
    if win("X"):
        end("You win!")
        return
    
    if early_draw():
        end("It's a draw!")
        return

    if draw():
        end("No empty spaces left.\n It's draw!")
        return

    turn = 0
bord = creat()
draw_board()

#--------------------------
#      craet menubar

menubar = Menu(root)
file_menu = Menu(menubar, tearoff=0)
#---file---#
file_menu.add_command(label="Save Game", command=save_game)
file_menu.add_command(label="Load Game", command=load_game)
menubar.add_cascade(label="File", menu=file_menu)

#---mood---#
mood_menu =Menu(menubar, tearoff=0)
mood_menu.add_command(label="Two Players", command=set_two_player)
mood_menu.add_command(label="Single Player (vs AI)", command=set_single_player)
menubar.add_cascade(label="Mood", menu=mood_menu)

#---help---#
help_menu =Menu(menubar, tearoff=0)
help_menu.add_command(label="About Game", command=rules)
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)
#--------------------------
canvas.bind("<Button-1>", click)

root.mainloop()
