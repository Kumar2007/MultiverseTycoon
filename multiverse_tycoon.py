#!/usr/bin/env python3

import json
import random
import time
import os
import sys

class MultiVerseTycoon:
    def __init__(self):
        """Initialize the game with default settings."""
        from achievements import AchievementSystem
        self.achievement_system = AchievementSystem()
        self.player = {
            "name": "",
            "universes": {},
            "current_universe": None,
            "turn": 1,
            "game_over": False,
            "end_reason": ""
        }
        
        self.universes = {
            "blade_runner": {
                "name": "Blade Runner",
                "description": "A dystopian future where AI businesses thrive but are highly regulated.",
                "currency": "Credits",
                "risk_factor": 75,
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
                "events": [
                    {
                        "name": "Replicant Uprising",
                        "description": "Your replicants are rebelling against poor working conditions!",
                        "effect": {"cash": -3000, "danger": 20, "reputation": -15}
                    },
                    {
                        "name": "Blade Runner Investigation",
                        "description": "Your business is being investigated by a Blade Runner.",
                        "effect": {"cash": -1000, "danger": 15, "reputation": -5}
                    },
                    {
                        "name": "Off-world Expansion",
                        "description": "Opportunity to expand your business to off-world colonies.",
                        "effect": {"cash": 5000, "danger": 5, "reputation": 10}
                    },
                    {
                        "name": "Corporate Favor",
                        "description": "A Tyrell Corporation executive offers you a partnership.",
                        "effect": {"cash": 2000, "danger": -10, "reputation": 15}
                    },
                    {
                        "name": "Blackout",
                        "description": "Digital systems fail during a city-wide blackout.",
                        "effect": {"cash": -2000, "danger": 0, "reputation": 0}
                    }
                ]
            },
            "gta_v": {
                "name": "GTA V",
                "description": "A world of organized crime, corruption, and fast money.",
                "currency": "Dollars",
                "risk_factor": 60,
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
                "events": [
                    {
                        "name": "Police Raid",
                        "description": "The LSPD is raiding one of your businesses!",
                        "effect": {"cash": -5000, "danger": 25, "reputation": -10}
                    },
                    {
                        "name": "Gang War",
                        "description": "Local gangs are fighting in your territory.",
                        "effect": {"cash": -3000, "danger": 15, "reputation": 5}
                    },
                    {
                        "name": "Heist Opportunity",
                        "description": "You've been invited to participate in a major bank heist.",
                        "effect": {"cash": 10000, "danger": 20, "reputation": 10}
                    },
                    {
                        "name": "Corrupt Official",
                        "description": "A police officer offers protection for your businesses.",
                        "effect": {"cash": -2000, "danger": -15, "reputation": 0}
                    },
                    {
                        "name": "Celebrity Client",
                        "description": "A famous celebrity becomes a regular at your establishment.",
                        "effect": {"cash": 3000, "danger": 0, "reputation": 15}
                    }
                ]
            },
            "mcu": {
                "name": "MCU",
                "description": "A world of superheroes, advanced technology, and constant innovation.",
                "currency": "USD",
                "risk_factor": 50,
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
                "events": [
                    {
                        "name": "Avengers Battle",
                        "description": "A battle between The Avengers and a villain destroyed part of your business!",
                        "effect": {"cash": -6000, "danger": 10, "reputation": 0}
                    },
                    {
                        "name": "Stark Partnership",
                        "description": "Tony Stark offers to collaborate on a new technology.",
                        "effect": {"cash": 8000, "danger": -5, "reputation": 20}
                    },
                    {
                        "name": "Alien Artifact",
                        "description": "You discovered an alien artifact with valuable technology.",
                        "effect": {"cash": 5000, "danger": 15, "reputation": 5}
                    },
                    {
                        "name": "Government Scrutiny",
                        "description": "Your business is being investigated for potential Hydra connections.",
                        "effect": {"cash": -2000, "danger": 10, "reputation": -10}
                    },
                    {
                        "name": "Multiverse Entrepreneur Award",
                        "description": "Your innovative business model wins a prestigious award.",
                        "effect": {"cash": 3000, "danger": 0, "reputation": 15}
                    }
                ]
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
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def slow_print(self, text, delay=0.03):
        """Print text with a typing effect."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        
    def display_title(self):
        """Display the game title."""
        title = """
        ███╗   ███╗██╗   ██╗██╗  ████████╗██╗██╗   ██╗███████╗██████╗ ███████╗███████╗
        ████╗ ████║██║   ██║██║  ╚══██╔══╝██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝
        ██╔████╔██║██║   ██║██║     ██║   ██║██║   ██║█████╗  ██████╔╝███████╗█████╗  
        ██║╚██╔╝██║██║   ██║██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝  
        ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║ ╚████╔╝ ███████╗██║  ██║███████║███████╗
        ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                      
        ████████╗██╗   ██╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗                         
        ╚══██╔══╝╚██╗ ██╔╝██╔════╝██╔═══██╗██╔═══██╗████╗  ██║                         
           ██║    ╚████╔╝ ██║     ██║   ██║██║   ██║██╔██╗ ██║                         
           ██║     ╚██╔╝  ██║     ██║   ██║██║   ██║██║╚██╗██║                         
           ██║      ██║   ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║                         
           ╚═╝      ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝                         
        """
        print(title)
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
        else:
            print("\nInvalid choice. Please try again.")
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
        
        self.slow_print(f"\nWelcome, {player_name}! You are now an entrepreneur in the multiverse.")
        self.slow_print("You'll start your journey in the Blade Runner universe.")
        self.slow_print("Your goal is to build businesses across multiple universes and become a multiverse tycoon!")
        self.slow_print("But be careful - if your danger level reaches 100 in any universe, you'll be caught!")
        
        input("\nPress Enter to begin your adventure...")
        self.main_game_loop()
        
    def save_game(self):
        """Save the current game state to a file."""
        try:
            with open(f"multiverse_tycoon_save_{self.player['name']}.json", "w") as save_file:
                json.dump(self.player, save_file)
            print(f"\nGame saved successfully as 'multiverse_tycoon_save_{self.player['name']}.json'!")
        except Exception as e:
            print(f"\nError saving game: {e}")
        
        input("\nPress Enter to continue...")
            
    def load_game(self):
        """Load a saved game state from a file."""
        save_files = [f for f in os.listdir() if f.startswith("multiverse_tycoon_save_") and f.endswith(".json")]
        
        if not save_files:
            print("\nNo saved games found!")
            time.sleep(1.5)
            self.start_game()
            return
            
        print("\n=== Load Game ===\n")
        for i, save_file in enumerate(save_files, 1):
            print(f"{i}. {save_file[22:-5]}")  # Extract player name from filename
            
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
                time.sleep(1.5)
                self.main_game_loop()
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1.5)
                self.load_game()
        except Exception as e:
            print(f"\nError loading game: {e}")
            time.sleep(1.5)
            self.load_game()
            
    def display_universe_info(self):
        """Display information about the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]
        
        # Display unlocked achievements
        unlocked = [ach for ach in self.achievement_system.achievements.values() if ach.unlocked]
        if unlocked:
            print("\n=== Achievements Unlocked ===")
            for achievement in unlocked:
                print(f"✓ {achievement.name} - {achievement.description}")
        
        self.clear_screen()
        print(f"\n=== {universe['name']} Universe ===")
        print(f"Description: {universe['description']}")
        print(f"Currency: {universe['currency']}")
        print(f"Risk Factor: {universe['risk_factor']}/100")
        print(f"Economic Traits: {', '.join(universe['economic_traits'])}")
        
        print("\n=== Your Status ===")
        print(f"Cash: {player_universe_data['cash']} {universe['currency']}")
        print(f"Danger Level: {player_universe_data['danger']}/100")
        print(f"Reputation: {player_universe_data['reputation']}")
        
        if player_universe_data['businesses']:
            print("\n=== Your Businesses ===")
            for business_id in player_universe_data['businesses']:
                business = universe['businesses'][business_id]
                print(f"- {business['name']} (Income: {business['income_per_turn']} {universe['currency']}/turn)")
        
        if player_universe_data['employees']:
            print("\n=== Your Employees ===")
            for employee in player_universe_data['employees']:
                emp_type = self.employee_types[employee['type']]
                print(f"- {emp_type['name']} (Salary: {emp_type['salary_per_turn']} {universe['currency']}/turn)")
                
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
            print("3. Bribe officials (Reduce danger level)")
            print("4. Jump to another universe")
            print("5. Save game")
            print("6. Quit game")
            
            choice = input("\nChoose an action (1-6): ")
            
            if choice == "1":
                self.start_business()
            elif choice == "2":
                self.hire_employee()
            elif choice == "3":
                self.bribe_officials()
            elif choice == "4":
                self.jump_universe()
            elif choice == "5":
                self.save_game()
            elif choice == "6":
                confirm = input("\nAre you sure you want to quit? Progress will be lost unless saved. (y/n): ")
                if confirm.lower() == "y":
                    print("\nThanks for playing Multiverse Tycoon!")
                    sys.exit()
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1.5)
                continue
                
            # Only advance the turn if the player didn't save/quit
            if choice not in ["5", "6"]:
                self.advance_turn()
                
            # Check for game over conditions
            if player_universe_data["danger"] >= self.DANGER_THRESHOLD:
                self.player["game_over"] = True
                self.player["end_reason"] = f"Your danger level reached {self.DANGER_THRESHOLD} in the {universe['name']} universe!"
                
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
        print(f"Available Cash: {player_universe_data['cash']} {universe['currency']}")
        
        # Display available businesses
        available_businesses = [b for b in universe["businesses"] if b not in player_universe_data["businesses"]]
        
        if not available_businesses:
            print("\nYou already own all possible businesses in this universe!")
            input("\nPress Enter to continue...")
            return
            
        print("\nAvailable Businesses:")
        for i, business_id in enumerate(available_businesses, 1):
            business = universe["businesses"][business_id]
            print(f"{i}. {business['name']} - Cost: {business['income_per_turn']} {universe['currency']}")
            print(f"   Income: {business['income_per_turn']} {universe['currency']}/turn")
            print(f"   Risk Increase: {business['risk_increase']}")
            print(f"   Description: {business['description']}\n")
            
        print(f"{len(available_businesses) + 1}. Cancel")
        
        try:
            choice = int(input("\nWhich business would you like to start? "))
            
            if choice == len(available_businesses) + 1:
                return
                
            if 1 <= choice <= len(available_businesses):
                selected_business_id = available_businesses[choice - 1]
                selected_business = universe["businesses"][selected_business_id]
                
                if player_universe_data["cash"] < selected_business["cost"]:
                    print(f"\nNot enough cash! You need {selected_business['cost']} {universe['currency']}.")
                    input("\nPress Enter to continue...")
                    return
                    
                # Purchase the business
                player_universe_data["cash"] -= selected_business["cost"]
                player_universe_data["businesses"].append(selected_business_id)
                player_universe_data["danger"] += selected_business["risk_increase"]
                
                self.slow_print(f"\nCongratulations! You now own a {selected_business['name']} in the {universe['name']} universe!")
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1.5)
                self.start_business()
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(1.5)
            self.start_business()
            
    def hire_employee(self):
        """Hire an employee for the current universe."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]
        
        self.clear_screen()
        print(f"\n=== Hire Employees in {universe['name']} ===")
        print(f"Available Cash: {player_universe_data['cash']} {universe['currency']}")
        
        # Display available employee types
        print("\nAvailable Employee Types:")
        for i, (emp_id, emp_type) in enumerate(self.employee_types.items(), 1):
            print(f"{i}. {emp_type['name']} - Cost: {emp_type['hiring_cost']} {universe['currency']}")
            print(f"   Salary: {emp_type['salary_per_turn']} {universe['currency']}/turn")
            print(f"   Efficiency Bonus: +{emp_type['efficiency_bonus']*100}% income")
            print(f"   Risk Reduction: -{emp_type['risk_reduction']} danger/turn\n")
            
        print(f"{len(self.employee_types) + 1}. Cancel")
        
        try:
            choice = int(input("\nWhich type of employee would you like to hire? "))
            
            if choice == len(self.employee_types) + 1:
                return
                
            if 1 <= choice <= len(self.employee_types):
                emp_id = list(self.employee_types.keys())[choice - 1]
                emp_type = self.employee_types[emp_id]
                
                if player_universe_data["cash"] < emp_type["hiring_cost"]:
                    print(f"\nNot enough cash! You need {emp_type['hiring_cost']} {universe['currency']}.")
                    input("\nPress Enter to continue...")
                    return
                    
                # Hire the employee
                player_universe_data["cash"] -= emp_type["hiring_cost"]
                player_universe_data["employees"].append({
                    "type": emp_id,
                    "loyalty": 100  # Starting loyalty
                })
                
                self.slow_print(f"\nYou've hired a {emp_type['name']} in the {universe['name']} universe!")
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1.5)
                self.hire_employee()
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(1.5)
            self.hire_employee()
    
    def bribe_officials(self):
        """Bribe officials to reduce danger level."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]
        
        self.clear_screen()
        print(f"\n=== Bribe Officials in {universe['name']} ===")
        print(f"Available Cash: {player_universe_data['cash']} {universe['currency']}")
        print(f"Current Danger Level: {player_universe_data['danger']}/100")
        
        # Calculate bribe options based on universe and current danger
        small_bribe = 1000
        medium_bribe = 3000
        large_bribe = 7000
        
        small_reduction = 5
        medium_reduction = 15
        large_reduction = 35
        
        print(f"\n1. Small Bribe: {small_bribe} {universe['currency']} (-{small_reduction} danger)")
        print(f"2. Medium Bribe: {medium_bribe} {universe['currency']} (-{medium_reduction} danger)")
        print(f"3. Large Bribe: {large_bribe} {universe['currency']} (-{large_reduction} danger)")
        print("4. Cancel")
        
        choice = input("\nChoose a bribe option: ")
        
        if choice == "1":
            if player_universe_data["cash"] < small_bribe:
                print(f"\nNot enough cash! You need {small_bribe} {universe['currency']}.")
            else:
                player_universe_data["cash"] -= small_bribe
                player_universe_data["danger"] = max(0, player_universe_data["danger"] - small_reduction)
                print(f"\nYou bribed a minor official. Danger reduced by {small_reduction}.")
        elif choice == "2":
            if player_universe_data["cash"] < medium_bribe:
                print(f"\nNot enough cash! You need {medium_bribe} {universe['currency']}.")
            else:
                player_universe_data["cash"] -= medium_bribe
                player_universe_data["danger"] = max(0, player_universe_data["danger"] - medium_reduction)
                print(f"\nYou bribed a police captain. Danger reduced by {medium_reduction}.")
        elif choice == "3":
            if player_universe_data["cash"] < large_bribe:
                print(f"\nNot enough cash! You need {large_bribe} {universe['currency']}.")
            else:
                player_universe_data["cash"] -= large_bribe
                player_universe_data["danger"] = max(0, player_universe_data["danger"] - large_reduction)
                print(f"\nYou bribed a high-ranking government official. Danger reduced by {large_reduction}.")
        elif choice == "4":
            return
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1.5)
            self.bribe_officials()
            return
            
        input("\nPress Enter to continue...")
        
    def jump_universe(self):
        """Jump to another universe."""
        current_universe_id = self.player["current_universe"]
        
        self.clear_screen()
        print("\n=== Jump to Another Universe ===")
        print(f"Current Universe: {self.universes[current_universe_id]['name']}")
        
        # Display available universes
        print("\nAvailable Universes:")
        for i, (universe_id, universe) in enumerate(self.universes.items(), 1):
            if universe_id != current_universe_id:
                player_universe_data = self.player["universes"][universe_id]
                print(f"{i}. {universe['name']}")
                print(f"   Cash: {player_universe_data['cash']} {universe['currency']}")
                print(f"   Danger Level: {player_universe_data['danger']}/100")
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
                
                self.slow_print(f"\nYou've jumped to the {self.universes[target_universe_id]['name']} universe!")
                self.slow_print("The dimensional shift temporarily disoriented you...")
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1.5)
                self.jump_universe()
        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(1.5)
            self.jump_universe()
        
    def trigger_random_event(self):
        """Trigger a random event from the current universe's event pool."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]
        
        # Select a random event from the universe's event pool
        event = random.choice(universe["events"])
        
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
            player_universe_data["employees"] = [e for e in player_universe_data["employees"] if e["loyalty"] > 0]
            
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
            player_universe_data["danger"] = max(0, player_universe_data["danger"] - total_reduction)
            
        return total_reduction
        
    def advance_turn(self):
        """Advance the game by one turn."""
        universe_id = self.player["current_universe"]
        universe = self.universes[universe_id]
        player_universe_data = self.player["universes"][universe_id]
        
        # Check achievements
        self.achievement_system.check_achievements(self.player)
        
        # Calculate and apply business income
        income = self.calculate_business_income()
        
        # Pay employee salaries
        salaries = self.pay_employee_salaries()
        
        # Apply danger reductions from employees
        danger_reduction = self.apply_danger_reductions()
        
        # Trigger a random event
        self.trigger_random_event()
        
        # Display turn summary
        self.clear_screen()
        print("\n=== Turn Summary ===")
        print(f"Total Business Income: +{income} {universe['currency']}")
        print(f"Employee Salaries: -{salaries} {universe['currency']}")
        print(f"Danger Reduction from Employees: -{danger_reduction}")
        
        # Increase the turn counter
        self.player["turn"] += 1
        
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
            
        print(f"\nTotal Wealth Across Multiverse: {total_wealth}")
        print(f"Total Businesses: {total_businesses}")
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

# Start the game if run directly
if __name__ == "__main__":
    game = MultiVerseTycoon()
    game.start_game()
