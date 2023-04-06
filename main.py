import random

# Define the game rules
rules = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

# Define the reinforcement learning parameters
alpha = 0.1
gamma = 0.9

# Define the initial Q-values for each state-action pair
Q = {}
for i in range(3):
    for j in range(3):
        state = (i, j)
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
    result = game_history[-1]
    for i in range(len(game_history) - 1):
        state, action = game_history[i]
        reward = -1 if result == 'loss' else 0 if result == 'tie' else 1
        next_state = game_history[i+1][0]
        Q[(state, action)] += alpha * (reward + gamma * max([Q[(next_state, a)] for a in range(3)]) - Q[(state, action)])

# Play the game multiple times
while True:
    # Initialize the game state
    player_score = 0
    bot_score = 0
    game_history = []
    state = (0, 0)

    # Ask the player to choose their action
    player_action = input("Choose your action: rock (0), paper (1), or scissors (2) ")

    # Keep asking for player's input until it is valid
    while player_action not in ['0', '1', '2']:
        player_action = input("Invalid input. Choose your action: rock (0), paper (1), or scissors (2) ")

    # Convert the player's action to an integer
    player_action = int(player_action)

    # Select the bot's action based on the current state and Q-values
    bot_action = select_action(state, epsilon=0.1)

    # Determine the winner of the round
    if rules[list(rules.keys())[player_action]] == list(rules.keys())[bot_action]:
        player_score += 1
        result = 'win'
    elif list(rules.keys())[bot_action] == list(rules.keys())[player_action]:
        bot_score += 1
        result = 'loss'
    else:
        result = 'tie'

    # Update the game history and state
    game_history.append((state, bot_action))
    state = (bot_action, player_action)

    # Print the results of the round
    print(f"You played {list(rules.keys())[player_action]} and the bot played {list(rules.keys())[bot_action]}")
