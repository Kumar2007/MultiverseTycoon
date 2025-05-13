#!/usr/bin/env python3

class Quest:
    def __init__(self, id, name, description, objectives, rewards, prerequisites=None):
        """Initialize a quest.
        
        Args:
            id (str): Unique identifier for the quest
            name (str): Display name of the quest
            description (str): Description of the quest and its lore context
            objectives (list): List of objectives to complete the quest
            rewards (dict): Rewards for completing the quest
            prerequisites (list, optional): List of quest IDs that must be completed first
        """
        self.id = id
        self.name = name
        self.description = description
        self.objectives = objectives  # List of {description, target, current, completed}
        self.rewards = rewards  # Dictionary with keys: cash, quantum, xp
        self.prerequisites = prerequisites if prerequisites else []
        self.completed = False
        self.active = False
        self.universe_specific = ""  # Can be set to a universe ID if specific

class QuestSystem:
    def __init__(self):
        """Initialize the quest system with predefined quests."""
        self.quests = {
            # Beginner quests - guide the player through basic gameplay
            "business_basics": Quest(
                "business_basics",
                "Business Basics",
                "Start your interdimensional business empire with some basic operations.",
                [
                    {"description": "Start your first business", "target": 1, "current": 0, "completed": False},
                    {"description": "Hire your first employee", "target": 1, "current": 0, "completed": False},
                    {"description": "Complete 5 turns", "target": 5, "current": 0, "completed": False},
                ],
                {"cash": 2000, "quantum": 10, "xp": 200}
            ),
            
            "risk_management": Quest(
                "risk_management",
                "Risk Management",
                "Learn to manage detection risk in your operations.",
                [
                    {"description": "Reduce detection risk 3 times", "target": 3, "current": 0, "completed": False},
                    {"description": "Keep risk below 30 for 5 turns", "target": 5, "current": 0, "completed": False},
                ],
                {"cash": 1500, "quantum": 15, "xp": 250},
                ["business_basics"]
            ),
            
            "multiverse_expansion": Quest(
                "multiverse_expansion",
                "Multiverse Expansion",
                "Expand your business operations to multiple universes.",
                [
                    {"description": "Unlock universe travel", "target": 1, "current": 0, "completed": False},
                    {"description": "Jump to another universe", "target": 1, "current": 0, "completed": False},
                    {"description": "Start a business in a second universe", "target": 1, "current": 0, "completed": False},
                ],
                {"cash": 0, "quantum": 50, "xp": 500},
                ["business_basics"]
            ),
            
            "research_initiative": Quest(
                "research_initiative",
                "Research Initiative",
                "Begin researching technologies to improve your operations.",
                [
                    {"description": "Unlock research", "target": 1, "current": 0, "completed": False},
                    {"description": "Complete 1 research project", "target": 1, "current": 0, "completed": False},
                ],
                {"cash": 2500, "quantum": 25, "xp": 300},
                ["business_basics"]
            ),
            
            "entertainment_mogul": Quest(
                "entertainment_mogul",
                "Entertainment Mogul",
                "Become skilled at the mini-games across universes.",
                [
                    {"description": "Win 5 mini-games", "target": 5, "current": 0, "completed": False},
                    {"description": "Win 1 mini-game on hard difficulty", "target": 1, "current": 0, "completed": False},
                ],
                {"cash": 3000, "quantum": 30, "xp": 400},
                ["business_basics"]
            ),
            
            # Advanced universe-specific quests
            "blade_runner_quest": Quest(
                "blade_runner_quest",
                "Replicant Revolution",
                "Manage replicant resources in the Blade Runner universe to gain special benefits.",
                [
                    {"description": "Own a Replicant Manufacturing business", "target": 1, "current": 0, "completed": False},
                    {"description": "Achieve 10,000 Credits in the Blade Runner universe", "target": 10000, "current": 0, "completed": False},
                    {"description": "Reduce detection risk 5 times in Blade Runner", "target": 5, "current": 0, "completed": False},
                ],
                {"cash": 5000, "quantum": 50, "xp": 500}
            ),
            
            "gta_quest": Quest(
                "gta_quest",
                "Criminal Enterprise",
                "Build a criminal network in the GTA universe.",
                [
                    {"description": "Own a Nightclub and Auto Shop", "target": 2, "current": 0, "completed": False},
                    {"description": "Complete a successful heist in GTA", "target": 1, "current": 0, "completed": False},
                    {"description": "Achieve $50,000 in the GTA universe", "target": 50000, "current": 0, "completed": False},
                ],
                {"cash": 10000, "quantum": 75, "xp": 750},
                ["multiverse_expansion"]
            ),
            
            "mcu_quest": Quest(
                "mcu_quest",
                "Superhero Solutions",
                "Provide tech solutions for superheroes in the MCU universe.",
                [
                    {"description": "Own a Stark Tech Competitor business", "target": 1, "current": 0, "completed": False},
                    {"description": "Experience the 'Stark Partnership' event", "target": 1, "current": 0, "completed": False},
                    {"description": "Reach 20 local influence in MCU", "target": 20, "current": 0, "completed": False},
                ],
                {"cash": 15000, "quantum": 100, "xp": 1000},
                ["multiverse_expansion"]
            ),
            
            # Master-level quests
            "quantum_mastery": Quest(
                "quantum_mastery",
                "Quantum Entrepreneur",
                "Master quantum business operations across the multiverse.",
                [
                    {"description": "Own 10 businesses across all universes", "target": 10, "current": 0, "completed": False},
                    {"description": "Accumulate 500 Quantum Credits", "target": 500, "current": 0, "completed": False},
                    {"description": "Reach player level 10", "target": 10, "current": 0, "completed": False},
                ],
                {"cash": 50000, "quantum": 250, "xp": 2000},
                ["multiverse_expansion", "research_initiative"]
            ),
        }
        
        # Universe-specific quests
        self.quests["blade_runner_quest"].universe_specific = "blade_runner"
        self.quests["gta_quest"].universe_specific = "gta_v"
        self.quests["mcu_quest"].universe_specific = "mcu"
        
        # Track active quests
        self.active_quests = []
        self.completed_quests = []
        
        # Initialize with the first quest active
        self.activate_quest("business_basics")
    
    def activate_quest(self, quest_id):
        """Activate a quest.
        
        Args:
            quest_id (str): Quest ID to activate
            
        Returns:
            bool: True if activated, False if not available
        """
        if quest_id in self.quests and not self.quests[quest_id].active and not self.quests[quest_id].completed:
            # Check prerequisites
            prereqs_met = True
            for prereq_id in self.quests[quest_id].prerequisites:
                if prereq_id not in self.completed_quests:
                    prereqs_met = False
                    break
            
            if prereqs_met:
                self.quests[quest_id].active = True
                if quest_id not in self.active_quests:
                    self.active_quests.append(quest_id)
                return True
        
        return False
    
    def get_available_quests(self, game_state):
        """Get a list of quests that are available but not active or completed.
        
        Args:
            game_state (dict): Current game state
            
        Returns:
            list: List of available quest objects
        """
        available_quests = []
        
        for quest_id, quest in self.quests.items():
            # Skip active or completed quests
            if quest.active or quest.completed:
                continue
            
            # Check if universe-specific and player has access
            if quest.universe_specific and quest.universe_specific not in game_state["unlocked_universes"]:
                continue
            
            # Check prerequisites
            prereqs_met = True
            for prereq_id in quest.prerequisites:
                if prereq_id not in self.completed_quests:
                    prereqs_met = False
                    break
            
            if prereqs_met:
                available_quests.append(quest)
        
        return available_quests
    
    def update_quest_progress(self, quest_id, objective_index, progress):
        """Update progress on a quest objective.
        
        Args:
            quest_id (str): ID of the quest to update
            objective_index (int): Index of the objective to update
            progress (int): Amount of progress to add
            
        Returns:
            bool: True if the quest is completed as a result
        """
        if quest_id not in self.quests or not self.quests[quest_id].active:
            return False
        
        quest = self.quests[quest_id]
        objective = quest.objectives[objective_index]
        
        if objective["completed"]:
            return False
        
        objective["current"] += progress
        
        # Check if objective is completed
        if objective["current"] >= objective["target"]:
            objective["completed"] = True
            objective["current"] = objective["target"]  # Cap at target
        
        # Check if all objectives are completed
        all_completed = True
        for obj in quest.objectives:
            if not obj["completed"]:
                all_completed = False
                break
        
        if all_completed:
            quest.completed = True
            quest.active = False
            if quest_id in self.active_quests:
                self.active_quests.remove(quest_id)
            if quest_id not in self.completed_quests:
                self.completed_quests.append(quest_id)
            return True
        
        return False
    
    def get_quest_completion_rewards(self, quest_id):
        """Get the rewards for completing a quest.
        
        Args:
            quest_id (str): ID of the completed quest
            
        Returns:
            dict: Rewards dictionary, or None if quest not found or not completed
        """
        if quest_id in self.quests and self.quests[quest_id].completed:
            return self.quests[quest_id].rewards
        return None
    
    def check_and_update_quests(self, game_state, update_type, value=1, universe_id=None):
        """Check and update all active quests based on a game action.
        
        Args:
            game_state (dict): Current game state
            update_type (str): Type of update (e.g., "business_started", "turn_completed")
            value: Value to update by (can be int for counters or str for specific identifiers)
            universe_id (str, optional): Universe ID if action is universe-specific
            
        Returns:
            list: List of newly completed quests
        """
        newly_completed = []
        
        for quest_id in self.active_quests[:]:  # Copy to avoid modification during iteration
            quest = self.quests[quest_id]
            
            # Skip universe-specific quests if not in that universe
            if quest.universe_specific and universe_id and quest.universe_specific != universe_id:
                continue
            
            for i, objective in enumerate(quest.objectives):
                # Map update_type to objective descriptions
                update_matches = False
                
                # Business related objectives
                if update_type == "business_started" and "Start" in objective["description"] and "business" in objective["description"]:
                    update_matches = True
                
                # Employee related objectives
                elif update_type == "employee_hired" and "Hire" in objective["description"] and "employee" in objective["description"]:
                    update_matches = True
                
                # Universe travel objectives
                elif update_type == "universe_traveled" and "Jump to another universe" in objective["description"]:
                    update_matches = True
                
                # Turn completion objectives
                elif update_type == "turn_completed" and "turns" in objective["description"]:
                    update_matches = True
                
                # Risk reduction objectives
                elif update_type == "risk_reduced" and "Reduce detection risk" in objective["description"]:
                    update_matches = True
                
                # Risk management objectives (keep below threshold)
                elif update_type == "low_risk_maintained" and "Keep risk below" in objective["description"]:
                    update_matches = True
                
                # Feature unlock objectives
                elif update_type == "feature_unlocked":
                    if "Unlock universe travel" in objective["description"] and isinstance(value, str) and value == "universe_travel":
                        update_matches = True
                    elif "Unlock research" in objective["description"] and isinstance(value, str) and value == "research":
                        update_matches = True
                
                # Research completion objectives
                elif update_type == "research_completed" and "Complete" in objective["description"] and "research" in objective["description"]:
                    update_matches = True
                
                # Mini-game objectives
                elif update_type == "minigame_won" and "Win" in objective["description"] and "mini-game" in objective["description"]:
                    update_matches = True
                
                # Cash threshold objectives
                elif update_type == "cash_threshold":
                    if "Achieve" in objective["description"] and "Credits" in objective["description"] and "Blade Runner" in objective["description"]:
                        if isinstance(value, int) and isinstance(universe_id, str):
                            update_matches = universe_id == "blade_runner" and value >= int(''.join(filter(str.isdigit, objective["description"])))
                    elif "Achieve" in objective["description"] and "$" in objective["description"] and "GTA" in objective["description"]:
                        if isinstance(value, int) and isinstance(universe_id, str):
                            update_matches = universe_id == "gta_v" and value >= int(''.join(filter(str.isdigit, objective["description"])))
                
                # Specific business ownership objectives
                elif update_type == "specific_business_owned":
                    if "Own a Replicant Manufacturing business" in objective["description"]:
                        update_matches = value == "replicant_manufacturing"
                    elif "Own a Nightclub and Auto Shop" in objective["description"]:
                        current_businesses = set(game_state["universes"].get("gta_v", {}).get("businesses", []))
                        target_businesses = {"nightclub", "auto_shop"}
                        if target_businesses.issubset(current_businesses):
                            update_matches = True
                            objective["current"] = objective["target"]  # Complete this objective
                    elif "Own a Stark Tech Competitor business" in objective["description"]:
                        update_matches = value == "stark_tech_competitor"
                
                # Specific event experience objectives
                elif update_type == "event_experienced" and "Experience the 'Stark Partnership' event" in objective["description"]:
                    update_matches = value == "Stark Partnership"
                
                # Influence objectives
                elif update_type == "influence_threshold" and "Reach" in objective["description"] and "influence" in objective["description"]:
                    target_influence = int(''.join(filter(str.isdigit, objective["description"])))
                    # Ensure value is an integer for comparison
                    try:
                        current_value = int(value) if isinstance(value, str) else value
                        if universe_id == "mcu" and current_value >= target_influence:
                            update_matches = True
                            objective["current"] = objective["target"]  # Complete this objective
                    except (ValueError, TypeError):
                        # Skip if value can't be converted to int for comparison
                        pass
                
                # Total businesses objectives
                elif update_type == "total_businesses" and "Own" in objective["description"] and "businesses across all universes" in objective["description"]:
                    total = 0
                    for uni_id, uni_data in game_state["universes"].items():
                        total += len(uni_data.get("businesses", []))
                    if total >= objective["target"]:
                        update_matches = True
                        objective["current"] = objective["target"]  # Complete this objective
                
                # Quantum credits objectives
                elif update_type == "quantum_credits" and "Accumulate" in objective["description"] and "Quantum Credits" in objective["description"]:
                    if value >= objective["target"]:
                        update_matches = True
                        objective["current"] = objective["target"]  # Complete this objective
                
                # Player level objectives
                elif update_type == "player_level" and "Reach player level" in objective["description"]:
                    if value >= objective["target"]:
                        update_matches = True
                        objective["current"] = objective["target"]  # Complete this objective
                
                # If update matches this objective, update progress
                if update_matches and not objective["completed"]:
                    if self.update_quest_progress(quest_id, i, 1):  # Quest completed
                        newly_completed.append(quest_id)
                        break  # No need to check other objectives for this quest
        
        # Check for new quests to activate
        for completed_id in newly_completed:
            # Look for quests that have this as a prerequisite
            for quest_id, quest in self.quests.items():
                if completed_id in quest.prerequisites and not quest.active and not quest.completed:
                    self.activate_quest(quest_id)
        
        return newly_completed
    
    def get_active_quests_with_progress(self):
        """Get active quests with their progress information.
        
        Returns:
            list: List of active quest objects with progress
        """
        result = []
        for quest_id in self.active_quests:
            result.append(self.quests[quest_id])
        return result
    
    def get_quest_suggestions(self, game_state):
        """Get quest suggestions based on game state.
        
        Args:
            game_state (dict): Current game state
            
        Returns:
            list: List of suggested next steps based on active quests
        """
        suggestions = []
        
        active_quests = self.get_active_quests_with_progress()
        for quest in active_quests:
            # Find incomplete objectives
            for objective in quest.objectives:
                if not objective["completed"]:
                    # Add suggestion with context
                    suggestions.append({
                        "quest_name": quest.name,
                        "objective": objective["description"],
                        "progress": f"{objective['current']}/{objective['target']}"
                    })
        
        return suggestions