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