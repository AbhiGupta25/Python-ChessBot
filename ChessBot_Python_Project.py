import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import chess
import random

piece_images = {}
player_color = None  # Will be set to 'white' or 'black'
bot_level = None    # Will be set to 'beginner', 'intermediate', etc.

def load_images():
    pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
    colors = ['w', 'b']
    for color in colors:
        for piece in pieces:
            key = color + piece
            filename = fr"C:\\Users\\Lenovo\\Pictures\\Python\\{key}.png"
            image = Image.open(filename).convert("RGBA")
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
            piece_images[key] = ImageTk.PhotoImage(image)



class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Playing against: Magnus.exe")
        self.board = chess.Board()
        self.selected_square = None
        self.dragged_piece = None
        self.drag_image_id = None

        self.canvas = tk.Canvas(self.root, width=512, height=512)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.drop_piece)

        

        self.comment_box = tk.Label(self.root, text="Magnus.exe: Ready to crush you.", font=("Arial", 10), wraplength=300)
        self.comment_box.pack(pady=5)

        self.draw_board()

        if player_color == 'black':
            self.root.after(500, self.bot_move)

    def draw_board(self):
        self.canvas.delete("all")
        light_color = "#F0D9B5"
        dark_color = "#B58863"

        for row in range(8):
            for col in range(8):
                board_row = 7 - row
                x1, y1 = col * 64, row * 64
                x2, y2 = x1 + 64, y1 + 64
                color = light_color if (board_row + col) % 2 == 0 else dark_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                square = chess.square(col, board_row)
                piece = self.board.piece_at(square)
                if piece:
                    key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
                    self.canvas.create_image(x1, y1, anchor='nw', image=piece_images[key])

    def start_drag(self, event):
        if self.board.turn != (player_color == 'white'):
            return
        col = event.x // 64
        row = 7 - (event.y // 64)
        square = chess.square(col, row)
        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:
            self.selected_square = square
            key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
            self.dragged_piece = piece_images[key]
            self.drag_image_id = self.canvas.create_image(event.x - 32, event.y - 32, image=self.dragged_piece)

    def drag_motion(self, event):
        if self.drag_image_id:
            self.canvas.coords(self.drag_image_id, event.x - 32, event.y - 32)

    def drop_piece(self, event):
        if self.selected_square is None or self.drag_image_id is None:
            return
        col = event.x // 64
        row = 7 - (event.y // 64)
        target_square = chess.square(col, row)

        move = chess.Move(self.selected_square, target_square)
        if move in self.board.legal_moves:
            self.board.push(move)
            self.draw_board()
            if self.board.is_game_over():
                self.game_over()
            else:
                self.root.after(500, self.bot_move)
        else:
            self.draw_board()

        self.selected_square = None
        self.dragged_piece = None
        self.drag_image_id = None

    def bot_move(self):
        if self.board.is_game_over():
            self.game_over()
            return

        depth_by_level = {
            'beginner': 1,
            'intermediate': 2,
            'pro': 3,
            'advanced': 4
        }
        depth = depth_by_level.get(bot_level, 2)
        move = self.best_minimax_move(depth=depth)

        captured = self.board.is_capture(move)
        self.board.push(move)
        self.draw_board()
        self.generate_snark(captured)

        if self.board.is_game_over():
            self.game_over()

    def best_minimax_move(self, depth):
        best_score = float('-inf')
        best_move = None
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.minimax(depth - 1, -float('inf'), float('inf'))
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, depth, alpha, beta):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board(add_positional=True)

        max_eval = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = -self.minimax(depth - 1, -beta, -alpha)
            self.board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    def evaluate_board(self, add_positional=False):
        values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
        white, black = 0, 0
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece:
                value = values[piece.piece_type]
                if add_positional:
                    value += self.positional_bonus(sq, piece)
                if piece.color == chess.WHITE:
                    white += value
                else:
                    black += value
        return (black - white) if player_color == 'white' else (white - black)

    def positional_bonus(self, square, piece):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        return 0.2 if file in [3, 4] and rank in [3, 4] else 0

    def generate_snark(self, captured):
        if self.board.is_check():
            comment = random.choice([
                "Check yourself before you wreck yourself.",
                "Careful... the king is naked.",
                "Did you forget your king needs protection?"
            ])
        elif captured:
            comment = random.choice([
                "I'll take that. You won't miss it, right?",
                "Easy pickings.",
                "Thanks for the gift."
            ])
        else:
            comment = random.choice([
                "Your move was... interesting. In a bad way.",
                "Trying your best, huh?",
                "I expected a little more."
            ])
        self.comment_box.config(text=f"Magnus.exe: {comment}")

    def game_over(self):
        result = self.board.result()
        if self.board.is_checkmate():
            if self.board.turn == (player_color == 'white'):
                messagebox.showinfo("Game Over", "Checkmate! Magnus.exe wins.")
            else:
                messagebox.showinfo("Game Over", "Checkmate! You win.")
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate.")
        else:
            messagebox.showinfo("Game Over", f"Game ended: {result}")

def choose_color():
    def pick_white():
        global player_color
        player_color = 'white'
        selection_win.destroy()
        start_game()

    def pick_black():
        global player_color
        player_color = 'black'
        selection_win.destroy()
        start_game()

    selection_win = tk.Tk()
    selection_win.title("Choose Your Side")
    tk.Label(selection_win, text="Choose your color to play:").pack(pady=10)
    tk.Button(selection_win, text="Play as White", command=pick_white).pack(pady=5)
    tk.Button(selection_win, text="Play as Black", command=pick_black).pack(pady=5)
    selection_win.mainloop()

def choose_difficulty():
    def set_level(level):
        global bot_level
        bot_level = level
        difficulty_win.destroy()
        choose_color()

    difficulty_win = tk.Tk()
    difficulty_win.title("Magnus.exe Difficulty")
    tk.Label(difficulty_win, text="Choose your challenge level:").pack(pady=10)
    levels = ['Beginner', 'Intermediate', 'Pro', 'Advanced']
    for lvl in levels:
        tk.Button(difficulty_win, text=lvl, width=20, command=lambda l=lvl.lower(): set_level(l)).pack(pady=2)
    difficulty_win.mainloop()

def start_game():
    print(f"[DEBUG] Player is playing as: {player_color}, Magnus.exe level: {bot_level}")
    root = tk.Tk()
    load_images()
    app = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    choose_difficulty()
