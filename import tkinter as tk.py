import tkinter as tk
import random

CELL = 28
ROWS, COLS = 15, 21


class MouseMaze:
	def __init__(self, root):
		self.root = root
		self.root.title("老鼠迷宮")
		self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL,
								bg="white", highlightthickness=0)
		self.canvas.pack()
		self.info = tk.Label(root, text="使用方向鍵移動老鼠，吃到起司即可獲勝！")
		self.info.pack(pady=6)
		root.bind("<KeyPress>", self.move)
		self.new_game()

	def new_game(self):
		self.maze = [[1] * COLS for _ in range(ROWS)]
		self.carve(1, 1)
		self.maze[1][1] = 0
		self.maze[ROWS - 2][COLS - 2] = 0
		self.mouse = [1, 1]
		self.cheese = [ROWS - 2, COLS - 2]
		self.won = False
		self.draw()

	def carve(self, r, c):
		self.maze[r][c] = 0
		directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
		random.shuffle(directions)
		for dr, dc in directions:
			nr, nc = r + dr, c + dc
			if 1 <= nr < ROWS - 1 and 1 <= nc < COLS - 1 and self.maze[nr][nc]:
				self.maze[r + dr // 2][c + dc // 2] = 0
				self.carve(nr, nc)

	def draw(self):
		self.canvas.delete("all")
		for r in range(ROWS):
			for c in range(COLS):
				color = "#3949ab" if self.maze[r][c] else "#fffde7"
				self.canvas.create_rectangle(c * CELL, r * CELL,
											 (c + 1) * CELL, (r + 1) * CELL,
											 fill=color, outline=color)
		cr, cc = self.cheese
		self.canvas.create_text(cc * CELL + CELL // 2, cr * CELL + CELL // 2,
								text="🧀", font=("Arial", 18))
		mr, mc = self.mouse
		self.canvas.create_text(mc * CELL + CELL // 2, mr * CELL + CELL // 2,
								text="🐭", font=("Arial", 18))

	def move(self, event):
		if self.won:
			if event.keysym.lower() == "r":
				self.new_game()
			return
		moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
		if event.keysym not in moves:
			return
		dr, dc = moves[event.keysym]
		r, c = self.mouse[0] + dr, self.mouse[1] + dc
		if 0 <= r < ROWS and 0 <= c < COLS and not self.maze[r][c]:
			self.mouse = [r, c]
			self.draw()
			if self.mouse == self.cheese:
				self.won = True
				self.info.config(text="恭喜！老鼠找到起司了！按 R 再玩一次。")


if __name__ == "__main__":
	window = tk.Tk()
	MouseMaze(window)
	window.mainloop()
