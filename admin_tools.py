#!/usr/bin/env python3
"""
Admin tools for debugging and testing the Multiverse Tycoon game.
This module is not used in the main game and is only for development purposes.
"""

import json
import os
import sys
import random
import glob

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"{text.center(80)}")
    print("=" * 80)

def admin_menu():
    """Main admin menu."""
    # This is a simple admin menu for debugging purposes
    while True:
        clear_screen()
        print_header("MULTIVERSE TYCOON ADMIN TOOLS")
        print("\n1. Generate reward codes")
        print("2. Reset active rewards")
        print("3. List active rewards")
        print("4. Reset ad watch cooldown")
        print("5. Delete save files")
        print("6. Return to game")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == "1":
            generate_reward_codes()
        elif choice == "2":
            reset_active_rewards()
        elif choice == "3":
            list_active_rewards()
        elif choice == "4":
            reset_ad_cooldown()
        elif choice == "5":
            delete_save_files()
        elif choice == "6":
            break
        else:
            print("\nInvalid option. Try again.")
            input("\nPress Enter to continue...")

def delete_save_files():
    """Delete save files."""
    clear_screen()
    print_header("DELETE SAVE FILES")
    
    # Get list of save files
    save_files = glob.glob("saves/multiverse_tycoon_save_*.json")
    
    if not save_files:
        print("\nNo save files found.")
        input("\nPress Enter to continue...")
        return
    
    print("\nAvailable save files:")
    for i, save_file in enumerate(save_files, 1):
        # Extract player name from filename
        player_name = save_file.split("_")[-1].replace(".json", "")
        print(f"{i}. {player_name}")
    
    print("\nOptions:")
    print("1-N. Delete specific save")
    print("A. Delete all saves")
    print("C. Cancel")
    
    choice = input("\nSelect an option: ").upper()
    
    if choice == "C":
        return
    elif choice == "A":
        confirm = input("\nAre you sure you want to delete ALL save files? (yes/no): ").lower()
        if confirm == "yes":
            for save_file in save_files:
                try:
                    os.remove(save_file)
                    print(f"Deleted: {save_file}")
                except Exception as e:
                    print(f"Error deleting {save_file}: {e}")
            print("\nAll save files deleted.")
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(save_files):
                save_file = save_files[index]
                player_name = save_file.split("_")[-1].replace(".json", "")
                confirm = input(f"\nAre you sure you want to delete save file for {player_name}? (yes/no): ").lower()
                if confirm == "yes":
                    try:
                        os.remove(save_file)
                        print(f"\nDeleted save file for {player_name}")
                    except Exception as e:
                        print(f"\nError deleting save file: {e}")
            else:
                print("\nInvalid selection.")
        except ValueError:
            print("\nInvalid input.")
    
    input("\nPress Enter to continue...")

def generate_reward_codes():
    """Generate reward codes for testing."""
    clear_screen()
    print_header("GENERATE REWARD CODES")
    
    # Check if ad codes file exists
    if not os.path.exists("saves/ad_codes.json"):
        print("\nAd codes file not found. Creating a new one.")
        
        try:
            # Ensure the saves directory exists
            if not os.path.exists("saves"):
                os.makedirs("saves")
                
            # Create an empty ad codes file
            with open("saves/ad_codes.json", "w") as file:
                json.dump({"codes": {}, "generated_time": 0}, file)
                
        except Exception as e:
            print(f"\nError creating ad codes file: {e}")
            input("\nPress Enter to continue...")
            return
    
    # Load the ad codes
    try:
        with open("saves/ad_codes.json", "r") as file:
            ad_codes = json.load(file)
    except Exception as e:
        print(f"\nError loading ad codes: {e}")
        input("\nPress Enter to continue...")
        return
    
    # Generate 5 new codes
    import string
    import time
    from datetime import datetime, timedelta
    
    current_time = time.time()
    
    # Generate some codes without overwriting existing ones
    new_codes = {}
    
    for i in range(5):
        code = 'MVT-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        
        # Pick a random reward type
        reward_types = ["small_quantum", "medium_quantum", "large_quantum", "cash_boost", "safety_net"]
        reward_type = random.choice(reward_types)
        
        # Set expiry to 7 days from now
        expiry_time = current_time + (7 * 24 * 60 * 60)
        
        new_codes[code] = {
            "reward_type": reward_type,
            "claimed": False,
            "expiry_time": expiry_time
        }
        
        # Display the new code
        expiry_date = datetime.fromtimestamp(expiry_time).strftime("%Y-%m-%d")
        print(f"\nGenerated code: {code}")
        print(f"Reward type: {reward_type}")
        print(f"Expires: {expiry_date}")
    
    # Update the codes file
    ad_codes["codes"].update(new_codes)
    ad_codes["generated_time"] = current_time
    
    try:
        with open("saves/ad_codes.json", "w") as file:
            json.dump(ad_codes, file)
        print("\nCodes generated and saved successfully.")
    except Exception as e:
        print(f"\nError saving ad codes: {e}")
    
    input("\nPress Enter to continue...")

def reset_active_rewards():
    """Reset all active rewards."""
    clear_screen()
    print_header("RESET ACTIVE REWARDS")
    
    # Check if active rewards file exists
    if not os.path.exists("saves/active_rewards.json"):
        print("\nActive rewards file not found. Nothing to reset.")
        input("\nPress Enter to continue...")
        return
    
    try:
        # Reset the active rewards
        with open("saves/active_rewards.json", "w") as file:
            empty_rewards = {"active_boosts": [], "redeemed_codes": [], "last_ad_time": 0}
            json.dump(empty_rewards, file)
        
        print("\nActive rewards have been reset successfully.")
    except Exception as e:
        print(f"\nError resetting active rewards: {e}")
    
    input("\nPress Enter to continue...")

def list_active_rewards():
    """List all active rewards."""
    clear_screen()
    print_header("ACTIVE REWARDS")
    
    # Check if active rewards file exists
    if not os.path.exists("saves/active_rewards.json"):
        print("\nActive rewards file not found.")
        input("\nPress Enter to continue...")
        return
    
    try:
        # Load the active rewards
        with open("saves/active_rewards.json", "r") as file:
            active_rewards = json.load(file)
        
        # Display active boosts
        if active_rewards.get("active_boosts"):
            print("\nActive Boosts:")
            for boost in active_rewards["active_boosts"]:
                print(f"• {boost.get('name', 'Unknown')} - {boost.get('turns_remaining', 0)} turns remaining")
        else:
            print("\nNo active boosts.")
        
        # Display redeemed codes
        if active_rewards.get("redeemed_codes"):
            print("\nRedeemed Codes:")
            for code in active_rewards["redeemed_codes"]:
                print(f"• {code}")
        else:
            print("\nNo redeemed codes.")
        
        # Display last ad time
        last_ad_time = active_rewards.get("last_ad_time", 0)
        if last_ad_time > 0:
            from datetime import datetime
            last_time = datetime.fromtimestamp(last_ad_time)
            print(f"\nLast ad watched at: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("\nNo ads watched yet.")
        
    except Exception as e:
        print(f"\nError loading active rewards: {e}")
    
    input("\nPress Enter to continue...")

def reset_ad_cooldown():
    """Reset the ad watch cooldown."""
    clear_screen()
    print_header("RESET AD WATCH COOLDOWN")
    
    # Check if active rewards file exists
    if not os.path.exists("saves/active_rewards.json"):
        print("\nActive rewards file not found.")
        input("\nPress Enter to continue...")
        return
    
    try:
        # Load the active rewards
        with open("saves/active_rewards.json", "r") as file:
            active_rewards = json.load(file)
        
        # Reset the ad watch cooldown
        active_rewards["last_ad_time"] = 0
        
        # Save the updated active rewards
        with open("saves/active_rewards.json", "w") as file:
            json.dump(active_rewards, file)
        
        print("\nAd watch cooldown has been reset successfully.")
        print("You can now watch another ad for a reward.")
    except Exception as e:
        print(f"\nError resetting ad watch cooldown: {e}")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    admin_menu()