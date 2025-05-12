
class Achievement:
    def __init__(self, id, name, description, reward_cash=0):
        self.id = id
        self.name = name
        self.description = description
        self.reward_cash = reward_cash
        self.unlocked = False

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            # Business achievements
            "business_tycoon": Achievement("business_tycoon", "Business Tycoon", "Own 5 businesses across all universes", 5000),
            "universe_monopoly": Achievement("universe_monopoly", "Universe Monopoly", "Own all businesses in a single universe", 10000),
            "multiverse_empire": Achievement("multiverse_empire", "Multiverse Empire", "Own at least one business in each universe", 15000),
            
            # Financial achievements
            "millionaire": Achievement("millionaire", "Millionaire", "Accumulate 1,000,000 total cash across universes", 50000),
            "smooth_operator": Achievement("smooth_operator", "Smooth Operator", "Successfully bribe officials 5 times", 2000),
            
            # Employee achievements
            "job_creator": Achievement("job_creator", "Job Creator", "Hire 10 employees across all universes", 3000),
            "loyal_boss": Achievement("loyal_boss", "Loyal Boss", "Have 5 employees with 100% loyalty", 5000),
            
            # Risk achievements
            "risk_taker": Achievement("risk_taker", "Risk Taker", "Survive with 90+ danger level", 10000),
            "master_negotiator": Achievement("master_negotiator", "Master Negotiator", "Reduce danger level from 80+ to 0 in one universe", 8000),
            
            # Special achievements
            "dimensional_explorer": Achievement("dimensional_explorer", "Dimensional Explorer", "Visit all universes", 5000),
            "event_survivor": Achievement("event_survivor", "Event Survivor", "Experience 20 random events", 4000)
        }
        
    def check_achievements(self, game_state):
        """Check and unlock achievements based on game state"""
        total_businesses = sum(len(universe_data['businesses']) for universe_data in game_state["universes"].values())
        total_employees = sum(len(universe_data['employees']) for universe_data in game_state["universes"].values())
        total_cash = sum(universe_data['cash'] for universe_data in game_state["universes"].values())
        
        # Check business achievements
        if total_businesses >= 5:
            self.unlock_achievement("business_tycoon", game_state)
            
        # Check financial achievements    
        if total_cash >= 1000000:
            self.unlock_achievement("millionaire", game_state)
            
        # Check employee achievements
        if total_employees >= 10:
            self.unlock_achievement("job_creator", game_state)
            
        # Check universe-specific achievements
        universes_with_businesses = sum(1 for universe_data in game_state["universes"].values() 
                                      if len(universe_data['businesses']) > 0)
        if universes_with_businesses == len(game_state["universes"]):
            self.unlock_achievement("multiverse_empire", game_state)
    
    def unlock_achievement(self, achievement_id, game_state):
        """Unlock an achievement and grant its reward"""
        achievement = self.achievements[achievement_id]
        if not achievement.unlocked:
            achievement.unlocked = True
            current_universe = game_state["current_universe"]
            game_state["universes"][current_universe]["cash"] += achievement.reward_cash
            return True
        return False
