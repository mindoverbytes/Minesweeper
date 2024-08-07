import random

class Minesweeper:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.num_revealed = 0
        self.create_mines()
        self.number_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def create_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] != 'X':
                self.board[row][col] = 'X'
                mines_placed += 1

    def print_board(self, show_mines=False):
        print("\n")
        print('   ' + '  '.join(str(i) for i in range(self.cols)))
        for i, row in enumerate(self.board):
            print(i, ' '.join(self.get_cell_display(i, j, show_mines) for j in range(self.cols)))
        print("\n")

    def get_cell_display(self, row, col, show_mines):
        if self.revealed[row][col]:
            if self.board[row][col] == ' ':
                return '⬛'
            elif self.board[row][col].isdigit():
                return self.number_emojis[int(self.board[row][col])] + ' '
            else:
                return self.board[row][col] + ' '
        elif self.flags[row][col]:
            return '🚩'
        elif show_mines and self.board[row][col] == 'X':
            return '💣'
        else:
            return '⬜'

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (0 <= r < self.rows) and (0 <= c < self.cols) and (r != row or c != col):
                    if self.board[r][c] == 'X':
                        count += 1
        return count

    def reveal_cell(self, row, col):
        if not self.is_valid_position(row, col):
            print("Invalid input. Row and column numbers must be within range.")
            return False
        if self.flags[row][col]:
            print("Cell is flagged. Unflag it before revealing.")
            return True
        if self.board[row][col] == 'X':
            print("Hit a mine!")
            return False
        if self.revealed[row][col]:
            return True
        
        count = self.count_adjacent_mines(row, col)
        self.board[row][col] = str(count) if count > 0 else ' '
        self.revealed[row][col] = True
        self.num_revealed += 1
        if count == 0:
            self.reveal_empty_cells(row, col)
        return True

    def reveal_empty_cells(self, row, col):
        queue = [(row, col)]
        while queue:
            r, c = queue.pop(0)
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if self.is_valid_position(nr, nc) and not self.revealed[nr][nc] and not self.flags[nr][nc]:
                        count = self.count_adjacent_mines(nr, nc)
                        self.board[nr][nc] = str(count) if count > 0 else ' '
                        self.revealed[nr][nc] = True
                        self.num_revealed += 1
                        if count == 0:
                            queue.append((nr, nc))

    def toggle_flag(self, row, col):
        if not self.is_valid_position(row, col):
            print("Invalid input. Row and column numbers must be within range.")
            return
        self.flags[row][col] = not self.flags[row][col]

    def check_win(self):
        total_cells = self.rows * self.cols
        return total_cells - self.num_revealed == self.num_mines

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

def get_valid_input(prompt, valid_range):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            else:
                print(f"Please enter a value within the range {valid_range}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def play_game():
    rows = get_valid_input("Enter number of rows (maximum 9): ", range(1, 10))
    cols = get_valid_input("Enter number of columns (maximum 9): ", range(1, 10))
    num_mines = get_valid_input("Enter number of mines: ", range(1, rows * cols))

    game = Minesweeper(rows, cols, num_mines)
    game.print_board()

    while True:
        action = input("Enter 'R' to reveal, 'F' to flag/unflag a cell: ").upper()
        if action in ('R', 'F'):
            row = get_valid_input(f"Enter row number (0 to {rows - 1}): ", range(rows))
            col = get_valid_input(f"Enter column number (0 to {cols - 1}): ", range(cols))

            if action == 'R':
                if not game.reveal_cell(row, col):
                    print("Game Over! You hit a mine.")
                    game.print_board(show_mines=True)
                    break
                game.print_board()
                if game.check_win():
                    print("Congratulations! You have won!")
                    game.print_board(show_mines=True)
                    break
            elif action == 'F':
                game.toggle_flag(row, col)
                game.print_board()
                if game.check_win():
                    print("Congratulations! You have won!")
                    game.print_board(show_mines=True)
                    break
        else:
            print("Invalid action. Please enter 'R' to reveal or 'F' to flag/unflag a cell.")

if __name__ == "__main__":
    play_game()
