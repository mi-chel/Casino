import random 
import time

MIN_BET = 1
CARD_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 
CARDS = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] 
deck = [(card, category) for category in CARD_SUITS for card in CARDS] 

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

def get_bet():
    while True:
        # Continue until player has entered a valid number in the range
        bet = input("How much would you like to bet? $")
        if bet.isdigit():
            bet = int(bet)
            if bet < MIN_BET:
                print(f"The bet amount must be at least ${MIN_BET}.")
            else:
                print("\n")
                break
        else:
            print("Please enter a valid number.")
    return bet

def card_value(card, curr_score): 
    if card[0] in ['Jack', 'Queen', 'King']: 
        return 10
    elif card[0] == 'Ace':
        if curr_score + 11 > 21:
            return 1
        else:
            return 11
    else: 
        return int(card[0]) 
 
def deal_cards(d):
    random.shuffle(d) 
    player_cards = [d.pop(), d.pop()] 
    dealer_cards = [d.pop(), d.pop()]
    return player_cards, dealer_cards
  
def sum_of_cards(p_cards, d_cards):
    # Calculate player's score
    player_score = 0
    for card in p_cards:
        player_score += card_value(card, player_score)
    # Calculate dealer's score
    dealer_score = 0
    for card in d_cards:
        dealer_score += card_value(card, dealer_score)
    return player_score, dealer_score

def print_results(d_cards, d_score, p_cards, p_score, msg):
    print("\n") 
    print("Cards Dealer Has:", d_cards) 
    print("Score Of The Dealer:", d_score) 
    print("Cards Player Has:", p_cards) 
    print("Score Of The Player:", p_score) 
    print(msg) 

def check_naturals(player_score, dealer_score):
    if player_score == 21 and dealer_score == 21:
        print("Both player and dealer have BLACKJACK! It's a tie.")
        return "tie"
    elif player_score == 21:
        print("BLACKJACK! Congratulations, you win!")
        return "player"
    elif dealer_score == 21:
        print("BLACKJACK! Dealer wins!")
        return "dealer"
    return None


def check_winnings(p_score, d_score, p_cards, d_cards, bet):
    player_win, dealer_win = False, False
    if p_score == 21:
        print("BLACKJACK! Congratulations, you win!")
        player_win = True
    elif d_score == 21:
        print("BLACKJACK! Dealer wins!")
        dealer_win = True
    elif d_score > 21 and p_score < 21: 
        print_results(d_cards, d_score, p_cards, p_score, 
                    "Player wins (Dealer Loss Because Dealer Score has exceeded 21)")
        player_win = True
    elif p_score > 21 and d_score < 21:
        print_results(d_cards, d_score, p_cards, p_score, 
                        "Dealer wins (Player Loss Because Player Score has exceeded 21)")
        dealer_win = True
    elif p_score > d_score: 
        print_results(d_cards, d_score, p_cards, p_score, 
                    "Player wins (Player Has High Score than Dealer)")
        player_win = True
    elif d_score > p_score: 
        print_results(d_cards, d_score, p_cards, p_score, 
                    "Dealer wins (Dealer Has High Score than Player)")
        dealer_win = True
    else: 
        print_results(d_cards, d_score, p_cards, p_score, "It's a tie.")

    if player_win and not dealer_win:
        return bet * 2.5
    elif not player_win and dealer_win:
        return -bet
    return 0

def player_turn(deck, p_cards, revealed_card):
    print("The dealer's revealed card is:", revealed_card)
    print("The dealer's current score is:", card_value(revealed_card, 0))
    while True: 
        player_score, _ = sum_of_cards(p_cards, [])
        print("You have the cards:", p_cards) 
        print("Your current score:", player_score) 
        print("\n") 
        if player_score > 21:
            print("BUST")
            break
        choice = input('What do you want to do? ["HIT" to request another card, "STAND" to stay at your current total]: ').lower() 
        if choice == "hit": 
            new_card = deck.pop() 
            p_cards.append(new_card) 
        elif choice == "stand": 
            break
        else: 
            print("Invalid choice. Please try again.") 
    return player_score

def dealer_turn(deck, dealer_cards):
    _, dealer_score = sum_of_cards([], dealer_cards)
    print("The dealer's second card is:", dealer_cards[1])
    print("The dealer's current score is:", dealer_score)
    time.sleep(3)
    while dealer_score < 17:
        new_card = deck.pop()
        dealer_cards.append(new_card)
        dealer_score += card_value(new_card, dealer_score)
        print("\n")
        print("The dealer has pulled the card:", new_card)
        print("The dealer's current score is:", dealer_score)
        time.sleep(3)
    print("\n")
    return dealer_score

def play_game(balance):
    player_cards, dealer_cards = deal_cards(deck)
    bet = get_bet()
    while bet > balance:
        print(f"You do not have enough to bet that amount. Your current balance is {balance}.")
        bet = get_bet()
    player_score, dealer_score = sum_of_cards(player_cards, dealer_cards)
    # Check for naturals before proceeding
    result = check_naturals(player_score, dealer_score)
    if result == "player":
        return bet * 2.5
    elif result == "dealer":
        return -bet
    elif result == "tie":
        return 0
    
    player_score = player_turn(deck, player_cards, dealer_cards[0])
    dealer_score = dealer_turn(deck, dealer_cards)

    return check_winnings(player_score, dealer_score, player_cards, dealer_cards, bet)

def main():
    balance = deposit()
    while True:
        print(f"Your current balance is ${balance}.")
        res = input("Press enter to play (q to quit). ")
        if res == "q":
            break
        balance += play_game(balance)
        if balance == 0:
            break
    print(f"You left with ${balance}.")
    
if __name__ == '__main__':
    main()