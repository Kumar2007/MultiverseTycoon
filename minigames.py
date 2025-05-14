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
            "john_wick": {
                "name_prefix": "Continental ",
                "game_descriptions": {
                    "number_guess": "Predict the combination to high-security Continental vaults.",
                    "code_breaker": "Break into the High Table's encrypted communication network.",
                    "word_unscramble": "Decode messages from the underground assassin network.",
                    "reaction_test": "Test your combat reflexes in intense gunfight scenarios.",
                    "memory_match": "Memorize critical intelligence about rival assassins."
                },
                "symbols": ['🔫', '🎭', '🗡️', '🏨', '💰', '🚗', '🎯', '🕴️', '📱', '🔑']
            },
            "monsterverse": {
                "name_prefix": "Monarch ",
                "game_descriptions": {
                    "number_guess": "Calculate Titan biometric readings for tracking purposes.",
                    "code_breaker": "Access classified Monarch facility security systems.",
                    "word_unscramble": "Decode ancient texts about Titan origins.",
                    "reaction_test": "Test your evacuation response time during Titan encounters.",
                    "memory_match": "Match Titan behavioral patterns for prediction models."
                },
                "symbols": ['🦎', '🦍', '🌋', '☢️', '🏢', '🚁', '📡', '🗺️', '🌊', '⚡']
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
            "john_wick": {
                "easy": [
                    "marker", "coin", "suit", "gun", "hotel",
                    "rules", "blood", "oath", "task", "kill"
                ],
                "medium": [
                    "continental", "excommunicado", "contract", "sanctuary",
                    "bounty", "assassin", "high table", "manager", "service"
                ],
                "hard": [
                    "consequences", "adjudicator", "marker holder", "blood oath",
                    "impossible task", "declaration of war", "safe passage",
                    "director", "elder", "consequences"
                ]
            },
            "monsterverse": {
                "easy": [
                    "titan", "kong", "orca", "apex", "nest",
                    "scan", "base", "team", "data", "site"
                ],
                "medium": [
                    "godzilla", "monarch", "hollow earth", "outpost",
                    "radiation", "bioacoustics", "muto", "ghidorah"
                ],
                "hard": [
                    "king of monsters", "skull island", "titan detection",
                    "ancient rivalry", "apex cybernetics", "hollow earth energy",
                    "oxygen destroyer", "terrestrial threat", "alpha predator"
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