import tkinter as tk
from tkinter import messagebox
import random
import os

class Morpion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Morpion")
        self.root.geometry("300x350")
        self.root.resizable(False, False)

        self.current_player = "X"
        self.board = [[" "]*3 for _ in range(3)]

        self.buttons = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=" ", font=('Arial', 20), width=5, height=2,
                                                command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, row, col):
        if self.board[row][col] == " ":
            self.buttons[row][col].config(text=self.current_player)
            self.board[row][col] = self.current_player
            self.play_sound("click.wav")
            if self.check_winner(self.current_player):
                self.play_sound("win.wav")
                messagebox.showinfo("Fin de la partie", f"Le joueur {self.current_player} a gagné !")
                self.reset_board()
            elif all(self.board[i][j] != " " for i in range(3) for j in range(3)):
                self.play_sound("draw.wav")
                messagebox.showinfo("Fin de la partie", "Match nul !")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.ai_move()

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
            if all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def reset_board(self):
        self.current_player = "X"
        self.board = [[" "]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")

    def ai_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        row, col = self.minimax(self.board, empty_cells, "O")
        self.buttons[row][col].config(text="O")
        self.board[row][col] = "O"
        self.play_sound("click.wav")
        if self.check_winner("O"):
            self.play_sound("lose.wav")
            messagebox.showinfo("Fin de la partie", "L'IA a gagné !")
            self.reset_board()
        elif all(self.board[i][j] != " " for i in range(3) for j in range(3)):
            self.play_sound("draw.wav")
            messagebox.showinfo("Fin de la partie", "Match nul !")
            self.reset_board()
        else:
            self.current_player = "X"

    def minimax(self, board, empty_cells, player):
        if self.check_winner("X"):
            return -1, -1, -10
        elif self.check_winner("O"):
            return -1, -1, 10
        elif not empty_cells:
            return -1, -1, 0

        if player == "O":
            best_score = float("-inf")
            best_move = (-1, -1)
            for i, j in empty_cells:
                board[i][j] = player
                score = self.minimax(board, [(x, y) for x, y in empty_cells if (x, y) != (i, j)], "X")[2]
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
                board[i][j] = " "
            return best_move[0], best_move[1], best_score
        else:
            best_score = float("inf")
            best_move = (-1, -1)
            for i, j in empty_cells:
                board[i][j] = player
                score = self.minimax(board, [(x, y) for x, y in empty_cells if (x, y) != (i, j)], "O")[2]
                if score < best_score:
                    best_score = score
                    best_move = (i, j)
                board[i][j] = " "
            return best_move[0], best_move[1], best_score

    def play_sound(self, filename):
        path = os.path.join(os.path.dirname(__file__), "sounds", filename)
        if os.path.exists(path):
            os.system(f'start "{path}"')

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Morpion()
    game.run()

