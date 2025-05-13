#!/usr/bin/env python3

import random
import time
import sys
import os

class MiniGameSystem:
    """A collection of mini games that can be played in the Multiverse Tycoon game."""
    
    def __init__(self):
        """Initialize the mini game system."""
        # Define the mini games with base settings
        self.mini_games = {
            "number_guess": {
                "name": "Number Prediction System",
                "base_description": "Predict a number within a specific range.",
                "difficulty": "Easy",
                "rewards": {
                    "easy": {"local_currency": 500, "quantum_credits": 5, "reputation": 1},
                    "medium": {"local_currency": 1000, "quantum_credits": 10, "reputation": 2},
                    "hard": {"local_currency": 2000, "quantum_credits": 20, "reputation": 3}
                }
            },
            "code_breaker": {
                "name": "Security Bypass Protocol",
                "base_description": "Break a secret code by determining the correct sequence.",
                "difficulty": "Medium",
                "rewards": {
                    "easy": {"local_currency": 800, "quantum_credits": 8, "reputation": 2},
                    "medium": {"local_currency": 1600, "quantum_credits": 16, "reputation": 4},
                    "hard": {"local_currency": 3200, "quantum_credits": 32, "reputation": 6}
                }
            },
            "word_unscramble": {
                "name": "Language Decryption Matrix",
                "base_description": "Unscramble jumbled words from various realities.",
                "difficulty": "Medium",
                "rewards": {
                    "easy": {"local_currency": 700, "quantum_credits": 7, "reputation": 2},
                    "medium": {"local_currency": 1400, "quantum_credits": 14, "reputation": 3},
                    "hard": {"local_currency": 2800, "quantum_credits": 28, "reputation": 5}
                }
            },
            "reaction_test": {
                "name": "Temporal Reflex Calibrator",
                "base_description": "Test your quantum reflexes with split-second timing.",
                "difficulty": "Easy",
                "rewards": {
                    "easy": {"local_currency": 600, "quantum_credits": 6, "reputation": 1},
                    "medium": {"local_currency": 1200, "quantum_credits": 12, "reputation": 3},
                    "hard": {"local_currency": 2400, "quantum_credits": 24, "reputation": 5}
                }
            },
            "memory_match": {
                "name": "Neural Pattern Recognition",
                "base_description": "Memorize and reproduce interdimensional patterns.",
                "difficulty": "Hard",
                "rewards": {
                    "easy": {"local_currency": 1000, "quantum_credits": 10, "reputation": 3},
                    "medium": {"local_currency": 2000, "quantum_credits": 20, "reputation": 5},
                    "hard": {"local_currency": 4000, "quantum_credits": 40, "reputation": 8}
                }
            }
        }
        
        # Universe-specific game themes and descriptions
        self.universe_themes = {
            "blade_runner": {
                "name_prefix": "Replicant ",
                "game_descriptions": {
                    "number_guess": "Predict replicant identification numbers to bypass Tyrell security protocols.",
                    "code_breaker": "Hack into Tyrell Corporation's systems by breaking encoded security sequences.",
                    "word_unscramble": "Decipher scrambled memory fragments from replicant mind implants.",
                    "reaction_test": "Test your reflexes to evade Blade Runner detection systems.",
                    "memory_match": "Match pattern sequences to implant new memories into replicants."
                },
                "symbols": ['👁️', '⚡', '🔍', '🧠', '🦾', '🏙️', '🌧️', '🔫', '📊', '🚔']
            },
            "gta_v": {
                "name_prefix": "Los Santos ",
                "game_descriptions": {
                    "number_guess": "Crack safe combinations in high-stakes Los Santos heists.",
                    "code_breaker": "Bypass police security systems by decoding encrypted communications.",
                    "word_unscramble": "Decode scrambled messages from crime syndicate contacts.",
                    "reaction_test": "Test your getaway driving reflexes in high-speed police pursuits.",
                    "memory_match": "Memorize patrol patterns to plan the perfect heist escape route."
                },
                "symbols": ['💰', '🚗', '🚁', '💣', '🔫', '🏢', '🏖️', '🚔', '💎', '🚀']
            },
            "mcu": {
                "name_prefix": "Avengers ",
                "game_descriptions": {
                    "number_guess": "Calculate quantum realm coordinates for precise interdimensional travel.",
                    "code_breaker": "Decrypt S.H.I.E.L.D. intelligence by breaking their security codes.",
                    "word_unscramble": "Decipher Asgardian runes and alien language fragments.",
                    "reaction_test": "Test your superhero reflexes against Quicksilver's movements.",
                    "memory_match": "Match Infinity Stone energy signatures for secure containment."
                },
                "symbols": ['🛡️', '⚡', '👊', '💫', '🔨', '🕸️', '🧠', '🚀', '💎', '🔮']
            },
            "doraemon": {
                "name_prefix": "Gadget ",
                "game_descriptions": {
                    "number_guess": "Predict which pocket dimension contains Doraemon's secret gadgets.",
                    "code_breaker": "Decode time travel coordinates to access different eras.",
                    "word_unscramble": "Unscramble the names of futuristic gadgets from the 22nd century.",
                    "reaction_test": "Test your reflexes to catch malfunctioning gadgets before they cause chaos.",
                    "memory_match": "Memorize the correct sequence of buttons to activate complex future tech."
                },
                "symbols": ['🚪', '⏱️', '🐱', '🔮', '🚀', '🍩', '🎁', '🤖', '✨', '🔍']
            },
            "wizarding_world": {
                "name_prefix": "Magical ",
                "game_descriptions": {
                    "number_guess": "Predict the correct combination for magical vault access at Gringotts.",
                    "code_breaker": "Break enchanted codes to access restricted sections of ancient grimoires.",
                    "word_unscramble": "Unscramble powerful spell incantations and potion ingredients.",
                    "reaction_test": "Test your wizarding reflexes in magical duels against dark wizards.",
                    "memory_match": "Match magical creature patterns to identify rare species."
                },
                "symbols": ['⚡', '🧙', '🔮', '🧪', '🦉', '📜', '🐉', '🧹', '✨', '⚗️']
            },
            "dark": {
                "name_prefix": "Winden ",
                "game_descriptions": {
                    "number_guess": "Calculate precise dates in the 33-year cycle to navigate time travel.",
                    "code_breaker": "Decode the secrets of the cave system by breaking temporal lock codes.",
                    "word_unscramble": "Unscramble paradoxical family connections in Winden's timeline.",
                    "reaction_test": "Test your timing to activate the God Particle at the exact moment.",
                    "memory_match": "Match cause and effect patterns across multiple timelines."
                },
                "symbols": ['⏳', '☢️', '🌑', '🌧️', '⚰️', '⌛', '🕯️', '🌲', '🔍', '🚪']
            }
        }
        
        # Universe-specific word lists for Word Unscrambler game
        self.universe_word_lists = {
            "blade_runner": {
                "easy": [
                    "replicant", "android", "tyrell", "memory", "blade",
                    "runner", "implant", "nexus", "urban", "neon"
                ],
                "medium": [
                    "voight-kampff", "offworld", "corporation", "synthetic", "dystopian",
                    "retirement", "bioengineered", "interrogation", "baseline", "implanted"
                ],
                "hard": [
                    "more human than human", "tears in rain", "incept date", "tanhauser gate",
                    "combat model", "memory implantation", "emotional response", "empathy test",
                    "rachel is a replicant", "attack ships on fire"
                ]
            },
            "gta_v": {
                "easy": [
                    "heist", "money", "crime", "police", "chase",
                    "robbery", "gang", "weapons", "cars", "drugs"
                ],
                "medium": [
                    "los santos", "trevor", "michael", "franklin", "criminal",
                    "lester", "vehicle", "nightclub", "ammunition", "launder"
                ],
                "hard": [
                    "five star wanted", "pacific standard", "humane labs", "merryweather", "military base",
                    "diamond casino", "doomsday heist", "agency deal", "yacht mission", "underground bunker"
                ]
            },
            "mcu": {
                "easy": [
                    "avenger", "shield", "stark", "hulk", "thor",
                    "hydra", "marvel", "power", "hero", "thanos"
                ],
                "medium": [
                    "infinity stone", "wakanda", "vibranium", "multiverse", "quantum realm",
                    "asgardian", "kree empire", "chitauri", "tesseract", "super soldier"
                ],
                "hard": [
                    "battle of new york", "infinity gauntlet", "celestial beings", "doctor strange",
                    "captain america", "guardians of galaxy", "black order", "scarlet witch",
                    "multiverse of madness", "secret invasion"
                ]
            },
            "doraemon": {
                "easy": [
                    "gadget", "nobita", "future", "pocket", "time",
                    "doraemon", "robot", "machine", "japan", "friend"
                ],
                "medium": [
                    "anywhere door", "time machine", "bamboo copter", "small light", "big light",
                    "translation jelly", "memory bread", "future catalog", "reality mirror", "takecopter"
                ],
                "hard": [
                    "fourth dimensional pocket", "time paradox prevention", "twenty second century",
                    "gadget malfunction", "nobita descendants", "reality alteration device",
                    "interdimensional travel", "emotional programming", "temporal displacement", "future prediction"
                ]
            },
            "wizarding_world": {
                "easy": [
                    "magic", "wand", "spell", "potion", "wizard",
                    "witch", "dragon", "hogwarts", "muggle", "owl"
                ],
                "medium": [
                    "expelliarmus", "patronus", "leviosa", "animagus", "horcrux",
                    "gryffindor", "slytherin", "azkaban", "pensieve", "occlumency"
                ],
                "hard": [
                    "expecto patronum", "wingardium leviosa", "avada kedavra", "sectumsempra",
                    "chamber of secrets", "deathly hallows", "polyjuice potion", "unbreakable vow",
                    "ministry of magic", "order of the phoenix"
                ]
            },
            "dark": {
                "easy": [
                    "time", "travel", "winden", "cave", "nuclear",
                    "cycle", "sic", "mundus", "loop", "past"
                ],
                "medium": [
                    "god particle", "time loop", "thirty three", "adam and eva", "temporal knot",
                    "bootstrap paradox", "travelers", "sic mundus", "causality", "determinism"
                ],
                "hard": [
                    "the beginning is the end", "dark matter bubble", "casual deterministic loop",
                    "bootstrap paradox", "quantum entanglement", "temporal displacement",
                    "apocalypse prevention", "triquetra connection", "nielsen family tree", "reality fragmentation"
                ]
            }
        }
        
        # Default generic word list as fallback
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
        
        # Default symbols for Memory Match game (fallback)
        self.symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '-']
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_all_games(self, universe_id=None):
        """
        Return all available mini games, themed to the current universe if provided.
        
        Args:
            universe_id (str, optional): The current universe ID. If provided,
                                       games will be themed to this universe.
        
        Returns:
            dict: Dictionary of themed mini games.
        """
        if not universe_id or universe_id not in self.universe_themes:
            # Return generic games if no universe specified or if it's not in our themes
            return self.mini_games
            
        # Create a copy of the mini games with universe-specific theming
        themed_games = {}
        universe_theme = self.universe_themes[universe_id]
        
        for game_id, game_info in self.mini_games.items():
            # Create a deep copy of the game info
            themed_game = game_info.copy()
            
            # Apply universe-specific name prefix
            themed_game["name"] = universe_theme["name_prefix"] + game_info["name"]
            
            # Apply universe-specific description if available
            if game_id in universe_theme["game_descriptions"]:
                themed_game["description"] = universe_theme["game_descriptions"][game_id]
            else:
                themed_game["description"] = game_info["base_description"]
                
            themed_games[game_id] = themed_game
            
        return themed_games
    
    def play_number_guess(self, difficulty, universe_id=None):
        """
        Play the number guessing game.
        
        The player has to guess a random number within a range.
        Game is themed to match the current universe if provided.
        
        - Easy: 1-50, 7 guesses
        - Medium: 1-100, 7 guesses
        - Hard: 1-200, 8 guesses
        
        Args:
            difficulty (str): The difficulty level ('easy', 'medium', or 'hard')
            universe_id (str, optional): The current universe ID for themed content
            
        Returns:
            bool: True if the player wins, False otherwise.
        """
        self.clear_screen()
        
        # Get universe-specific title and description if available
        title = "Number Guessing Game"
        description = "I'm thinking of a number between 1 and {max_number}."
        
        if universe_id and universe_id in self.universe_themes:
            universe_theme = self.universe_themes[universe_id]
            title = universe_theme["name_prefix"] + "Number Prediction System"
            
            if "number_guess" in universe_theme["game_descriptions"]:
                description = universe_theme["game_descriptions"]["number_guess"]
        
        print(f"\n=== {title} ===")
        
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
        
        # Format the description by replacing {max_number} with the actual max_number
        formatted_description = description.replace("{max_number}", str(max_number))
        print(formatted_description)
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
    
    def play_code_breaker(self, difficulty, universe_id=None):
        """
        Play the code breaker game.
        
        The player has to guess a sequence of numbers.
        After each guess, feedback is given on how many numbers are correct
        and how many are in the correct position.
        Game is themed to match the current universe if provided.
        
        - Easy: 3 digits (1-6), 8 guesses
        - Medium: 4 digits (1-6), 10 guesses
        - Hard: 5 digits (1-8), 12 guesses
        
        Args:
            difficulty (str): The difficulty level ('easy', 'medium', or 'hard')
            universe_id (str, optional): The current universe ID for themed content
            
        Returns:
            bool: True if the player wins, False otherwise.
        """
        self.clear_screen()
        
        # Get universe-specific title and description if available
        title = "Code Breaker"
        description = "Break a secret code by guessing the correct sequence of numbers."
        
        if universe_id and universe_id in self.universe_themes:
            universe_theme = self.universe_themes[universe_id]
            title = universe_theme["name_prefix"] + "Security Bypass Protocol"
            
            if "code_breaker" in universe_theme["game_descriptions"]:
                description = universe_theme["game_descriptions"]["code_breaker"]
        
        print(f"\n=== {title} ===")
        
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
        
        print(description)
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
    
    def play_word_unscramble(self, difficulty, universe_id=None):
        """
        Play the word unscrambler game.
        
        The player is presented with scrambled words and has to unscramble them.
        Words are themed to the current universe if provided.
        
        - Easy: 5 words, 30 seconds per word
        - Medium: 6 words, 25 seconds per word
        - Hard: 8 words, 20 seconds per word
        
        Args:
            difficulty (str): The difficulty level ('easy', 'medium', or 'hard')
            universe_id (str, optional): The current universe ID for themed content
            
        Returns:
            bool: True if the player unscrambles at least 70% of the words, False otherwise.
        """
        self.clear_screen()
        
        # Get universe-specific title and description if available
        title = "Word Unscrambler"
        description = "Unscramble the following words related to multiverse business."
        
        if universe_id and universe_id in self.universe_themes:
            universe_theme = self.universe_themes[universe_id]
            title = universe_theme["name_prefix"] + "Language Decryption Matrix"
            
            if "word_unscramble" in universe_theme["game_descriptions"]:
                description = universe_theme["game_descriptions"]["word_unscramble"]
        
        print(f"\n=== {title} ===")
        
        # Set difficulty parameters
        if difficulty == "easy":
            num_words = 5
            time_per_word = 30
        elif difficulty == "medium":
            num_words = 6
            time_per_word = 25
        else:  # hard
            num_words = 8
            time_per_word = 20
        
        # Get the appropriate word list based on universe and difficulty
        if universe_id and universe_id in self.universe_word_lists:
            word_list = self.universe_word_lists[universe_id][difficulty]
        else:
            word_list = self.word_lists[difficulty]
            
        # Select random words (ensure we don't try to sample more words than available)
        num_words = min(num_words, len(word_list))
        selected_words = random.sample(word_list, num_words)
        correct_count = 0
        
        print(description)
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
                time.sleep(1.0)  # Reduced delay for faster gameplay
                continue
                
            # Check guess
            if guess == "skip":
                print(f"Skipped. The word was: {word}")
            elif guess == word:
                print("Correct!")
                correct_count += 1
            else:
                print(f"Wrong! The word was: {word}")
                
            time.sleep(0.75)  # Reduced delay for faster gameplay
            
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
    
    def play_reaction_test(self, difficulty, universe_id=None):
        """
        Play the reaction time test game.
        
        The player has to press Enter exactly when prompted after a random delay.
        Test is themed to match the current universe if provided.
        
        - Easy: 5 rounds, 3 second maximum delay, 0.3s error margin
        - Medium: 7 rounds, 4 second maximum delay, 0.2s error margin
        - Hard: 10 rounds, 5 second maximum delay, 0.1s error margin
        
        Args:
            difficulty (str): The difficulty level ('easy', 'medium', or 'hard')
            universe_id (str, optional): The current universe ID for themed content
            
        Returns:
            bool: True if the player succeeds in at least 70% of rounds, False otherwise.
        """
        self.clear_screen()
        
        # Get universe-specific title and description if available
        title = "Reaction Time Test"
        description = "Test your reflexes! Press Enter exactly when you see 'NOW!'"
        
        if universe_id and universe_id in self.universe_themes:
            universe_theme = self.universe_themes[universe_id]
            title = universe_theme["name_prefix"] + "Temporal Reflex Calibrator"
            
            if "reaction_test" in universe_theme["game_descriptions"]:
                description = universe_theme["game_descriptions"]["reaction_test"]
        
        print(f"\n=== {title} ===")
        
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
        
        print(description)
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
                
            time.sleep(0.75)  # Reduced delay for faster gameplay
            
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
    
    def play_memory_match(self, difficulty, universe_id=None):
        """
        Play the memory match game.
        
        The player is shown a sequence of symbols and has to repeat it from memory.
        Symbols are themed to the current universe if provided.
        
        - Easy: Start with 3 symbols, up to 7
        - Medium: Start with 4 symbols, up to 9
        - Hard: Start with 5 symbols, up to 12
        
        Args:
            difficulty (str): The difficulty level ('easy', 'medium', or 'hard')
            universe_id (str, optional): The current universe ID for themed content
            
        Returns:
            bool: True if the player reaches at least the minimum threshold, False otherwise.
        """
        self.clear_screen()
        
        # Get universe-specific title, description and symbols if available
        title = "Memory Match"
        description = "Memorize the sequence of symbols and repeat it back."
        
        if universe_id and universe_id in self.universe_themes:
            universe_theme = self.universe_themes[universe_id]
            title = universe_theme["name_prefix"] + "Neural Pattern Recognition"
            
            if "memory_match" in universe_theme["game_descriptions"]:
                description = universe_theme["game_descriptions"]["memory_match"]
        
        print(f"\n=== {title} ===")
        
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
        
        # Get the universe-specific symbols if available
        symbols_to_use = self.symbols
        if universe_id and universe_id in self.universe_themes and "symbols" in self.universe_themes[universe_id]:
            symbols_to_use = self.universe_themes[universe_id]["symbols"]
        
        print(description)
        print(f"Starting with {start_length} symbols, we'll increase the length as you succeed.")
        print(f"You need to reach a sequence of at least {success_threshold} symbols to win.")
        print(f"Symbols used: {' '.join(symbols_to_use[:10])}")
        input("\nPress Enter to start...")
        
        while current_length <= max_length:
            # Generate a random sequence
            sequence = random.choices(symbols_to_use, k=current_length)
            
            # Show the sequence
            self.clear_screen()
            print(f"\nMemorize this sequence ({current_length} symbols):")
            print("It will disappear soon...")
            time.sleep(0.5)  # Reduced delay for faster gameplay
            
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
                time.sleep(0.75)  # Reduced delay for faster gameplay
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
        
    def play_game(self, game_id, difficulty, universe_id=None):
        """
        Play a specific mini game with the given difficulty and universe-specific theming.
        
        Args:
            game_id (str): The ID of the game to play
            difficulty (str): The difficulty level ('easy', 'medium', or 'hard')
            universe_id (str, optional): The current universe ID for themed content
            
        Returns:
            bool: True if the player wins, False otherwise
        """
        if game_id == "number_guess":
            return self.play_number_guess(difficulty, universe_id)
        elif game_id == "code_breaker":
            return self.play_code_breaker(difficulty, universe_id)
        elif game_id == "word_unscramble":
            return self.play_word_unscramble(difficulty, universe_id)
        elif game_id == "reaction_test":
            return self.play_reaction_test(difficulty, universe_id)
        elif game_id == "memory_match":
            return self.play_memory_match(difficulty, universe_id)
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