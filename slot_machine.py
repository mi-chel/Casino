import random

# constant that does not change
MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1

ROWS = 3
COLS = 3

# Randomly select symbols
symbol_count = {
    "Seven": 2,
    "Bars": 3,
    "Diamonds": 4,
    "Bell": 6,
    "Cherries": 8,
    "Lemons": 10
}
# Determine multiplier
symbol_value = {
    "Seven": 5,
    "Bars": 4,
    "Diamonds": 3,
    "Bell": 2,
    "Cherries": 1.75,
    "Lemons": 1.5
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    if isinstance(lines, int):
        lines = [lines]
    else:
        # Loops through each line and checks if each column contains the same symbol
        lines = sorted(lines)
        for line in lines:
            symbol = columns[0][line - 1]
            for col in columns:
                if symbol != col[line - 1]:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line)
    return winnings, winning_lines

def print_losses(bet, winnings):
    if bet > winnings:
        print(f"You lost ${bet - winnings}.")

def print_winning_lines(winning_lines):
    if len(winning_lines) == 1:
        print(f"You won on line:", winning_lines[0])
    else:
        print(f"You won on lines:", *winning_lines, sep = ", ")

def get_slot_machine_spin(rows, cols, symbols):
    # Create a list containing all symbols
    all_symbols = [k for k, v in symbols.items() for _ in range(v)]
    columns = []
    for _ in range(cols):
        column = []
        # Create a copy of all_symbols to remove values
        curr_symbols = all_symbols[:]
        for _ in range(rows):
            # Randomly select a symbol
            value = random.choice(curr_symbols)
            # Remove the symbol from the copy
            curr_symbols.remove(value)
            # Add the symbol to the column
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, col in enumerate(columns):
            # Make sure a row is printed on the same line
            print(col[row], end = " | ") if i != len(columns) - 1 else print(col[row], end = "")
        print()

def deposit():
    # Continue until user has entered a valid number
    while True:
        amount = input("How much would you like to deposit? $")
        # Ensures entered amount is a number
        if amount.isdigit():
            # Converts string amount into an int
            amount = int(amount)
            # Ensures amount is a positive value
            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break
        else:
            print("Please enter a number.")
    return amount

def get_number_of_lines():
    while True:
        # Continue until user has entered a valid number in the range
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if lines > MAX_LINES or lines < 1:
                print("You must bet on 1-" + str(MAX_LINES) + " lines.")
            else:
                break
        else:
            print("Please enter a valid number.")
    return lines

def get_chosen_lines(lines):
    while True:
        # Let player choose which line(s) to bet on
        new_lines = input("Choose which line to bet on (1, 2, 3). ")
        if lines == 1:
            if new_lines.isdigit() and lines == len(new_lines):
                new_lines = int(new_lines)
                if new_lines > 3 or new_lines < 1:
                    print("Please enter a valid number.")
                else:
                    print(f"You have chosen to bet on line: {new_lines}")
                    break
            else: 
                print("Please enter a valid number.")
        else:
            try:
                # Split input by commas
                new_lines = [int(line.strip()) for line in new_lines.split(',')]
            except:
                print("Unable to accept input. Try again.")
            # Check if chosen lines are valid
            if all(line in [1, 2, 3] for line in new_lines) and lines == len(new_lines):
                print(f"You have chosen to bet on lines:", *new_lines, sep = ", ")
                break
            else:
                print("Please enter valid numbers separated by commas.")
    return new_lines

def get_bet():
    while True:
        # Continue until player has entered a valid number in the range
        bet = input("How much would you like to bet on each line? $")
        if bet.isdigit():
            bet = int(bet)
            if bet < MIN_BET or bet > MAX_BET:
                print(f"The bet amount must be between ${MIN_BET} - ${MAX_BET}.")
            else:
                break
        else:
            print("Please enter a valid number.")
    return bet

# Spins the slot machine three times
def spin(balance):
    some_lines = get_number_of_lines()
    lines = get_chosen_lines(some_lines)
    # Check that bet amount does not exceed balance
    while True:
        bet = get_bet()
        if isinstance(lines, int):
            total_bet = bet
        else:
            total_bet = bet * len(lines)
        if total_bet > balance:
            print(f"You do not have enough to bet that amount. Your current balance is {balance}.")
            if balance == 0:
                    break        
        else:
            break
    # Make sure player cannot bet when balance is $0
    if balance != 0:
        print(f"You are betting ${bet} on line(s) {lines}. Your total bet is equal to: ${total_bet}.")
        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        print_slot_machine(slots)
        winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
        print(f"You won ${winnings}. ", end = "")
        print_losses(total_bet, winnings)
        print_winning_lines(winning_lines)
        return winnings - total_bet
    return 0

def main():
    balance = deposit()
    while True:
        print(f"Your current balance is ${balance}.")
        res = input("Press enter to spin (q to quit). ")
        if res == "q":
            break
        balance += spin(balance)
    print(f"You left with ${balance}.")

if __name__ == '__main__':
    main()
