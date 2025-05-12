#!/usr/bin/env python3

import os
import json
import time
import random
import string
from datetime import datetime, timedelta

class AdRewardsSystem:
    """
    A system to manage ad-based rewards for the Multiverse Tycoon game.
    
    This system simulates ad watching through codes that can be redeemed
    for quantum credits and other in-game bonuses.
    """
    
    def __init__(self):
        """Initialize the ad rewards system."""
        self.rewards = {
            "small_quantum": {
                "name": "Small Quantum Credit Boost",
                "description": "Earn 50 Quantum Credits instantly",
                "quantum_credits": 50,
                "cash_multiplier": 1.0,
                "risk_reduction": 0,
                "duration_turns": 0,
                "probability": 0.4  # 40% chance
            },
            "medium_quantum": {
                "name": "Medium Quantum Credit Boost",
                "description": "Earn 150 Quantum Credits instantly",
                "quantum_credits": 150,
                "cash_multiplier": 1.0,
                "risk_reduction": 0,
                "duration_turns": 0,
                "probability": 0.25  # 25% chance
            },
            "large_quantum": {
                "name": "Large Quantum Credit Boost",
                "description": "Earn 300 Quantum Credits instantly",
                "quantum_credits": 300,
                "cash_multiplier": 1.0,
                "risk_reduction": 0,
                "duration_turns": 0,
                "probability": 0.15  # 15% chance
            },
            "cash_boost": {
                "name": "Income Multiplier",
                "description": "Earn 2x cash from all businesses for 5 turns",
                "quantum_credits": 0,
                "cash_multiplier": 2.0,
                "risk_reduction": 0,
                "duration_turns": 5,
                "probability": 0.1  # 10% chance
            },
            "safety_net": {
                "name": "Safety Net",
                "description": "Reduce danger levels by 30 points instantly",
                "quantum_credits": 0,
                "cash_multiplier": 1.0,
                "risk_reduction": 30,
                "duration_turns": 0,
                "probability": 0.1  # 10% chance
            }
        }
        
        # Load or create active rewards data
        self.active_rewards_file = "saves/active_rewards.json"
        self.active_rewards = self.load_active_rewards()
        
        # Load or create ad code database
        self.codes_file = "saves/ad_codes.json"
        self.ad_codes = self.load_ad_codes()
        
        # Reward cooldown time (12 hours in seconds)
        self.cooldown_seconds = 12 * 60 * 60
        
    def load_active_rewards(self):
        """Load active rewards from file or create a new empty rewards structure."""
        if os.path.exists(self.active_rewards_file):
            try:
                with open(self.active_rewards_file, 'r') as file:
                    return json.load(file)
            except:
                return {"active_boosts": [], "redeemed_codes": [], "last_ad_time": 0}
        else:
            # Create saves directory if it doesn't exist
            if not os.path.exists("saves"):
                try:
                    os.makedirs("saves")
                except:
                    pass
            return {"active_boosts": [], "redeemed_codes": [], "last_ad_time": 0}
    
    def save_active_rewards(self):
        """Save active rewards to file."""
        try:
            # Create saves directory if it doesn't exist
            if not os.path.exists("saves"):
                try:
                    os.makedirs("saves")
                except:
                    pass
                    
            with open(self.active_rewards_file, 'w') as file:
                json.dump(self.active_rewards, file)
        except:
            print("Warning: Unable to save active rewards data.")
    
    def load_ad_codes(self):
        """Load ad codes from file or create a new empty codes structure."""
        if os.path.exists(self.codes_file):
            try:
                with open(self.codes_file, 'r') as file:
                    return json.load(file)
            except:
                return {"codes": {}, "generated_time": 0}
        else:
            return {"codes": {}, "generated_time": 0}
    
    def save_ad_codes(self):
        """Save ad codes to file."""
        try:
            # Create saves directory if it doesn't exist
            if not os.path.exists("saves"):
                try:
                    os.makedirs("saves")
                except:
                    pass
                    
            with open(self.codes_file, 'w') as file:
                json.dump(self.ad_codes, file)
        except:
            print("Warning: Unable to save ad codes data.")
    
    def generate_code(self):
        """Generate a random alphanumeric code."""
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(characters) for _ in range(8))
        return f"MVT-{code}"
    
    def generate_reward_codes(self, num_codes=5):
        """Generate a set of reward codes for ads."""
        current_time = time.time()
        
        # Only regenerate codes once a day (86400 seconds)
        if current_time - self.ad_codes.get("generated_time", 0) < 86400:
            return self.ad_codes["codes"]
        
        # Clear old codes and generate new ones
        self.ad_codes["codes"] = {}
        self.ad_codes["generated_time"] = current_time
        
        for _ in range(num_codes):
            code = self.generate_code()
            # Randomly select a reward based on probability
            reward_type = self.select_random_reward()
            self.ad_codes["codes"][code] = {
                "reward_type": reward_type,
                "claimed": False,
                "expiry_time": current_time + (7 * 24 * 60 * 60)  # 7 days
            }
        
        self.save_ad_codes()
        return self.ad_codes["codes"]
    
    def select_random_reward(self):
        """Select a random reward based on probabilities."""
        rand = random.random()
        cumulative_prob = 0
        
        for reward_id, reward_data in self.rewards.items():
            cumulative_prob += reward_data["probability"]
            if rand <= cumulative_prob:
                return reward_id
        
        # Fallback to the first reward if something goes wrong
        return list(self.rewards.keys())[0]
    
    def redeem_code(self, player, code):
        """Redeem an ad reward code and apply the rewards to the player."""
        # Convert code to uppercase to be case-insensitive
        code = code.upper()
        
        # Generate codes if needed
        self.generate_reward_codes()
        
        # Check if code exists
        if code not in self.ad_codes["codes"]:
            return False, "Invalid code. Please check and try again."
        
        # Check if code has been claimed
        if self.ad_codes["codes"][code]["claimed"]:
            return False, "This code has already been redeemed."
        
        # Check if code has expired
        current_time = time.time()
        if current_time > self.ad_codes["codes"][code]["expiry_time"]:
            return False, "This code has expired."
        
        # Mark code as claimed
        self.ad_codes["codes"][code]["claimed"] = True
        self.active_rewards["redeemed_codes"].append(code)
        
        # Get the reward type
        reward_type = self.ad_codes["codes"][code]["reward_type"]
        reward = self.rewards[reward_type]
        
        # Apply instant rewards
        if reward["quantum_credits"] > 0:
            player["quantum_credits"] += reward["quantum_credits"]
        
        if reward["risk_reduction"] > 0:
            current_universe = player["current_universe"]
            if current_universe in player["universes"]:
                player["universes"][current_universe]["danger"] = max(
                    0, 
                    player["universes"][current_universe]["danger"] - reward["risk_reduction"]
                )
        
        # Add time-based boosts to active boosts
        if reward["duration_turns"] > 0:
            boost = {
                "reward_type": reward_type,
                "name": reward["name"],
                "turns_remaining": reward["duration_turns"],
                "cash_multiplier": reward["cash_multiplier"]
            }
            self.active_rewards["active_boosts"].append(boost)
        
        # Save changes
        self.save_ad_codes()
        self.save_active_rewards()
        
        return True, f"Successfully redeemed: {reward['name']} - {reward['description']}"
    
    def watch_ad_for_reward(self, player):
        """Simulate watching an ad and get a reward."""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.active_rewards.get("last_ad_time", 0) < self.cooldown_seconds:
            last_time = datetime.fromtimestamp(self.active_rewards.get("last_ad_time", 0))
            next_time = last_time + timedelta(seconds=self.cooldown_seconds)
            hours, remainder = divmod((next_time - datetime.now()).seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            return False, f"You can watch another ad in {hours} hours and {minutes} minutes."
        
        # Update last ad time
        self.active_rewards["last_ad_time"] = current_time
        
        # Select a random reward
        reward_type = self.select_random_reward()
        reward = self.rewards[reward_type]
        
        # Apply rewards (same logic as redeeming a code)
        if reward["quantum_credits"] > 0:
            player["quantum_credits"] += reward["quantum_credits"]
        
        if reward["risk_reduction"] > 0:
            current_universe = player["current_universe"]
            if current_universe in player["universes"]:
                player["universes"][current_universe]["danger"] = max(
                    0, 
                    player["universes"][current_universe]["danger"] - reward["risk_reduction"]
                )
        
        # Add time-based boosts to active boosts
        if reward["duration_turns"] > 0:
            boost = {
                "reward_type": reward_type,
                "name": reward["name"],
                "turns_remaining": reward["duration_turns"],
                "cash_multiplier": reward["cash_multiplier"]
            }
            self.active_rewards["active_boosts"].append(boost)
        
        # Save changes
        self.save_active_rewards()
        
        return True, f"Ad watched! Reward: {reward['name']} - {reward['description']}"
    
    def update_turn(self, player):
        """Update active boosts at the end of a turn."""
        updated = False
        cash_multiplier = 1.0
        
        # Update remaining turns for active boosts
        active_boosts = []
        for boost in self.active_rewards["active_boosts"]:
            if boost["turns_remaining"] > 1:
                boost["turns_remaining"] -= 1
                active_boosts.append(boost)
                # Apply multiplier effect
                cash_multiplier = max(cash_multiplier, boost["cash_multiplier"])
                updated = True
            else:
                # Boost has expired
                updated = True
        
        if updated:
            self.active_rewards["active_boosts"] = active_boosts
            self.save_active_rewards()
        
        return cash_multiplier
    
    def get_active_boosts(self):
        """Get a list of currently active boosts."""
        return self.active_rewards["active_boosts"]
    
    def print_reward_codes(self):
        """Print all available reward codes - for testing/admin purposes."""
        self.generate_reward_codes()
        print("\n=== Available Ad Reward Codes ===")
        for code, data in self.ad_codes["codes"].items():
            reward = self.rewards[data["reward_type"]]
            status = "CLAIMED" if data["claimed"] else "AVAILABLE"
            expiry = datetime.fromtimestamp(data["expiry_time"]).strftime("%Y-%m-%d")
            print(f"{code}: {reward['name']} ({status}, Expires: {expiry})")