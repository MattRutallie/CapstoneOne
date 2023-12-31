import random

# ideas for flagging a cell and adding a ? mark option
# These were initally seperate but are so similar that I included em in one update

FLAG_SYMBOL = '\u2691'  # Unicode flag symbol
QUESTION_MARK_SYMBOL = '?'

alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]


class Minefield:
    def __init__(self, size):
        self.size = size
        self.board = [['☐' for _ in range(size)] for _ in range(size)]

    def display(self, board):
        self.board = board
        print("    ", end="")
        for j in range(1, self.size + 1):
            print(f"{j}", end="   " if j < 10 else "  ")
        print("\n" + " " * 4 + "-" * (4 * self.size))
        # This part includes the flag symbol on the players board
        for i in range(self.size):
            print(
                f"{alphabet[i]} | {' | '.join(self.board[i]).replace('F', FLAG_SYMBOL).replace('?', QUESTION_MARK_SYMBOL)} |\n" + " " * 4 + "-" * (
                            4 * self.size))


class Hidden(Minefield):
    def __init__(self, size, num_mines):
        super().__init__(size)
        self.num_mines = num_mines
        self.place_mines()
        self.count_adjacent_mines()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.board[row][col] != '☀':
                self.board[row][col] = '☀'
                mines_placed += 1

    def count_adjacent_mines(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != '☀':
                    count = 0
                    for row_change in [-1, 0, 1]:
                        for col_change in [-1, 0, 1]:
                            new_row = row + row_change
                            new_col = col + col_change

                            # Make this more readable
                            if 0 <= new_row < self.size and 0 <= new_col < self.size and self.board[new_row][
                                new_col] == '☀':
                                count += 1
                    self.board[row][col] = str(count) if count > 0 else ' '


class MinesweeperGame():
    def __init__(self):
        self.size = int(input("Enter the size of the minefield: "))
        if self.size > 15:
            print("Relax superhero. Let's stick to 15 max and see if you aren't vaporized after.")
            self.size = 15
        self.num_mines = int(input("Enter the number of mines: "))
        if self.num_mines > ((self.size ** 2) - 1):
            print("Daring today aren't we?")
            self.num_mines = round(((self.size ** 2) * 0.15))
            print(f'How about we stick to {self.num_mines} instead.')
        self.hidden_board = Hidden(self.size, self.num_mines)
        self.player_board = Minefield(self.size)
        self.play()

    def uncover(self, row, col):
        if self.hidden_board.board[row][col] == '☀':
            return 'Game Over'
        count = self.hidden_board.board[row][col]
        self.player_board.board[row][col] = str(count)

        # Simplify/Make easier to read. Potentially split into 2 methods

        if count == ' ':
            for row_change in [-1, 0, 1]:
                for col_change in [-1, 0, 1]:
                    new_row = row + row_change
                    new_col = col + col_change
                    if 0 <= new_row < self.size and 0 <= new_col < self.size and self.player_board.board[new_row][
                        new_col] == '☐':
                        self.player_board.board[new_row][new_col] = self.hidden_board.board[new_row][new_col]
                        if self.hidden_board.board[new_row][new_col] == ' ':
                            self.uncover(new_row, new_col)

    def all_mines_flagged(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.hidden_board.board[row][col] == '☀' and self.player_board.board[row][col] != FLAG_SYMBOL:
                    return False
        return True

    # this updates the "MinesweeperGame" to include flagging funcationality. with ~flavor~
    def play(self):


        while True:
            self.player_board.display(self.player_board.board)
            print('U - Uncover | F - Flag/Undo flag | Q - Flag/Undo Flag with question mark')
            action = input('Please enter the action you would like to perform: ')

            if action.upper() == 'U':
                row = input(f"Enter row (A to {alphabet[self.size - 1]}): ")
                row = row = alphabet.index(row.upper())
                col = int(input(f"Enter column (1 to {self.size}): "))
                col -= 1
                if 0 <= row < self.size and 0 <= col < self.size:
                    result = self.uncover(row, col)
                    if result == 'Game Over':
                        print(
                             "Upon stepping into the room, you hear a soft click as a pressure plate depresses underfoot.\n" 
                             "As you relize the gravity of your actions, you find yourself relived of your wordly belongings (and your legs, oof).")
                        self.hidden_board.display(self.hidden_board.board)
                        print('You are cast into the void, game over.')
                        exit()
                    else:
                        print("This room appears to not be lined with anti-personal mines, nice. Keep it up!")
                else:
                    print(f"While I respect the creativity, we are all bound to confines of space and time(and the rules of this game)." 
                          f"Row and column must be between 1 and {self.size}.")


            elif action.upper() == 'F':
                row = input(f"Enter row (A to {alphabet[self.size - 1]}): ")
                row = alphabet.index(row.upper())
                col = int(input(f"Enter column (1 to {self.size}): "))
                col -= 1  
                if 0 <= row < self.size and 0 <= col < self.size:
                    if self.player_board.board[row][col] == FLAG_SYMBOL:
                        self.player_board.board[row][col] = '☐'
                        print(f'Flag removed from [{alphabet[row]},{col + 1}] tread lightly.')
                    else:
                        self.player_board.board[row][col] = FLAG_SYMBOL
                        print("Cell marked as full of deadly explosives and should be avoided at all costs. Nice!")
                else:
                    print(
                        f"Were you looking to place a flag in the void? Or on the board? The choices are between 1 and {self.size}.")

            elif action.upper() == 'Q' or action.upper() == '?':
                row = input(f"Enter row (A to {alphabet[self.size - 1]}) to mark a cell: ")
                row = alphabet.index(row.upper())
                col = int(input(f"Enter column (1 to {self.size}): "))
                col -= 1
                if 0 <= row < self.size and 0 <= col < self.size:
                    if self.player_board.board[row][col] == QUESTION_MARK_SYMBOL:
                        self.player_board.board[row][col] = '☐'
                        print(f"'?' removed from [{alphabet[row]},{col + 1}]." 
                               "Congrats on finally making up your mind.")
                    else:
                        self.player_board.board[row][col] = QUESTION_MARK_SYMBOL
                        print('Ah yes, the greatest question of all: "Will I violently explode if I enter this room?" Room marked.')

            else:
                print('Action not recognized, please try again.')

            if self.all_mines_flagged():
                self.hidden_board.display(self.hidden_board.board)
                print("Congratulations! You've flagged all mines and won the game!")
                exit()    


if __name__ == '__main__':
    print("Welcome to Minesweeper! You pulled the short straw eh? Gooooooooooood luck pal.")
    MinesweeperGame()
