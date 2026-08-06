import random

class Guess_Game:
    def __init__(self, low, high): # Initializing the class with a range of numbers
        self.low = low
        self.high = high
        self.__the_number = random.randint(low, high)   # Double underscore to make it private

    def guess(self, number): # Method to check the user's guess against the randomly generated number
        while number != self.__the_number:
            if number < self.__the_number:
                return "You're too low."
            elif number > self.__the_number:
                return "You're too high."
        return "Correct!"

def main():
    
    guessing = Guess_Game(1, 100) # This line creates an instance of the Guess_Game class with a range from 1 to 100.
    
    print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
    

    attempts = input("How many attempts would you like to have? (default is 5): ")
    if attempts.isdigit():
        attempts = int(attempts)
    else:
        print("Invalid input. Defaulting to 5 attempts.")
        attempts = 5
    
    while attempts > 0:
        try:
            user_guess = int(input("Enter your guess: "))
            result = guessing.guess(user_guess)
            print(result)
            attempts -= 1
            if result == "Correct!":
                break
            elif result == "You're too low.":
                print("Try a higher number.")

            elif result == "You're too high.":
                print("Try a lower number.")

        except ValueError:
            print("Enter a valid number.")
    
    print(f"The correct number was: {guessing._Guess_Game__the_number}") # This line accesses the private variable __the_number using name mangling to reveal the correct number after the game ends.



if __name__ == "__main__": # This ensures that the main function is called only when the script is run directly, not when imported as a module.
    
    main()
