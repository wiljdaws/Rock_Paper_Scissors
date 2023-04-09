
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
    
# display the hands
def display_hands(user_move, bot_move, user_score, bot_score):
        player_hand = display_ascii(user_move)
        bot_hand = flip_ascii(display_ascii(bot_move), is_bot=True)
        scoreboard = scoreboard_ascii['scores'].format(user_score=user_score, bot_score=bot_score)
        for player_line, bot_line, scoreboard in zip(player_hand.split("\n"), bot_hand.split("\n"), scoreboard.split("\n")):
            print(f"{player_line:<30} {bot_line:>20} {scoreboard: >55}")