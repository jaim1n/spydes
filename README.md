# spydes
A Python-based CLI card game inspired by Spades. 

This version follows two-player rules. An AI player named *Spyder* will be your opponent. You will be prompted to enter your name the first time you play; this information will be stored in `player_name.txt`, so you won’t need to enter it in subsequent sessions. A coin toss is used at the beginning of every game for fairness; you must choose either heads or tails.

### Setup:
- Each player is dealt 13 cards.
- Players bid on how many tricks they expect to win. Bids can range from 0 (nil) to 13.

### Bidding:
- You and Spyder each declare a bid.
- The loser of the coin toss must make the first bid.

### Trick Play:
- The player who wins the coin toss leads the first trick.
- The lead player can choose any card except a spade unless spades are the only suit in the player’s hand.
- Players must follow the lead suit if they can. If they cannot follow suit, they may play any other card.
- Spades are the trump suit and can only be played if a player has no cards of the lead suit or if spades have been broken.

### Scoring:
- Players earn 10 points per bid trick if they achieve their bid.
- Overbidding results in a sandbag per overtrick and earns 1 point each. A 100-point penalty is applied every 10 sandbags.
- A successful nil bid earns 100 points; a failed nil bid deducts 100 points.
- If a player's score reaches 500 or more, they win; a score of -200 or lower results in a loss.
  
### Winning:
- The game continues until one player reaches a total score of 500 or more or drops to -200 points.

## TODO
- [x] Prompt user to input name replacing "Player 1" and store in dictionary
  - [x] Give Player 2 a unique name
- [ ] Implement blind nil system
- [ ] Improve AI
- [ ] Add a way to play with four players and make appropriate changes to the game logic to accommodate four players
  - [ ] Provide options for pairs or solo play
- [ ] Work on aesthetics and user interface

ASCII art generated using https://patorjk.com/software/taag/
