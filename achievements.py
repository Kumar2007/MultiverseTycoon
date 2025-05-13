
#!/usr/bin/env python3

class Achievement:
    def __init__(self, id, name, description, reward_cash=0, reward_quantum=0, universe_specific=False, hidden=False):
        """Initialize an achievement.
        
        Args:
            id (str): Unique identifier for the achievement
            name (str): Display name of the achievement
            description (str): Description of how to earn the achievement
            reward_cash (int): Cash reward when unlocked
            reward_quantum (int): Quantum credits reward when unlocked
            universe_specific (bool): Whether this achievement is specific to a universe
            hidden (bool): Whether this achievement should be hidden until unlocked
        """
        self.id = id
        self.name = name
        self.description = description
        self.reward_cash = reward_cash
        self.reward_quantum = reward_quantum
        self.unlocked = False
        self.universe_specific = universe_specific
        self.hidden = hidden
        self.unlock_time = None

class AchievementSystem:
    def __init__(self):
        """Initialize the achievement system with predefined achievements."""
        self.achievements = {
            # Beginner achievements - guide the player early in the game
            "first_business": Achievement(
                "first_business", 
                "Entrepreneur", 
                "Start your first business", 
                reward_cash=1000
            ),
            "first_hire": Achievement(
                "first_hire", 
                "First Hire", 
                "Hire your first employee", 
                reward_cash=1000
            ),
            "first_jump": Achievement(
                "first_jump", 
                "Dimensional Traveler", 
                "Travel to your first new universe", 
                reward_quantum=50
            ),
            
            # Business achievements
            "business_tycoon": Achievement(
                "business_tycoon", 
                "Business Tycoon", 
                "Own 5 businesses across all universes", 
                reward_cash=5000
            ),
            "business_magnate": Achievement(
                "business_magnate", 
                "Business Magnate", 
                "Own 10 businesses across all universes", 
                reward_cash=15000,
                reward_quantum=100
            ),
            "universe_monopoly": Achievement(
                "universe_monopoly", 
                "Universe Monopoly", 
                "Own all businesses in a single universe", 
                reward_cash=10000,
                reward_quantum=150
            ),
            "multiverse_empire": Achievement(
                "multiverse_empire", 
                "Multiverse Empire", 
                "Own at least one business in each universe", 
                reward_cash=15000,
                reward_quantum=200
            ),
            
            # Financial achievements
            "money_maker": Achievement(
                "money_maker", 
                "Money Maker", 
                "Earn 100,000 in total across universes", 
                reward_cash=5000
            ),
            "hundred_thousandaire": Achievement(
                "hundred_thousandaire", 
                "Hundred-Thousandaire", 
                "Accumulate 100,000 cash in a single universe", 
                reward_cash=10000
            ),
            "millionaire": Achievement(
                "millionaire", 
                "Millionaire", 
                "Accumulate 1,000,000 total cash across universes", 
                reward_cash=50000,
                reward_quantum=300
            ),
            "quantum_collector": Achievement(
                "quantum_collector", 
                "Quantum Collector", 
                "Accumulate 1,000 Quantum Credits", 
                reward_quantum=200
            ),
            
            # Security achievements (renamed from smooth_operator for terminology consistency)
            "security_specialist": Achievement(
                "security_specialist", 
                "Security Specialist", 
                "Successfully reduce detection risk 5 times", 
                reward_cash=2000
            ),
            
            # Employee achievements
            "job_creator": Achievement(
                "job_creator", 
                "Job Creator", 
                "Hire 10 employees across all universes", 
                reward_cash=3000
            ),
            "hiring_spree": Achievement(
                "hiring_spree", 
                "Hiring Spree", 
                "Hire 3 employees in a single universe", 
                reward_cash=2000
            ),
            
            # Risk achievements (updated for terminology consistency)
            "risk_taker": Achievement(
                "risk_taker", 
                "Risk Taker", 
                "Survive with 90+ detection risk", 
                reward_cash=10000,
                reward_quantum=100
            ),
            "master_negotiator": Achievement(
                "master_negotiator", 
                "Master Negotiator", 
                "Reduce detection risk from 80+ to below 20 in one universe", 
                reward_cash=8000
            ),
            
            # Research achievements
            "research_enthusiast": Achievement(
                "research_enthusiast", 
                "Research Enthusiast", 
                "Complete your first research project", 
                reward_quantum=50
            ),
            "tech_visionary": Achievement(
                "tech_visionary", 
                "Tech Visionary", 
                "Complete 5 research projects", 
                reward_quantum=150
            ),
            
            # Heist achievements
            "first_heist": Achievement(
                "first_heist", 
                "Daring Heist", 
                "Successfully complete your first heist", 
                reward_cash=5000
            ),
            "master_thief": Achievement(
                "master_thief", 
                "Master Thief", 
                "Successfully complete 3 heists", 
                reward_cash=15000,
                reward_quantum=100
            ),
            
            # Mini-game achievements
            "game_winner": Achievement(
                "game_winner", 
                "Game Winner", 
                "Win your first mini-game", 
                reward_cash=1000
            ),
            "game_master": Achievement(
                "game_master", 
                "Game Master", 
                "Win 5 mini-games", 
                reward_cash=5000,
                reward_quantum=50
            ),
            
            # Special achievements
            "dimensional_explorer": Achievement(
                "dimensional_explorer", 
                "Dimensional Explorer", 
                "Visit all universes", 
                reward_cash=5000,
                reward_quantum=100
            ),
            "event_survivor": Achievement(
                "event_survivor", 
                "Event Survivor", 
                "Experience 20 random events", 
                reward_cash=4000,
                reward_quantum=100
            ),
            "full_turn": Achievement(
                "full_turn", 
                "Full Turn", 
                "Complete 10 game turns", 
                reward_cash=2000
            ),
            "long_haul": Achievement(
                "long_haul", 
                "Long Haul", 
                "Complete 50 game turns", 
                reward_cash=10000,
                reward_quantum=200
            )
        }
        
        # Track statistics for achievements
        self.stats = {
            "risk_reductions": 0,
            "heists_completed": 0,
            "minigames_won": 0,
            "businesses_started": 0,
            "total_businesses": 0,
            "universe_jumps": 0,  # Count of universe jumps
            "universe_visited": {},  # Dictionary tracking which universes were visited
            "different_universes_visited": 0,  # Count of different universes visited
            "events_experienced": 0
        }
        
        # Keep unlocked achievements in a list for easy access
        self.unlocked_achievements = []
        
    def check_achievements(self, game_state):
        """Check and unlock achievements based on game state.
        
        Returns:
            list: Newly unlocked achievements (if any)
        """
        newly_unlocked = []
        
        # Calculate totals
        total_businesses = sum(len(universe_data['businesses']) for universe_data in game_state["universes"].values())
        total_employees = sum(len(universe_data['employees']) for universe_data in game_state["universes"].values())
        total_cash = sum(universe_data['cash'] for universe_data in game_state["universes"].values())
        
        # Check beginner achievements
        if total_businesses >= 1 and self.unlock_achievement("first_business", game_state):
            newly_unlocked.append(self.achievements["first_business"])
            
        if total_employees >= 1 and self.unlock_achievement("first_hire", game_state):
            newly_unlocked.append(self.achievements["first_hire"])
        
        # Check business achievements
        if total_businesses >= 5 and self.unlock_achievement("business_tycoon", game_state):
            newly_unlocked.append(self.achievements["business_tycoon"])
            
        if total_businesses >= 10 and self.unlock_achievement("business_magnate", game_state):
            newly_unlocked.append(self.achievements["business_magnate"])
            
        # Check financial achievements    
        if total_cash >= 100000 and self.unlock_achievement("money_maker", game_state):
            newly_unlocked.append(self.achievements["money_maker"])
            
        if total_cash >= 1000000 and self.unlock_achievement("millionaire", game_state):
            newly_unlocked.append(self.achievements["millionaire"])
            
        # Check for universe-specific cash achievements
        for universe_id, universe_data in game_state["universes"].items():
            if universe_data["cash"] >= 100000 and self.unlock_achievement("hundred_thousandaire", game_state):
                newly_unlocked.append(self.achievements["hundred_thousandaire"])
                break
                
        # Check quantum credits achievement
        if game_state["quantum_credits"] >= 1000 and self.unlock_achievement("quantum_collector", game_state):
            newly_unlocked.append(self.achievements["quantum_collector"])
                
        # Check employee achievements
        if total_employees >= 10 and self.unlock_achievement("job_creator", game_state):
            newly_unlocked.append(self.achievements["job_creator"])
            
        # Check for hiring spree in a single universe
        for universe_id, universe_data in game_state["universes"].items():
            if len(universe_data["employees"]) >= 3 and self.unlock_achievement("hiring_spree", game_state):
                newly_unlocked.append(self.achievements["hiring_spree"])
                break
                
        # Check universe monopoly (all businesses in one universe)
        for universe_id, universe_data in game_state["universes"].items():
            # Check if player owns every business in this universe
            if "businesses" in universe_data and len(universe_data["businesses"]) > 0:
                all_universe_businesses = set(game_state.get("universe_businesses", {}).get(universe_id, []))
                owned_businesses = set(universe_data["businesses"])
                
                if all_universe_businesses and all_universe_businesses.issubset(owned_businesses):
                    if self.unlock_achievement("universe_monopoly", game_state):
                        newly_unlocked.append(self.achievements["universe_monopoly"])
                        break
            
        # Check multiverse empire (at least one business in each universe)
        universes_with_businesses = sum(1 for universe_data in game_state["universes"].values() 
                                      if len(universe_data.get('businesses', [])) > 0)
        if universes_with_businesses == len(game_state["universes"]) and self.unlock_achievement("multiverse_empire", game_state):
            newly_unlocked.append(self.achievements["multiverse_empire"])
            
        # Check dimensional explorer achievement (visited all universes)
        if len(self.stats.get("universe_visited", {})) == len(game_state["universes"]) and self.unlock_achievement("dimensional_explorer", game_state):
            newly_unlocked.append(self.achievements["dimensional_explorer"])
            
        # Check risk-related achievements (using updated terminology)
        for universe_id, universe_data in game_state["universes"].items():
            if universe_data.get("danger", 0) >= 90 and self.unlock_achievement("risk_taker", game_state):
                newly_unlocked.append(self.achievements["risk_taker"])
                break
                
        # Check turn-based achievements
        if game_state["turn"] >= 10 and self.unlock_achievement("full_turn", game_state):
            newly_unlocked.append(self.achievements["full_turn"])
            
        if game_state["turn"] >= 50 and self.unlock_achievement("long_haul", game_state):
            newly_unlocked.append(self.achievements["long_haul"])
            
        # Check event survivor
        if self.stats["events_experienced"] >= 20 and self.unlock_achievement("event_survivor", game_state):
            newly_unlocked.append(self.achievements["event_survivor"])
            
        # Check research achievements
        completed_research = game_state.get("completed_research", [])
        if len(completed_research) >= 1 and self.unlock_achievement("research_enthusiast", game_state):
            newly_unlocked.append(self.achievements["research_enthusiast"])
            
        if len(completed_research) >= 5 and self.unlock_achievement("tech_visionary", game_state):
            newly_unlocked.append(self.achievements["tech_visionary"])
            
        # Check heist achievements
        if self.stats["heists_completed"] >= 1 and self.unlock_achievement("first_heist", game_state):
            newly_unlocked.append(self.achievements["first_heist"])
            
        if self.stats["heists_completed"] >= 3 and self.unlock_achievement("master_thief", game_state):
            newly_unlocked.append(self.achievements["master_thief"])
            
        # Check mini-game achievements
        if self.stats["minigames_won"] >= 1 and self.unlock_achievement("game_winner", game_state):
            newly_unlocked.append(self.achievements["game_winner"])
            
        if self.stats["minigames_won"] >= 5 and self.unlock_achievement("game_master", game_state):
            newly_unlocked.append(self.achievements["game_master"])
            
        # Check security achievement (renamed from smooth_operator)
        if self.stats["risk_reductions"] >= 5 and self.unlock_achievement("security_specialist", game_state):
            newly_unlocked.append(self.achievements["security_specialist"])
            
        return newly_unlocked
    
    def update_stats(self, stat_name, value=1, universe_id=None):
        """Update achievement statistics.
        
        Args:
            stat_name (str): The statistic to update
            value (int): Value to increment (default 1)
            universe_id (str, optional): Universe ID for universe-specific stats
        """
        if stat_name == "universe_jump" and universe_id:
            # Mark this universe as visited
            self.stats["universe_jumps"][universe_id] = True
        elif stat_name in self.stats:
            # Increment counter stats
            self.stats[stat_name] += value
            
    def check_master_negotiator(self, game_state, universe_id, previous_risk, current_risk):
        """Special check for master negotiator achievement.
        
        Args:
            game_state (dict): Current game state
            universe_id (str): Universe ID where risk was reduced
            previous_risk (int): Previous detection risk level
            current_risk (int): Current detection risk level
        
        Returns:
            bool: True if achievement was unlocked
        """
        if previous_risk >= 80 and current_risk < 20:
            if self.unlock_achievement("master_negotiator", game_state):
                return True
        return False
    
    def unlock_achievement(self, achievement_id, game_state):
        """Unlock an achievement and grant its reward.
        
        Args:
            achievement_id (str): ID of the achievement to unlock
            game_state (dict): Current game state
            
        Returns:
            bool: True if newly unlocked, False if already unlocked
        """
        if achievement_id not in self.achievements:
            return False
            
        achievement = self.achievements[achievement_id]
        if not achievement.unlocked:
            achievement.unlocked = True
            achievement.unlock_time = game_state["turn"]  # Record when it was unlocked
            
            # Add to list of unlocked achievements
            self.unlocked_achievements.append(achievement_id)
            
            # Grant rewards
            current_universe = game_state["current_universe"]
            if achievement.reward_cash > 0:
                game_state["universes"][current_universe]["cash"] += achievement.reward_cash
                
            if achievement.reward_quantum > 0:
                game_state["quantum_credits"] += achievement.reward_quantum
                
            return True
        return False
        
    def get_unlocked_achievements(self):
        """Get a list of all unlocked achievements.
        
        Returns:
            list: List of unlocked Achievement objects
        """
        return [self.achievements[ach_id] for ach_id in self.unlocked_achievements]
        
    def get_progress_report(self, game_state):
        """Get a detailed progress report for upcoming achievements.
        
        Args:
            game_state (dict): Current game state
            
        Returns:
            dict: Progress information for achievements close to completion
        """
        progress = {}
        
        # Calculate game state totals
        total_businesses = sum(len(universe_data.get('businesses', [])) for universe_data in game_state["universes"].values())
        total_employees = sum(len(universe_data.get('employees', [])) for universe_data in game_state["universes"].values())
        total_cash = sum(universe_data.get('cash', 0) for universe_data in game_state["universes"].values())
        
        # Check business achievements progress
        if not self.achievements["business_tycoon"].unlocked:
            progress["business_tycoon"] = {
                "current": total_businesses,
                "target": 5,
                "percentage": min(100, int(total_businesses / 5 * 100))
            }
            
        if not self.achievements["business_magnate"].unlocked:
            progress["business_magnate"] = {
                "current": total_businesses,
                "target": 10,
                "percentage": min(100, int(total_businesses / 10 * 100))
            }
            
        # Financial progress
        if not self.achievements["money_maker"].unlocked:
            progress["money_maker"] = {
                "current": total_cash,
                "target": 100000,
                "percentage": min(100, int(total_cash / 100000 * 100))
            }
            
        if not self.achievements["millionaire"].unlocked:
            progress["millionaire"] = {
                "current": total_cash,
                "target": 1000000,
                "percentage": min(100, int(total_cash / 1000000 * 100))
            }
            
        # Quantum credits progress
        if not self.achievements["quantum_collector"].unlocked:
            progress["quantum_collector"] = {
                "current": game_state["quantum_credits"],
                "target": 1000,
                "percentage": min(100, int(game_state["quantum_credits"] / 1000 * 100))
            }
            
        # Employee achievements
        if not self.achievements["job_creator"].unlocked:
            progress["job_creator"] = {
                "current": total_employees,
                "target": 10,
                "percentage": min(100, int(total_employees / 10 * 100))
            }
            
        # Research progress
        completed_research = len(game_state.get("completed_research", []))
        if not self.achievements["tech_visionary"].unlocked:
            progress["tech_visionary"] = {
                "current": completed_research,
                "target": 5,
                "percentage": min(100, int(completed_research / 5 * 100))
            }
            
        # Heist progress
        if not self.achievements["master_thief"].unlocked:
            progress["master_thief"] = {
                "current": self.stats["heists_completed"],
                "target": 3,
                "percentage": min(100, int(self.stats["heists_completed"] / 3 * 100))
            }
            
        # Mini-game progress
        if not self.achievements["game_master"].unlocked:
            progress["game_master"] = {
                "current": self.stats["minigames_won"],
                "target": 5,
                "percentage": min(100, int(self.stats["minigames_won"] / 5 * 100))
            }
            
        # Security specialist progress
        if not self.achievements["security_specialist"].unlocked:
            progress["security_specialist"] = {
                "current": self.stats["risk_reductions"],
                "target": 5,
                "percentage": min(100, int(self.stats["risk_reductions"] / 5 * 100))
            }
            
        # Universe exploration progress
        if not self.achievements["dimensional_explorer"].unlocked:
            progress["dimensional_explorer"] = {
                "current": len(self.stats["universe_jumps"]),
                "target": len(game_state["universes"]),
                "percentage": min(100, int(len(self.stats["universe_jumps"]) / len(game_state["universes"]) * 100))
            }
            
        # Event survivor progress
        if not self.achievements["event_survivor"].unlocked:
            progress["event_survivor"] = {
                "current": self.stats["events_experienced"],
                "target": 20,
                "percentage": min(100, int(self.stats["events_experienced"] / 20 * 100))
            }
            
        return progress
