import random

# Declaring constants
FLAG_SYMBOL = '\u2691'
ALPHABET = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

class MinesweeperBoard:
    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.shown = [['☐' for i in range(size)] for i in range(size)]
        self.hidden = [['☐' for i in range(size)] for i in range(size)]
        self.place_mines()
        self.count_adjacent_mines()

    def place_mines(self):
        """
        Picks random cell and places mine there until desired mine quota is met.
        """
        mines_placed = 0
        while mines_placed < self.num_mines:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.hidden[row][col] != '☀':
                self.hidden[row][col] = '☀'
                mines_placed += 1

    def count_adjacent_mines(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.hidden[row][col] != '☀':
                    count = 0
                    for row_change in [-1, 0, 1]:
                        for col_change in [-1, 0, 1]:
                            new_row = row + row_change
                            new_col = col + col_change

                            # Adds 1 to count for each adjacent mine
                            if (0 <= new_row < self.size and 
                                    0 <= new_col < self.size and 
                                        self.hidden[new_row][new_col] == '☀'):
                                
                                count += 1

                    self.hidden[row][col] = str(count) if count > 0 else ' '


def display_board(board):
    size = len(board)
    print("    ", end="")
    for j in range(1, size + 1):
        print(f"{j}", end="   " if j < 10 else "  ")
    print("\n" + " " * 4 + "-" * (4 * size))
    for i in range(size):
        print(f"{ALPHABET[i]} | {' | '.join(board[i])} |\n" + " " * 4 + "-" * 
                (4 * size))

def uncover(board, hidden_board, row, col):
    """
    Uncovers desired cell. If cell is empty, recursively
    checks adjacent cells and uncovers empty cells.

    Returns:
        Game over if mine is uncovered
    """
    
    if hidden_board[row][col] == '☀':
        return 'Game Over'
    count = hidden_board[row][col]
    board[row][col] = str(count)
    if count == ' ':
        for row_change in [-1, 0, 1]:
            for col_change in [-1, 0, 1]:
                new_row = row + row_change
                new_col = col + col_change
                # Checks that the cell is in bounds and it is uncovered
                # Sets cell in shown grid to the value in hidden grid's counterpart
                if (0 <= new_row < len(board) and 0 <= new_col < len(board) and board[new_row][new_col] == '☐'):
                    board[new_row][new_col] = hidden_board[new_row][new_col]
                    # Recursive check
                    if hidden_board[new_row][new_col] == ' ':
                        uncover(board, hidden_board, new_row, new_col)

def all_mines_flagged(shown_board, hidden_board, size):
    """
    Checks win condition after each turn taken by player

    Returns:
        Boolean. True = win, False = continue game
    """
    for row in range(size):
        for col in range(size):
            if hidden_board[row][col] == '☀' and shown_board[row][col] != FLAG_SYMBOL:
                return False
    return True

def play_game():
    # Takes user input for desired size and amt of mines.
    # If user input is too large/small sets it to a predetermined value
    size = int(input("Enter the size of the minefield: "))  
    if size > 15:
        print("Relax superhero. Let's stick to 15 max and see if you aren't vaporized after.")
        size = 15
    if size < 3:
        print("That's too small, how about we up it a bit?")
        size = 7

    num_mines = int(input("Enter the number of mines: "))
    if num_mines > ((size ** 2) - 1):
        print("Daring today aren't we?")
        num_mines = round(((size ** 2) * 0.15))
        print(f'How about we stick to {num_mines} instead.')
    if num_mines == 0:
        print("There is no peaceful mode. Let's spice it up.")
        num_mines = round(((size ** 2) * 0.1))
        print(f"We'll start of easy with {num_mines} mines. Good luck!")

    board = MinesweeperBoard(size, num_mines)

    while True:
        display_board(board.shown)
        print('U - Uncover | F - Flag/Undo flag | Q - Flag/Undo Flag with question mark')
        action = input('Please enter the action you would like to perform: ')

        row = input(f"Enter row (A to {ALPHABET[size - 1]}): ")
        row = ALPHABET.index(row.upper())
        col = int(input(f"Enter column (1 to {size}): "))
        col -= 1 
        
        if action.upper() == 'F' or action.upper() == 'FLAG': 
            if 0 <= row < size and 0 <= col < size:
                if board.shown[row][col] == FLAG_SYMBOL:
                    board.shown[row][col] = '☐'
                    print(f'Flag removed from ({ALPHABET[row]},{col + 1}) tread lightly.')
                else:
                    board.shown[row][col] = FLAG_SYMBOL
                    print("Cell marked as full of deadly explosives and should be avoided at all costs. Nice!")
            else:
                print(f"Were you looking to place a flag in the void? Or on the board?"
                      f"The choices are between 1 and {size}.")
        
        elif action.upper() == 'U' or action.upper() == 'UNCOVER':
            if 0 <= row < size and 0 <= col < size:
                result = uncover(board.shown, board.hidden, row, col)
                if result == 'Game Over':
                    display_board(board.hidden)
                    print("Game Over. You hit a mine!")
                    exit()
                else:
                    print("This room appears to be safe. Keep it up!")
            else:
                print(f"Row and column must be between 1 and {size}.")
        
        elif action.upper() == 'Q' or action == '?':
                if 0 <= row < size and 0 <= col < size:
                    if board.shown[row][col] == '?':
                        board.shown[row][col] = '☐'
                        print(f"'?' removed from ({ALPHABET[row]},{col + 1})." 
                               "Congrats on finally making up your mind.")
                    else:
                        board.shown[row][col] = '?'
                        print('Ah yes, the greatest question of all: "Will I violently explode if I enter this room?" Room marked.')

        else:
            print('Action not recognized, please try again.')

        if all_mines_flagged(board.shown, board.hidden, size):
            display_board(board.hidden)
            print("Congratulations! You've flagged all mines and won the game!")
            exit()

if __name__ == '__main__':
    print("Welcome to Minesweeper! Good luck!")
    play_game()