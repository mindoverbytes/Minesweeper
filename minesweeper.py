import random

class Minesweeper:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]  
        self.num_revealed = 0  
        self.create_mines()

    def create_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] != 'X':
                self.board[row][col] = 'X'
                mines_placed += 1

    def print_board(self, show_mines=False):
        print('   ' + '  '.join(str(i) for i in range(self.cols)))
        print('  ' + '+---' * self.cols + '+')
        for i, row in enumerate(self.board):
            print(i, '| ' + ' | '.join(
                cell if (cell != 'X' and not self.flags[i][j]) or (show_mines and cell == 'X') else 'F'
                if self.flags[i][j] else ' '
                for j, cell in enumerate(row)) + ' |')
            print('  ' + '+---' * self.cols + '+')

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (0 <= r < self.rows) and (0 <= c < self.cols) and (r != row or c != col):
                    if self.board[r][c] == 'X':
                        count += 1
        return count

    def reveal_cell(self, row, col):
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            print("Invalid input. Row and column numbers must be within range.")
            return True  
        if self.flags[row][col]:
            print("Cell is flagged. Unflag it before revealing.")
            return True  
        if self.board[row][col] == 'X':
            print("Hit a mine!")
            return False  
        else:
            count = self.count_adjacent_mines(row, col)
            self.board[row][col] = str(count) if count > 0 else ' '
            self.num_revealed += 1
            if count == 0:
                self.reveal_empty_cells(row, col)
            return True

    def reveal_empty_cells(self, row, col):
        stack = [(row, col)]
        visited = set()  
        while stack:
            r, c = stack.pop()
            visited.add((r, c))
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.rows) and (0 <= nc < self.cols) and (nr, nc) not in visited:
                        count = self.count_adjacent_mines(nr, nc)
                        self.board[nr][nc] = str(count) if count > 0 else ' '
                        self.num_revealed += 1
                        visited.add((nr, nc))
                        if count == 0:
                            stack.append((nr, nc))

    def toggle_flag(self, row, col):
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            print("Invalid input. Row and column numbers must be within range.")
            return  
        self.flags[row][col] = not self.flags[row][col]

    def check_win(self):
        total_cells = self.rows * self.cols
        return total_cells - self.num_revealed == self.num_mines

def play_game():
    while True:
        rows = input("Enter number of rows (maximum 9): ")
        cols = input("Enter number of columns (maximum 9): ")
        num_mines = input("Enter number of mines: ")

        try:
            rows = int(rows)
            cols = int(cols)
            num_mines = int(num_mines)
            if rows <= 0 or rows > 9 or cols <= 0 or cols > 9:
                print("Rows and columns must be between 1 and 9.")
                continue
            if num_mines <= 0:
                print("Number of mines must be greater than zero.")
                continue
        except ValueError:
            print("Invalid input. Please enter valid integers for rows, columns, and mines.")
            continue

        game = Minesweeper(rows, cols, num_mines)
        game.print_board()

        while True:
            action = input("Enter 'R' to reveal, 'F' to flag/unflag a cell: ").upper()
            if action == 'R':
                try:
                    row = int(input("Enter row number (0 to {}): ".format(rows - 1)))
                    col = int(input("Enter column number (0 to {}): ".format(cols - 1)))
                except ValueError:
                    print("Invalid input. Please enter valid integers for row and column numbers.")
                    continue

                if not (0 <= row < rows) or not (0 <= col < cols):
                    print("Invalid input. Row and column numbers must be within range.")
                    continue

                if not game.reveal_cell(row, col):
                    print("Game Over! You hit a mine.")
                    print("Final board:")
                    game.print_board(show_mines=True)
                    break  
                game.print_board()
                if game.check_win():
                    print("Congratulations! You have won!")
                    game.print_board(show_mines=True)
                    break  
            elif action == 'F':
                try:
                    row = int(input("Enter row number (0 to {}): ".format(rows - 1)))
                    col = int(input("Enter column number (0 to {}): ".format(cols - 1)))
                except ValueError:
                    print("Invalid input. Please enter valid integers for row and column numbers.")
                    continue

                if not (0 <= row < rows) or not (0 <= col < cols):
                    print("Invalid input. Row and column numbers must be within range.")
                    continue

                game.toggle_flag(row, col)
                game.print_board()
                if game.check_win():
                    print("Congratulations! You have won!")
                    game.print_board(show_mines=True)
                    break  
            else:
                print("Invalid action. Please enter 'R' to reveal or 'F' to flag/unflag a cell.")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            break

if __name__ == "__main__":
    play_game()
