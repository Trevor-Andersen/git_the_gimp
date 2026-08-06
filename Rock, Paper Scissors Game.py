# Rock, Paper Scissors Game

import random
def rps():


    choice_list = ["rock", "paper", "scissors"] # choice options for the game   

    hierarchy = {"rock": "scissors", "scissors": "paper", "paper": "rock"} # dictionary of winning choices for each option, where the key beats the value

    i = True
    while i == True:

        user_throw = input("Enter your throw (rock, paper, scissors): ") # prompt the user to input their choice
        if user_throw not in choice_list:
            print("Invalid input. Please try again.")
            continue

        computer_choice = random.choice(choice_list) # generate the computer's choice randomly from the list of options

        if user_throw == computer_choice:
            print(f"Computer chose {computer_choice}. It's a tie.")
        elif hierarchy[user_throw] == computer_choice:
            print(f"Computer chose {computer_choice}. You won.")
        else:
            print(f"Computer chose {computer_choice}. You lost.")
        
        again = input("Press Enter to play again or Ctrl+C to exit.") # prompt for the user to play again or exit
        if again != "":
            i = False
        else:
            i = True    
          
if __name__ == "__main__":
    rps()



