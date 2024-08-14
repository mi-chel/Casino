import random
import sys

def print_intro_text():
    print('=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=')
    print('         Welcome to spin the wheel')
    print('                  With bets')
    print('=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=')
    print('There are 6 options on the wheel.')
    print('Green doubles your bet.')
    print('Blue halves your money.')
    print('Yellow 1.5x your bet.')
    print('Red wins you your bet.')
    print('Orange loses your bet.')
    print("Purple gives you another spin.")

def get_deposit():
    while True:
        deposit = input('Please deposit money to play: $')
        try:
            deposit = float(deposit)
            if deposit > 0:
                return deposit
            else:
                print(f'Please deposit more than $0')
        except ValueError:
            print('Please enter a valid numerical amount.')

def get_bet(balance):
    while True:
        bet = input('How much do you want to bet on this spin: $')
        try:
            bet = float(bet)
            if bet <= balance and bet > 0:
                print(f'Thank you, you have bet: ${bet:.2f}.')
                return bet
            else:
                print(f'Please bet an amount more than $0 and less than or equal to your balance of ${balance:.2f}.')
        except ValueError:
            print('Please enter a valid numerical amount.')

def spin_wheel(balance):
    while True:
        bet = get_bet(balance)    
        results = {1: {'result': bet * 2, 'color': 'Green', 'description': 'doubles your bet'},
                   2: {'result': -(balance * 0.5), 'color': 'Blue', 'description': 'halves your money'},
                   3: {'result': bet * 1.5, 'color': 'Yellow', 'description': 'gives you 1.5x your bet'}, 
                   4: {'result': bet, 'color': 'Red', 'description': 'win your bet'},
                   5: {'result': -bet, 'color': 'Orange', 'description': 'loses your bet'},
                   6: {'result': None, 'color': 'Purple', 'description': 'gives you another spin'}}
        spin = random.randint(1, 6)
        result = results[spin]
        if result['color'] == 'Purple':
            print(f"Spin result: {result['color']} - {result['description']}. Spin again!")
            return spin_wheel(balance)
        
        print(f"Spin result: {result['color']} - {result['description']}.")
        return result['result']

def main():
    print_intro_text()
    balance = get_deposit()
    while True:
        print(f"Your current balance is ${balance}.")
        res = input("Press enter to spin the wheel (q to quit). ")
        if res == "q":
            break
        balance += spin_wheel(balance)
        if balance == 0:
            print("Sorry, you have lost all your money.")
            break
    print(f"You left with ${balance}.")

if __name__ == '__main__':
    main()