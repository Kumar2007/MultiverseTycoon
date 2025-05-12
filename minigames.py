#!/usr/bin/env python3

import random
import time
import sys
import os

class MiniGameSystem:
    """A collection of mini games that can be played in the Multiverse Tycoon game."""
    
    def __init__(self):
        """Initialize the mini game system."""
        # Define the mini games and their rewards
        self.mini_games = {
            "number_guess": {
                "name": "Number Guessing Game",
                "description": "Guess a number between 1 and 100.",
                "difficulty": "Easy",
                "rewards": {
                    "easy": {"local_currency": 500, "quantum_credits": 5, "reputation": 1},
                    "medium": {"local_currency": 1000, "quantum_credits": 10, "reputation": 2},
                    "hard": {"local_currency": 2000, "quantum_credits": 20, "reputation": 3}
                }
            },
            "code_breaker": {
                "name": "Code Breaker",
                "description": "Break a secret code by guessing the correct sequence of numbers.",
                "difficulty": "Medium",
                "rewards": {
                    "easy": {"local_currency": 800, "quantum_credits": 8, "reputation": 2},
                    "medium": {"local_currency": 1600, "quantum_credits": 16, "reputation": 4},
                    "hard": {"local_currency": 3200, "quantum_credits": 32, "reputation": 6}
                }
            },
            "word_unscramble": {
                "name": "Word Unscrambler",
                "description": "Unscramble jumbled words related to multiverse business.",
                "difficulty": "Medium",
                "rewards": {
                    "easy": {"local_currency": 700, "quantum_credits": 7, "reputation": 2},
                    "medium": {"local_currency": 1400, "quantum_credits": 14, "reputation": 3},
                    "hard": {"local_currency": 2800, "quantum_credits": 28, "reputation": 5}
                }
            },
            "reaction_test": {
                "name": "Reaction Time Test",
                "description": "Test your reflexes by pressing Enter exactly when prompted.",
                "difficulty": "Easy",
                "rewards": {
                    "easy": {"local_currency": 600, "quantum_credits": 6, "reputation": 1},
                    "medium": {"local_currency": 1200, "quantum_credits": 12, "reputation": 3},
                    "hard": {"local_currency": 2400, "quantum_credits": 24, "reputation": 5}
                }
            },
            "memory_match": {
                "name": "Memory Match",
                "description": "Remember a sequence of symbols and repeat it back.",
                "difficulty": "Hard",
                "rewards": {
                    "easy": {"local_currency": 1000, "quantum_credits": 10, "reputation": 3},
                    "medium": {"local_currency": 2000, "quantum_credits": 20, "reputation": 5},
                    "hard": {"local_currency": 4000, "quantum_credits": 40, "reputation": 8}
                }
            }
        }
        
        # Word list for Word Unscrambler game
        self.word_lists = {
            "easy": [
                "business", "money", "profit", "trade", "sell", 
                "cash", "deal", "market", "buy", "work"
            ],
            "medium": [
                "multiverse", "dimension", "quantum", "universe", "reality", 
                "investor", "corporate", "finance", "economy", "strategy"
            ],
            "hard": [
                "entrepreneur", "interdimensional", "cryptocurrency", "investment", "corporation", 
                "acquisition", "diversification", "conglomerate", "monopoly", "speculation"
            ]
        }
        
        # Symbols for Memory Match game
        self.symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '-']
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_all_games(self):
        """Return all available mini games."""
        return self.mini_games
    
    def play_number_guess(self, difficulty):
        """
        Play the number guessing game.
        
        The player has to guess a random number within a range.
        - Easy: 1-50, 7 guesses
        - Medium: 1-100, 7 guesses
        - Hard: 1-200, 8 guesses
        
        Returns True if the player wins, False otherwise.
        """
        self.clear_screen()
        print("\n=== Number Guessing Game ===")
        
        # Set difficulty parameters
        if difficulty == "easy":
            max_number = 50
            max_guesses = 7
        elif difficulty == "medium":
            max_number = 100
            max_guesses = 7
        else:  # hard
            max_number = 200
            max_guesses = 8
            
        target_number = random.randint(1, max_number)
        guesses_left = max_guesses
        
        print(f"I'm thinking of a number between 1 and {max_number}.")
        print(f"You have {guesses_left} guesses to find it.")
        
        while guesses_left > 0:
            try:
                guess = int(input("\nYour guess: "))
                
                if guess < 1 or guess > max_number:
                    print(f"Please enter a number between 1 and {max_number}.")
                    continue
                    
                guesses_left -= 1
                
                if guess == target_number:
                    print(f"\nCongratulations! You guessed the number {target_number}!")
                    return True
                elif guess < target_number:
                    print(f"Higher! You have {guesses_left} guesses left.")
                else:
                    print(f"Lower! You have {guesses_left} guesses left.")
                    
            except ValueError:
                print("Please enter a valid number.")
                
        print(f"\nGame over! The number was {target_number}.")
        return False
    
    def play_code_breaker(self, difficulty):
        """
        Play the code breaker game.
        
        The player has to guess a sequence of numbers.
        After each guess, feedback is given on how many numbers are correct
        and how many are in the correct position.
        
        - Easy: 3 digits (1-6), 8 guesses
        - Medium: 4 digits (1-6), 10 guesses
        - Hard: 5 digits (1-8), 12 guesses
        
        Returns True if the player wins, False otherwise.
        """
        self.clear_screen()
        print("\n=== Code Breaker ===")
        
        # Set difficulty parameters
        if difficulty == "easy":
            code_length = 3
            number_range = 6
            max_guesses = 8
        elif difficulty == "medium":
            code_length = 4
            number_range = 6
            max_guesses = 10
        else:  # hard
            code_length = 5
            number_range = 8
            max_guesses = 12
            
        # Generate a random code
        secret_code = [random.randint(1, number_range) for _ in range(code_length)]
        guesses_left = max_guesses
        
        print(f"I've created a code with {code_length} digits (1-{number_range}).")
        print(f"You have {guesses_left} attempts to crack it.")
        print("After each guess, you'll get feedback:")
        print("- 'Correct' means right digit in the right position")
        print("- 'Misplaced' means right digit in the wrong position")
        
        while guesses_left > 0:
            # Get player's guess
            valid_guess = False
            guess = []  # Initialize guess outside the loop to prevent "possibly unbound" errors
            
            while not valid_guess:
                guess_input = input(f"\nEnter your {code_length}-digit guess (e.g., {' '.join(map(str, range(1, code_length+1)))}): ")
                
                try:
                    # Parse input, accept both space-separated and non-spaced input
                    if ' ' in guess_input:
                        guess = [int(x) for x in guess_input.split()]
                    else:
                        guess = [int(x) for x in guess_input]
                        
                    # Validate guess
                    if len(guess) != code_length:
                        print(f"Your guess must be {code_length} digits long.")
                    elif any(d < 1 or d > number_range for d in guess):
                        print(f"Each digit must be between 1 and {number_range}.")
                    else:
                        valid_guess = True
                except ValueError:
                    print("Please enter valid numbers.")
            
            guesses_left -= 1
            
            # Make sure guess is valid before proceeding
            if not guess:
                print("Error: Invalid guess. Skipping this turn.")
                continue
                
            # Check if the guess is correct
            if guess == secret_code:
                print(f"\nCongratulations! You broke the code: {' '.join(map(str, secret_code))}")
                return True
                
            # Calculate feedback
            correct = sum(1 for i in range(code_length) if guess[i] == secret_code[i])
            
            # Count total matches (regardless of position)
            guess_counts = {}
            code_counts = {}
            for d in range(1, number_range+1):
                guess_counts[d] = guess.count(d)
                code_counts[d] = secret_code.count(d)
                
            total_matches = sum(min(guess_counts[d], code_counts[d]) for d in range(1, number_range+1))
            misplaced = total_matches - correct
            
            print(f"Feedback: {correct} correct, {misplaced} misplaced. {guesses_left} guesses left.")
            
        print(f"\nGame over! The code was: {' '.join(map(str, secret_code))}")
        return False
    
    def play_word_unscramble(self, difficulty):
        """
        Play the word unscrambler game.
        
        The player is presented with scrambled words and has to unscramble them.
        
        - Easy: 5 words, 30 seconds per word
        - Medium: 6 words, 25 seconds per word
        - Hard: 8 words, 20 seconds per word
        
        Returns True if the player unscrambles at least 70% of the words, False otherwise.
        """
        self.clear_screen()
        print("\n=== Word Unscrambler ===")
        
        # Set difficulty parameters
        if difficulty == "easy":
            num_words = 5
            time_per_word = 30
            word_list = self.word_lists["easy"]
        elif difficulty == "medium":
            num_words = 6
            time_per_word = 25
            word_list = self.word_lists["medium"]
        else:  # hard
            num_words = 8
            time_per_word = 20
            word_list = self.word_lists["hard"]
            
        # Select random words
        selected_words = random.sample(word_list, num_words)
        correct_count = 0
        
        print("Unscramble the following words related to multiverse business.")
        print(f"You have {time_per_word} seconds per word.")
        print("Type 'skip' to skip a word.")
        input("\nPress Enter to start...")
        
        for i, word in enumerate(selected_words, 1):
            # Scramble the word
            scrambled = list(word)
            random.shuffle(scrambled)
            scrambled = ''.join(scrambled)
            
            self.clear_screen()
            print(f"\nWord {i}/{num_words}: {scrambled}")
            print(f"Time: {time_per_word} seconds")
            
            # Start timer
            start_time = time.time()
            
            # Get player's guess
            guess = input("Your answer: ").lower().strip()
            
            # Check time
            elapsed_time = time.time() - start_time
            if elapsed_time > time_per_word:
                print(f"Time's up! The word was: {word}")
                time.sleep(2)
                continue
                
            # Check guess
            if guess == "skip":
                print(f"Skipped. The word was: {word}")
            elif guess == word:
                print("Correct!")
                correct_count += 1
            else:
                print(f"Wrong! The word was: {word}")
                
            time.sleep(1.5)
            
        # Calculate success rate
        success_rate = correct_count / num_words
        threshold = 0.7  # 70% success rate required to win
        
        self.clear_screen()
        print(f"\nGame over! You unscrambled {correct_count} out of {num_words} words.")
        print(f"Success rate: {int(success_rate * 100)}%")
        
        if success_rate >= threshold:
            print("Congratulations! You've successfully completed the challenge.")
            return True
        else:
            print(f"You needed to unscramble at least {int(threshold * 100)}% of the words to succeed.")
            return False
    
    def play_reaction_test(self, difficulty):
        """
        Play the reaction time test game.
        
        The player has to press Enter exactly when prompted after a random delay.
        
        - Easy: 5 rounds, 3 second maximum delay, 0.3s error margin
        - Medium: 7 rounds, 4 second maximum delay, 0.2s error margin
        - Hard: 10 rounds, 5 second maximum delay, 0.1s error margin
        
        Returns True if the player succeeds in at least 70% of rounds, False otherwise.
        """
        self.clear_screen()
        print("\n=== Reaction Time Test ===")
        
        # Set difficulty parameters
        if difficulty == "easy":
            num_rounds = 5
            max_delay = 3
            error_margin = 0.3
        elif difficulty == "medium":
            num_rounds = 7
            max_delay = 4
            error_margin = 0.2
        else:  # hard
            num_rounds = 10
            max_delay = 5
            error_margin = 0.1
            
        successful_rounds = 0
        
        print("Test your reflexes! Press Enter exactly when you see 'NOW!'")
        print(f"You'll have {error_margin} seconds margin of error.")
        print(f"Get ready for {num_rounds} rounds!")
        input("\nPress Enter to start...")
        
        for round_num in range(1, num_rounds + 1):
            self.clear_screen()
            print(f"\nRound {round_num}/{num_rounds}")
            print("\nWait for it...")
            
            # Random delay before prompt
            delay = random.uniform(1.5, max_delay)
            time.sleep(delay)
            
            print("\nNOW! (Press Enter)")
            start_time = time.time()
            
            # Wait for player input
            input()
            reaction_time = time.time() - start_time
            
            # Evaluate response
            if reaction_time <= error_margin:
                print(f"Perfect! Your reaction time: {reaction_time:.3f} seconds")
                successful_rounds += 1
            elif reaction_time <= error_margin * 2:
                print(f"Close! Your reaction time: {reaction_time:.3f} seconds")
                print(f"Needed to be under {error_margin} seconds")
            else:
                print(f"Too slow! Your reaction time: {reaction_time:.3f} seconds")
                print(f"Needed to be under {error_margin} seconds")
                
            time.sleep(1.5)
            
        # Calculate success rate
        success_rate = successful_rounds / num_rounds
        threshold = 0.7  # 70% success rate required to win
        
        self.clear_screen()
        print(f"\nGame over! You succeeded in {successful_rounds} out of {num_rounds} rounds.")
        print(f"Success rate: {int(success_rate * 100)}%")
        
        if success_rate >= threshold:
            print("Congratulations! You've successfully completed the challenge.")
            return True
        else:
            print(f"You needed to succeed in at least {int(threshold * 100)}% of the rounds.")
            return False
    
    def play_memory_match(self, difficulty):
        """
        Play the memory match game.
        
        The player is shown a sequence of symbols and has to repeat it from memory.
        
        - Easy: Start with 3 symbols, up to 7
        - Medium: Start with 4 symbols, up to 9
        - Hard: Start with 5 symbols, up to 12
        
        Returns True if the player reaches at least the minimum threshold, False otherwise.
        """
        self.clear_screen()
        print("\n=== Memory Match ===")
        
        # Set difficulty parameters
        if difficulty == "easy":
            start_length = 3
            max_length = 7
            view_time = 1.0  # seconds per symbol
        elif difficulty == "medium":
            start_length = 4
            max_length = 9
            view_time = 0.8
        else:  # hard
            start_length = 5
            max_length = 12
            view_time = 0.6
            
        current_length = start_length
        success_threshold = max(start_length + 2, int(max_length * 0.7))
        
        print("Memorize the sequence of symbols and repeat it back!")
        print(f"Starting with {start_length} symbols, we'll increase the length as you succeed.")
        print(f"You need to reach a sequence of at least {success_threshold} symbols to win.")
        input("\nPress Enter to start...")
        
        while current_length <= max_length:
            # Generate a random sequence
            sequence = random.choices(self.symbols, k=current_length)
            
            # Show the sequence
            self.clear_screen()
            print(f"\nMemorize this sequence ({current_length} symbols):")
            print("It will disappear soon...")
            time.sleep(1)
            
            print("\n" + " ".join(sequence))
            time.sleep(current_length * view_time)
            
            self.clear_screen()
            print("\nNow, repeat the sequence!")
            
            # Get player's input
            player_sequence = []
            for i in range(current_length):
                symbol = input(f"Symbol {i+1}: ").strip()
                player_sequence.append(symbol)
                
            # Check if the sequence is correct
            correct = (player_sequence == sequence)
            
            if correct:
                print("\nCorrect! Well done!")
                current_length += 1
                time.sleep(1.5)
            else:
                print("\nIncorrect! Game over.")
                print(f"The correct sequence was: {' '.join(sequence)}")
                print(f"Your sequence was: {' '.join(player_sequence)}")
                print(f"You reached a sequence length of {current_length}.")
                
                # Check if player has reached the minimum threshold
                if current_length >= success_threshold:
                    print(f"Congratulations! You've surpassed the minimum threshold of {success_threshold}.")
                    return True
                else:
                    print(f"You needed to reach a sequence of at least {success_threshold} symbols.")
                    return False
                    
        # If we've reached the maximum length, the player wins
        print("\nAmazing! You've mastered the maximum sequence length!")
        return True
        
    def play_game(self, game_id, difficulty):
        """Play a specific mini game with the given difficulty."""
        if game_id == "number_guess":
            return self.play_number_guess(difficulty)
        elif game_id == "code_breaker":
            return self.play_code_breaker(difficulty)
        elif game_id == "word_unscramble":
            return self.play_word_unscramble(difficulty)
        elif game_id == "reaction_test":
            return self.play_reaction_test(difficulty)
        elif game_id == "memory_match":
            return self.play_memory_match(difficulty)
        else:
            print(f"Unknown game ID: {game_id}")
            return False
            
    def get_rewards(self, game_id, difficulty):
        """Get the rewards for completing a specific mini game at the given difficulty."""
        if game_id in self.mini_games and difficulty in self.mini_games[game_id]["rewards"]:
            return self.mini_games[game_id]["rewards"][difficulty]
        return {"local_currency": 0, "quantum_credits": 0, "reputation": 0}


# For testing the mini games directly
if __name__ == "__main__":
    games = MiniGameSystem()
    games.play_memory_match("easy")