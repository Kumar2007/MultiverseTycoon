#!/usr/bin/env python3

import json
import random
import time
import os
import sys
from currency import CurrencyExchange, QuantumBusinesses, QuantumEvents
from heists import HeistSystem
from minigames import MiniGameSystem
from ad_rewards import AdRewardsSystem


class MultiVerseTycoon:

    def __init__(self):
        """Initialize the game with default settings."""
        self.player = {
            "name": "",
            "universes": {},
            "current_universe": None,
            "turn": 1,
            "game_over": False,
            "end_reason": "",
            "event_history": {},
            "last_event_turn": 0,
            "quantum_credits": 0,  # Interdimensional currency
            "quantum_businesses": [],  # List of quantum businesses owned
            "last_quantum_event_turn": 0,
            "heist_specialists": [],  # List of specialist crew members owned
            "special_items": [],  # List of special items owned for heists
            "heist_history": [],  # History of completed heists
            "heist_cooldown": 0,  # Turns until next heist is available
            "mini_games_played": 0,  # Total number of mini games played
            "mini_games_won": 0,  # Total number of mini games won
            "mini_game_history": [],  # History of played mini games
            "mini_game_cooldown": 0,  # Turns until next mini game is available
            "unlocked_features": {  # Features that have been unlocked by the player
                "universe_travel": False,  # Ability to travel between universes
                "currency_exchange": False,  # Ability to exchange currencies
                "heist_operations": False,  # Ability to perform heists
                "specialists": False,  # Ability to recruit specialists
                "special_items": False,  # Ability to purchase special items
                "mini_games": False  # Ability to play mini-games
            }
        }

        self.universes = {
            "blade_runner": {
                "name":
                "Blade Runner",
                "description":
                "A dystopian future where AI businesses thrive but are highly regulated.",
                "currency":
                "Credits",
                "risk_factor":
                75,
                "economic_traits":
                ["High-tech", "Unstable Politics", "AI-driven"],
                "businesses": {
                    "replicant_manufacturing": {
                        "name":
                        "Replicant Manufacturing",
                        "cost":
                        10000,
                        "income_per_turn":
                        2500,
                        "risk_increase":
                        10,
                        "description":
                        "Create synthetic humans for dangerous work."
                    },
                    "memory_implants": {
                        "name":
                        "Memory Implants",
                        "cost":
                        7500,
                        "income_per_turn":
                        1800,
                        "risk_increase":
                        5,
                        "description":
                        "Design and sell artificial memories for replicants."
                    },
                    "surveillance_tech": {
                        "name":
                        "Surveillance Tech",
                        "cost":
                        5000,
                        "income_per_turn":
                        1200,
                        "risk_increase":
                        3,
                        "description":
                        "Develop technology to track replicants and citizens."
                    }
                },
                "events": [{
                    "name": "Replicant Uprising",
                    "description":
                    "Your replicants are rebelling against poor working conditions!",
                    "effect": {
                        "cash": -3000,
                        "danger": 20,
                        "reputation": -15
                    }
                }, {
                    "name": "Blade Runner Investigation",
                    "description":
                    "Your business is being investigated by a Blade Runner.",
                    "effect": {
                        "cash": -1000,
                        "danger": 15,
                        "reputation": -5
                    }
                }, {
                    "name": "Off-world Expansion",
                    "description":
                    "Opportunity to expand your business to off-world colonies.",
                    "effect": {
                        "cash": 5000,
                        "danger": 5,
                        "reputation": 10
                    }
                }, {
                    "name": "Corporate Favor",
                    "description":
                    "A Tyrell Corporation executive offers you a partnership.",
                    "effect": {
                        "cash": 2000,
                        "danger": -10,
                        "reputation": 15
                    }
                }, {
                    "name": "Blackout",
                    "description":
                    "Digital systems fail during a city-wide blackout.",
                    "effect": {
                        "cash": -2000,
                        "danger": 0,
                        "reputation": 0
                    }
                }]
            },
            "gta_v": {
                "name":
                "GTA V",
                "description":
                "A world of organized crime, corruption, and fast money.",
                "currency":
                "Dollars",
                "risk_factor":
                60,
                "economic_traits":
                ["Corruption", "Criminal Opportunities", "Fast Money"],
                "businesses": {
                    "nightclub": {
                        "name":
                        "Nightclub",
                        "cost":
                        15000,
                        "income_per_turn":
                        3500,
                        "risk_increase":
                        8,
                        "description":
                        "Run a popular nightclub as a front for criminal activities."
                    },
                    "auto_shop": {
                        "name":
                        "Auto Shop",
                        "cost":
                        12000,
                        "income_per_turn":
                        2800,
                        "risk_increase":
                        5,
                        "description":
                        "Modify stolen cars and sell them for profit."
                    },
                    "weapon_dealing": {
                        "name": "Weapon Dealing",
                        "cost": 20000,
                        "income_per_turn": 4500,
                        "risk_increase": 15,
                        "description":
                        "Trade illegal weapons on the black market."
                    }
                },
                "events": [{
                    "name": "Police Raid",
                    "description":
                    "The LSPD is raiding one of your businesses!",
                    "effect": {
                        "cash": -5000,
                        "danger": 25,
                        "reputation": -10
                    }
                }, {
                    "name": "Gang War",
                    "description":
                    "Local gangs are fighting in your territory.",
                    "effect": {
                        "cash": -3000,
                        "danger": 15,
                        "reputation": 5
                    }
                }, {
                    "name": "Heist Opportunity",
                    "description":
                    "You've been invited to participate in a major bank heist.",
                    "effect": {
                        "cash": 10000,
                        "danger": 20,
                        "reputation": 10
                    }
                }, {
                    "name": "Corrupt Official",
                    "description":
                    "A police officer offers protection for your businesses.",
                    "effect": {
                        "cash": -2000,
                        "danger": -15,
                        "reputation": 0
                    }
                }, {
                    "name": "Celebrity Client",
                    "description":
                    "A famous celebrity becomes a regular at your establishment.",
                    "effect": {
                        "cash": 3000,
                        "danger": 0,
                        "reputation": 15
                    }
                }]
            },
            "mcu": {
                "name":
                "MCU",
                "description":
                "A world of superheroes, advanced technology, and constant innovation.",
                "currency":
                "USD",
                "risk_factor":
                50,
                "economic_traits":
                ["High Innovation", "Superhero Interference", "Tech-driven"],
                "businesses": {
                    "stark_tech_competitor": {
                        "name":
                        "Stark Tech Competitor",
                        "cost":
                        25000,
                        "income_per_turn":
                        5000,
                        "risk_increase":
                        7,
                        "description":
                        "Develop advanced technology to compete with Stark Industries."
                    },
                    "superhero_insurance": {
                        "name":
                        "Superhero Insurance",
                        "cost":
                        15000,
                        "income_per_turn":
                        3000,
                        "risk_increase":
                        3,
                        "description":
                        "Provide insurance against damage caused by superhero battles."
                    },
                    "shield_supplies": {
                        "name":
                        "S.H.I.E.L.D. Supplies",
                        "cost":
                        20000,
                        "income_per_turn":
                        4000,
                        "risk_increase":
                        5,
                        "description":
                        "Supply equipment and technology to S.H.I.E.L.D. agents."
                    }
                },
                "events": [{
                    "name": "Avengers Battle",
                    "description":
                    "A battle between The Avengers and a villain destroyed part of your business!",
                    "effect": {
                        "cash": -6000,
                        "danger": 10,
                        "reputation": 0
                    }
                }, {
                    "name": "Stark Partnership",
                    "description":
                    "Tony Stark offers to collaborate on a new technology.",
                    "effect": {
                        "cash": 8000,
                        "danger": -5,
                        "reputation": 20
                    }
                }, {
                    "name": "Alien Artifact",
                    "description":
                    "You discovered an alien artifact with valuable technology.",
                    "effect": {
                        "cash": 5000,
                        "danger": 15,
                        "reputation": 5
                    }
                }, {
                    "name": "Government Scrutiny",
                    "description":
                    "Your business is being investigated for potential Hydra connections.",
                    "effect": {
                        "cash": -2000,
                        "danger": 10,
                        "reputation": -10
                    }
                }, {
                    "name": "Multiverse Entrepreneur Award",
                    "description":
                    "Your innovative business model wins a prestigious award.",
                    "effect": {
                        "cash": 3000,
                        "danger": 0,
                        "reputation": 15
                    }
                }]
            }
        }

        self.employee_types = {
            "manager": {
                "name": "Manager",
                "hiring_cost": 1000,
                "salary_per_turn": 500,
                "efficiency_bonus": 0.15,  # 15% more income
                "risk_reduction": 1,  # Reduces danger by 1 each turn
            },
            "security": {
                "name": "Security Personnel",
                "hiring_cost": 800,
                "salary_per_turn": 400,
                "efficiency_bonus": 0.05,  # 5% more income
                "risk_reduction": 3,  # Reduces danger by 3 each turn
            },
            "tech_expert": {
                "name": "Tech Expert",
                "hiring_cost": 1500,
                "salary_per_turn": 700,
                "efficiency_bonus": 0.2,  # 20% more income
                "risk_reduction": 2,  # Reduces danger by 2 each turn
            }
        }

        self.DANGER_THRESHOLD = 100
        self.starting_cash = 10000

        # Initialize currency exchange system
        self.currency_exchange = CurrencyExchange(self.universes)

        # Initialize quantum business system
        self.quantum_businesses = QuantumBusinesses()

        # Initialize quantum events
        self.quantum_events = QuantumEvents()

        # Constants for quantum events
        self.QUANTUM_EVENT_PROBABILITY = 0.15  # 15% chance per turn
        self.QUANTUM_EVENT_COOLDOWN = 3  # At least 3 turns between events

        # Initialize heist system
        self.heist_system = HeistSystem(self.universes)
        
        # Initialize mini game system
        self.mini_game_system = MiniGameSystem()
        
        # Initialize ad rewards system
        self.ad_rewards_system = AdRewardsSystem()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def slow_print(self, text, delay=0.01):
        """Print text with a typing effect, but faster."""
        # Reduced delay from 0.03 to 0.01 for faster typing effect
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def display_title(self):
        """Display the game title."""
        # Smaller, simpler version of the title without ASCII art stripes
        title_lines = [
            "  __  __       _ _   _                            ",
            " |  \\/  |_   _| | |_(_)_   _____ _ __ ___  ___   ",
            " | |\\/| | | | | | __| \\ \\ / / _ \\ '__/ __|/ _ \\  ",
            " | |  | | |_| | | |_| |\\ V /  __/ |  \\__ \\  __/  ",
            " |_|  |_|\\__,_|_|\\__|_| \\_/ \\___|_|  |___/\\___|  ",
            "                                                  ",
            "  _____                            ",
            " |_   _|   _ ___ ___   ___  _ __   ",
            "   | || | | / __/ _ \\ / _ \\| '_ \\  ",
            "   | || |_| | (_| (_) | (_) | | | | ",
            "   |_| \\__, |\\___\\___/ \\___/|_| |_| ",
            "       |___/                        "
        ]
        
        # Get terminal width
        terminal_width = os.get_terminal_size().columns
        
        # Print each line centered
        print("")  # Add a blank line before the title
        for line in title_lines:
            print(line.center(terminal_width))
        
        print("\n" + "=" * 80)
        print("\tManage businesses across multiple universes!")
        print("\tBuild your multiverse empire and avoid detection.")
        print("=" * 80 + "\n")

    def start_game(self):
        """Start a new game or load a saved game."""
        self.clear_screen()
        self.display_title()

        print("\n\n1. New Game")
        print("2. Load Game")
        print("3. Quit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            self.new_game()
        elif choice == "2":
            self.load_game()
        elif choice == "3":
            print("\nThanks for playing Multiverse Tycoon!")
            sys.exit()
        elif choice.lower() == "admin":  # Secret admin access
            self.admin_tools()
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.start_game()
            
    def admin_tools(self):
        """Access admin tools for developers and debugging."""
        try:
            import admin_tools
            admin_tools.admin_menu()
            self.start_game()
        except ImportError:
            print("\nAdmin tools not found. This feature is only for developers.")
            time.sleep(1.5)
            self.start_game()

    def new_game(self):
        """Initialize a new game."""
        self.clear_screen()
        print("\n=== New Multiverse Tycoon Game ===\n")

        player_name = input("Enter your name, multiverse entrepreneur: ")
        self.player["name"] = player_name

        # Initialize player state for each universe
        for universe_id, universe in self.universes.items():
            self.player["universes"][universe_id] = {
                "cash": self.starting_cash,
                "danger": 0,
                "reputation": 0,
                "businesses": [],
                "employees": []
            }

        # Start in the Blade Runner universe
        self.player["current_universe"] = "blade_runner"

        self.slow_print(
            f"\nWelcome, {player_name}! You are now an entrepreneur in the multiverse."
        )
        self.slow_print(
            "You'll start your journey in the Blade Runner universe.")
        self.slow_print(
            "Your goal is to build businesses across multiple universes and become a multiverse tycoon!"
        )
        self.slow_print(
            "But be careful - if your danger level reaches 100 in any universe, you'll be caught!"
        )

        input("\nPress Enter to begin your adventure...")
        self.main_game_loop()

    def save_game(self):
        """Save the current game state to a file."""
        # Create saves directory if it doesn't exist
        if not os.path.exists("saves"):
            try:
                os.makedirs("saves")
            except Exception:
                # If we can't create the directory, save in the current directory
                pass
                
        # Try to save in the saves directory first
        try:
            save_path = os.path.join("saves", f"multiverse_tycoon_save_{self.player['name']}.json")
            with open(save_path, "w") as save_file:
                json.dump(self.player, save_file)
            print(f"\nGame saved successfully as '{save_path}'!")
        except Exception as e:
            # Fall back to current directory if saves directory doesn't work
            try:
                fallback_path = f"multiverse_tycoon_save_{self.player['name']}.json"
                with open(fallback_path, "w") as save_file:
                    json.dump(self.player, save_file)
                print(f"\nGame saved successfully as '{fallback_path}'!")
            except Exception as e:
                print(f"\nError saving game: {e}")

        input("\nPress Enter to continue...")

    def load_game(self):
        """Load a saved game state from a file."""
        # Check for save files in both the saves directory and current directory
        save_files = []
        
        # Check saves directory if it exists
        if os.path.exists("saves"):
            save_files.extend([
                os.path.join("saves", f) for f in os.listdir("saves")
                if f.startswith("multiverse_tycoon_save_") and f.endswith(".json")
            ])
        
        # Also check current directory
        save_files.extend([
            f for f in os.listdir()
            if f.startswith("multiverse_tycoon_save_") and f.endswith(".json")
        ])

        if not save_files:
            print("\nNo saved games found!")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.start_game()
            return

        print("\n=== Load Game ===\n")
        for i, save_file in enumerate(save_files, 1):
            # Extract player name from filename, handling both path formats
            file_name = os.path.basename(save_file)
            player_name = file_name[22:-5]
            print(f"{i}. {player_name}")

        print(f"{len(save_files) + 1}. Back")

        try:
            choice = int(input("\nSelect a save file: "))
            if choice == len(save_files) + 1:
                self.start_game()
                return

            if 1 <= choice <= len(save_files):
                filename = save_files[choice - 1]
                with open(filename, "r") as file:
                    self.player = json.load(file)
                print(f"\nWelcome back, {self.player['name']}!")
                time.sleep(0.75)  # Reduced delay for faster gameplay
                self.main_game_loop()
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
                self.load_game()
        except Exception as e:
            print(f"\nError loading game: {e}")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.load_game()

    def display_universe_info(self):
        """Display information about the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print(f"\n=== {universe['name']} Universe ===")
        print(f"Description: {universe['description']}")
        print(f"Currency: {universe['currency']}")
        print(f"Risk Factor: {universe['risk_factor']}/100")
        print(f"Economic Traits: {', '.join(universe['economic_traits'])}")

        print("\n=== Your Status ===")
        print(f"Cash: {player_universe_data['cash']} {universe['currency']}")
        print(f"Quantum Credits: {self.player['quantum_credits']} Q¢")
        print(f"Danger Level: {player_universe_data['danger']}/100")
        print(f"Reputation: {player_universe_data['reputation']}")

        if player_universe_data['businesses']:
            print("\n=== Your Businesses ===")
            for business_id in player_universe_data['businesses']:
                business = universe['businesses'][business_id]
                print(
                    f"- {business['name']} (Income: {business['income_per_turn']} {universe['currency']}/turn)"
                )

        if player_universe_data['employees']:
            print("\n=== Your Employees ===")
            for employee in player_universe_data['employees']:
                emp_type = self.employee_types[employee['type']]
                print(
                    f"- {emp_type['name']} (Salary: {emp_type['salary_per_turn']} {universe['currency']}/turn)"
                )

        print(f"\nTurn: {self.player['turn']}")

    def main_game_loop(self):
        """Main game loop."""
        while not self.player["game_over"]:
            universe_id = self.player["current_universe"]
            universe = self.universes[universe_id]
            player_universe_data = self.player["universes"][universe_id]

            # Display universe and player info
            self.display_universe_info()

            # Display menu options
            print("\n=== Actions ===")
            print("1. Start a new business")
            print("2. Hire employees")
            print("3. Fire employees")
            print("4. Bribe officials (Reduce danger level)")
            
            # Only show unlocked features
            options = []
            option_index = 5  # Start counting from option 5
            
            # Universe travel (unlocks at turn 10)
            if self.player["unlocked_features"]["universe_travel"]:
                print(f"{option_index}. Jump to another universe")
                options.append("universe_travel")
                option_index += 1
            
            # Currency exchange (unlocks at turn 15)
            if self.player["unlocked_features"]["currency_exchange"]:
                print(f"{option_index}. Currency exchange")
                options.append("currency_exchange")
                option_index += 1
                print(f"{option_index}. View exchange rates")
                options.append("exchange_rates")
                option_index += 1
            
            # Heist operations (unlocks at turn 20)
            if self.player["unlocked_features"]["heist_operations"]:
                print(f"{option_index}. Heist operations")
                options.append("heist_operations")
                option_index += 1
            
            # Specialists (unlocks after completing 2 heists)
            if self.player["unlocked_features"]["specialists"]:
                print(f"{option_index}. Recruit specialists")
                options.append("specialists")
                option_index += 1
            
            # Special items (unlocks after recruiting 2 specialists)
            if self.player["unlocked_features"]["special_items"]:
                print(f"{option_index}. Purchase special items")
                options.append("special_items")
                option_index += 1
            
            # Mini games (unlocks at turn 5)
            if self.player["unlocked_features"]["mini_games"]:
                print(f"{option_index}. Play mini games")
                options.append("mini_games")
                option_index += 1
                
            # Ad rewards (always available)
            print(f"{option_index}. Ad rewards")
            options.append("ad_rewards")
            option_index += 1
            
            # Always available options
            print(f"{option_index}. Save game")
            options.append("save")
            option_index += 1
            
            print(f"{option_index}. Quit game")
            options.append("quit")
            
            choice = input(f"\nChoose an action (1-{option_index}): ")

            # Basic actions always available
            if choice == "1":
                self.start_business()
            elif choice == "2":
                self.hire_employee()
            elif choice == "3":
                self.fire_employee()
            elif choice == "4":
                self.bribe_officials()
            else:
                # Process dynamic menu options
                try:
                    choice_index = int(choice) - 5  # Adjust for the 4 standard options
                    
                    if 0 <= choice_index < len(options):
                        option = options[choice_index]
                        
                        if option == "universe_travel":
                            self.jump_universe()
                        elif option == "currency_exchange":
                            self.currency_exchange_menu()
                        elif option == "exchange_rates":
                            self.view_exchange_rates()
                        elif option == "heist_operations":
                            self.heist_operations()
                        elif option == "specialists":
                            self.recruit_specialists()
                        elif option == "special_items":
                            self.purchase_special_items()
                        elif option == "mini_games":
                            self.play_mini_games()
                        elif option == "ad_rewards":
                            self.ad_rewards_menu()
                        elif option == "save":
                            self.save_game()
                        elif option == "quit":
                            confirm = input(
                                "\nAre you sure you want to quit? Progress will be lost unless saved. (y/n): "
                            )
                            if confirm.lower() == "y":
                                print("\nThanks for playing Multiverse Tycoon!")
                                sys.exit()
                    else:
                        print("\nInvalid choice. Please try again.")
                        time.sleep(0.75)  # Reduced delay for faster gameplay
                except ValueError:
                    print("\nInvalid choice. Please enter a number.")
                    time.sleep(0.75)  # Reduced delay for faster gameplay

            # Only advance the turn if the player didn't save/quit
            should_advance = True
            if choice != "1" and choice != "2" and choice != "3" and choice != "4":
                try:
                    choice_index = int(choice) - 5
                    if 0 <= choice_index < len(options):
                        if options[choice_index] == "save" or options[choice_index] == "quit":
                            should_advance = False
                except:
                    pass
                    
            if should_advance:
                self.advance_turn()

            # Check for game over conditions
            if player_universe_data["danger"] >= self.DANGER_THRESHOLD:
                self.player["game_over"] = True
                self.player[
                    "end_reason"] = f"Your danger level reached {self.DANGER_THRESHOLD} in the {universe['name']} universe!"

            # If game is over, show game over screen
            if self.player["game_over"]:
                self.game_over()

    def start_business(self):
        """Start a new business in the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print(f"\n=== Start a Business in {universe['name']} ===")
        print(
            f"Available Cash: {player_universe_data['cash']} {universe['currency']}"
        )

        # Display available businesses
        available_businesses = [
            b for b in universe["businesses"]
            if b not in player_universe_data["businesses"]
        ]

        if not available_businesses:
            print(
                "\nYou already own all possible businesses in this universe!")
            input("\nPress Enter to continue...")
            return

        print("\nAvailable Businesses:")
        for i, business_id in enumerate(available_businesses, 1):
            business = universe["businesses"][business_id]
            print(
                f"{i}. {business['name']} - Cost: {business['income_per_turn']} {universe['currency']}"
            )
            print(
                f"   Income: {business['income_per_turn']} {universe['currency']}/turn"
            )
            print(f"   Risk Increase: {business['risk_increase']}")
            print(f"   Description: {business['description']}\n")

        print(f"{len(available_businesses) + 1}. Cancel")

        try:
            choice = int(input("\nWhich business would you like to start? "))

            if choice == len(available_businesses) + 1:
                return

            if 1 <= choice <= len(available_businesses):
                selected_business_id = available_businesses[choice - 1]
                selected_business = universe["businesses"][
                    selected_business_id]

                if player_universe_data["cash"] < selected_business["cost"]:
                    print(
                        f"\nNot enough cash! You need {selected_business['cost']} {universe['currency']}."
                    )
                    input("\nPress Enter to continue...")
                    return

                # Purchase the business
                player_universe_data["cash"] -= selected_business["cost"]
                player_universe_data["businesses"].append(selected_business_id)
                player_universe_data["danger"] += selected_business[
                    "risk_increase"]

                self.slow_print(
                    f"\nCongratulations! You now own a {selected_business['name']} in the {universe['name']} universe!"
                )
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
                self.start_business()
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.start_business()

    def hire_employee(self):
        """Hire an employee for the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print(f"\n=== Hire Employees in {universe['name']} ===")
        print(
            f"Available Cash: {player_universe_data['cash']} {universe['currency']}"
        )

        # Display available employee types
        print("\nAvailable Employee Types:")
        for i, (emp_id, emp_type) in enumerate(self.employee_types.items(), 1):
            print(
                f"{i}. {emp_type['name']} - Cost: {emp_type['hiring_cost']} {universe['currency']}"
            )
            print(
                f"   Salary: {emp_type['salary_per_turn']} {universe['currency']}/turn"
            )
            print(
                f"   Efficiency Bonus: +{emp_type['efficiency_bonus']*100}% income"
            )
            print(
                f"   Risk Reduction: -{emp_type['risk_reduction']} danger/turn\n"
            )

        print(f"{len(self.employee_types) + 1}. Cancel")

        try:
            choice = int(
                input("\nWhich type of employee would you like to hire? "))

            if choice == len(self.employee_types) + 1:
                return

            if 1 <= choice <= len(self.employee_types):
                emp_id = list(self.employee_types.keys())[choice - 1]
                emp_type = self.employee_types[emp_id]

                if player_universe_data["cash"] < emp_type["hiring_cost"]:
                    print(
                        f"\nNot enough cash! You need {emp_type['hiring_cost']} {universe['currency']}."
                    )
                    input("\nPress Enter to continue...")
                    return

                # Hire the employee
                player_universe_data["cash"] -= emp_type["hiring_cost"]
                player_universe_data["employees"].append({
                    "type": emp_id,
                    "loyalty": 100  # Starting loyalty
                })

                self.slow_print(
                    f"\nYou've hired a {emp_type['name']} in the {universe['name']} universe!"
                )
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
                self.hire_employee()
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.hire_employee()

    def fire_employee(self):
        """Fire an employee in the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print(f"\n=== Fire Employees in {universe['name']} ===")

        # Check if there are any employees to fire
        if not player_universe_data['employees']:
            print("\nYou don't have any employees to fire in this universe!")
            input("\nPress Enter to continue...")
            return

        # Display current employees
        print("\nYour Current Employees:")
        for i, employee in enumerate(player_universe_data['employees'], 1):
            emp_type = self.employee_types[employee['type']]
            print(
                f"{i}. {emp_type['name']} - Salary: {emp_type['salary_per_turn']} {universe['currency']}/turn"
            )
            print(
                f"   Efficiency Bonus: +{emp_type['efficiency_bonus']*100}% income"
            )
            print(
                f"   Risk Reduction: -{emp_type['risk_reduction']} danger/turn"
            )
            print(f"   Loyalty: {employee['loyalty']}%\n")

        print(f"{len(player_universe_data['employees']) + 1}. Cancel")

        try:
            choice = int(input("\nWhich employee would you like to fire? "))

            if choice == len(player_universe_data['employees']) + 1:
                return

            if 1 <= choice <= len(player_universe_data['employees']):
                # Get the employee to fire
                employee_index = choice - 1
                employee = player_universe_data['employees'][employee_index]
                emp_type = self.employee_types[employee['type']]

                # Severance pay (25% of hiring cost)
                severance_pay = int(emp_type['hiring_cost'] * 0.25)

                # Check if player has enough cash for severance
                if player_universe_data["cash"] < severance_pay:
                    print(
                        f"\nNot enough cash for severance pay! You need {severance_pay} {universe['currency']}."
                    )
                    input("\nPress Enter to continue...")
                    return

                # Pay severance and fire the employee
                player_universe_data["cash"] -= severance_pay
                fired_employee = player_universe_data['employees'].pop(
                    employee_index)

                # Reputation impact based on loyalty
                reputation_change = -10 + int(
                    employee['loyalty'] /
                    10)  # Better loyalty = less reputation damage
                player_universe_data["reputation"] += reputation_change

                self.slow_print(
                    f"\nYou've fired a {emp_type['name']} from the {universe['name']} universe."
                )
                print(f"Severance pay: {severance_pay} {universe['currency']}")

                if reputation_change < 0:
                    print(f"Reputation change: {reputation_change}")
                else:
                    print(f"Reputation change: +{reputation_change}")

                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
                self.fire_employee()
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.fire_employee()

    def bribe_officials(self):
        """Bribe officials to reduce danger level."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print(f"\n=== Bribe Officials in {universe['name']} ===")
        print(
            f"Available Cash: {player_universe_data['cash']} {universe['currency']}"
        )
        print(f"Current Danger Level: {player_universe_data['danger']}/100")

        # Calculate bribe options based on universe and current danger
        small_bribe = 1000
        medium_bribe = 3000
        large_bribe = 7000

        small_reduction = 5
        medium_reduction = 15
        large_reduction = 35

        print(
            f"\n1. Small Bribe: {small_bribe} {universe['currency']} (-{small_reduction} danger)"
        )
        print(
            f"2. Medium Bribe: {medium_bribe} {universe['currency']} (-{medium_reduction} danger)"
        )
        print(
            f"3. Large Bribe: {large_bribe} {universe['currency']} (-{large_reduction} danger)"
        )
        print("4. Cancel")

        choice = input("\nChoose a bribe option: ")

        if choice == "1":
            if player_universe_data["cash"] < small_bribe:
                print(
                    f"\nNot enough cash! You need {small_bribe} {universe['currency']}."
                )
            else:
                player_universe_data["cash"] -= small_bribe
                player_universe_data["danger"] = max(
                    0, player_universe_data["danger"] - small_reduction)
                print(
                    f"\nYou bribed a minor official. Danger reduced by {small_reduction}."
                )
        elif choice == "2":
            if player_universe_data["cash"] < medium_bribe:
                print(
                    f"\nNot enough cash! You need {medium_bribe} {universe['currency']}."
                )
            else:
                player_universe_data["cash"] -= medium_bribe
                player_universe_data["danger"] = max(
                    0, player_universe_data["danger"] - medium_reduction)
                print(
                    f"\nYou bribed a police captain. Danger reduced by {medium_reduction}."
                )
        elif choice == "3":
            if player_universe_data["cash"] < large_bribe:
                print(
                    f"\nNot enough cash! You need {large_bribe} {universe['currency']}."
                )
            else:
                player_universe_data["cash"] -= large_bribe
                player_universe_data["danger"] = max(
                    0, player_universe_data["danger"] - large_reduction)
                print(
                    f"\nYou bribed a high-ranking government official. Danger reduced by {large_reduction}."
                )
        elif choice == "4":
            return
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.bribe_officials()
            return

        input("\nPress Enter to continue...")

    def jump_universe(self):
        """Jump to another universe."""
        # Check if universe travel is unlocked
        if not self.player["unlocked_features"]["universe_travel"]:
            print("\nUniverse travel is not available yet.")
            print("This feature will unlock as you progress through the game.")
            input("\nPress Enter to continue...")
            return
        current_universe_id = self.player["current_universe"]

        self.clear_screen()
        print("\n=== Jump to Another Universe ===")
        print(
            f"Current Universe: {self.universes[current_universe_id]['name']}")

        # Display available universes
        print("\nAvailable Universes:")
        for i, (universe_id, universe) in enumerate(self.universes.items(), 1):
            if universe_id != current_universe_id:
                player_universe_data = self.player["universes"][universe_id]
                print(f"{i}. {universe['name']}")
                print(
                    f"   Cash: {player_universe_data['cash']} {universe['currency']}"
                )
                print(f"   Danger Level: {player_universe_data['danger']}/100")
                print(
                    f"   Businesses: {len(player_universe_data['businesses'])}"
                )
                print(
                    f"   Employees: {len(player_universe_data['employees'])}\n"
                )

        print(f"{len(self.universes) + 1}. Cancel")

        try:
            choice = int(input("\nWhich universe would you like to jump to? "))

            if choice == len(self.universes) + 1:
                return

            if 1 <= choice <= len(self.universes):
                target_universe_id = list(self.universes.keys())[choice - 1]

                # If selected the current universe
                if target_universe_id == current_universe_id:
                    print("\nYou're already in this universe!")
                    input("\nPress Enter to continue...")
                    return

                # Jump to the selected universe
                self.player["current_universe"] = target_universe_id

                self.slow_print(
                    f"\nYou've jumped to the {self.universes[target_universe_id]['name']} universe!"
                )
                self.slow_print(
                    "The dimensional shift temporarily disoriented you...")
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
                self.jump_universe()
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.jump_universe()

    def maybe_trigger_random_event(self):
        """Decide whether to trigger a random event based on probability."""
        # Event cooldown - minimum turns between events
        EVENT_COOLDOWN = 2
        # Base probability of event occurring (30%)
        EVENT_PROBABILITY = 0.45

        universe_id = self.player["current_universe"]
        current_turn = self.player["turn"]

        # Initialize event history for this universe if not present
        if universe_id not in self.player["event_history"]:
            self.player["event_history"][universe_id] = []

        # Check if enough turns have passed since last event
        turns_since_last_event = current_turn - self.player["last_event_turn"]
        if turns_since_last_event < EVENT_COOLDOWN:
            return

        # Calculate probability based on danger level
        player_universe_data = self.player["universes"][universe_id]
        danger_level = player_universe_data["danger"]
        # Increase probability based on danger (up to +20%)
        adjusted_probability = EVENT_PROBABILITY + (danger_level / 500)

        # Roll the dice - if random value is less than probability, trigger event
        if random.random() < adjusted_probability:
            self.trigger_random_event()
            self.player["last_event_turn"] = current_turn

    def trigger_random_event(self):
        """Trigger a random event from the current universe's event pool."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        # Get list of recent events to avoid repetition
        recent_events = self.player["event_history"].get(
            universe_id, [])[-3:]  # Last 3 events

        # Filter out recently occurred events if possible
        available_events = [
            e for e in universe["events"] if e["name"] not in recent_events
        ]

        # If all events were recently used, fall back to all events
        if not available_events:
            available_events = universe["events"]

        # Add weighting based on rarity
        # For now, equal weighting, but could be expanded
        event = random.choice(available_events)

        # Record this event
        self.player["event_history"].setdefault(universe_id,
                                                []).append(event["name"])

        # Keep history manageable
        while len(self.player["event_history"][universe_id]) > 10:
            self.player["event_history"][universe_id].pop(0)

        self.clear_screen()
        print("\n=== MULTIVERSE RIFT EVENT ===")
        self.slow_print(f"Event: {event['name']}")
        self.slow_print(f"Description: {event['description']}")

        # Apply the event effects
        player_universe_data["cash"] += event["effect"]["cash"]
        player_universe_data["danger"] += event["effect"]["danger"]
        player_universe_data["reputation"] += event["effect"]["reputation"]

        # Ensure danger doesn't go below 0
        player_universe_data["danger"] = max(0, player_universe_data["danger"])

        print("\nEffect:")
        if event["effect"]["cash"] > 0:
            print(f"• Cash: +{event['effect']['cash']} {universe['currency']}")
        else:
            print(f"• Cash: {event['effect']['cash']} {universe['currency']}")

        if event["effect"]["danger"] > 0:
            print(f"• Danger: +{event['effect']['danger']}")
        else:
            print(f"• Danger: {event['effect']['danger']}")

        if event["effect"]["reputation"] > 0:
            print(f"• Reputation: +{event['effect']['reputation']}")
        else:
            print(f"• Reputation: {event['effect']['reputation']}")

        input("\nPress Enter to continue...")

    def calculate_business_income(self):
        """Calculate and apply income from all businesses in the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        total_income = 0

        # Calculate base income from businesses
        for business_id in player_universe_data["businesses"]:
            business = universe["businesses"][business_id]
            total_income += business["income_per_turn"]

        # Apply employee efficiency bonuses
        employee_bonus = 0
        for employee in player_universe_data["employees"]:
            emp_type = self.employee_types[employee["type"]]
            employee_bonus += total_income * emp_type["efficiency_bonus"]

        total_income += employee_bonus
        
        # Apply ad reward multipliers if any are active
        ad_reward_multiplier = self.apply_ad_reward_effects()
        if ad_reward_multiplier > 1.0:
            original_income = total_income
            total_income *= ad_reward_multiplier
            print(f"\n💰 Ad reward bonus applied! Income multiplier: x{ad_reward_multiplier}")
            print(f"   Original income: {int(original_income)} {universe['currency']}")
            print(f"   Boosted income: {int(total_income)} {universe['currency']}")

        # Apply income
        player_universe_data["cash"] += int(total_income)

        return int(total_income)

    def pay_employee_salaries(self):
        """Pay salaries to all employees in the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        total_salaries = 0

        # Calculate total salaries
        for employee in player_universe_data["employees"]:
            emp_type = self.employee_types[employee["type"]]
            total_salaries += emp_type["salary_per_turn"]

        # Pay salaries if you have enough cash
        if player_universe_data["cash"] >= total_salaries:
            player_universe_data["cash"] -= total_salaries

            # Increase loyalty for being paid
            for employee in player_universe_data["employees"]:
                employee["loyalty"] = min(100, employee["loyalty"] + 5)
        else:
            # Couldn't pay salaries
            for employee in player_universe_data["employees"]:
                employee["loyalty"] -= 20

            # Remove employees with zero loyalty
            player_universe_data["employees"] = [
                e for e in player_universe_data["employees"]
                if e["loyalty"] > 0
            ]

        return total_salaries

    def apply_danger_reductions(self):
        """Apply danger reductions from employees."""
        universe_id = self.player["current_universe"]
        player_universe_data = self.player["universes"][universe_id]

        total_reduction = 0

        # Calculate total danger reduction
        for employee in player_universe_data["employees"]:
            emp_type = self.employee_types[employee["type"]]
            total_reduction += emp_type["risk_reduction"]

        # Apply reduction
        if total_reduction > 0:
            player_universe_data["danger"] = max(
                0, player_universe_data["danger"] - total_reduction)

        return total_reduction

    def check_feature_unlocks(self):
        """Check if any features should be unlocked based on game progress."""
        # Unlock universe travel at turn 10
        if self.player["turn"] >= 10 and not self.player["unlocked_features"]["universe_travel"]:
            self.player["unlocked_features"]["universe_travel"] = True
            print("\n🔓 New feature unlocked: Universe Travel!")
            print("You can now jump between different universes.")
            input("\nPress Enter to continue...")
            
        # Unlock currency exchange at turn 15
        if self.player["turn"] >= 15 and not self.player["unlocked_features"]["currency_exchange"]:
            self.player["unlocked_features"]["currency_exchange"] = True
            print("\n🔓 New feature unlocked: Currency Exchange!")
            print("You can now exchange currencies between universes.")
            input("\nPress Enter to continue...")
            
        # Unlock mini games at turn 5
        if self.player["turn"] >= 5 and not self.player["unlocked_features"]["mini_games"]:
            self.player["unlocked_features"]["mini_games"] = True
            print("\n🔓 New feature unlocked: Mini Games!")
            print("Play games to earn extra rewards!")
            input("\nPress Enter to continue...")
            
        # Unlock heist operations at turn 20
        if self.player["turn"] >= 20 and not self.player["unlocked_features"]["heist_operations"]:
            self.player["unlocked_features"]["heist_operations"] = True
            print("\n🔓 New feature unlocked: Heist Operations!")
            print("Plan and execute heists for big rewards!")
            input("\nPress Enter to continue...")
            
        # Unlock specialists after completing 2 heists
        if len(self.player["heist_history"]) >= 2 and not self.player["unlocked_features"]["specialists"]:
            self.player["unlocked_features"]["specialists"] = True
            print("\n🔓 New feature unlocked: Specialists Recruitment!")
            print("Hire specialist crew members to improve your heist success rates.")
            input("\nPress Enter to continue...")
            
        # Unlock special items after recruiting 2 specialists
        if len(self.player["heist_specialists"]) >= 2 and not self.player["unlocked_features"]["special_items"]:
            self.player["unlocked_features"]["special_items"] = True
            print("\n🔓 New feature unlocked: Special Items!")
            print("Purchase special equipment to help with your heists.")
            input("\nPress Enter to continue...")

    def game_over(self):
        """Display game over screen and final stats."""
        self.clear_screen()

        print("""
        ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
        ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
        ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
        ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
        ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
         ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
        """)

        self.slow_print(f"\nReason: {self.player['end_reason']}")

        # Display final stats
        print("\n=== Final Stats ===")
        print(f"Entrepreneur: {self.player['name']}")
        print(f"Turns Survived: {self.player['turn']}")

        total_wealth = 0
        total_businesses = 0
        max_danger = 0

        for universe_id, universe_data in self.player["universes"].items():
            universe = self.universes[universe_id]
            print(f"\n{universe['name']} Universe:")
            print(f"• Cash: {universe_data['cash']} {universe['currency']}")
            print(f"• Businesses: {len(universe_data['businesses'])}")
            print(f"• Employees: {len(universe_data['employees'])}")
            print(f"• Danger Level: {universe_data['danger']}/100")
            print(f"• Reputation: {universe_data['reputation']}")

            total_wealth += universe_data['cash']
            total_businesses += len(universe_data['businesses'])
            max_danger = max(max_danger, universe_data['danger'])

        # Display quantum/interdimensional stats
        print(f"\nInterdimensional Empire:")
        print(f"• Quantum Credits: {self.player['quantum_credits']} Q¢")
        print(
            f"• Quantum Businesses: {len(self.player['quantum_businesses'])}")

        # Calculate total wealth in quantum credits for comparison
        total_quantum_wealth = self.currency_exchange.calculate_total_quantum_wealth(
            self.player)

        print(
            f"\nTotal Wealth Across Multiverse: {total_wealth} (combined currencies)"
        )
        print(f"Total Wealth in Quantum Credits: {total_quantum_wealth} Q¢")
        print(
            f"Total Businesses: {total_businesses + len(self.player['quantum_businesses'])}"
        )
        print(f"Maximum Danger Level: {max_danger}/100")

        # Ask if the player wants to play again
        print("\n1. Return to Main Menu")
        print("2. Quit Game")

        choice = input("\nWhat would you like to do? ")

        if choice == "1":
            # Reset the game
            self.__init__()
            self.start_game()
        else:
            print("\nThanks for playing Multiverse Tycoon!")
            sys.exit()

    def currency_exchange_menu(self):
        """Display the currency exchange menu and handle transactions."""
        # Check if currency exchange is unlocked
        if not self.player["unlocked_features"]["currency_exchange"]:
            print("\nCurrency exchange is not available yet.")
            print("This feature will unlock as you progress through the game.")
            input("\nPress Enter to continue...")
            return
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print("\n=== Quantum Credit Exchange ===")
        print(
            f"Local Currency: {player_universe_data['cash']} {universe['currency']}"
        )
        print(f"Quantum Credits: {self.player['quantum_credits']} Q¢")
        print(
            f"Exchange Rate: {self.currency_exchange.get_exchange_rate(universe_id)} {universe['currency']} = 1 Q¢"
        )
        print(f"Exchange Fee: {self.currency_exchange.exchange_fee}%")

        print("\n1. Exchange local currency for Quantum Credits")
        print("2. Exchange Quantum Credits for local currency")
        print("3. Back")

        choice = input("\nWhat would you like to do? ")

        if choice == "1":
            # Local to Quantum
            try:
                amount = int(
                    input(
                        f"\nHow much {universe['currency']} would you like to exchange? "
                    ))

                if amount <= 0:
                    print("\nPlease enter a positive amount.")
                    time.sleep(0.75)  # Reduced delay for faster gameplay
                    return

                if amount > player_universe_data["cash"]:
                    print(f"\nYou don't have enough {universe['currency']}.")
                    time.sleep(0.75)  # Reduced delay for faster gameplay
                    return

                quantum_amount = self.currency_exchange.local_to_quantum(
                    amount, universe_id)

                print(
                    f"\nYou will receive {quantum_amount} Q¢ for {amount} {universe['currency']}."
                )
                confirm = input("Proceed with the exchange? (y/n): ")

                if confirm.lower() == "y":
                    # Deduct local currency
                    player_universe_data["cash"] -= amount
                    # Add quantum credits
                    self.player["quantum_credits"] += quantum_amount

                    print(
                        f"\nExchange complete! You now have {self.player['quantum_credits']} Q¢."
                    )
            except ValueError:
                print("\nPlease enter a valid number.")

            time.sleep(0.75)  # Reduced delay for faster gameplay

        elif choice == "2":
            # Quantum to Local
            try:
                amount = float(
                    input(
                        "\nHow many Quantum Credits would you like to exchange? "
                    ))

                if amount <= 0:
                    print("\nPlease enter a positive amount.")
                    time.sleep(0.75)  # Reduced delay for faster gameplay
                    return

                if amount > self.player["quantum_credits"]:
                    print("\nYou don't have enough Quantum Credits.")
                    time.sleep(0.75)  # Reduced delay for faster gameplay
                    return

                local_amount = self.currency_exchange.quantum_to_local(
                    amount, universe_id)

                print(
                    f"\nYou will receive {local_amount} {universe['currency']} for {amount} Q¢."
                )
                confirm = input("Proceed with the exchange? (y/n): ")

                if confirm.lower() == "y":
                    # Deduct quantum credits
                    self.player["quantum_credits"] -= amount
                    # Add local currency
                    player_universe_data["cash"] += local_amount

                    print(
                        f"\nExchange complete! You now have {player_universe_data['cash']} {universe['currency']}."
                    )
            except ValueError:
                print("\nPlease enter a valid number.")

            time.sleep(0.75)  # Reduced delay for faster gameplay

    def view_exchange_rates(self):
        """View the exchange rates for all universes."""
        # Check if currency exchange is unlocked
        if not self.player["unlocked_features"]["currency_exchange"]:
            print("\nCurrency exchange is not available yet.")
            print("This feature will unlock as you progress through the game.")
            input("\nPress Enter to continue...")
            return
        self.clear_screen()
        print(self.currency_exchange.display_exchange_rates())
        input("\nPress Enter to continue...")

    def quantum_business_center(self):
        """Manage quantum businesses that operate across universes."""
        self.clear_screen()
        print("\n=== Quantum Business Center ===")
        print(
            "These special businesses operate across all universes using Quantum Credits."
        )
        print(
            f"Available Quantum Credits: {self.player['quantum_credits']} Q¢")

        # Display owned quantum businesses
        if self.player["quantum_businesses"]:
            print("\n=== Your Quantum Businesses ===")
            for business_id in self.player["quantum_businesses"]:
                business = self.quantum_businesses.quantum_businesses[
                    business_id]
                print(
                    f"- {business['name']} (Income: {business['income_per_turn']} Q¢/turn)"
                )
                print(f"  Description: {business['description']}")

        # Display available quantum businesses
        available_businesses = self.quantum_businesses.get_available_businesses(
            self.player, self.currency_exchange)

        if available_businesses:
            print("\n=== Available Quantum Businesses ===")
            for i, (business_id,
                    business) in enumerate(available_businesses.items(), 1):
                print(
                    f"{i}. {business['name']} (Cost: {business['cost']['quantum_credits']} Q¢)"
                )
                print(f"   Income: {business['income_per_turn']} Q¢/turn")
                print(f"   Description: {business['description']}")
                print(f"   Risk Increase: {business['risk_increase']}")
                print()

            print(f"{len(available_businesses) + 1}. Back")

            try:
                choice = int(
                    input("\nWhich business would you like to start? "))

                if choice == len(available_businesses) + 1:
                    return

                if 1 <= choice <= len(available_businesses):
                    business_id = list(available_businesses.keys())[choice - 1]
                    business = available_businesses[business_id]

                    # Check if player has enough quantum credits
                    if self.player["quantum_credits"] < business["cost"][
                            "quantum_credits"]:
                        print("\nYou don't have enough Quantum Credits!")
                        time.sleep(0.75)  # Reduced delay for faster gameplay
                        return

                    # Purchase the business
                    self.player["quantum_credits"] -= business["cost"][
                        "quantum_credits"]
                    self.player["quantum_businesses"].append(business_id)

                    print(
                        f"\nCongratulations! You now own a {business['name']}!"
                    )
                    print(
                        f"It will generate {business['income_per_turn']} Q¢ per turn."
                    )

                    # Update current universe's danger level
                    universe_id = self.player["current_universe"]
                    player_universe_data = self.player["universes"][
                        universe_id]
                    player_universe_data["danger"] += business["risk_increase"]

                    # Check if danger level exceeds threshold
                    if player_universe_data["danger"] >= self.DANGER_THRESHOLD:
                        self.player["game_over"] = True
                        self.player[
                            "end_reason"] = f"Your operation in the {self.universes[universe_id]['name']} universe was discovered!"
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nPlease enter a valid number.")
        else:
            print("\nNo quantum businesses available yet.")
            print(
                "You may need to build more regular businesses or increase your reputation."
            )

        input("\nPress Enter to continue...")

    def calculate_quantum_business_income(self):
        """Calculate and apply income from quantum businesses."""
        if not self.player["quantum_businesses"]:
            return

        total_income = 0

        for business_id in self.player["quantum_businesses"]:
            business = self.quantum_businesses.quantum_businesses[business_id]
            total_income += business["income_per_turn"]

        self.player["quantum_credits"] += total_income
        print(
            f"\nYour quantum businesses generated {total_income} Q¢ this turn!"
        )

    def check_for_quantum_events(self):
        """Check if a quantum event should occur this turn."""
        current_turn = self.player["turn"]

        # Check if enough turns have passed since last quantum event
        turns_since_last_event = current_turn - self.player.get(
            "last_quantum_event_turn", 0)
        if turns_since_last_event < self.QUANTUM_EVENT_COOLDOWN:
            return

        # Roll the dice - if random value is less than probability, trigger event
        if random.random() < self.QUANTUM_EVENT_PROBABILITY:
            self.trigger_quantum_event()
            self.player["last_quantum_event_turn"] = current_turn

    def trigger_quantum_event(self):
        """Trigger a random quantum event that affects interdimensional operations."""
        event = self.quantum_events.get_random_event()

        if not event:
            return

        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]

        self.clear_screen()
        print("\n=== QUANTUM ANOMALY DETECTED ===")
        self.slow_print(f"Event: {event['name']}")
        self.slow_print(f"Description: {event['description']}")

        # Apply the event effects
        effect = event["effect"]

        if "quantum_credits" in effect:
            self.player["quantum_credits"] += effect["quantum_credits"]
            self.player["quantum_credits"] = max(
                0, self.player["quantum_credits"])  # Ensure not negative

        if "exchange_rate_modifier" in effect:
            # This would modify exchange rates temporarily - simplified implementation
            pass

        if "exchange_fee_reduction" in effect:
            # This would reduce exchange fees temporarily - simplified implementation
            pass

        print("\nEffect:")
        if "quantum_credits" in effect:
            if effect["quantum_credits"] > 0:
                print(f"• Quantum Credits: +{effect['quantum_credits']} Q¢")
            else:
                print(f"• Quantum Credits: {effect['quantum_credits']} Q¢")

        if "exchange_rate_modifier" in effect:
            print(
                f"• Exchange rates have been temporarily modified by {effect['exchange_rate_modifier'] * 100}%"
            )

        if "exchange_fee_reduction" in effect:
            print(
                f"• Exchange fees have been temporarily reduced by {effect['exchange_fee_reduction']}%"
            )

        input("\nPress Enter to continue...")

    def heist_operations(self):
        """Manage heist planning and execution."""
        # Check if heist operations are unlocked
        if not self.player["unlocked_features"]["heist_operations"]:
            print("\nHeist operations are not available yet.")
            print("This feature will unlock as you progress through the game.")
            input("\nPress Enter to continue...")
            return
        # Check if player is on heist cooldown
        if self.player["heist_cooldown"] > 0:
            self.clear_screen()
            print("\n=== Heist Operations ===")
            print(
                f"Your crew is laying low after the last heist. Cooldown: {self.player['heist_cooldown']} turns."
            )
            input("\nPress Enter to continue...")
            return

        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print("\n=== Interdimensional Heist Operations ===")
        print(f"Current Universe: {universe['name']}")
        print(
            f"Available Cash: {player_universe_data['cash']} {universe['currency']}"
        )
        print(f"Quantum Credits: {self.player['quantum_credits']} Q¢")
        print(f"Danger Level: {player_universe_data['danger']}/100")

        # Display available heists in the current universe
        available_heists = self.heist_system.get_available_heists(universe_id)

        if not available_heists:
            print(
                f"\nNo heist opportunities available in the {universe['name']} universe."
            )
            input("\nPress Enter to continue...")
            return

        print("\n=== Available Heists ===")
        for i, heist in enumerate(available_heists, 1):
            print(f"{i}. {heist['name']}")
            print(f"   Description: {heist['description']}")
            print(
                f"   Base Reward: {heist['base_reward']} {universe['currency']} + {heist['quantum_reward']} Q¢"
            )
            print(f"   Required Skills: {', '.join(heist['required_skills'])}")
            print(f"   Special Item: {heist['special_item']}")
            print()

        print(f"{len(available_heists) + 1}. Back")

        try:
            choice = int(input("\nSelect a heist to plan: "))

            if choice == len(available_heists) + 1:
                return

            if 1 <= choice <= len(available_heists):
                selected_heist = available_heists[choice - 1]
                self.plan_heist(selected_heist)
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay

    def plan_heist(self, heist):
        """Plan the details of a heist."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        # Determine which difficulty levels are available
        self.clear_screen()
        print(f"\n=== Planning: {heist['name']} ===")
        print(f"Description: {heist['description']}")
        print(f"Required Skills: {', '.join(heist['required_skills'])}")

        # Check if player has any specialists with required skills
        has_required_skills = False
        for skill in heist['required_skills']:
            for specialist_id in self.player["heist_specialists"]:
                specialist = self.heist_system.specialists[specialist_id]
                if skill in specialist["skills"]:
                    has_required_skills = True
                    break
            if has_required_skills:
                break

        # Check if player has the special item for this heist
        has_special_item = False
        special_item_id = heist['special_item']
        if special_item_id in self.player["special_items"]:
            has_special_item = True
            special_item = self.heist_system.special_items[special_item_id]

        # Display difficulty options
        print("\n=== Select Difficulty ===")

        difficulty_options = []
        for diff_id, difficulty in self.heist_system.difficulty_levels.items():
            # Check if player has enough crew members for this difficulty
            has_enough_crew = len(
                self.player["heist_specialists"]) >= difficulty["min_crew"]

            # Calculate base success chance
            base_success = int(difficulty["success_chance"] * 100)

            # Calculate potential success chance with player's specialists and items
            potential_crew = self.player["heist_specialists"]
            potential_items = self.player["special_items"]
            potential_success = int(
                self.heist_system.get_heist_success_chance(
                    heist, diff_id, potential_crew, potential_items) * 100)

            # Calculate rewards at this difficulty
            reward_multiplier = difficulty["reward_multiplier"]
            local_reward = int(heist["base_reward"] * reward_multiplier)
            quantum_reward = int(heist["quantum_reward"] * reward_multiplier)

            # Add to available difficulties if player has enough crew
            if has_enough_crew:
                difficulty_options.append(diff_id)
                print(f"{len(difficulty_options)}. {difficulty['name']}")
                print(f"   Base Success Chance: {base_success}%")
                print(f"   Your Success Chance: {potential_success}%")
                print(
                    f"   Reward: {local_reward} {universe['currency']} + {quantum_reward} Q¢"
                )
                print(f"   Danger Increase: {difficulty['danger_increase']}")
                print(
                    f"   Required Crew: {difficulty['min_crew']} specialists")
                print(
                    f"   Preparation Cost: {difficulty['min_preparation']} {universe['currency']}"
                )
                print()

        if not difficulty_options:
            print(
                "\nYou don't have enough crew members for any difficulty level."
            )
            print("Consider recruiting more specialists first.")
            input("\nPress Enter to continue...")
            return

        print(f"{len(difficulty_options) + 1}. Back")

        try:
            choice = int(input("\nSelect a difficulty level: "))

            if choice == len(difficulty_options) + 1:
                return

            if 1 <= choice <= len(difficulty_options):
                selected_difficulty = difficulty_options[choice - 1]
                difficulty = self.heist_system.difficulty_levels[
                    selected_difficulty]

                # Check if player has enough cash for preparation
                if player_universe_data["cash"] < difficulty[
                        "min_preparation"]:
                    print(
                        f"\nYou don't have enough {universe['currency']} for the necessary preparations."
                    )
                    print(
                        f"You need {difficulty['min_preparation']} {universe['currency']}."
                    )
                    input("\nPress Enter to continue...")
                    return

                # Confirm heist attempt
                preparation_cost = difficulty["min_preparation"]
                print(
                    f"\nPreparing this heist will cost {preparation_cost} {universe['currency']}."
                )
                confirm = input("Proceed with the heist? (y/n): ")

                if confirm.lower() == "y":
                    # Deduct preparation cost
                    player_universe_data["cash"] -= preparation_cost

                    # Execute the heist
                    self.execute_heist(heist, selected_difficulty)

            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay

    def execute_heist(self, heist, difficulty_id):
        """Execute a heist and determine the outcome."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print(f"\n=== Executing Heist: {heist['name']} ===")

        # Build suspense with typing effect
        self.slow_print("Infiltrating target location...")
        time.sleep(1)
        self.slow_print("Bypassing security systems...")
        time.sleep(1)
        self.slow_print("Accessing the objective...")
        time.sleep(0.75)  # Reduced delay for faster gameplay

        # Execute the heist and get results
        result = self.heist_system.execute_heist(
            heist, difficulty_id, self.player["heist_specialists"],
            self.player["special_items"])

        # Display outcome
        print("\n=== Heist Result ===")

        if result["success"]:
            print(
                "\nSUCCESS! You completed the heist and escaped with the loot!"
            )
        else:
            print(
                "\nFAILURE! Something went wrong and you had to abort the heist."
            )

        print(f"Success Chance: {int(result['success_chance'] * 100)}%")
        print(f"Roll: {int(result['roll'] * 100)}%")

        # Apply rewards if successful
        if result["success"]:
            # Calculate crew payment
            print("\n=== Rewards ===")
            print(
                f"Total Haul: {result['gross_reward']['local_currency']} {universe['currency']} + {result['gross_reward']['quantum_credits']} Q¢"
            )
            print(
                f"Crew Payment: {result['crew_payment']['local_currency']} {universe['currency']} + {result['crew_payment']['quantum_credits']} Q¢ ({result['crew_payment']['percentage']}%)"
            )
            print(
                f"Your Share: {result['net_reward']['local_currency']} {universe['currency']} + {result['net_reward']['quantum_credits']} Q¢"
            )

            # Add rewards to player
            player_universe_data["cash"] += result["net_reward"][
                "local_currency"]
            self.player["quantum_credits"] += result["net_reward"][
                "quantum_credits"]

            # Increase danger level
            danger_increase = result["danger_increase"]
            player_universe_data["danger"] += danger_increase
            print(f"\nDanger level increased by {danger_increase}!")

            # Check if danger level exceeds threshold
            if player_universe_data["danger"] >= self.DANGER_THRESHOLD:
                self.player["game_over"] = True
                self.player[
                    "end_reason"] = f"Your heist operation in {universe['name']} was discovered by authorities!"

            # Add to heist history
            self.player["heist_history"].append({
                "name":
                heist["name"],
                "universe":
                universe["name"],
                "difficulty":
                self.heist_system.difficulty_levels[difficulty_id]["name"],
                "success":
                True,
                "reward_local":
                result["net_reward"]["local_currency"],
                "reward_quantum":
                result["net_reward"]["quantum_credits"],
                "turn":
                self.player["turn"]
            })

            # Set cooldown
            self.player["heist_cooldown"] = 3  # 3 turns until next heist
        else:
            print("\nSince the heist failed, you didn't earn any rewards.")
            print("However, your escape was clean and didn't raise suspicion.")

            # Add to heist history
            self.player["heist_history"].append({
                "name":
                heist["name"],
                "universe":
                universe["name"],
                "difficulty":
                self.heist_system.difficulty_levels[difficulty_id]["name"],
                "success":
                False,
                "reward_local":
                0,
                "reward_quantum":
                0,
                "turn":
                self.player["turn"]
            })

            # Set cooldown
            self.player["heist_cooldown"] = 2  # 2 turns until next heist

        input("\nPress Enter to continue...")

    def recruit_specialists(self):
        """Recruit specialists for heist operations."""
        # Check if specialists are unlocked
        if not self.player["unlocked_features"]["specialists"]:
            print("\nSpecialist recruitment is not available yet.")
            print("This feature will unlock after you've completed a few heists.")
            input("\nPress Enter to continue...")
            return
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print("\n=== Recruit Heist Specialists ===")
        print(
            f"Available Cash: {player_universe_data['cash']} {universe['currency']}"
        )
        print(f"Quantum Credits: {self.player['quantum_credits']} Q¢")

        # Show currently owned specialists
        if self.player["heist_specialists"]:
            print("\n=== Your Specialist Crew ===")
            for specialist_id in self.player["heist_specialists"]:
                specialist = self.heist_system.specialists[specialist_id]
                print(f"- {specialist['name']}")
                print(f"  Skills: {', '.join(specialist['skills'])}")
                print(
                    f"  Payment: {specialist['payment_percentage']}% of heist rewards"
                )
                print()

        # Get available specialists for recruitment
        available_specialists = self.heist_system.get_available_specialists(
            self.player["heist_specialists"])

        if not available_specialists:
            print("\nThere are no more specialists available for recruitment.")
            input("\nPress Enter to continue...")
            return

        print("\n=== Available Specialists ===")
        specialists_list = list(available_specialists.items())

        for i, (specialist_id, specialist) in enumerate(specialists_list, 1):
            print(f"{i}. {specialist['name']}")
            print(f"   Skills: {', '.join(specialist['skills'])}")
            print(
                f"   Hiring Cost: {specialist['hiring_cost']} {universe['currency']}"
            )
            print(
                f"   Payment: {specialist['payment_percentage']}% of heist rewards"
            )
            print(
                f"   Success Bonus: +{int(specialist['success_bonus'] * 100)}% for heists using their skills"
            )
            print()

        print(f"{len(specialists_list) + 1}. Back")

        try:
            choice = int(
                input("\nWhich specialist would you like to recruit? "))

            if choice == len(specialists_list) + 1:
                return

            if 1 <= choice <= len(specialists_list):
                specialist_id, specialist = specialists_list[choice - 1]

                # Check if player has enough cash
                if player_universe_data["cash"] < specialist["hiring_cost"]:
                    print(
                        f"\nYou don't have enough {universe['currency']} to hire this specialist."
                    )
                    time.sleep(0.75)  # Reduced delay for faster gameplay
                    return

                # Confirm recruitment
                confirm = input(
                    f"\nHire {specialist['name']} for {specialist['hiring_cost']} {universe['currency']}? (y/n): "
                )

                if confirm.lower() == "y":
                    # Deduct cost and add specialist to crew
                    player_universe_data["cash"] -= specialist["hiring_cost"]
                    self.player["heist_specialists"].append(specialist_id)

                    print(f"\n{specialist['name']} has joined your crew!")
                    print(
                        f"They will help with heists requiring {', '.join(specialist['skills'])} skills."
                    )
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay

        input("\nPress Enter to continue...")

    def purchase_special_items(self):
        """Purchase special items for heist operations."""
        # Check if special items are unlocked
        if not self.player["unlocked_features"]["special_items"]:
            print("\nSpecial items are not available yet.")
            print("This feature will unlock after you've recruited a few specialists.")
            input("\nPress Enter to continue...")
            return
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print("\n=== Purchase Special Items ===")
        print(
            f"Available Cash: {player_universe_data['cash']} {universe['currency']}"
        )
        print(f"Quantum Credits: {self.player['quantum_credits']} Q¢")

        # Show currently owned items
        if self.player["special_items"]:
            print("\n=== Your Special Items ===")
            for item_id in self.player["special_items"]:
                item = self.heist_system.special_items[item_id]
                print(f"- {item['name']}")
                print(f"  Description: {item['description']}")
                print(
                    f"  Success Bonus: +{int(item['success_bonus'] * 100)}% for applicable heists"
                )
                print(
                    f"  Applicable Heists: {', '.join(item['applicable_heists'])}"
                )
                print()

        # Get available items for purchase
        available_items = self.heist_system.get_available_special_items(
            self.player["special_items"])

        if not available_items:
            print("\nThere are no more special items available for purchase.")
            input("\nPress Enter to continue...")
            return

        print("\n=== Available Special Items ===")
        items_list = list(available_items.items())

        for i, (item_id, item) in enumerate(items_list, 1):
            print(f"{i}. {item['name']}")
            print(f"   Description: {item['description']}")
            print(f"   Cost: {item['cost']} {universe['currency']}")
            print(
                f"   Success Bonus: +{int(item['success_bonus'] * 100)}% for applicable heists"
            )
            print(
                f"   Applicable Heists: {', '.join(item['applicable_heists'])}"
            )
            print()

        print(f"{len(items_list) + 1}. Back")

        try:
            choice = int(input("\nWhich item would you like to purchase? "))

            if choice == len(items_list) + 1:
                return

            if 1 <= choice <= len(items_list):
                item_id, item = items_list[choice - 1]

                # Check if player has enough cash
                if player_universe_data["cash"] < item["cost"]:
                    print(
                        f"\nYou don't have enough {universe['currency']} to purchase this item."
                    )
                    time.sleep(0.75)  # Reduced delay for faster gameplay
                    return

                # Confirm purchase
                confirm = input(
                    f"\nPurchase {item['name']} for {item['cost']} {universe['currency']}? (y/n): "
                )

                if confirm.lower() == "y":
                    # Deduct cost and add item to inventory
                    player_universe_data["cash"] -= item["cost"]
                    self.player["special_items"].append(item_id)

                    print(f"\nYou have acquired the {item['name']}!")
                    print(
                        f"This will be useful for the following heists: {', '.join(item['applicable_heists'])}"
                    )
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay

        input("\nPress Enter to continue...")

    def advance_turn(self):
        """Advance the game by one turn."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        # Increase the turn counter
        self.player["turn"] += 1

        # Calculate and apply business income
        income = self.calculate_business_income()

        # Calculate income from quantum businesses (only show if it's unlocked)
        quantum_income = 0
        
        # Pay employee salaries
        salaries = self.pay_employee_salaries()

        # Apply danger reductions from employees
        danger_reduction = self.apply_danger_reductions()

        # Trigger a random event with probability
        self.maybe_trigger_random_event()

        # Reduce heist cooldown if active
        if self.player["heist_cooldown"] > 0:
            self.player["heist_cooldown"] -= 1
            if self.player["heist_cooldown"] == 0:
                print("\nYour crew is ready for another heist!")
                
        # Reduce mini game cooldown if active
        if self.player["mini_game_cooldown"] > 0:
            self.player["mini_game_cooldown"] -= 1
            if self.player["mini_game_cooldown"] == 0:
                print("\nYou're ready to play mini games again!")

        # Check for new feature unlocks
        self.check_feature_unlocks()

        # Display turn summary
        self.clear_screen()
        print("\n=== Turn Summary ===")


    def play_mini_games(self):
        """Play mini games to earn rewards."""
        # Check if mini games are unlocked
        if not self.player["unlocked_features"]["mini_games"]:
            print("\nMini games are not available yet.")
            print("This feature will unlock as you progress through the game.")
            input("\nPress Enter to continue...")
            return
            
        # Check if player is on mini game cooldown
        if self.player["mini_game_cooldown"] > 0:
            self.clear_screen()
            print("\n=== Mini Games ===")
            print(f"You need to rest before playing more mini games. Cooldown: {self.player['mini_game_cooldown']} turns.")
            input("\nPress Enter to continue...")
            return
            
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]
        
        self.clear_screen()
        print("\n=== Multiverse Mini Games ===")
        print("Play games to earn rewards and boost your business empire!")
        print(f"Current Universe: {universe['name']}")
        print(f"Local Currency: {player_universe_data['cash']} {universe['currency']}")
        print(f"Quantum Credits: {self.player['quantum_credits']} Q¢")
        
        # Get all mini games
        all_games = self.mini_game_system.get_all_games()
        games_list = list(all_games.items())
        
        # Display available mini games
        print("\n=== Available Games ===")
        for i, (game_id, game) in enumerate(games_list, 1):
            print(f"{i}. {game['name']} - {game['difficulty']}")
            print(f"   Description: {game['description']}")
            print()
            
        print(f"{len(games_list) + 1}. Back")
        
        try:
            choice = int(input("\nWhich game would you like to play? "))
            
            if choice == len(games_list) + 1:
                return
                
            if 1 <= choice <= len(games_list):
                game_id, game = games_list[choice - 1]
                self.select_mini_game_difficulty(game_id, game)
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            
    def select_mini_game_difficulty(self, game_id, game):
        """Select the difficulty level for a mini game."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        
        self.clear_screen()
        print(f"\n=== {game['name']} ===")
        print(f"Description: {game['description']}")
        
        # Display difficulty options
        print("\n=== Select Difficulty ===")
        difficulties = ["easy", "medium", "hard"]
        
        for i, diff in enumerate(difficulties, 1):
            rewards = game["rewards"][diff]
            print(f"{i}. {diff.capitalize()}")
            print(f"   Rewards: {rewards['local_currency']} {universe['currency']}, {rewards['quantum_credits']} Q¢")
            print(f"   Reputation Gain: +{rewards['reputation']}")
            print()
            
        print(f"{len(difficulties) + 1}. Back")
        
        try:
            choice = int(input("\nSelect difficulty level: "))
            
            if choice == len(difficulties) + 1:
                return
                
            if 1 <= choice <= len(difficulties):
                selected_difficulty = difficulties[choice - 1]
                self.play_selected_mini_game(game_id, selected_difficulty)
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)  # Reduced delay for faster gameplay
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            
    def play_selected_mini_game(self, game_id, difficulty):
        """Play the selected mini game at the chosen difficulty."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]
        
        # Play the game
        success = self.mini_game_system.play_game(game_id, difficulty)
        
        # Update player stats
        self.player["mini_games_played"] += 1
        if success:
            self.player["mini_games_won"] += 1
            
        # Add to mini game history
        self.player["mini_game_history"].append({
            "game_id": game_id,
            "game_name": self.mini_game_system.mini_games[game_id]["name"],
            "difficulty": difficulty,
            "success": success,
            "turn": self.player["turn"],
            "universe": universe["name"]
        })
        
        # Apply rewards if successful
        if success:
            rewards = self.mini_game_system.get_rewards(game_id, difficulty)
            
            # Add local currency
            player_universe_data["cash"] += rewards["local_currency"]
            
            # Add quantum credits
            self.player["quantum_credits"] += rewards["quantum_credits"]
            
            # Add reputation
            player_universe_data["reputation"] += rewards["reputation"]
            
            # Display rewards
            self.clear_screen()
            print("\n=== Mini Game Rewards ===")
            print(f"Congratulations! You've earned:")
            print(f"• {rewards['local_currency']} {universe['currency']}")
            print(f"• {rewards['quantum_credits']} Quantum Credits")
            print(f"• +{rewards['reputation']} Reputation")
        else:
            self.clear_screen()
            print("\n=== Mini Game Results ===")
            print("Better luck next time! You didn't earn any rewards.")
        
        # Set cooldown (1 turn for mini games)
        self.player["mini_game_cooldown"] = 1
        
        input("\nPress Enter to continue...")
    
    def ad_rewards_menu(self):
        """Display and handle the ad rewards menu."""
        while True:
            self.clear_screen()
            
            # Display a header
            print("\n=== Ad Rewards System ===")
            print("Boost your progress by watching ads or redeeming codes!")
            
            # Show active boosts
            active_boosts = self.ad_rewards_system.get_active_boosts()
            if active_boosts:
                print("\n=== Active Boosts ===")
                for boost in active_boosts:
                    print(f"• {boost['name']} - {boost['turns_remaining']} turns remaining")
            else:
                print("\nNo active boosts at the moment.")
                
            # Show menu options
            print("\nOptions:")
            print("1. Watch an ad for a random reward")
            print("2. Redeem a reward code")
            print("3. About ad rewards")
            print("4. Back to main menu")
            
            choice = input("\nSelect an option (1-4): ")
            
            if choice == "1":
                self.watch_ad_for_reward()
            elif choice == "2":
                self.redeem_reward_code()
            elif choice == "3":
                self.display_ad_rewards_info()
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def watch_ad_for_reward(self):
        """Simulate watching an ad and receive a reward."""
        self.clear_screen()
        print("\n=== Watch Ad for Reward ===")
        print("Watching an ad will get you a random reward.")
        print("You can do this once every 12 hours in real time.")
        
        confirm = input("\nWould you like to watch an ad now? (y/n): ")
        
        if confirm.lower() == "y":
            print("\nSimulating ad watching...")
            for _ in range(5):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()
            
            # Process the ad watch
            success, message = self.ad_rewards_system.watch_ad_for_reward(self.player)
            
            if success:
                print(f"\n✓ {message}")
            else:
                print(f"\n✗ {message}")
        
        input("\nPress Enter to continue...")
    
    def redeem_reward_code(self):
        """Allow the player to enter and redeem a reward code."""
        self.clear_screen()
        print("\n=== Redeem Reward Code ===")
        print("Enter a valid reward code to receive special bonuses.")
        
        code = input("\nEnter reward code (or type 'back' to return): ")
        
        if code.lower() == "back":
            return
            
        # Process the code redemption
        success, message = self.ad_rewards_system.redeem_code(self.player, code)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
        
        input("\nPress Enter to continue...")
    
    def display_ad_rewards_info(self):
        """Display information about possible ad rewards."""
        self.clear_screen()
        print("\n=== About Ad Rewards ===")
        print("The ad rewards system allows you to earn special bonuses by:")
        print("1. Watching ads (simulated in this version)")
        print("2. Redeeming special codes you may receive")
        
        print("\nPossible rewards include:")
        
        # Display information about rewards
        for reward_id, reward_data in self.ad_rewards_system.rewards.items():
            print(f"\n• {reward_data['name']}")
            print(f"  {reward_data['description']}")
        
        input("\nPress Enter to continue...")
    
    def apply_ad_reward_effects(self):
        """Apply the effects of active ad rewards."""
        # Get the multiplier for cash income
        cash_multiplier = self.ad_rewards_system.update_turn(self.player)
        return cash_multiplier


if __name__ == "__main__":
    game = MultiVerseTycoon()
    game.start_game()
