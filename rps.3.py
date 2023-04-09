import random
import numpy as np
import csv
import display_hands as hands
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Constants
MOVES = ['rock', 'paper', 'scissors']
NUM_MOVES = len(MOVES)
REWARD_MATRIX = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
user_score = 0
bot_score = 0

# Load or create Q-table
try:
    q_table = np.loadtxt('q_table.csv', delimiter=',')
    print('Q-table loaded')
except IOError:
    q_table = np.zeros((NUM_MOVES, NUM_MOVES))
    print('Q-table created')

# Deep Q-Learning agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural network with 2 hidden layers
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam('learning_rate'==self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # Add a new axis to the state input
        state = np.expand_dims(state, axis=0)
        
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            return np.argmax(self.model.predict(state)[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.expand_dims(next_state, axis=0))[0])
            target_f = self.model.predict(np.expand_dims(state, axis=0))
            target_f[0][action] = target
            self.model.fit(np.expand_dims(state, axis=0), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, name):
        self.model.save_weights(name)

# Initialize agent
state_size = 2
action_size = NUM_MOVES
agent = DQNAgent(state_size, action_size)

def read_game_results(filename = 'game_results.csv'):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        global user_score
        global bot_score
        for row in reader:
            result = row[2].strip()
            if result == "win":
                user_score += 1
            elif result == "loss":
                bot_score += 1
    return user_score, bot_score

def update_scores(player_choice, bot_choice, result):
    file_path = 'game_results.csv'
    
    # Read the existing scores from the file
    with open(file_path, 'r') as file:
        scores = file.readlines()
    
    # Update the scores with the new result
    new_score = f"Player choice: {player_choice}, Bot choice: {bot_choice}, Result: {result}\n"
    scores.append(new_score)
    
    # Write the updated scores back to the file
    with open(file_path, 'w') as file:
        file.writelines(scores)

# Play game and update Q-table
reward = 0
while True:
    # Get user move
    while True:
        user_move = input('Enter your move (0 for rock, 1 for paper, 2 for scissors): ')
        if user_move.isdigit() and int(user_move) in range(NUM_MOVES):
            user_move = int(user_move)
            break
        elif user_move == 'q':
            exit()
        else:
            print('Invalid input. Please enter a number between 0 and 2.')
    
    # Get bot move
    bot_move = agent.act(np.array([user_move, 0]).reshape(1, state_size))
    
    # Determine winner
    winner = REWARD_MATRIX[user_move][bot_move]
    user_score, bot_score = read_game_results("game_results.csv")
  
    if user_move == bot_move:
            print("It's a tie!")
            outcome = 'tie'
            reward += 0
    elif (user_move == 0 and bot_move == 2) or (user_move == 1 and bot_move == 0) or (user_move == 2 and bot_move == 1):
            print("You win!")
            outcome = 'loss'
            user_score += 1
            reward -= 1
    else:
            print("Bot win!")
            outcome = 'win'
            bot_score += 1
            reward += 1 

    agent.remember(np.array([user_move, bot_move]), bot_move, reward, np.array([bot_move, user_move]), False)
    q_table[user_move][bot_move] = (1 - agent.learning_rate) * q_table[user_move][bot_move] + agent.learning_rate * (reward + agent.gamma * np.max(q_table[bot_move]))
    # Print result
    hands.display_hands(user_move, bot_move, user_score, bot_score)
    update_scores(user_move, bot_move, outcome)

    
        
    # Train agent
    agent.replay(32)

    # Save Q-table
    np.savetxt('q_table.csv', q_table, delimiter=',')
    print('Q-table saved')

    # Save agent
    agent.save('dqn_agent.h5')
    print('Agent saved')



