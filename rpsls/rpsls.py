# Rock Paper Scissors Lizard Spock
# (c) 2024 Graeme Kieran
# MIT License

# Rock Paper Scissors Lizard Spock
# (c) 2024 Graeme Kieran
# MIT License

# map numbers to moves
moves = {
    1: "rock",
    2: "spock",
    3: "paper",
    4: "lizard",
    5: "scissors"
}

# Reverse dictionary mapping plays to numbers
moves_reverse = {v: k for k, v in moves.items()}

winning_map = {
    1: {5, 4},  # Rock beats Scissors (5) and Lizard (4)
    2: {1, 5},  # Spock beats Rock (1) and Scissors (5)
    3: {1, 2},  # Paper beats Rock (1) and Spock (2)
    4: {3, 2},  # Lizard beats Paper (3) and Spock (2)
    5: {3, 4}   # Scissors beats Paper (3) and Lizard (4)
}

def string_to_num(play_str):
    return moves_reverse.get(play_str.lower(), None)

def num_to_string(play_num):
    return moves.get(play_num, None)

def determine_winner(play1, play2):
    if play1 == play2:
        return 'Draw'  

    if play2 in winning_map[play1]:
        
    else:
        return play2 

play1_str = input("Enter the first play (rock, spock, paper, lizard, scissors): ")
play2_str = input("Enter the second play (rock, spock, paper, lizard, scissors): ")

play1_num = string_to_num(play1_str)
play2_num = string_to_num(play2_str)

if play1_num is None or play2_num is None:
    print("Invalid input. Please enter a valid play.")
else:
    winner_num = determine_winner(play1_num, play2_num)
    winner_str = num_to_string(winner_num)
    
    print(f"Play1: {play1_str}, Play2: {play2_str}")
    print(f"Winner: {winner_str if winner_str else 'Draw'}")
