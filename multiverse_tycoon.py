#!/usr/bin/env python3

import json
import random
import time
import os
import sys
from currency import CurrencyExchange, QuantumBusinesses, QuantumEvents
from heists import HeistSystem
from minigames import MiniGameSystem
from research import ResearchSystem
from achievements import AchievementSystem
from quests import QuestSystem


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
            "player_level": 1,  # Player's current level
            "experience": 0,  # Experience points
            "unlocked_universes": ["blade_runner"],  # List of unlocked universe IDs
            "completed_research": [],  # List of completed research technologies
            "current_research": {},  # Dictionary of technologies currently being researched
            "unlocked_features": {  # Features that have been unlocked by the player
                "universe_travel": False,  # Ability to travel between universes
                "currency_exchange": False,  # Ability to exchange currencies
                "heist_operations": False,  # Ability to perform heists
                "specialists": False,  # Ability to recruit specialists
                "special_items": False,  # Ability to purchase special items
                "mini_games": False,  # Ability to play mini-games
                "research": False  # Ability to research new technologies
            }
        }

        # Universe data includes level requirements for unlocking
        self.universes = {
            # Default starting universe
            "blade_runner": {
                "name": "Blade Runner",
                "description": "A dystopian future where AI businesses thrive but are highly regulated.",
                "currency": "Credits",
                "risk_factor": 75,
                "level_required": 1,  # Available from the start
                "economic_traits": ["High-tech", "Unstable Politics", "AI-driven"],
                "businesses": {
                    "replicant_manufacturing": {
                        "name": "Replicant Manufacturing",
                        "cost": 10000,
                        "income_per_turn": 2500,
                        "risk_increase": 10,
                        "description": "Create synthetic humans for dangerous work."
                    },
                    "memory_implants": {
                        "name": "Memory Implants",
                        "cost": 7500,
                        "income_per_turn": 1800,
                        "risk_increase": 5,
                        "description": "Design and sell artificial memories for replicants."
                    },
                    "surveillance_tech": {
                        "name": "Surveillance Tech",
                        "cost": 5000,
                        "income_per_turn": 1200,
                        "risk_increase": 3,
                        "description": "Develop technology to track replicants and citizens."
                    }
                },
                "events": [{
                    "name": "Replicant Uprising",
                    "description": "Your replicants are rebelling against poor working conditions!",
                    "effect": {
                        "cash": -3000,
                        "danger": 20,
                        "reputation": -15
                    }
                }, {
                    "name": "Blade Runner Investigation",
                    "description": "Your business is being investigated by a Blade Runner.",
                    "effect": {
                        "cash": -1000,
                        "danger": 15,
                        "reputation": -5
                    }
                }, {
                    "name": "Off-world Expansion",
                    "description": "Opportunity to expand your business to off-world colonies.",
                    "effect": {
                        "cash": 5000,
                        "danger": 5,
                        "reputation": 10
                    }
                }, {
                    "name": "Corporate Favor",
                    "description": "A Tyrell Corporation executive offers you a partnership.",
                    "effect": {
                        "cash": 2000,
                        "danger": -10,
                        "reputation": 15
                    }
                }, {
                    "name": "Blackout",
                    "description": "Digital systems fail during a city-wide blackout.",
                    "effect": {
                        "cash": -2000,
                        "danger": 0,
                        "reputation": 0
                    }
                }]
            },
            "gta_v": {
                "name": "GTA V",
                "description": "A world of organized crime, corruption, and fast money.",
                "currency": "Dollars",
                "risk_factor": 60,
                "level_required": 2,  # Unlocked at level 2
                "economic_traits": ["Corruption", "Criminal Opportunities", "Fast Money"],
                "businesses": {
                    "nightclub": {
                        "name": "Nightclub",
                        "cost": 15000,
                        "income_per_turn": 3500,
                        "risk_increase": 8,
                        "description": "Run a popular nightclub as a front for criminal activities."
                    },
                    "auto_shop": {
                        "name": "Auto Shop",
                        "cost": 12000,
                        "income_per_turn": 2800,
                        "risk_increase": 5,
                        "description": "Modify stolen cars and sell them for profit."
                    },
                    "weapon_dealing": {
                        "name": "Weapon Dealing",
                        "cost": 20000,
                        "income_per_turn": 4500,
                        "risk_increase": 15,
                        "description": "Trade illegal weapons on the black market."
                    }
                },
                "events": [{
                    "name": "Police Raid",
                    "description": "The LSPD is raiding one of your businesses!",
                    "effect": {
                        "cash": -5000,
                        "danger": 25,
                        "reputation": -10
                    }
                }, {
                    "name": "Gang War",
                    "description": "Local gangs are fighting in your territory.",
                    "effect": {
                        "cash": -3000,
                        "danger": 15,
                        "reputation": 5
                    }
                }, {
                    "name": "Heist Opportunity",
                    "description": "You've been invited to participate in a major bank heist.",
                    "effect": {
                        "cash": 10000,
                        "danger": 20,
                        "reputation": 10
                    }
                }, {
                    "name": "Corrupt Official",
                    "description": "A police officer offers protection for your businesses.",
                    "effect": {
                        "cash": -2000,
                        "danger": -15,
                        "reputation": 0
                    }
                }, {
                    "name": "Celebrity Client",
                    "description": "A famous celebrity becomes a regular at your establishment.",
                    "effect": {
                        "cash": 3000,
                        "danger": 0,
                        "reputation": 15
                    }
                }]
            },
            "mcu": {
                "name": "MCU",
                "description": "A world of superheroes, advanced technology, and constant innovation.",
                "currency": "USD",
                "risk_factor": 50,
                "level_required": 3,  # Unlocked at level 3
                "economic_traits": ["High Innovation", "Superhero Interference", "Tech-driven"],
                "businesses": {
                    "stark_tech_competitor": {
                        "name": "Stark Tech Competitor",
                        "cost": 25000,
                        "income_per_turn": 5000,
                        "risk_increase": 7,
                        "description": "Develop advanced technology to compete with Stark Industries."
                    },
                    "superhero_insurance": {
                        "name": "Superhero Insurance",
                        "cost": 15000,
                        "income_per_turn": 3000,
                        "risk_increase": 3,
                        "description": "Provide insurance against damage caused by superhero battles."
                    },
                    "shield_supplies": {
                        "name": "S.H.I.E.L.D. Supplies",
                        "cost": 20000,
                        "income_per_turn": 4000,
                        "risk_increase": 5,
                        "description": "Supply equipment and technology to S.H.I.E.L.D. agents."
                    }
                },
                "events": [{
                    "name": "Avengers Battle",
                    "description": "A battle between The Avengers and a villain destroyed part of your business!",
                    "effect": {
                        "cash": -6000,
                        "danger": 10,
                        "reputation": 0
                    }
                }, {
                    "name": "Stark Partnership",
                    "description": "Tony Stark offers to collaborate on a new technology.",
                    "effect": {
                        "cash": 8000,
                        "danger": -5,
                        "reputation": 20
                    }
                }, {
                    "name": "Alien Artifact",
                    "description": "You discovered an alien artifact with valuable technology.",
                    "effect": {
                        "cash": 5000,
                        "danger": 15,
                        "reputation": 5
                    }
                }, {
                    "name": "Government Scrutiny",
                    "description": "Your business is being investigated for potential Hydra connections.",
                    "effect": {
                        "cash": -2000,
                        "danger": 10,
                        "reputation": -10
                    }
                }, {
                    "name": "Multiverse Entrepreneur Award",
                    "description": "Your innovative business model wins a prestigious award.",
                    "effect": {
                        "cash": 3000,
                        "danger": 0,
                        "reputation": 15
                    }
                }]
            },
            # New worlds as requested
            "doraemon": {
                "name": "Doraemon",
                "description": "A world where futuristic gadgets from the 22nd century help solve everyday problems.",
                "currency": "Yen",
                "risk_factor": 40,
                "level_required": 4,  # Unlocked at level 4
                "economic_traits": ["Future Technology", "Kid-Friendly", "Gadget-Based"],
                "businesses": {
                    "gadget_shop": {
                        "name": "Future Gadget Shop",
                        "cost": 20000,
                        "income_per_turn": 4000,
                        "risk_increase": 5,
                        "description": "Sell unique gadgets from the 22nd century to help with daily life."
                    },
                    "anywhere_door_transport": {
                        "name": "Anywhere Door Transport",
                        "cost": 30000,
                        "income_per_turn": 6000,
                        "risk_increase": 10,
                        "description": "Provide instantaneous transportation services to any location."
                    },
                    "time_machine_tours": {
                        "name": "Time Machine Tours",
                        "cost": 40000,
                        "income_per_turn": 8000,
                        "risk_increase": 15,
                        "description": "Offer guided historical tours through different time periods."
                    }
                },
                "events": [{
                    "name": "Gadget Malfunction",
                    "description": "One of your futuristic gadgets has gone haywire!",
                    "effect": {
                        "cash": -4000,
                        "danger": 15,
                        "reputation": -5
                    }
                }, {
                    "name": "Rival Inventor",
                    "description": "A jealous inventor tries to sabotage your technology.",
                    "effect": {
                        "cash": -3000,
                        "danger": 10,
                        "reputation": -10
                    }
                }, {
                    "name": "Temporal Agency Inspection",
                    "description": "The Time Patrol is inspecting your time machine tours for regulations compliance.",
                    "effect": {
                        "cash": -2000,
                        "danger": 5,
                        "reputation": 0
                    }
                }, {
                    "name": "Future Tech Award",
                    "description": "Your gadget innovations win a prestigious award from the 22nd century.",
                    "effect": {
                        "cash": 5000,
                        "danger": 0,
                        "reputation": 20
                    }
                }, {
                    "name": "Special Customer",
                    "description": "A mysterious blue cat robot becomes a loyal customer and promoter.",
                    "effect": {
                        "cash": 3000,
                        "danger": -10,
                        "reputation": 15
                    }
                }]
            },
            "harry_potter": {
                "name": "Wizarding World",
                "description": "A hidden magical society with its own economy, government, and educational system.",
                "currency": "Galleons",
                "risk_factor": 65,
                "level_required": 5,  # Unlocked at level 5
                "economic_traits": ["Magic-Powered", "Secretive", "Traditional"],
                "businesses": {
                    "wand_shop": {
                        "name": "Wand Crafting",
                        "cost": 25000,
                        "income_per_turn": 5500,
                        "risk_increase": 8,
                        "description": "Craft and sell magical wands to witches and wizards."
                    },
                    "potion_brewery": {
                        "name": "Potion Brewery",
                        "cost": 20000,
                        "income_per_turn": 4500,
                        "risk_increase": 12,
                        "description": "Brew and sell various magical potions for any need."
                    },
                    "magical_creatures_sanctuary": {
                        "name": "Magical Creatures Sanctuary",
                        "cost": 35000,
                        "income_per_turn": 7000,
                        "risk_increase": 15,
                        "description": "Care for and study magical creatures while offering tours to visitors."
                    }
                },
                "events": [{
                    "name": "Ministry Raid",
                    "description": "The Ministry of Magic is investigating your business for illegal magical artifacts.",
                    "effect": {
                        "cash": -5000,
                        "danger": 20,
                        "reputation": -10
                    }
                }, {
                    "name": "Dark Wizard Threat",
                    "description": "Dark wizards are threatening your business unless you pay protection money.",
                    "effect": {
                        "cash": -4000,
                        "danger": 15,
                        "reputation": -5
                    }
                }, {
                    "name": "Magical Mishap",
                    "description": "A spell gone wrong has caused chaos in your establishment.",
                    "effect": {
                        "cash": -3000,
                        "danger": 10,
                        "reputation": 0
                    }
                }, {
                    "name": "Famous Wizard Visit",
                    "description": "A famous wizard publicly endorses your business.",
                    "effect": {
                        "cash": 6000,
                        "danger": 0,
                        "reputation": 20
                    }
                }, {
                    "name": "Magical Innovation",
                    "description": "You've discovered a new magical process that revolutionizes your industry.",
                    "effect": {
                        "cash": 8000,
                        "danger": 5,
                        "reputation": 15
                    }
                }]
            },
            "dark_netflix": {
                "name": "Dark (Netflix)",
                "description": "A world where time travel connects multiple generations across different eras in a complex web of cause and effect.",
                "currency": "Euros",
                "risk_factor": 80,
                "level_required": 6,  # Unlocked at level 6
                "economic_traits": ["Time-Influenced", "Paradox-Prone", "Mysterious"],
                "businesses": {
                    "temporal_consultancy": {
                        "name": "Temporal Consultancy",
                        "cost": 40000,
                        "income_per_turn": 8000,
                        "risk_increase": 20,
                        "description": "Provide strategic advice to clients across different time periods."
                    },
                    "nuclear_power": {
                        "name": "Nuclear Power Research",
                        "cost": 50000,
                        "income_per_turn": 10000,
                        "risk_increase": 25,
                        "description": "Research advanced nuclear technology with help from different time periods."
                    },
                    "cave_expeditions": {
                        "name": "Winden Cave Tours",
                        "cost": 30000,
                        "income_per_turn": 6000,
                        "risk_increase": 15,
                        "description": "Guide special tours through the mysterious cave system (avoiding the time portal)."
                    }
                },
                "events": [{
                    "name": "Temporal Paradox",
                    "description": "A paradox has occurred affecting your business across multiple time periods!",
                    "effect": {
                        "cash": -8000,
                        "danger": 30,
                        "reputation": -15
                    }
                }, {
                    "name": "Prophet's Warning",
                    "description": "A mysterious old man warns you of impending apocalypse.",
                    "effect": {
                        "cash": -3000,
                        "danger": 20,
                        "reputation": -5
                    }
                }, {
                    "name": "Time Travel Incident",
                    "description": "An employee accidentally traveled through time and altered something.",
                    "effect": {
                        "cash": -5000,
                        "danger": 25,
                        "reputation": -10
                    }
                }, {
                    "name": "Future Investment",
                    "description": "Someone from the future has invested heavily in your business.",
                    "effect": {
                        "cash": 10000,
                        "danger": 10,
                        "reputation": 10
                    }
                }, {
                    "name": "Temporal Loop Advantage",
                    "description": "You've managed to exploit knowledge from a time loop for business gain.",
                    "effect": {
                        "cash": 12000,
                        "danger": 15,
                        "reputation": 5
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

        self.DETECTION_RISK_THRESHOLD = 100  # Maximum allowed detection risk
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
        
        # Initialize research system
        self.research_system = ResearchSystem()
        
        # Initialize achievement system
        self.achievement_system = AchievementSystem()
        
        # Initialize quest system
        self.quest_system = QuestSystem()

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
                "danger": 0,  # This is now detection_risk but keeping variable name for compatibility
                "reputation": 0,
                "businesses": [],
                "employees": []
            }

        # Start in the Blade Runner universe
        self.player["current_universe"] = "blade_runner"

        # Core narrative introduction
        self.clear_screen()
        print("\n=== THE QUANTUM CORPORATION ===\n")
        
        self.slow_print("CONFIDENTIAL TRANSMISSION")
        self.slow_print("FROM: Dr. Eleanor Quantum, Founder & CEO")
        self.slow_print(f"TO: {player_name}, Special Operative\n")
        
        self.slow_print("Welcome to the Quantum Corporation's Multiverse Division.")
        self.slow_print("As you know, our discovery of the Quantum Nexus has allowed us to access")
        self.slow_print("multiple parallel realities, each with their own unique characteristics.")
        
        self.slow_print("\nYour mission is of the utmost importance:")
        self.slow_print("1. Establish business operations across these universes")
        self.slow_print("2. Gather Quantum Credits - the only currency that maintains value across all realities")
        self.slow_print("3. Build a network that will allow us to stabilize the fracturing multiverse")
        
        self.slow_print("\nOur scientists have detected dangerous instabilities in the multiverse fabric.")
        self.slow_print("These interdimensional fluctuations threaten to collapse all realities into one.")
        self.slow_print("Only by establishing a network of businesses across multiple universes")
        self.slow_print("can we generate enough Quantum Credits to power our stabilization technology.")
        
        self.slow_print("\nYou'll begin in the Blade Runner universe - a dystopian future where")
        self.slow_print("AI technology thrives but is highly regulated. As you progress,")
        self.slow_print("you'll gain access to other universes, each with their own unique")
        self.slow_print("challenges and opportunities.")
        
        self.slow_print("\nBe cautious - if your activities draw too much attention in any universe,")
        self.slow_print("local authorities will detect your interdimensional nature,")
        self.slow_print("forcing a permanent retreat from that reality.")
        
        self.slow_print("\nThe fate of all realities rests in your hands. Good luck, Tycoon.")

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
        
        # Quantum Corporation mission header
        print("\n=== QUANTUM CORPORATION ===")
        print("Multiverse Stabilization Initiative")
        print(f"Operative: {self.player['name']}")
        print(f"Field Agent Level: {self.player['player_level']}")
        print(f"Experience: {self.player['experience']} / {self.player['player_level'] * 1000} XP")
        
        # Universe information
        print(f"\n=== {universe['name']} - Reality Designation ===")
        print(f"Description: {universe['description']}")
        print(f"Local Currency: {universe['currency']}")
        print(f"Instability Index: {universe['risk_factor']}/100")
        print(f"Economic Factors: {', '.join(universe['economic_traits'])}")

        # Mission status
        print("\n=== Operation Status ===")
        print(f"Local Resources: {player_universe_data['cash']} {universe['currency']}")
        print(f"Quantum Credits: {self.player['quantum_credits']} Q¢")
        print(f"Detection Risk: {player_universe_data['danger']}/100")
        print(f"Local Influence: {player_universe_data['reputation']}")
        
        # Network statistics
        print(f"\nNetwork Status: {sum(len(universe_data['businesses']) for universe_data in self.player['universes'].values())} business nodes")
        print(f"Network Spread: {sum(1 for universe_data in self.player['universes'].values() if len(universe_data['businesses']) > 0)}/{len(self.player['unlocked_universes'])} universes")
        print(f"Mission Cycle: {self.player['turn']}")
        
        # Research status
        if self.player['unlocked_features']['research']:
            # Check current research
            current_research = self.research_system.get_research_progress(self.player)
            if current_research:
                print("\n=== Research Division ===")
                for tech_id, progress in current_research.items():
                    print(f"Researching: {progress['name']} - {progress['progress_percent']}% complete")
                    print(f"Turns remaining: {progress['turns_remaining']}")
            
            # Show completed research count
            completed_count = len(self.player.get('completed_research', []))
            if completed_count > 0:
                print(f"Completed technologies: {completed_count}")
        
        # Display recent achievements (if any)
        unlocked_achievements = self.achievement_system.get_unlocked_achievements()
        recent_achievements = [a for a in unlocked_achievements if a.unlock_time and self.player["turn"] - a.unlock_time <= 3]
        if recent_achievements:
            print("\n🏆 Recent Achievements:")
            for achievement in recent_achievements[:3]:  # Show max 3 recent achievements
                print(f"- {achievement.name}: {achievement.description}")
        
        # Display current quest objectives (if any)
        quest_suggestions = self.quest_system.get_quest_suggestions(self.player)
        if quest_suggestions:
            print("\n📋 Current Quests:")
            for suggestion in quest_suggestions[:2]:  # Show max 2 active quest objectives
                print(f"- {suggestion['quest_name']}: {suggestion['objective']} ({suggestion['progress']})")
        
        # Alert if detection risk is getting high
        if player_universe_data['danger'] >= 80:
            print("\n⚠️ WARNING: Detection risk critical! Consider reducing risk or relocating.")
        elif player_universe_data['danger'] >= 60:
            print("\n⚠️ CAUTION: Detection risk elevated. Monitor situation closely.")

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
            print("4. Reduce Detection Risk")
            
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
                
            if self.player["unlocked_features"]["research"]:
                print(f"{option_index}. Research new technologies")
                options.append("research")
                option_index += 1
                
            # Achievements are always available
            print(f"{option_index}. View Achievements")
            options.append("achievements")
            option_index += 1
            
            # Quests are always available
            print(f"{option_index}. View Quests")
            options.append("quests")
            option_index += 1
                
            # Ad rewards option removed
            
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
                self.reduce_detection_risk()
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
                        elif option == "research":
                            self.research_menu()
                        elif option == "achievements":
                            self.achievements_menu()
                        elif option == "quests":
                            self.quests_menu()
                        # Ad rewards option removed
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
            if player_universe_data["danger"] >= self.DETECTION_RISK_THRESHOLD:
                self.player["game_over"] = True
                self.player[
                    "end_reason"] = f"Your detection risk reached {self.DETECTION_RISK_THRESHOLD} in the {universe['name']} universe!"

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
                    "risk_increase"]  # Adding to detection risk

                # Update achievement stats
                self.achievement_system.update_stats("businesses_started")
                self.achievement_system.update_stats(f"businesses_in_{universe_id}")
                
                # Check for total businesses achievement threshold
                total_businesses = 0
                for uni_id in self.player["universes"]:
                    total_businesses += len(self.player["universes"][uni_id]["businesses"])
                self.achievement_system.stats["total_businesses"] = total_businesses
                
                # Check for new achievements
                newly_unlocked = self.achievement_system.check_achievements(self.player)
                if newly_unlocked:
                    print("\n🏆 ACHIEVEMENTS UNLOCKED:")
                    for achievement in newly_unlocked:
                        reward_text = []
                        if achievement.reward_cash > 0:
                            reward_text.append(f"{achievement.reward_cash} {universe['currency']}")
                            # Add the cash reward to player's account
                            player_universe_data["cash"] += achievement.reward_cash
                        if achievement.reward_quantum > 0:
                            reward_text.append(f"{achievement.reward_quantum} Quantum Credits")
                            # Add the quantum reward
                            self.player["quantum_credits"] += achievement.reward_quantum
                        reward_str = " and ".join(reward_text)
                        
                        print(f"- {achievement.name}: {achievement.description}")
                        if reward_str:
                            print(f"  Reward: {reward_str}")
                
                # Check for quest progress - business started
                completed_quests = self.quest_system.check_and_update_quests(
                    self.player, "business_started", universe_id=universe_id)
                
                # Also track specific business ownership for quests
                self.quest_system.check_and_update_quests(
                    self.player, "specific_business_owned", value=selected_business_id)
                
                # Award rewards for any completed quests
                if completed_quests:
                    print("\n📋 QUESTS COMPLETED:")
                    
                    for quest_id in completed_quests:
                        quest = self.quest_system.quests[quest_id]
                        print(f"\n✓ {quest.name}")
                        print(f"  {quest.description}")
                        
                        # Apply rewards
                        if quest.rewards["cash"] > 0:
                            player_universe_data["cash"] += quest.rewards["cash"]
                            print(f"  + {quest.rewards['cash']} {universe['currency']}")
                        
                        if quest.rewards["quantum"] > 0:
                            self.player["quantum_credits"] += quest.rewards["quantum"]
                            print(f"  + {quest.rewards['quantum']} Quantum Credits")
                        
                        if quest.rewards["xp"] > 0:
                            self.player["experience"] += quest.rewards["xp"]
                            print(f"  + {quest.rewards['xp']} XP")

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
                
                # Update achievement stats
                self.achievement_system.update_stats("employees_hired")
                
                # Update quest progress - employee hired
                completed_quests = self.quest_system.check_and_update_quests(
                    self.player, "employee_hired", universe_id=universe_id)
                
                # Award rewards for any completed quests
                if completed_quests:
                    print("\n📋 QUESTS COMPLETED:")
                    
                    for quest_id in completed_quests:
                        quest = self.quest_system.quests[quest_id]
                        print(f"\n✓ {quest.name}")
                        print(f"  {quest.description}")
                        
                        # Apply rewards
                        if quest.rewards["cash"] > 0:
                            player_universe_data["cash"] += quest.rewards["cash"]
                            print(f"  + {quest.rewards['cash']} {universe['currency']}")
                        
                        if quest.rewards["quantum"] > 0:
                            self.player["quantum_credits"] += quest.rewards["quantum"]
                            print(f"  + {quest.rewards['quantum']} Quantum Credits")
                        
                        if quest.rewards["xp"] > 0:
                            self.player["experience"] += quest.rewards["xp"]
                            print(f"  + {quest.rewards['xp']} XP")

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

    def reduce_detection_risk(self):
        """Reduce the detection risk through various countermeasures."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]

        self.clear_screen()
        print(f"\n=== Reduce Detection Risk in {universe['name']} ===")
        print(
            f"Available Cash: {player_universe_data['cash']} {universe['currency']}"
        )
        print(f"Current Detection Risk: {player_universe_data['danger']}/100")

        # Calculate countermeasure options based on universe and current risk
        small_cost = 1000
        medium_cost = 3000
        large_cost = 7000

        small_reduction = 5
        medium_reduction = 15
        large_reduction = 35

        print(
            f"\n1. Basic Countermeasures: {small_cost} {universe['currency']} (-{small_reduction} risk)"
        )
        print(
            f"2. Advanced Protocols: {medium_cost} {universe['currency']} (-{medium_reduction} risk)"
        )
        print(
            f"3. Elite Security System: {large_cost} {universe['currency']} (-{large_reduction} risk)"
        )
        print("4. Cancel")

        choice = input("\nChoose a countermeasure option: ")

        if choice == "1":
            if player_universe_data["cash"] < small_cost:
                print(
                    f"\nNot enough cash! You need {small_cost} {universe['currency']}."
                )
            else:
                player_universe_data["cash"] -= small_cost
                player_universe_data["danger"] = max(
                    0, player_universe_data["danger"] - small_reduction)
                print(
                    f"\nYou implemented basic security measures. Detection risk reduced by {small_reduction}."
                )
        elif choice == "2":
            if player_universe_data["cash"] < medium_cost:
                print(
                    f"\nNot enough cash! You need {medium_cost} {universe['currency']}."
                )
            else:
                player_universe_data["cash"] -= medium_cost
                player_universe_data["danger"] = max(
                    0, player_universe_data["danger"] - medium_reduction)
                print(
                    f"\nYou deployed advanced security protocols. Detection risk reduced by {medium_reduction}."
                )
        elif choice == "3":
            if player_universe_data["cash"] < large_cost:
                print(
                    f"\nNot enough cash! You need {large_cost} {universe['currency']}."
                )
            else:
                player_universe_data["cash"] -= large_cost
                player_universe_data["danger"] = max(
                    0, player_universe_data["danger"] - large_reduction)
                print(
                    f"\nYou installed an elite security system. Detection risk reduced by {large_reduction}."
                )
        elif choice == "4":
            return
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(0.75)  # Reduced delay for faster gameplay
            self.reduce_detection_risk()
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
        available_universes = []
        
        # Only show unlocked universes
        for universe_id, universe in self.universes.items():
            if universe_id != current_universe_id and universe_id in self.player["unlocked_universes"]:
                available_universes.append((universe_id, universe))
        
        if not available_universes:
            print("No other universes available yet! Continue playing to unlock new worlds.")
            input("\nPress Enter to continue...")
            return
            
        for i, (universe_id, universe) in enumerate(available_universes, 1):
            player_universe_data = self.player["universes"][universe_id]
            print(f"{i}. {universe['name']}")
            print(f"   Cash: {player_universe_data['cash']} {universe['currency']}")
            print(f"   Detection Risk: {player_universe_data['danger']}/100")
            print(f"   Businesses: {len(player_universe_data['businesses'])}")
            print(f"   Employees: {len(player_universe_data['employees'])}\n")

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
                
                # Update achievement stats for universe jumps
                self.achievement_system.update_stats("universe_jumps")
                self.achievement_system.stats["universe_visited"][target_universe_id] = True
                
                # Count how many different universes have been visited
                universes_visited = sum(1 for uni_id, visited in 
                                      self.achievement_system.stats.get("universe_visited", {}).items() 
                                      if visited)
                self.achievement_system.stats["different_universes_visited"] = universes_visited
                
                # Check for achievements
                newly_unlocked = self.achievement_system.check_achievements(self.player)
                if newly_unlocked:
                    print("\n🏆 ACHIEVEMENTS UNLOCKED:")
                    for achievement in newly_unlocked:
                        reward_text = []
                        target_universe = self.universes[target_universe_id]
                        if achievement.reward_cash > 0:
                            reward_text.append(f"{achievement.reward_cash} {target_universe['currency']}")
                            # Add the cash reward to player's account
                            self.player["universes"][target_universe_id]["cash"] += achievement.reward_cash
                        if achievement.reward_quantum > 0:
                            reward_text.append(f"{achievement.reward_quantum} Quantum Credits")
                            # Add the quantum reward
                            self.player["quantum_credits"] += achievement.reward_quantum
                        reward_str = " and ".join(reward_text)
                        
                        print(f"- {achievement.name}: {achievement.description}")
                        if reward_str:
                            print(f"  Reward: {reward_str}")
                
                # Save a reference to the target universe for later use
                target_universe = self.universes[target_universe_id]
                
                # Update quest progress - universe jump
                completed_quests = self.quest_system.check_and_update_quests(
                    self.player, "universe_jump", value=1, universe_id=target_universe_id)
                
                # Also track specific universe visits for quests - we use None for the default value
                # to avoid type issues
                self.quest_system.check_and_update_quests(
                    self.player, "specific_universe_visited", value=target_universe_id, universe_id=None)
                
                # Award rewards for any completed quests
                if completed_quests:
                    print("\n📋 QUESTS COMPLETED:")
                    
                    for quest_id in completed_quests:
                        quest = self.quest_system.quests[quest_id]
                        print(f"\n✓ {quest.name}")
                        print(f"  {quest.description}")
                        
                        # Apply rewards
                        if quest.rewards["cash"] > 0:
                            self.player["universes"][target_universe_id]["cash"] += quest.rewards["cash"]
                            print(f"  + {quest.rewards['cash']} {target_universe['currency']}")
                        
                        if quest.rewards["quantum"] > 0:
                            self.player["quantum_credits"] += quest.rewards["quantum"]
                            print(f"  + {quest.rewards['quantum']} Quantum Credits")
                        
                        if quest.rewards["xp"] > 0:
                            self.player["experience"] += quest.rewards["xp"]
                            print(f"  + {quest.rewards['xp']} XP")

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

        # Calculate probability based on detection risk level
        player_universe_data = self.player["universes"][universe_id]
        detection_risk = player_universe_data["danger"]
        # Increase probability based on detection risk (up to +20%)
        adjusted_probability = EVENT_PROBABILITY + (detection_risk / 500)

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
        player_universe_data["danger"] += event["effect"]["danger"]  # danger is detection_risk
        player_universe_data["reputation"] += event["effect"]["reputation"]

        # Ensure detection risk doesn't go below 0
        player_universe_data["danger"] = max(0, player_universe_data["danger"])

        print("\nEffect:")
        if event["effect"]["cash"] > 0:
            print(f"• Cash: +{event['effect']['cash']} {universe['currency']}")
        else:
            print(f"• Cash: {event['effect']['cash']} {universe['currency']}")

        if event["effect"]["danger"] > 0:
            print(f"• Detection Risk: +{event['effect']['danger']}")
        else:
            print(f"• Detection Risk: {event['effect']['danger']}")

        if event["effect"]["reputation"] > 0:
            print(f"• Reputation: +{event['effect']['reputation']}")
        else:
            print(f"• Reputation: {event['effect']['reputation']}")

        input("\nPress Enter to continue...")

    def research_menu(self):
        """Display the research menu and handle research operations."""
        while True:
            self.clear_screen()
            print("=== Quantum Research Division ===")
            print("Develop advanced technologies to enhance your interdimensional operations.\n")
            
            print(f"Available Quantum Credits: {self.player['quantum_credits']}")
            print()
            
            # Check current research
            current_research = self.research_system.get_research_progress(self.player)
            if current_research:
                print("=== Current Research Projects ===")
                for tech_id, progress in current_research.items():
                    print(f"{progress['name']} - {progress['progress_percent']}% complete")
                    print(f"Turns remaining: {progress['turns_remaining']}/{progress['total_turns']}")
                print()
            
            # Get available technologies
            available_techs = self.research_system.get_available_technologies(self.player)
            
            if not available_techs:
                print("No technologies available for research at this time.")
                print("Increase your operative level or complete current research projects to unlock more options.")
                input("\nPress Enter to return to the main menu...")
                return
            
            # Print menu options
            print("=== Available Technologies ===")
            options = []
            for category, technologies in available_techs.items():
                print(f"\n--- {category.replace('_', ' ').title()} Technologies ---")
                for tech_id, tech in technologies.items():
                    options.append((category, tech_id))
                    print(f"{len(options)}. {tech['name']} - {tech['cost']['quantum_credits']} QC, {tech['research_turns']} turns")
                    print(f"   {tech['description']}")
            
            print("\n0. Return to Main Menu")
            
            # Get user choice
            try:
                choice = input("\nSelect a technology to research: ")
                if choice == "0":
                    return
                
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(options):
                    category, tech_id = options[choice_index]
                    
                    # Confirm research
                    tech = available_techs[category][tech_id]
                    print(f"\nYou are about to research: {tech['name']}")
                    print(f"Cost: {tech['cost']['quantum_credits']} Quantum Credits")
                    print(f"Duration: {tech['research_turns']} turns")
                    print(f"Effect: {tech['description']}")
                    
                    confirm = input("\nConfirm research? (y/n): ")
                    if confirm.lower() == "y":
                        success, message = self.research_system.start_research(self.player, tech_id, category)
                        print(f"\n{message}")
                        input("\nPress Enter to continue...")
                        
                        if success:
                            return
                
                else:
                    print("\nInvalid choice. Please try again.")
                    time.sleep(0.75)
            
            except ValueError:
                print("\nInvalid input. Please enter a number.")
                time.sleep(0.75)
    
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
        
        # Apply research effects
        research_effects = self.research_system.apply_research_effects(self.player, universe_id)
        if research_effects["business_income_multiplier"] > 1.0:
            research_bonus = total_income * (research_effects["business_income_multiplier"] - 1.0)
            total_income += research_bonus
            
        # Generate quantum income from research
        if research_effects["quantum_income"] > 0:
            self.player["quantum_credits"] += research_effects["quantum_income"]
        
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

    def apply_detection_risk_reductions(self):
        """Apply detection risk reductions from employees."""
        universe_id = self.player["current_universe"]
        player_universe_data = self.player["universes"][universe_id]

        total_reduction = 0

        # Calculate total detection risk reduction
        for employee in player_universe_data["employees"]:
            emp_type = self.employee_types[employee["type"]]
            total_reduction += emp_type["risk_reduction"]
        
        # Apply research effects for detection risk reduction
        research_effects = self.research_system.apply_research_effects(self.player, universe_id)
        if research_effects["detection_risk_reduction"] > 0:
            total_reduction += research_effects["detection_risk_reduction"]

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
            
        # Unlock research at turn 8
        if self.player["turn"] >= 8 and not self.player["unlocked_features"]["research"]:
            self.player["unlocked_features"]["research"] = True
            print("\n🔓 New feature unlocked: Quantum Research Division!")
            print("Research new technologies to enhance your interdimensional operations.")
            print("Advanced technologies can help stabilize the multiverse faster!")
            input("\nPress Enter to continue...")
            
        # Unlock heist operations at turn 20
        if self.player["turn"] >= 20 and not self.player["unlocked_features"]["heist_operations"]:
            self.player["unlocked_features"]["heist_operations"] = True
            print("\n🔓 New feature unlocked: Heist Operations!")
            print("Plan and execute heists for big rewards!")
            input("\nPress Enter to continue...")
            
        # Check for level ups and universe unlocks
        self.check_level_up()
            
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

    def check_level_up(self):
        """Check if player should level up and unlock new universes."""
        # Calculate XP threshold for next level (increases with each level)
        xp_threshold = self.player["player_level"] * 1000
        
        # Check if player has enough XP to level up
        if self.player["experience"] >= xp_threshold:
            # Level up
            old_level = self.player["player_level"]
            self.player["player_level"] += 1
            self.player["experience"] -= xp_threshold  # Reset XP counter (keeping extra XP)
            
            # Notify player
            self.clear_screen()
            print("\n🌟 LEVEL UP! 🌟")
            print(f"You've reached level {self.player['player_level']}!")
            
            # Get research effects
            research_effects = self.research_system.apply_research_effects(self.player, self.player["current_universe"])
            universe_level_reduction = research_effects["universe_level_reduction"]
            ignore_requirements = research_effects["ignore_universe_requirements"]
            
            # Check for newly unlocked universes
            newly_unlocked = []
            for universe_id, universe in self.universes.items():
                # Apply research effects to level requirements
                effective_level_required = universe["level_required"] - universe_level_reduction
                
                if ((universe["level_required"] <= self.player["player_level"] or 
                     effective_level_required <= self.player["player_level"] or
                     ignore_requirements) and 
                    universe_id not in self.player["unlocked_universes"]):
                    # Unlock this universe
                    self.player["unlocked_universes"].append(universe_id)
                    
                    # Initialize player state for this universe
                    if universe_id not in self.player["universes"]:
                        self.player["universes"][universe_id] = {
                            "cash": self.starting_cash,
                            "danger": 0,
                            "reputation": 0,
                            "businesses": [],
                            "employees": []
                        }
                    
                    newly_unlocked.append(universe)
            
            # Notify about new universes
            if newly_unlocked:
                print("\n🌌 NEW UNIVERSES UNLOCKED! 🌌")
                for universe in newly_unlocked:
                    print(f"\n• {universe['name']}")
                    print(f"  {universe['description']}")
                
                print("\nYou can now travel to these new universes and build businesses there!")
            
            # Extra rewards for leveling up
            bonus_quantum = self.player["player_level"] * 50
            self.player["quantum_credits"] += bonus_quantum
            print(f"\nBonus reward: {bonus_quantum} Quantum Credits!")
            
            input("\nPress Enter to continue...")
            return True
        
        return False
        
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

        print("\n=== QUANTUM CORPORATION MISSION REPORT ===\n")
        self.slow_print("TRANSMISSION INTERRUPTED")
        self.slow_print(f"Field Operative: {self.player['name']}")
        
        self.slow_print(f"\nMission Status: TERMINATED")
        self.slow_print(f"Reason: {self.player['end_reason']}")
        
        # Narrative based on performance
        self.slow_print("\nDr. Eleanor Quantum's Assessment:")
        
        total_quantum = self.player["quantum_credits"]
        total_businesses_all = sum(len(universe_data['businesses']) for universe_data in self.player["universes"].values())
        universes_with_businesses = sum(1 for universe_data in self.player["universes"].values() if len(universe_data['businesses']) > 0)
        
        if total_quantum > 1000 and total_businesses_all > 10 and universes_with_businesses >= 3:
            self.slow_print("Despite your mission's end, your significant contributions to our")
            self.slow_print("interdimensional network have provided valuable data. The quantum credits")
            self.slow_print("you've accumulated will power our stabilization efforts for some time.")
            self.slow_print("We'll dispatch another operative to continue your work.")
        elif total_quantum > 500 or total_businesses_all > 5:
            self.slow_print("Your efforts showed promise, but ultimately fell short of what we needed.")
            self.slow_print("The multiverse stabilization project will continue with another operative.")
            self.slow_print("We've archived your strategies for future reference.")
        else:
            self.slow_print("Your premature mission failure has set our stabilization efforts back significantly.")
            self.slow_print("The Quantum Corporation will need to reassess our approach to interdimensional")
            self.slow_print("business ventures. We can only hope the multiverse holds together long enough")
            self.slow_print("for us to implement a new strategy.")
        
        # Display final stats
        print("\n=== Mission Statistics ===")
        print(f"Operative: {self.player['name']}")
        print(f"Mission Duration: {self.player['turn']} cycles")
        print(f"Final Level: {self.player['player_level']}")
        print(f"Experience Points: {self.player['experience']}")

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
                    if player_universe_data["danger"] >= self.DETECTION_RISK_THRESHOLD:
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
            if player_universe_data["danger"] >= self.DETECTION_RISK_THRESHOLD:
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

        # Apply detection risk reductions from employees
        risk_reduction = self.apply_detection_risk_reductions()

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
        
        # Award experience points based on actions this turn
        base_xp = 100  # Base XP for completing a turn
        business_xp = len(player_universe_data["businesses"]) * 20  # XP for each business owned
        employee_xp = len(player_universe_data["employees"]) * 15  # XP for each employee
        income_xp = int(income / 1000) * 10  # XP based on income (10 XP per 1000 currency)
        
        total_xp_gained = base_xp + business_xp + employee_xp + income_xp
        self.player["experience"] += total_xp_gained

        # Check for new feature unlocks
        self.check_feature_unlocks()
        
        # Check for newly unlocked achievements
        newly_unlocked = self.achievement_system.check_achievements(self.player)
        if newly_unlocked:
            self.clear_screen()
            print("\n🏆 ACHIEVEMENTS UNLOCKED:")
            for achievement in newly_unlocked:
                reward_text = []
                if achievement.reward_cash > 0:
                    reward_text.append(f"{achievement.reward_cash} cash")
                if achievement.reward_quantum > 0:
                    reward_text.append(f"{achievement.reward_quantum} Quantum Credits")
                reward_str = " and ".join(reward_text)
                
                print(f"- {achievement.name}: {achievement.description}")
                if reward_str:
                    print(f"  Reward: {reward_str}")
            input("\nPress Enter to continue...")
        
        # Update quest progress for turn completion
        completed_quests = self.quest_system.check_and_update_quests(
            self.player, "turn_completed")
        
        # Award rewards for any completed quests
        if completed_quests:
            self.clear_screen()
            print("\n📋 QUESTS COMPLETED:")
            
            for quest_id in completed_quests:
                quest = self.quest_system.quests[quest_id]
                print(f"\n✓ {quest.name}")
                print(f"  {quest.description}")
                
                # Apply rewards
                if quest.rewards["cash"] > 0:
                    self.player["universes"][universe_id]["cash"] += quest.rewards["cash"]
                    print(f"  + {quest.rewards['cash']} {universe['currency']}")
                
                if quest.rewards["quantum"] > 0:
                    self.player["quantum_credits"] += quest.rewards["quantum"]
                    print(f"  + {quest.rewards['quantum']} Quantum Credits")
                
                if quest.rewards["xp"] > 0:
                    self.player["experience"] += quest.rewards["xp"]
                    print(f"  + {quest.rewards['xp']} XP")
            
            input("\nPress Enter to continue...")
        
        # Update research progress
        completed_research = self.research_system.update_research(self.player)
        if completed_research:
            self.clear_screen()
            print("\n=== Research Completed! ===")
            for tech_id, tech_data in completed_research.items():
                print(f"You have completed research on: {tech_data['name']}")
                print(f"Effects: {', '.join([f'{k}: {v}' for k, v in tech_data['effects'].items()])}")
                print()
            input("\nPress Enter to continue...")

        # Display turn summary
        self.clear_screen()
        print("\n=== Turn Summary ===")
        print(f"Experience gained: {total_xp_gained} XP")
        print(f"Total XP: {self.player['experience']} / " + 
              f"{self.player['player_level'] * 1000} for next level")
              
        # Show research effects if any research is completed
        research_effects = self.research_system.apply_research_effects(self.player, universe_id)
        active_effects = []
        
        if research_effects["business_income_multiplier"] > 1.0:
            active_effects.append(f"Business Income Multiplier: {research_effects['business_income_multiplier']:.1f}x")
            
        if research_effects["detection_risk_reduction"] > 0:
            active_effects.append(f"Detection Risk Reduction: -{research_effects['detection_risk_reduction']} per turn")
            
        if research_effects["quantum_income"] > 0:
            active_effects.append(f"Quantum Credits Income: +{research_effects['quantum_income']} Q¢ per turn")
        
        if research_effects["universe_level_reduction"] > 0:
            active_effects.append(f"Universe Level Requirement: -{research_effects['universe_level_reduction']} levels")
            
        if research_effects["universe_travel_discount"] > 0:
            active_effects.append(f"Universe Travel Cost: -{int(research_effects['universe_travel_discount'] * 100)}%")
            
        if research_effects["ignore_universe_requirements"]:
            active_effects.append("Universe Requirements: Bypassed")
            
        if active_effects:
            print("\n=== Active Research Effects ===")
            for effect in active_effects:
                print(f"• {effect}")


    def quests_menu(self):
        """Display the quests menu and manage active quests."""
        while True:
            self.clear_screen()
            print("\n=== QUESTS ===")
            
            # Get active quests with progress
            active_quests = self.quest_system.get_active_quests_with_progress()
            
            # Get completed quests
            completed_quests = [self.quest_system.quests[quest_id] for quest_id in self.quest_system.completed_quests]
            
            # Get available quests
            available_quests = self.quest_system.get_available_quests(self.player)
            
            # Display quest suggestions based on active quests
            suggestions = self.quest_system.get_quest_suggestions(self.player)
            if suggestions:
                print("\n🔍 SUGGESTED TASKS:")
                for suggestion in suggestions[:3]:  # Show top 3 suggestions
                    print(f"• {suggestion['quest_name']}: {suggestion['objective']} - Progress: {suggestion['progress']}")
            
            print("\n1. View Active Quests")
            print("2. View Available Quests")
            print("3. View Completed Quests")
            print("4. Back to Main Menu")
            
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                # View active quests
                self.clear_screen()
                print("\n=== ACTIVE QUESTS ===")
                
                if not active_quests:
                    print("\nYou don't have any active quests.")
                else:
                    for quest in active_quests:
                        print(f"\n📋 {quest.name}")
                        print(f"   {quest.description}")
                        print("\n   Objectives:")
                        for objective in quest.objectives:
                            status = "✓" if objective["completed"] else "➤"
                            print(f"   {status} {objective['description']} - Progress: {objective['current']}/{objective['target']}")
                        
                        print("\n   Rewards:")
                        if quest.rewards["cash"] > 0:
                            universe_id = self.player["current_universe"]
                            universe = self.universes[universe_id]
                            print(f"   • {quest.rewards['cash']} {universe['currency']}")
                        if quest.rewards["quantum"] > 0:
                            print(f"   • {quest.rewards['quantum']} Quantum Credits")
                        if quest.rewards["xp"] > 0:
                            print(f"   • {quest.rewards['xp']} XP")
                
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                # View available quests
                self.clear_screen()
                print("\n=== AVAILABLE QUESTS ===")
                
                if not available_quests:
                    print("\nNo new quests available at this time.")
                    print("Progress further in the game to unlock more quests.")
                else:
                    for i, quest in enumerate(available_quests, 1):
                        print(f"\n{i}. {quest.name}")
                        print(f"   {quest.description}")
                        
                        print("\n   Rewards:")
                        if quest.rewards["cash"] > 0:
                            universe_id = self.player["current_universe"]
                            universe = self.universes[universe_id]
                            print(f"   • {quest.rewards['cash']} {universe['currency']}")
                        if quest.rewards["quantum"] > 0:
                            print(f"   • {quest.rewards['quantum']} Quantum Credits")
                        if quest.rewards["xp"] > 0:
                            print(f"   • {quest.rewards['xp']} XP")
                    
                    print("\n0. Back")
                    
                    try:
                        quest_choice = int(input("\nActivate a quest (0 to go back): "))
                        if 1 <= quest_choice <= len(available_quests):
                            selected_quest = available_quests[quest_choice - 1]
                            if self.quest_system.activate_quest(selected_quest.id):
                                print(f"\n✓ Quest '{selected_quest.name}' activated!")
                            else:
                                print("\nFailed to activate quest. Prerequisites may not be met.")
                            input("\nPress Enter to continue...")
                    except ValueError:
                        print("\nPlease enter a valid number.")
                        time.sleep(0.75)
                
            elif choice == "3":
                # View completed quests
                self.clear_screen()
                print("\n=== COMPLETED QUESTS ===")
                
                if not completed_quests:
                    print("\nYou haven't completed any quests yet.")
                else:
                    for quest in completed_quests:
                        print(f"\n✓ {quest.name}")
                        print(f"   {quest.description}")
                        
                        print("\n   Rewards Received:")
                        if quest.rewards["cash"] > 0:
                            print(f"   • {quest.rewards['cash']} Local Currency")
                        if quest.rewards["quantum"] > 0:
                            print(f"   • {quest.rewards['quantum']} Quantum Credits")
                        if quest.rewards["xp"] > 0:
                            print(f"   • {quest.rewards['xp']} XP")
                
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                # Back to main menu
                return
            
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)
                
    def achievements_menu(self):
        """Display the achievements menu and view achievement progress."""
        while True:
            self.clear_screen()
            print("\n=== ACHIEVEMENTS ===")
            
            # Get all achievements (both locked and unlocked)
            all_achievements = self.achievement_system.achievements
            unlocked_achievements = self.achievement_system.get_unlocked_achievements()
            unlocked_ids = [a.id for a in unlocked_achievements]
            
            # Count unlocked achievements
            total_achievements = len(all_achievements)
            unlocked_count = len(unlocked_achievements)
            
            print(f"\nProgress: {unlocked_count}/{total_achievements} achievements unlocked ({int(unlocked_count/total_achievements*100)}%)")
            
            # Get achievement progress for upcoming achievements
            progress_report = self.achievement_system.get_progress_report(self.player)
            
            print("\n1. View Unlocked Achievements")
            print("2. View Locked Achievements")
            print("3. View Achievement Progress")
            print("4. Back to Main Menu")
            
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                # View unlocked achievements
                self.clear_screen()
                print("\n=== UNLOCKED ACHIEVEMENTS ===")
                
                if not unlocked_achievements:
                    print("\nYou haven't unlocked any achievements yet.")
                else:
                    for achievement in unlocked_achievements:
                        reward_text = []
                        if achievement.reward_cash > 0:
                            reward_text.append(f"{achievement.reward_cash} cash")
                        if achievement.reward_quantum > 0:
                            reward_text.append(f"{achievement.reward_quantum} Quantum Credits")
                        reward_str = " and ".join(reward_text)
                        
                        print(f"\n🏆 {achievement.name}")
                        print(f"   {achievement.description}")
                        if reward_str:
                            print(f"   Reward: {reward_str}")
                
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                # View locked achievements
                self.clear_screen()
                print("\n=== LOCKED ACHIEVEMENTS ===")
                
                locked_achievements = [a for a in all_achievements.values() if a.id not in unlocked_ids]
                
                if not locked_achievements:
                    print("\nCongratulations! You've unlocked all achievements!")
                else:
                    for achievement in locked_achievements:
                        reward_text = []
                        if achievement.reward_cash > 0:
                            reward_text.append(f"{achievement.reward_cash} cash")
                        if achievement.reward_quantum > 0:
                            reward_text.append(f"{achievement.reward_quantum} Quantum Credits")
                        reward_str = " and ".join(reward_text)
                        
                        # Don't show hidden achievement details
                        if achievement.hidden:
                            print(f"\n🔒 [Hidden Achievement]")
                            print(f"   Complete special actions to discover this achievement")
                        else:
                            print(f"\n🔒 {achievement.name}")
                            print(f"   {achievement.description}")
                            if reward_str:
                                print(f"   Reward: {reward_str}")
                
                input("\nPress Enter to continue...")
                
            elif choice == "3":
                # View achievement progress
                self.clear_screen()
                print("\n=== ACHIEVEMENT PROGRESS ===")
                
                if not progress_report:
                    print("\nNo achievement progress data available.")
                else:
                    for achievement_id, progress_data in progress_report.items():
                        achievement = all_achievements[achievement_id]
                        print(f"\n➤ {achievement.name}")
                        print(f"   {achievement.description}")
                        print(f"   Progress: {progress_data['current']}/{progress_data['required']} " + 
                              f"({int(progress_data['current']/progress_data['required']*100)}%)")
                
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                # Back to main menu
                return
            
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(0.75)

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
        
        # Get all mini games with universe-specific theming
        all_games = self.mini_game_system.get_all_games(universe_id)
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
        
        # Play the game with universe-specific theming
        success = self.mini_game_system.play_game(game_id, difficulty, universe_id)
        
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
    
    # All ad rewards related functions removed


if __name__ == "__main__":
    game = MultiVerseTycoon()
    game.start_game()
