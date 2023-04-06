import random

# Define the game rules
rules = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

# print rules.keys()
print(rules.keys())
# print rules.values()
# print rules.items()



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
        result = 'tie'
    else:
        bot_score += 1
        result = 'loss'

    # Update the game history and state
    game_history.append((state, bot_action))
    state = (bot_action, player_action)


    print(f"You played {list(rules.keys())[player_action]} and the bot played {list(rules.keys())[bot_action]}")
    print(f"Your score: {player_score}")
    print(f"Bot score: {bot_score}")
    print(f"Result: {result}")
    # Print the results of the round
    
    rock = '''
          ____
    ---'   ____)
         (_____)
         (_____)
          (____)
    ---.__(___)
    '''

    paper = '''
          _____
    ---'   ____)____
            ________)
            ________)
            ________)
    ---.___________)
    '''

    scissors = '''
          _____
    ---'   ____)____
            ________)
        ____________)
        (____)
    ---.__(___)
    '''
    #print(f"You played {list(rules.keys())[player_action]} and the bot played {list(rules.keys())[bot_action]}")
    # Print the ASCII art for each option
    # To print out the player's choice and the computer's choice side by side, you can use the zip() function to iterate over the two lists of ASCII art, and use string formatting to align them properly:
    # player_art = [rock, paper, scissors][["rock", "paper", "scissors"].index(player_choice)]
    #computer_art = [rock, paper, scissors][["rock", "paper", "scissors"].index(computer_choice)]
    #for player_line, computer_line in zip(player_art.split("\n"), computer_art.split("\n")):
    #print(f"{player_line:<25}{computer_line:>25}")
    # Print the results of the game

    player_art = [rock, scissors , paper][["rock", "scissors", "paper"].index(list(rules.keys())[player_action])]
    computer_art = [rock, scissors, paper][["rock", "scissors", "paper"].index(list(rules.keys())[bot_action])]
    print(f"You played {list(rules.keys())[player_action]} and the bot played {list(rules.keys())[bot_action]}")
    for player_line, computer_line in zip(player_art.split("\n"), computer_art.split("\n")):
        print(f"{player_line:<20} {computer_line:>15}")
        #if player_action == 0:
         #   print(rock)
      #  elif player_action == 1:
      #      print(paper)
      #  else:
      #      print(scissors)
      #  if bot_action == 0:
      #      print(rock)
      #  elif bot_action == 1:
      #      print(paper)
      #  else:
      #      print(scissors)
   
    

