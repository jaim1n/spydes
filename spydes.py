import random
import os
import time

# Define suits, ranks, and their symbols
SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUIT_SYMBOLS = {
    'Clubs': '♣',
    'Diamonds': '♦',
    'Hearts': '♥',
    'Spades': '♠'
}

# ANSI escape codes for red text
RED_TEXT = '\033[91m'
RESET_TEXT = '\033[0m'

# Create a deck of cards
def create_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

# Deal cards to players
def deal_cards(deck):
    player1_hand = deck[:13]
    player2_hand = deck[13:26]
    return player1_hand, player2_hand

# Function to format cards nicely with symbols and colors
def format_card(card):
    rank, suit = card
    symbol = SUIT_SYMBOLS[suit]
    if suit in ['Diamonds', 'Hearts']:
        return f"{RED_TEXT}{symbol} {rank} of {suit}{RESET_TEXT}"
    else:
        return f"{symbol} {rank} of {suit}"

# Clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display Player 1's hand, sorted and with proper symbols and colors
def display_player1_hand(player1_hand):
    sorted_hand = sorted(player1_hand, key=lambda x: (SUITS.index(x[1]), RANKS.index(x[0])))

    hand_by_suit = {
        'Clubs': [],
        'Diamonds': [],
        'Hearts': [],
        'Spades': []
    }
    for card in sorted_hand:
        hand_by_suit[card[1]].append(card[0])

    print("Your hand:")
    for suit in SUITS:
        symbol = SUIT_SYMBOLS[suit]
        cards = " ".join(hand_by_suit[suit])

        if suit in ['Diamonds', 'Hearts']:
            print(f"{RED_TEXT}{symbol}: {cards}{RESET_TEXT}")
        else:
            print(f"{symbol}: {cards}")
    print()

# Function to get a bid from Player 1
def get_player1_bid(player1_hand):
    def calculate_guaranteed_tricks(hand):
        guaranteed_tricks = 0
        spades_ranking = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        spades_in_hand = sorted(
            [rank for rank, suit in hand if suit == 'Spades'],
            key=lambda r: spades_ranking.index(r)
        )
        for i, rank in enumerate(spades_in_hand):
            if spades_ranking.index(rank) <= i:
                guaranteed_tricks += 1
            else:
                break
        return guaranteed_tricks

    display_player1_hand(player1_hand)
    guaranteed_tricks = calculate_guaranteed_tricks(player1_hand)

    while True:
        try:
            bid = int(input(f"Enter your bid ({guaranteed_tricks} - 13): "))
            if bid < guaranteed_tricks:
                trick_word = "trick" if guaranteed_tricks == 1 else "tricks"
                print(f"You have {guaranteed_tricks} guaranteed {trick_word}. Try again.")
            elif bid > 13:
                print("You cannot bid more than 13.")
            else:
                print()
                return bid
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function for Player 2's bid based on hand analysis (enhanced strategy)
def get_player2_bid(player2_hand):
    high_cards = sum(1 for rank, _ in player2_hand if rank in ['A', 'K', 'Q', 'J'])
    spades = sum(1 for _, suit in player2_hand if suit == 'Spades')
    low_cards = sum(1 for rank, _ in player2_hand if rank in ['2', '3', '4', '5'])

    if high_cards <= 2 and low_cards >= 8:
        bid = 0
        print("Spyder bids Nil.\n")
    else:
        bid = high_cards + spades // 2
        bid = max(1, min(13, bid))
        print(f"Spyder bids: {bid}\n")
    
    return bid

# Determine the winner of a trick based on the cards played
def determine_trick_winner(card1, card2, lead_suit):
    rank1, suit1 = card1
    rank2, suit2 = card2

    if suit1 == suit2:
        return 1 if RANKS.index(rank1) > RANKS.index(rank2) else 2
    elif suit1 == 'Spades' and suit2 != 'Spades':
        return 1
    elif suit2 == 'Spades' and suit1 != 'Spades':
        return 2
    elif suit1 == lead_suit:
        return 1
    else:
        return 2

# Function for Player 1 to select a card to play
def get_player1_card(player1_hand, lead_suit, spades_broken, is_lead):
    sorted_hand = sorted(player1_hand, key=lambda x: (SUITS.index(x[1]), RANKS.index(x[0])))
    display_player1_hand(sorted_hand)
    print("Select a card to play:")
    for idx, card in enumerate(sorted_hand):
        print(f"{idx + 1}: {format_card(card)}")
    print()

    while True:
        try:
            choice = int(input("Enter the number of the card want to play: ")) - 1
            selected_card = sorted_hand[choice]

            if is_lead:
                if selected_card[1] == 'Spades' and not spades_broken:
                    non_spade_cards = [card for card in sorted_hand if card[1] != 'Spades']
                    if non_spade_cards:
                        print("Spades have not been broken yet. Try again.")
                        continue
                player1_hand.remove(selected_card)
                return selected_card

            # If Player 1 is not leading, they must follow the lead suit if possible
            if lead_suit and selected_card[1] != lead_suit:
                if any(card[1] == lead_suit for card in sorted_hand):
                    # Remove the trailing 's' for grammatical purposes
                    display_suit = lead_suit[:-1] if lead_suit.endswith('s') else lead_suit
                    print(f"You must play a {display_suit}. Try again.")
                    continue

            player1_hand.remove(selected_card)
            return selected_card

        except (ValueError, IndexError):
            print("Invalid choice. Try again.")

# Function for Player 2 to play a card with enhanced strategy
def get_player2_card(player2_hand, lead_suit, spades_broken, is_lead):
    if is_lead:
        if spades_broken:
            card = min(player2_hand, key=lambda x: RANKS.index(x[0]))
        else:
            non_spade_cards = [card for card in player2_hand if card[1] != 'Spades']
            if non_spade_cards:
                card = min(non_spade_cards, key=lambda x: RANKS.index(x[0]))
            else:
                card = min(player2_hand, key=lambda x: RANKS.index(x[0]))
    else:
        same_suit_cards = [card for card in player2_hand if card[1] == lead_suit]
        if same_suit_cards:
            card = min(same_suit_cards, key=lambda x: RANKS.index(x[0]))
        else:
            spades = [card for card in player2_hand if card[1] == 'Spades']
            if spades and spades_broken:
                card = min(spades, key=lambda x: RANKS.index(x[0]))
            else:
                card = min(player2_hand, key=lambda x: RANKS.index(x[0]))

    player2_hand.remove(card)
    print(f"Spyder plays: {format_card(card)}\n")
    return card

def get_player_name():
    if os.path.exists("player_name.txt"):
        with open("player_name.txt", "r") as file:
            player_name = file.read().strip()
        if not player_name or not player_name.isalpha():
            player_name = None
    else:
        player_name = None

    while not player_name:
        player_name = input("Enter your name: ").strip()
        if not player_name.isalpha():
            print("Invalid name. Please enter a name with only alphabetical characters (A-Z).")
            player_name = None

    # Format the name to capitalize the first letter and lowercase the rest
    player_name = player_name.capitalize()
    
    with open("player_name.txt", "w") as file:
        file.write(player_name)
    
    return player_name

# Play a single round of the game
def play_round(player1_hand, player2_hand, player1_bid, player2_bid, last_trick=None, player2_lead=False, spades_broken=False):
    player1_tricks = 0
    player2_tricks = 0
    spades_message = False
    lead_suit = None
    player_name = get_player_name()  # Get the player's name from the file

    for i in range(13):
        clear_terminal()

        print(f"{player_name}'s tricks: {player1_tricks}/{player1_bid}")
        print(f"Spyder's tricks: {player2_tricks}/{player2_bid}\n")

        if spades_message:
            print("Spades have been broken!\n")
            spades_message = False

        if last_trick:
            print(f"{last_trick}\n")

        if player2_lead:
            card2 = get_player2_card(player2_hand, lead_suit, spades_broken, is_lead=True)
            lead_suit = card2[1]
            card1 = get_player1_card(player1_hand, lead_suit, spades_broken, is_lead=False)
        else:
            card1 = get_player1_card(player1_hand, lead_suit, spades_broken, is_lead=True)
            lead_suit = card1[1]
            card2 = get_player2_card(player2_hand, lead_suit, spades_broken, is_lead=False)

        if not spades_broken and (card1[1] == 'Spades' or card2[1] == 'Spades'):
            spades_broken = True
            spades_message = True

        winner = determine_trick_winner(card1, card2, lead_suit)

        if winner == 1:
            player1_tricks += 1
            last_trick = f"{player_name} wins trick {i + 1} with {format_card(card1)} over {format_card(card2)}"
            player2_lead = False
        else:
            player2_tricks += 1
            last_trick = f"Spyder wins trick {i + 1} with {format_card(card2)} over {format_card(card1)}"
            player2_lead = True

    return player1_tricks, player2_tricks, last_trick

# Calculate the score based on bids, tricks won, and sandbags
def calculate_score(tricks, bid, sandbags):
    if bid == 0:
        if tricks == 0:
            return 100, sandbags
        else:
            return -100, sandbags
    else:
        score = 10 * bid if tricks >= bid else -10 * bid
        if tricks > bid:
            sandbags += (tricks - bid)
            score += (tricks - bid)
            if sandbags >= 10:
                score -= 100
                sandbags -= 10
        
        return score, sandbags

# Countdown to start of game  
def countdown_game(seconds=3):
    for i in range(seconds, 0, -1):
        # \r moves the cursor to the beginning of the line
        print(f"\rGame starts in {i}...", end='', flush=True)
        time.sleep(1)

# Countdown to next round
def countdown_round(seconds=10):
    print()
    for i in range(seconds, 0, -1):
        print(f"\rRound ends in {i}...", end='', flush=True)
        time.sleep(1)

def main():
    clear_terminal()

    print("""
                (                          
          (     )\ )  (      .------.      
 (  `  )  )\ ) (()/( ))\(    |A_  _ |      
 )\ /(/( (()/(  ((_))((_)\   |( \/ ).-----.
((_|(_)_\ )(_)) _| (_))((_)  | \  /|K /\  |
(_-< '_ \) || / _` / -_|_-<  |  \/ | /  \ |
/__/ .__/ \_, \__,_\___/__/  `-----| \  / |
   |_|    |__/                     |  \/ K|
                      by jaim1n    `------'\n
    """)
    
    player_name = get_player_name()
    print(f"Welcome, {player_name}!\n")

    while True:
        player1_total_score = 0
        player2_total_score = 0
        player1_sandbags = 0
        player2_sandbags = 0
        round_number = 1

        while player1_total_score < 500 and player2_total_score < 500 and player1_total_score > -200 and player2_total_score > -200:

            # Create a new deck for each round and shuffle it
            deck = create_deck()

            # Deal hands based on coin toss or alternating lead
            if round_number == 1:
                while True:
                    player_choice = input("Choose heads (1) or tails (2) for the coin toss: ")
                    if player_choice in ['1', '2']:
                        player_choice = 'heads' if player_choice == '1' else 'tails'
                        break
                    print("Invalid choice. Please enter '1' for heads or '2' for tails.")

                # Perform the coin toss with improved randomization
                coin_toss_result = random.choice(['heads', 'tails'])
                player2_lead = (player_choice != coin_toss_result)
                coin_toss_winner = "Spyder" if player2_lead else f"{player_name}"
                print(f"\nThe coin landed on {coin_toss_result}. {coin_toss_winner} won the toss and will draw the first card.\n")

            # Alternate lead player in subsequent rounds
            if round_number > 1:
                player2_lead = not player2_lead

            # Deal cards based on who draws first
            if player2_lead:
                player2_hand, player1_hand = deal_cards(deck)
            else:
                player1_hand, player2_hand = deal_cards(deck)

            # Bidding phase
            if player2_lead:
                player1_bid = get_player1_bid(player1_hand)
                player2_bid = get_player2_bid(player2_hand)
            else:
                player2_bid = get_player2_bid(player2_hand)
                player1_bid = get_player1_bid(player1_hand)

            countdown_game()
            clear_terminal()

            # Play the round and get the last trick details
            player1_tricks, player2_tricks, last_trick = play_round(
                player1_hand, player2_hand, player1_bid, player2_bid, player2_lead=player2_lead, spades_broken=False
            )

            clear_terminal()
            print(f"{last_trick}\n")
            print(f"{player_name}'s tricks: {player1_tricks}/{player1_bid}")
            print(f"Spyder's tricks: {player2_tricks}/{player2_bid}")

            # Calculate round scores including sandbags
            player1_round_score, player1_sandbags = calculate_score(player1_tricks, player1_bid, player1_sandbags)
            player2_round_score, player2_sandbags = calculate_score(player2_tricks, player2_bid, player2_sandbags)

            # Update total scores
            player1_total_score += player1_round_score
            player2_total_score += player2_round_score

            print(f"\n--- End of Round {round_number} ---\n")
            print(f"{player_name}'s round score: {player1_round_score}, total score: {player1_total_score}, sandbags: {player1_sandbags}")
            print(f"Spyder's round score: {player2_round_score}, total score: {player2_total_score}, sandbags: {player2_sandbags}")

            if player1_total_score >= 500 or player2_total_score >= 500 or player1_total_score <= -200 or player2_total_score <= -200:
                break

            round_number += 1
            countdown_round()
            clear_terminal()

        # Determine the winner
        if player1_total_score >= 500 or player2_total_score <= -200:
            print(f"\n{player_name} wins!")
        elif player2_total_score >= 500 or player1_total_score <= -200:
            print("\nSpyder wins!")
        else:
            print("Unexpected game end condition.")

        # Ask if the player wants to play again
        while True:
            play_again = input("\nWould you like to play another game? (y/n): ").strip().lower()
            if play_again == 'y':
                clear_terminal()
                break
            elif play_again == 'n':
                print("\nThanks for playing!")
                return
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()
