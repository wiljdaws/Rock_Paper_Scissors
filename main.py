import random
import os
import pandas as pd
import numpy as np
from collections import defaultdict

# Define the game rules
rules = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
# if file path does not exist create file "game_results.txt" in this dir
file_path = "game_results.csv"

# Define the reinforcement learning parameters
alpha = 0.1
gamma = 0.9

# Define the initial Q-values for each state-action pair
Q = {}
for i in range(2):
    for j in range(3):
        state = ('bot' if i==0 else 'user', j)
        for action in range(3):
            Q[(state, action)] = 0.5

# Define a function to select the bot's action based on the current Q-values
def select_action(state, epsilon):
    if random.uniform(0, 1) < epsilon:
        # Select a random action
        return random.choice([0, 1, 2])
    else:
        # Select the action with the highest Q-value
        q_values = [Q[(state, a)] for a in range(3)]
        max_q = max(q_values)
        count = q_values.count(max_q)
        if count > 1:
            # If there are multiple actions with the same Q-value, select one at random
            best = [i for i in range(3) if q_values[i] == max_q]
            return random.choice(best)
        else:
            return q_values.index(max_q)

# Define a function to update the Q-values based on the results of a single game
def update_Q_values(game_history):
    result = game_history[-1][1]
    for i in range(len(game_history) - 1):
        state, action = game_history[i]
        reward = -1 if result == 'loss' else 0 if result == 'tie' else 1
        next_state = game_history[i+1][0]
        Q[(state, action)][action] += alpha * (reward + gamma * max(Q[(next_state, a)][a] for a in range(3)) - Q[(state, action)][action])
        data = {'Player choice': [list(state)[1]],
                'Bot choice': [action],
                'Result': [result],
                'Reward': [reward]}
        df = pd.DataFrame(data)
        with open(file_path, "a") as f:
            df.to_csv(f, header=f.tell()==0, index=False)

print(rules.keys())

print("Let's play rock-paper-scissors!")
print("Enter 0 for rock, 1 for paper, 2 for scissors or -1 to quit")
score = {'win': 0, 'tie': 0, 'loss': 0}
game_history = []

while True:
    user_choice = input("Your move: ")
    if user



    while True:
        user_choice = input("Your move: ")
        if user_choice == "-1":
            print("Goodbye!")
            break
        elif user_choice not in ['0', '1', '2']:
            print("Invalid input, please try again.")
            continue
    
    state = ('user', user_choice)
    bot_action = np.argmax(Q[state])
    if np.random.uniform() < epsilon:
        bot_action = np.random.choice([0, 1, 2])
    bot_choice = list(rules.keys())[bot_action]

    print("User choice:")
    print([rock, scissors, paper][user_choice])
    print("Bot choice:")
    print([rock, scissors, paper][bot_action])

    result = rules[list(rules.keys())[user_choice]][bot_choice]
    if result == 1:
        print("You win!")
        # add one to score 'win'
        score['win'] += 1

    elif result == -1:
        print("You lose.")
        # add one to score 'loss'
        score['loss'] += 1
        
    else:
        print("Tie!")
        # add one to score 'tie'
        score['tie'] += 1

    update_Q_values([(state, bot_action), (('bot', bot_action), user_choice), (('user', user_choice), bot_action), (('bot', bot_action), result)])
    #write score to a csv file scoreboard.csv , if it does not exist in this directory create the file
    with open(file_path, "a") as f:
        df = pd.DataFrame(score)
        df.to_csv(f, header=f.tell()==0, index=False)

    print("Score: ", score)
  
    with open(file_path, "a") as f:
        df = pd.DataFrame(score)
        df.to_csv(f, header=f.tell()==0, index=False)
    #print the score
    print("Score: ", score)     

   
       
   
    

