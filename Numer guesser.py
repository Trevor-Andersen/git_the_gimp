import random

class NumberGuesser:
    def __init__(self, min_val=1, max_val=100):
        self.min_val = min_val
        self.max_val = max_val
        self.secret_number = random.randint(min_val, max_val)
        self.hints_left = 3
        
        # Private hint storage
        self._parity = ""
        self._factors = []
        self._multiples = []
        self._larger = ""
        self._smaller = ""
        
        # Calculate hints immediately on creation
        self.__calculate_hints()
        
        # Pool of available hint types
        self._available_hints = ["parity", "factors", "multiples", "larger", "smaller"]

    def __calculate_hints(self):
        """Private method to calculate all hint properties."""
        # 1. Parity
        self._parity = "even" if self.secret_number % 2 == 0 else "odd"
        
        # 2. Factors
        self._factors = [i for i in range(1, self.secret_number + 1) if self.secret_number % i == 0]
        
        # 3. Multiples (Sample multiples within a reasonable range above the number)
        self._multiples = [self.secret_number * i for i in range(2, 6)]
        
        # 4. Larger than (Random benchmark below the number)
        if self.secret_number > self.min_val:
            low_benchmark = random.randint(self.min_val, self.secret_number - 1)
            self._larger = f"larger than {low_benchmark}"
        else:
            self._larger = f"not smaller than {self.min_val}"
            
        # 5. Smaller than (Random benchmark above the number)
        if self.secret_number < self.max_val:
            high_benchmark = random.randint(self.secret_number + 1, self.max_val)
            self._smaller = f"smaller than {high_benchmark}"
        else:
            self._smaller = f"not larger than {self.max_val}"

    # Properties to access hints safely
    @property
    def parity(self):
        return f"The number is {self._parity}."

    @property
    def factors(self):
        valid_factors = [f for f in self._factors if f != 1 and f != self.secret_number]
        if valid_factors:
            return f"One of its factors is {random.choice(valid_factors)}."
        return "The number is prime (it only has 1 and itself as factors)."

    @property
    def multiples(self):
        return f"One of its multiples is {random.choice(self._multiples)}."

    @property
    def larger(self):
        return f"The number is {self._larger}."

    @property
    def smaller(self):
        return f"The number is {self._smaller}."

    def get_random_hint(self):
        """Randomly selects and returns an unused hint property."""
        if self.hints_left <= 0:
            return "You have no hints left!"
        
        if not self._available_hints:
            return "No more unique hint types available!"

        # Pick a random hint type and remove it from the pool so hints don't repeat
        hint_type = random.choice(self._available_hints)
        self._available_hints.remove(hint_type)
        self.hints_left -= 1

        # Dynamically call the corresponding property
        hint_message = getattr(self, hint_type)
        return f"Hint ({self.hints_left} left): {hint_message}"


def run_chatbot():
    print("Welcome to the Number Guesser Game!")
    print("I am thinking of a number between 1 and 100.")
    print("Type 'hint' to get a clue (Max 3). Type 'exit' to quit.\n")
    
    game = NumberGuesser(1, 100)
    attempts = 0

    while attempts < 5: #Max attempts: 5
        user_input = input("You: ").strip().lower()

        if user_input == 'exit':
            print(f"Goodbye! The number was {game.secret_number}.")
            break
            
        if user_input == 'hint':
            print(f"{game.get_random_hint()}")
            continue

        # Validate if input is a number
        try:
            guess = int(user_input)
        except ValueError:
            print("Please enter a valid integer, 'hint', or 'exit'.")
            continue

        attempts += 1

        if guess < game.secret_number:
            print("Too low! Try a higher number.")
        elif guess > game.secret_number:
            print("Too high! Try a lower number.")
        else:
            print(f"Correct! You guessed my number in {attempts} attempts!")
            break

if __name__ == "__main__":
    run_chatbot()