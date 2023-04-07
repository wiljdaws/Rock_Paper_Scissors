import pandas as pd
import random
from collections import Counter

# Define the game rules
rules = {
    0: 2,
    1: 0,
    2: 1
}

# Load the user's move history from a CSV file (if it exists)
try:
    history_df = pd.read_csv('history.csv', index_col=0)
    user_history = {row[0]: int(row[1]) for row in history_df.itertuples()}
except FileNotFoundError:
    user_history = {}

def display_ascii(move):
    if move == 0:
        return """     
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""
    elif move == 1:
        return """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""
    else:
        return """
     _______
---'    ____)____
           ______)
        __________)
       (____)
---.__(___)
"""



def flip_ascii(hand):
    return [line[::-1] for line in hand]

# Define ASCII art for the scoreboard
scoreboard_ascii = {
    'header': '''
 __     __             _       _       
 \ \   / /__ _ __ _ __(_) __ _| |_ ___ 
  \ \ / / _ \ '__| '__| |/ _` | __/ _ \\
   \ V /  __/ |  | |  | | (_| | ||  __/
    \_/ \___|_|  |_|  |_|\__,_|\__\___|
                                       
''',
    'scores': '''
+-----------------------------------------------+
|                  SCOREBOARD                   |
+------------------------+----------------------+
|          user: {user_score}       |         bot: {bot_score}       |
+------------------------+----------------------+
'''
}


# Define a function to flip the ASCII art horizontally
def flip_ascii(ascii_str, is_bot=False):
    if is_bot:
        return '\n'.join([line.replace("(", "temp").replace(")", "(").replace("temp", ")")[::-1] for line in ascii_str.split('\n')])
    else:
        return '\n'.join([line[::-1] for line in ascii_str.split('\n')])

# Initialize the scores
user_score = 0
bot_score = 0

#Get last 5 user names from history.csv 
try:
    history_df = pd.read_csv('history.csv', index_col=0)
    user_history = {row[0]: int(row[2]) for row in history_df.itertuples()}
    user_names = list(user_history.keys())
    user_names = user_names[-5:]
except FileNotFoundError:
    user_history = {}
    user_names = []

#display list of options for most recent usernames if not in list then get input for username
if user_names != []:
    print("Welcome back! Please select your username from the list below:")
    for i in range(len(user_names)):
        print(f"{i+1}. {user_names[i]}")
    user_name = input("Enter your name: ")
    while user_name not in user_names:
        user_name = input("Invalid input. Please enter your name: ")
        if user_name not in user_names:
            print("Invalid input. Please enter your name: ")
            continue
        else:
            break
else:
    user_name = input("Enter your name: ")
    while user_name == "":
        user_name = input("Invalid input. Please enter your name: ")
        if user_name == "":
            print("Invalid input. Please enter your name: ")
            continue
        else:
            break
bot_name = user_name[::-1]
print(scoreboard_ascii['header'])

# Start the game loop
while True:
        # Get the user's move history
        user_history = {}
        try:
            history_df = pd.read_csv('history.csv', index_col=0)
            user_history = {row[0]: int(row[1]) for row in history_df.itertuples()}
        except FileNotFoundError:
            user_history = {}

        # Print the scoreboard
        #print(scoreboard_ascii['header'])
        #print(scoreboard_ascii['scores'].format(user_score=user_score, bot_score=bot_score))

        # Get the user's move
        user_move = input("Enter 0 for Rock, 1 for Paper, 2 for Scissors, or q to Quit: ")
        while user_move not in ['0', '1', '2', 'q']:
            user_move = input("Invalid input. Please enter 0 for Rock, 1 for Paper, or 2 for Scissors: ")
        if user_move == 'q':
            print("\nThanks for playing!")
            break
        user_move = int(user_move)

        # Predict the user's next move based on their history
        if len(user_history) > 0:
            #look for user_name in the file
            if user_name in user_history:
                #if user_name is in the file, get the last move
                last_move = user_history[user_name]
            else:
                #if user_name is not in the file, get the last move
                last_move = max(rules.keys(), key=lambda x: rules[x] == 0)
            #get the most common move
            freq_dist = Counter(user_history.values())
            most_common_moves = freq_dist.most_common(2)
            if len(most_common_moves) == 1:
                predicted_move = most_common_moves[0][0]
            elif most_common_moves[0][1] > most_common_moves[1][1]:
                predicted_move = most_common_moves[0][0]
            else:
                predicted_move = max(rules.keys(), key=lambda x: rules[x] == last_move)
        else:
            predicted_move = random.randint(0, 2)


        # Pick the bot's move based on the predicted move and the user's history
        if predicted_move in rules:
            bot_move = rules[predicted_move]
        else:
            bot_move = random.randint(0, 2)

        if user_move == bot_move:
            print("It's a tie!")
            outcome = 'tie'
        elif (user_move == 0 and bot_move == 2) or (user_move == 1 and bot_move == 0) or (user_move == 2 and bot_move == 1):
            print(f"{user_name} wins!")
            outcome = 'loss'
            user_score += 1
        else:
            print(f"{bot_name} wins!")
            print("You win!")
            outcome = 'win'
            bot_score += 1

        # display the hands
        player_hand = display_ascii(user_move)
        bot_hand = flip_ascii(display_ascii(bot_move), is_bot=True)
        scoreboard = scoreboard_ascii['scores'].format(user_score=user_score, bot_score=bot_score)
        for player_line, bot_line, scoreboard in zip(player_hand.split("\n"), bot_hand.split("\n"), scoreboard.split("\n")):
            print(f"{player_line:<30} {bot_line:>20} {scoreboard: >55}")

        # Update the user's move history and write it to the CSV file
        user_history = {row[0]: int(row[1]) for row in history_df.iloc[1:].itertuples()}
        history_df = pd.DataFrame.from_dict(user_history, orient='columns')
        history_df['Round'] = range(1, len(history_df) + 1)
        history_df.set_index('Round', inplace = True)
        history_df.to_csv('history.csv')


        