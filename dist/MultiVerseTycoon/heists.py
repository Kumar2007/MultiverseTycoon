#!/usr/bin/env python3

import random
import time

class HeistSystem:
    """Manage interdimensional heists across multiple universes."""
    
    def __init__(self, universes):
        """Initialize the heist system with available universes."""
        self.universes = universes
        
        # Define heist difficulty levels and their modifiers
        self.difficulty_levels = {
            "easy": {
                "name": "Easy",
                "success_chance": 0.8,  # 80% success chance
                "reward_multiplier": 1.5,
                "danger_increase": 15,
                "min_preparation": 1000,  # Minimum cost to prepare
                "min_crew": 1,  # Minimum crew members required
            },
            "medium": {
                "name": "Medium",
                "success_chance": 0.6,  # 60% success chance
                "reward_multiplier": 2.5,
                "danger_increase": 25,
                "min_preparation": 3000,
                "min_crew": 2,
            },
            "hard": {
                "name": "Hard",
                "success_chance": 0.4,  # 40% success chance
                "reward_multiplier": 4.0,
                "danger_increase": 40,
                "min_preparation": 7000,
                "min_crew": 3,
            },
            "impossible": {
                "name": "Impossible",
                "success_chance": 0.2,  # 20% success chance
                "reward_multiplier": 8.0,
                "danger_increase": 60,
                "min_preparation": 15000,
                "min_crew": 5,
            }
        }
        
        # Define heist types for each universe
        self.heist_types = {
            "blade_runner": [
                {
                    "name": "Replicant Data Theft",
                    "description": "Steal valuable replicant design data from a Tyrell Corp facility.",
                    "base_reward": 8000,
                    "quantum_reward": 30,
                    "required_skills": ["hacking", "stealth"],
                    "special_item": "data_encryption_key",
                },
                {
                    "name": "Off-world Bank Robbery",
                    "description": "Rob a high-security bank in an off-world colony.",
                    "base_reward": 15000,
                    "quantum_reward": 50,
                    "required_skills": ["combat", "stealth", "lockpicking"],
                    "special_item": "security_override",
                },
                {
                    "name": "Replicant Smuggling",
                    "description": "Help escaped replicants flee the city and get them off-world.",
                    "base_reward": 10000,
                    "quantum_reward": 40,
                    "required_skills": ["disguise", "transport"],
                    "special_item": "false_identity_chips",
                }
            ],
            "gta_v": [
                {
                    "name": "Casino Vault Heist",
                    "description": "Break into the Diamond Casino vault and make off with millions.",
                    "base_reward": 20000,
                    "quantum_reward": 60,
                    "required_skills": ["lockpicking", "hacking", "demolition"],
                    "special_item": "vault_blueprints",
                },
                {
                    "name": "Yacht Hijacking",
                    "description": "Take control of a billionaire's yacht and steal all valuables.",
                    "base_reward": 12000,
                    "quantum_reward": 45,
                    "required_skills": ["combat", "pilot", "swimming"],
                    "special_item": "yacht_schedule",
                },
                {
                    "name": "Military Hardware Theft",
                    "description": "Break into Fort Zancudo and steal experimental military equipment.",
                    "base_reward": 25000,
                    "quantum_reward": 75,
                    "required_skills": ["hacking", "combat", "stealth", "pilot"],
                    "special_item": "security_keycard",
                }
            ],
            "mcu": [
                {
                    "name": "Stark Tech Infiltration",
                    "description": "Break into Stark Industries and steal prototype technology.",
                    "base_reward": 30000,
                    "quantum_reward": 80,
                    "required_skills": ["hacking", "stealth", "engineering"],
                    "special_item": "employee_badge",
                },
                {
                    "name": "Quantum Realm Expedition",
                    "description": "Enter the Quantum Realm and extract rare quantum particles.",
                    "base_reward": 40000,
                    "quantum_reward": 150,
                    "required_skills": ["science", "pilot", "survival"],
                    "special_item": "quantum_realm_map",
                },
                {
                    "name": "Infinity Stone Recovery",
                    "description": "Locate and retrieve a hidden fragment of an Infinity Stone.",
                    "base_reward": 50000,
                    "quantum_reward": 200,
                    "required_skills": ["combat", "magic", "stealth", "survival"],
                    "special_item": "infinity_detector",
                }
            ]
        }
        
        # Define specialist crew members that can be recruited
        self.specialists = {
            "hacker": {
                "name": "Hacker",
                "skills": ["hacking"],
                "hiring_cost": 5000,
                "payment_percentage": 10,  # Takes 10% of the heist reward
                "success_bonus": 0.15,  # +15% success chance for related heists
            },
            "thief": {
                "name": "Master Thief",
                "skills": ["stealth", "lockpicking"],
                "hiring_cost": 6000,
                "payment_percentage": 12,
                "success_bonus": 0.15,
            },
            "muscle": {
                "name": "Muscle",
                "skills": ["combat"],
                "hiring_cost": 4000,
                "payment_percentage": 8,
                "success_bonus": 0.1,
            },
            "wheelman": {
                "name": "Wheelman",
                "skills": ["pilot", "transport"],
                "hiring_cost": 5500,
                "payment_percentage": 10,
                "success_bonus": 0.12,
            },
            "engineer": {
                "name": "Engineer",
                "skills": ["engineering", "demolition"],
                "hiring_cost": 7000,
                "payment_percentage": 15,
                "success_bonus": 0.18,
            },
            "infiltrator": {
                "name": "Infiltrator",
                "skills": ["disguise", "stealth"],
                "hiring_cost": 6500,
                "payment_percentage": 12,
                "success_bonus": 0.15,
            },
            "scientist": {
                "name": "Interdimensional Scientist",
                "skills": ["science", "magic"],
                "hiring_cost": 8000,
                "payment_percentage": 18,
                "success_bonus": 0.2,
            },
        }
        
        # Define special items that can be acquired and used for heists
        self.special_items = {
            "data_encryption_key": {
                "name": "Data Encryption Key",
                "description": "Allows access to encrypted data systems.",
                "cost": 3000,
                "success_bonus": 0.2,
                "applicable_heists": ["Replicant Data Theft"],
            },
            "security_override": {
                "name": "Security Override Device",
                "description": "Bypasses most security systems.",
                "cost": 5000,
                "success_bonus": 0.15,
                "applicable_heists": ["Off-world Bank Robbery", "Casino Vault Heist"],
            },
            "false_identity_chips": {
                "name": "False Identity Chips",
                "description": "Provides fake identities that pass most checks.",
                "cost": 2500,
                "success_bonus": 0.25,
                "applicable_heists": ["Replicant Smuggling"],
            },
            "vault_blueprints": {
                "name": "Vault Blueprints",
                "description": "Detailed plans of the target vault.",
                "cost": 4000,
                "success_bonus": 0.3,
                "applicable_heists": ["Casino Vault Heist"],
            },
            "yacht_schedule": {
                "name": "Yacht Schedule",
                "description": "Detailed itinerary of the target yacht.",
                "cost": 2000,
                "success_bonus": 0.2,
                "applicable_heists": ["Yacht Hijacking"],
            },
            "security_keycard": {
                "name": "Security Keycard",
                "description": "Military-grade access card.",
                "cost": 6000,
                "success_bonus": 0.25,
                "applicable_heists": ["Military Hardware Theft"],
            },
            "employee_badge": {
                "name": "Stark Industries Employee Badge",
                "description": "Authentic employee credentials.",
                "cost": 7000,
                "success_bonus": 0.3,
                "applicable_heists": ["Stark Tech Infiltration"],
            },
            "quantum_realm_map": {
                "name": "Quantum Realm Map",
                "description": "Rare map showing safe paths through the Quantum Realm.",
                "cost": 10000,
                "success_bonus": 0.35,
                "applicable_heists": ["Quantum Realm Expedition"],
            },
            "infinity_detector": {
                "name": "Infinity Energy Detector",
                "description": "Locates traces of Infinity Stone energy.",
                "cost": 12000,
                "success_bonus": 0.4,
                "applicable_heists": ["Infinity Stone Recovery"],
            },
        }
    
    def get_available_heists(self, universe_id):
        """Get available heists for a specific universe."""
        if universe_id not in self.heist_types:
            return []
        return self.heist_types[universe_id]
    
    def get_heist_success_chance(self, heist, difficulty, crew_members, special_items):
        """Calculate the success chance of a heist based on various factors."""
        # Base success chance from difficulty
        success_chance = self.difficulty_levels[difficulty]["success_chance"]
        
        # Add bonuses from crew members
        for crew_member_id in crew_members:
            if crew_member_id in self.specialists:
                specialist = self.specialists[crew_member_id]
                # Check if specialist has relevant skills for this heist
                if any(skill in heist["required_skills"] for skill in specialist["skills"]):
                    success_chance += specialist["success_bonus"]
        
        # Add bonuses from special items
        for item_id in special_items:
            if item_id in self.special_items:
                item = self.special_items[item_id]
                if heist["name"] in item["applicable_heists"]:
                    success_chance += item["success_bonus"]
        
        # Cap success chance at 95%
        return min(0.95, success_chance)
    
    def calculate_heist_reward(self, heist, difficulty, success):
        """Calculate the reward for a heist based on difficulty and success."""
        if not success:
            return {"local_currency": 0, "quantum_credits": 0}
            
        # Get base reward values
        base_local = heist["base_reward"]
        base_quantum = heist["quantum_reward"]
        
        # Apply difficulty multiplier
        multiplier = self.difficulty_levels[difficulty]["reward_multiplier"]
        
        return {
            "local_currency": int(base_local * multiplier),
            "quantum_credits": int(base_quantum * multiplier)
        }
    
    def calculate_crew_payment(self, reward, crew_members):
        """Calculate how much of the reward goes to the crew."""
        total_percentage = 0
        
        for crew_member_id in crew_members:
            if crew_member_id in self.specialists:
                total_percentage += self.specialists[crew_member_id]["payment_percentage"]
        
        # Calculate payment amounts for local currency and quantum credits
        local_payment = int(reward["local_currency"] * (total_percentage / 100))
        quantum_payment = int(reward["quantum_credits"] * (total_percentage / 100))
        
        return {
            "local_currency": local_payment,
            "quantum_credits": quantum_payment,
            "percentage": total_percentage
        }
    
    def execute_heist(self, heist, difficulty, crew_members, special_items):
        """Execute a heist and determine the outcome."""
        # Calculate success chance
        success_chance = self.get_heist_success_chance(heist, difficulty, crew_members, special_items)
        
        # Roll for success
        roll = random.random()
        success = roll < success_chance
        
        # Calculate rewards
        reward = self.calculate_heist_reward(heist, difficulty, success)
        
        # Calculate crew payment
        crew_payment = self.calculate_crew_payment(reward, crew_members)
        
        # Calculate net reward (after paying the crew)
        net_reward = {
            "local_currency": reward["local_currency"] - crew_payment["local_currency"],
            "quantum_credits": reward["quantum_credits"] - crew_payment["quantum_credits"]
        }
        
        # Get danger increase from difficulty
        danger_increase = 0 if not success else self.difficulty_levels[difficulty]["danger_increase"]
        
        return {
            "success": success,
            "roll": roll,
            "success_chance": success_chance,
            "gross_reward": reward,
            "crew_payment": crew_payment,
            "net_reward": net_reward,
            "danger_increase": danger_increase
        }
    
    def get_available_specialists(self, owned_specialists):
        """Get specialists that are available for recruitment."""
        available = {}
        for specialist_id, specialist in self.specialists.items():
            if specialist_id not in owned_specialists:
                available[specialist_id] = specialist
        return available
    
    def get_available_special_items(self, owned_items):
        """Get special items that are available for purchase."""
        available = {}
        for item_id, item in self.special_items.items():
            if item_id not in owned_items:
                available[item_id] = item
        return available