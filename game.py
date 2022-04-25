class Puzzle:
    input_messages = ("Enter your board dimensions: ", "Enter the knight's starting position: ",
                      "Enter your next move: ")
    error_messages = ("Invalid dimensions!", "Invalid position!", "Invalid move! ")
    win_message = "\nWhat a great tour! Congratulations!"
    lose_message = "\nNo more possible moves!"
    option_message = "Do you want to try the puzzle? (y/n): "
    option_errors = ("No solution exists!", "Invalid input!")
    computer_message = "\nHere's the solution!"

    def __init__(self):
        self.dimensions = tuple()
        self.start_position = tuple()
        self.board = list()
        self.current_position = tuple()
        self.possible_moves = set()
        self.visited_squares = 0
        self.solution = list()
        self.cells_size = 0

    @staticmethod
    def get_numbers(input_message, error_message) -> tuple[int, int]:  # get dimensions, simply validate it
        while True:
            numbers = ''.join([i for i in input(input_message).split()])
            if len(numbers) != 2 or not numbers.isdigit() or int(numbers[0]) < 0 or int(numbers[1]) < 0:
                print(error_message)
            else:
                break
        return int(numbers[0]), int(numbers[1])

    def get_start_position(self, input_message, error_message) -> tuple[int, int]:  # get starting position
        while True:
            numbers = self.get_numbers(input_message, error_message)
            if not (0 < numbers[0] <= self.dimensions[0] or 0 < numbers[1] <= self.dimensions[1]):
                print(error_message)
            else:
                break
        return numbers[0], numbers[1]

    def get_next_move(self, input_message, error_message) -> tuple[int, int]:  # get and validate next move numbers
        print()
        while True:
            numbers = self.get_start_position(input_message, error_message)
            if numbers not in self.possible_moves:
                print(error_message, end='')
            else:
                break
        return numbers[0], numbers[1]

    def reset_board(self) -> None:  # reset the board after validating an existing solution
        self.board = [['_' * self.cells_size for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]
        self.board[-self.start_position[1]][self.start_position[0] - 1] = 'X'.rjust(self.cells_size)
        self.current_position = self.start_position
        self.visited_squares = 1
        self.possible_moves.clear()

    def set_board(self) -> None:  # set the board after creating
        self.dimensions = self.get_numbers(self.input_messages[0], self.error_messages[0])
        self.start_position = self.get_start_position(self.input_messages[1], self.error_messages[1])
        self.cells_size = len(str(self.dimensions[0] * self.dimensions[1]))
        self.solution = [[0 for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]
        self.reset_board()

    def find_possible_moves(self, position) -> None:  # check all possible positions
        possible_moves = set()

        if position[1] + 2 <= self.dimensions[1]:
            if position[0] - 1 >= 1:
                possible_moves.add((position[0] - 1, position[1] + 2))
            if position[0] + 1 <= self.dimensions[0]:
                possible_moves.add((position[0] + 1, position[1] + 2))
        if position[1] - 2 >= 1:
            if position[0] - 1 >= 1:
                possible_moves.add((position[0] - 1, position[1] - 2))
            if position[0] + 1 <= self.dimensions[0]:
                possible_moves.add((position[0] + 1, position[1] - 2))
        if position[0] - 2 >= 1:
            if position[1] - 1 >= 1:
                possible_moves.add((position[0] - 2, position[1] - 1))
            if position[1] + 1 <= self.dimensions[1]:
                possible_moves.add((position[0] - 2, position[1] + 1))
        if position[0] + 2 <= self.dimensions[0]:
            if position[1] - 1 >= 1:
                possible_moves.add((position[0] + 2, position[1] - 1))
            if position[1] + 1 <= self.dimensions[1]:
                possible_moves.add((position[0] + 2, position[1] + 1))

        visited = set()  # find and remove visited positions
        for i in possible_moves:
            if self.board[-i[1]][i[0] - 1] == '*'.rjust(self.cells_size):
                visited.add(i)
        possible_moves.difference_update(visited)

        if position == self.current_position:
            for i in possible_moves:
                self.possible_moves.add(i)
                self.find_possible_moves(i)
        else:
            if self.current_position in possible_moves:
                possible_moves.remove(self.current_position)
            self.board[-position[1]][position[0] - 1] = str(len(possible_moves)).rjust(self.cells_size)

    def draw_board(self, grid) -> None:
        digits_max_row = len(str(self.dimensions[1]))
        border_len = (self.cells_size + 1) * self.dimensions[0] + 3

        print(' ' * digits_max_row + '-' * border_len)
        for i in range(self.dimensions[1]):
            row_num = self.dimensions[1] - i
            row = str(row_num).rjust(digits_max_row) + "| "
            row += ' '.join([j for j in grid[i]]) + ' |'
            print(row)
        print(' ' * digits_max_row + '-' * border_len)

        row = ' '.rjust(digits_max_row) + '  '
        row += ' '.join([str(i).rjust(self.cells_size) for i in range(1, self.dimensions[0] + 1)])
        print(row)

    def make_move(self, is_computer=True) -> None:
        next_position = tuple()
        if is_computer:
            possible_moves = {self.board[-i[1]][i[0] - 1]: i for i in self.possible_moves}
            next_position = possible_moves.get(min(possible_moves))
        else:
            next_position = self.get_next_move(self.input_messages[2], self.error_messages[2])
        self.possible_moves.remove(next_position)

        self.board[-next_position[1]][next_position[0] - 1] = 'X'.rjust(self.cells_size)
        self.board[-self.current_position[1]][self.current_position[0] - 1] = '*'.rjust(self.cells_size)
        self.current_position = next_position

        for i in self.possible_moves:
            self.board[-i[1]][i[0] - 1] = '_' * self.cells_size
        self.possible_moves.clear()
        self.visited_squares += 1

    def work(self) -> None:
        self.set_board()
        self.choose_option()

    def choose_user_mode(self) -> None:
        self.find_possible_moves(self.current_position)
        self.draw_board(self.board)
        if self.dimensions[0] * self.dimensions[1] == self.visited_squares:
            print(self.win_message)
        elif not self.possible_moves:
            print(self.lose_message, f"Your knight visited {self.visited_squares} squares!", sep='\n')
        else:
            self.make_move(False)
            self.choose_user_mode()

    def has_solution(self, counter=1) -> bool:  # check the puzzle if it has at least one solution and store it
        self.solution[-self.current_position[1]][self.current_position[0] - 1] = str(counter).rjust(self.cells_size)
        self.find_possible_moves(self.current_position)
        if self.dimensions[0] * self.dimensions[1] == self.visited_squares:
            return True
        elif not self.possible_moves:
            return False
        else:
            self.make_move()
            return self.has_solution(counter + 1)

    def choose_option(self) -> None:
        while True:
            choice = input(self.option_message)
            if choice == 'y':
                if not self.has_solution():
                    print(self.option_errors[0])
                    break
                self.reset_board()
                self.choose_user_mode()
                break
            elif choice == 'n':
                if not self.has_solution():
                    print(self.option_errors[0])
                    break
                self.reset_board()
                print(self.computer_message)
                self.draw_board(self.solution)
                break
            print(self.option_errors[1])


p = Puzzle()
p.work()
