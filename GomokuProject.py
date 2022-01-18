print("This is Gomoku Deluxe!")

#starting off with tic-tac-toe
import os
import sys
import tkinter as tk 
from tkinter import Canvas
import random



class my_class(tk.Tk):
    def __init__(self, ai):
        tk.Tk.__init__(self)
        self.title("This is Gomoku Deluxe")

        menubar =tk.Menu(self)
        #menubar.add_command(label="Hello!", command=hello)
        menubar.add_command(label="Quit!", command=self.quit_app)
        self.config(menu=menubar)

        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 20
        self.columns = 20
        self.ai = ai
        self.gameover = False
        
        # Based on user selection, set up self.color and self.color_lookup appropriately
        self.color = "red"
        # Could create this dynamically based on user selection
        self.color_lookup = {
            'red': 1,
            'white': 2
        }

        self.board = []

        for i in range(self.rows):
            self.board.append([0] * self.columns)

        

        self.tiles = {}

        self.canvas.bind("<Configure>", self.start_up)
        self.status = tk.Label(self, anchor="w")
        self.status.pack(side="bottom", fill="x")

        #self.master_frame = tk.Tk()
        #self.master_frame.pack()

    def quit_app(self):

        self.destroy()

    def start_up(self, event = None):
        #self.canvas.delete("rect")
        cellwidth = int(self.canvas.winfo_width()/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.columns)
        
        for column in range(self.columns):
            for row in range(self.rows):

                x1 = column*cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                
                tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags="rect")
                self.tiles[row,column] = tile
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row, column=column: self.clicked(row, column))
                
        self.mainloop()

    def clicked(self, row, column):
        if self.gameover:
            return

        self.play_move(row, column)

        if self.gameover:
           return

        if self.ai and self.color == "white":
            while True:      
              next_move = ai_move(self.board,self.color_lookup['red'])
              if next_move:
                  row, column = next_move
              else:
                  row = random.randint(0,18)
                  column = random.randint(0,18)
              #row = random.randint(0,18)
              #column = random.randint(0,18)
              tile = self.tiles[row,column]
              tile_color = self.canvas.itemcget(tile, "fill")
              if tile_color == "blue":
                  break
            self.play_move(row, column)
    
    def play_move(self, row, column):
        tile = self.tiles[row,column]
        tile_color = self.canvas.itemcget(tile, "fill")
        if tile_color != "blue":
            print('Invalid play')
            return
        self.canvas.itemconfigure(tile, fill=self.color)

        
        piece = self.color_lookup[self.color]
        self.board[row][column] = piece
        self.status.configure(text="Player %s clicked on %s/%s" % (self.color, row, column))



        has_won = winning_move(self.board, piece)
        if has_won:
            print("player {} wins".format(self.color))
            self.gameover = True
            self.status.configure(text="Player %s won " % (self.color))
            
        # Update the color to be played next turn
        self.color = "white" if self.color == "red" else "red"

   
# this is where the code for the previous version starts
ROW_COUNT = 19
COLUMN_COUNT = 19

board = []

for i in range(19):
 board.append(["O"] * 19)

 

def print_board():
    #board = []
    #for i in range(19):
     # board.append(["O"] * 19)
    for row in board:
      print (row)

def drop_point(board, row, col, piece):
    board[row][col] = piece

def valid_location(board, row, col):
    temp = board[row][col] == "O"      
    return temp

def winning_move(board, piece):
    #finds horizontal wins
    for c in range(COLUMN_COUNT - 4):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece and board[r][c+4] == piece:
                return True

    #finds vertical wins
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 4):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece and board[r+4][c] == piece:
                return True

    #finds positive diagonals
    for c in range(COLUMN_COUNT - 4):
        for r in range(ROW_COUNT - 4):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece and board[r+4][c+4] == piece:
                return True

    #finds negative diagonals
    for c in range(COLUMN_COUNT - 4):
        for r in range(4, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece and board[r-4][c+4] == piece:
                return True

def ai_move(board, piece):
    
    #finds horizontal blocks
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece:
                if board [r][c-1] == 0:
                    return (r, c-1)
                elif board[r][c+2] == 0:
                    return (r, c+2)

    #finds vertical blocks
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if board[r][c] == piece and board[r+1][c] == piece:
                if board[r-1][c]  == 0:
                    return (r-1, c)
                elif board[r+2][c] == 0:
                    return (r+2, c)#top r-2 bottom

    #finds positive diagonals blocks
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT - 2):
            if board[r][c] == piece and board[r+1][c+1] == piece:
                if board[r-1][c-1] == 0:
                    return (r-1,c-1)
                elif board[r+2][c+2] ==0:
                    return (r+2,c+2)
            # r+2 c+2, r-1,c-1

    #finds negative diagonals blocks
    for c in range(COLUMN_COUNT - 2):
        for r in range(2, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece:
                if board[r-2][c+2] == 0:
                    return (r-2,c+2)
                elif board[r+1][c-1] == 0:
                    return (r+1,c-1)
            #r-2 c+2, r +1, c-1


# this loop handles user's piece 
print_board()
turn = 0
game_over = False

chose_ai = (input("Do you want to play against the AI? [y/n]") == "y")

while not game_over:

    temp = my_class(chose_ai)
    temp.start_up()

    if turn == 0:
        row = int(input("Player 1 Select a row: ")) - 1
        col = int(input("Player 1 Select a col: ")) - 1

    if valid_location(board, row, col):
        drop_point(board, row, col, 1)
    
    print_board()

    if winning_move(board, 1):
        print("Player 1 wins!! Congratulations!")
        game_over = True

    

    else:
        if chose_ai == "y":
            row1=random.randint(0,18)
            col1=random.randint(0,18)
        else:
            row1 = int(input("Player 2 Select a row: ")) - 1
            col1 = int(input("Player 2 Select a col: ")) - 1

    if valid_location(board, row1, col1):
        drop_point(board, row1, col1, 2)

    if winning_move(board, 2):
        print("Player 2 wins!! Congratulations!")
        game_over = True      

    print_board()

turn += 1
turn = turn % 2
