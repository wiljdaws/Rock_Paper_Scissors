from mysqlx import Row
import pandas as pd
from collections import Counter
import numpy as np
import random
import tensorflow as tf
import os
import csv

# Define the path to the CSV file
HISTORY_FILE = 'history.csv'

# Define the game rules
rules = {0: 2, 1: 0, 2: 1}

# Load the user's move history from a CSV file (if it exists)
def load_history():
    try:
        history_df = pd.read_csv('history.csv', index_col=0)
        return {row[0]: int(row[1]) for row in history_df.itertuples()}
    except FileNotFoundError:
        return {}

# Define ASCII art for moves
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


# Get the last 5 user names from history.csv 
def get_recent_users():
    try:
        history_df = pd.read_csv('history.csv', index_col=0)
        user_history = {row[0]: int(row[2]) for row in history_df.itertuples()}
        return list(user_history.keys())[-5:]
    except FileNotFoundError:
        return []

# Display recent user names
def display_recent_users(user_names):
    print("Welcome back! Please select your username from the list below:")
    for i, name in enumerate(user_names):
        print(f"{i+1}. {name}")
        
# Get user's name
def get_user_name():
    user_name = input("Enter your name: ")
    while not user_name:
        user_name = input("Invalid input. Please enter your name: ")
    return user_name

def get_user_move():
    while True:
        try:
            user_move = int(input("Enter your move (0 for rock, 1 for paper, 2 for scissors): "))
            if user_move in [0, 1, 2]:
                return user_move
            else:
                print("Invalid move. Please enter 0, 1, or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Create the deep Q-learning network
def create_network():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, input_shape=(3,), activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(3)
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse')
    return model

# Define the function to select the bot's move using deep Q-learning
def select_move(state, model, epsilon):
    if random.uniform(0, 1) < epsilon:
        # Select a random move
        return random.choice([0, 1, 2])
    else:
        # Use the model to select the best move
        q_values = model.predict(np.array(state).reshape(1, -1))[0]
        return np.argmax(q_values)

def get_reward(winner):
    if winner == 1:
        # Bot wins
        return 1
    elif winner == -1:
        # User wins
        return -1
    else:
        # Tie
        return 0


def train_network(model, memory, batch_size, discount_factor):
    # Get a random sample of past moves from memory
    mini_batch = random.sample(memory, batch_size)
    
    # Initialize the inputs and targets for the deep Q-learning network
    inputs = np.zeros((batch_size, 3))
    targets = np.zeros((batch_size, 3))
    
    # Populate the inputs and targets based on the mini_batch
    for i, (state, action, reward, next_state, done) in enumerate(mini_batch):
        inputs[i] = state
        targets[i] = model.predict(np.array([state]))[0]
        if done:
            targets[i][action] = reward
        else:
            targets[i][action] = reward + discount_factor * np.max(model.predict(np.array([next_state]))[0])
    
    # Train the deep Q-learning network on the mini_batch
    model.fit(inputs, targets, epochs=1, verbose=0)



def play_round():
    # Get user name
    user_name = get_user_name()
    
    # Load move history from CSV file
    history = load_history()
    user_history = history.get(user_name, [])
    
    # Create the deep Q-learning network
    model = create_network()
    
    # Get the bot's move
    bot_move = get_bot_move(model, user_history)
    
    # Get the user's move
    user_move = get_user_move()
    
    # Determine the winner and update the score
    winner = rules[user_move - bot_move]
    if winner == 1:
        user_score += 1
        reward = 1
    elif winner == 2:
        bot_score += 1
        reward = -1
    else:
        reward = 0
        
    # Update the move history
    user_history.append([user_move, bot_move, reward])
    history[user_name] = user_history
    
    # Save the move history to the CSV file
    save_history(history)
    
    # display the hands
    player_hand = display_ascii(user_move)
    bot_hand = flip_ascii(display_ascii(bot_move), is_bot=True)
    scoreboard = scoreboard_ascii.format(user_score=user_score, bot_score=bot_score)
    print(scoreboard)
    for player_line, bot_line in zip(player_hand.split("\n"), bot_hand.split("\n")):
        print(f"{player_line:<30} {bot_line:>20}")

    print(f"Thanks for playing, {user_name}!")

# Load the move history from the CSV file
def load_history():
    if not os.path.isfile(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        return {Row[0]: [[int(r) for r in row[1:4]] for row in csv_reader if row]}
    
# Save the move history to the CSV file
def save_history(history):
    with open(HISTORY_FILE, mode='w', newline='') as csv_file:
        fieldnames = ['user_name', 'user_move', 'bot_move', 'reward']
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)
        for user_name, user_history in history.items():
            for move in user_history:
                writer.writerow([user_name, *move])

if __name__ == '__main__':
    main()