#!/usr/bin/env python3

class ResearchSystem:
    """A system to manage research projects and technology development."""
    
    def __init__(self):
        """Initialize the research system with available technologies."""
        # Research technologies organized by categories
        self.technologies = {
            "business": {
                "efficient_management": {
                    "name": "Efficient Management",
                    "description": "Streamline operations to increase business income by 10%.",
                    "cost": {"quantum_credits": 150},
                    "research_turns": 3,
                    "effects": {"business_income_multiplier": 1.1},
                    "required_level": 2,
                    "prerequisites": []
                },
                "advanced_automation": {
                    "name": "Advanced Automation",
                    "description": "Automate routine tasks to increase business income by 20%.",
                    "cost": {"quantum_credits": 350},
                    "research_turns": 5,
                    "effects": {"business_income_multiplier": 1.2},
                    "required_level": 3,
                    "prerequisites": ["efficient_management"]
                },
                "quantum_networking": {
                    "name": "Quantum Networking",
                    "description": "Connect businesses with quantum technology for a 30% income boost.",
                    "cost": {"quantum_credits": 800},
                    "research_turns": 8,
                    "effects": {"business_income_multiplier": 1.3},
                    "required_level": 5,
                    "prerequisites": ["advanced_automation"]
                }
            },
            "risk_management": {
                "local_bribes": {
                    "name": "Local Influence Networks",
                    "description": "Establish connections with local officials to reduce detection risk by 2 per turn.",
                    "cost": {"quantum_credits": 100},
                    "research_turns": 2,
                    "effects": {"danger_reduction": 2},
                    "required_level": 2,
                    "prerequisites": []
                },
                "identity_masking": {
                    "name": "Identity Masking",
                    "description": "Use advanced technology to hide your true nature, reducing detection risk by 3 per turn.",
                    "cost": {"quantum_credits": 300},
                    "research_turns": 4,
                    "effects": {"danger_reduction": 3},
                    "required_level": 3,
                    "prerequisites": ["local_bribes"]
                },
                "dimensional_phasing": {
                    "name": "Dimensional Phasing",
                    "description": "Partially phase your operations into another dimension, reducing detection risk by 5 per turn.",
                    "cost": {"quantum_credits": 700},
                    "research_turns": 7,
                    "effects": {"danger_reduction": 5},
                    "required_level": 5,
                    "prerequisites": ["identity_masking"]
                }
            },
            "interdimensional": {
                "quantum_stabilizers": {
                    "name": "Quantum Stabilizers",
                    "description": "Stabilize quantum flux to generate 5 additional Quantum Credits per turn.",
                    "cost": {"quantum_credits": 200},
                    "research_turns": 3,
                    "effects": {"quantum_income": 5},
                    "required_level": 2,
                    "prerequisites": []
                },
                "reality_anchors": {
                    "name": "Reality Anchors",
                    "description": "Create stable points across universes, generating 12 Quantum Credits per turn.",
                    "cost": {"quantum_credits": 450},
                    "research_turns": 6,
                    "effects": {"quantum_income": 12},
                    "required_level": 4,
                    "prerequisites": ["quantum_stabilizers"]
                },
                "multiverse_resonance": {
                    "name": "Multiverse Resonance",
                    "description": "Harness the resonance between universes for 25 Quantum Credits per turn.",
                    "cost": {"quantum_credits": 900},
                    "research_turns": 9,
                    "effects": {"quantum_income": 25},
                    "required_level": 6,
                    "prerequisites": ["reality_anchors"]
                }
            },
            "expansion": {
                "dimensional_scanner": {
                    "name": "Dimensional Scanner",
                    "description": "Scan for new universes, reducing the level requirement for the next universe by 1.",
                    "cost": {"quantum_credits": 250},
                    "research_turns": 4,
                    "effects": {"universe_level_reduction": 1},
                    "required_level": 3,
                    "prerequisites": []
                },
                "quantum_tunneling": {
                    "name": "Quantum Tunneling",
                    "description": "Create stable tunnels between universes, reducing universe travel costs by 50%.",
                    "cost": {"quantum_credits": 400},
                    "research_turns": 5,
                    "effects": {"universe_travel_discount": 0.5},
                    "required_level": 4,
                    "prerequisites": ["dimensional_scanner"]
                },
                "reality_synthesis": {
                    "name": "Reality Synthesis",
                    "description": "Gain the ability to unlock any universe regardless of level requirements.",
                    "cost": {"quantum_credits": 1000},
                    "research_turns": 10,
                    "effects": {"ignore_universe_requirements": True},
                    "required_level": 7,
                    "prerequisites": ["quantum_tunneling"]
                }
            }
        }
    
    def get_available_technologies(self, player_data):
        """Get technologies available to research based on player level and completed research."""
        available_tech = {}
        completed_research = player_data.get("completed_research", [])
        current_research = player_data.get("current_research", {})
        player_level = player_data.get("player_level", 1)
        
        # Check each category
        for category, technologies in self.technologies.items():
            available_in_category = {}
            
            # Check each technology
            for tech_id, tech in technologies.items():
                # Skip if already researched or currently researching
                if tech_id in completed_research or tech_id in current_research:
                    continue
                
                # Check level requirement
                if tech["required_level"] > player_level:
                    continue
                
                # Check prerequisites
                prerequisites_met = True
                for prereq in tech["prerequisites"]:
                    if prereq not in completed_research:
                        prerequisites_met = False
                        break
                
                if prerequisites_met:
                    available_in_category[tech_id] = tech
            
            # Add category if it has available technologies
            if available_in_category:
                available_tech[category] = available_in_category
        
        return available_tech
    
    def start_research(self, player_data, tech_id, category):
        """Start researching a new technology."""
        # Find the technology
        if category not in self.technologies or tech_id not in self.technologies[category]:
            return False, "Technology not found."
        
        tech = self.technologies[category][tech_id]
        
        # Check if player can afford it
        if player_data["quantum_credits"] < tech["cost"]["quantum_credits"]:
            return False, "Not enough Quantum Credits to start this research."
        
        # Deduct cost
        player_data["quantum_credits"] -= tech["cost"]["quantum_credits"]
        
        # Initialize current_research if it doesn't exist
        if "current_research" not in player_data:
            player_data["current_research"] = {}
        
        # Start research
        player_data["current_research"][tech_id] = {
            "name": tech["name"],
            "category": category,
            "turns_remaining": tech["research_turns"],
            "total_turns": tech["research_turns"]
        }
        
        return True, f"Started research on {tech['name']}. It will take {tech['research_turns']} turns to complete."
    
    def update_research(self, player_data):
        """Update research progress at the end of a turn."""
        if "current_research" not in player_data:
            return {}
        
        completed = {}
        ongoing = {}
        
        for tech_id, research_data in player_data["current_research"].items():
            # Reduce turns remaining
            research_data["turns_remaining"] -= 1
            
            # Check if complete
            if research_data["turns_remaining"] <= 0:
                # Find the technology
                category = research_data["category"]
                tech = self.technologies[category][tech_id]
                
                # Add to completed research
                if "completed_research" not in player_data:
                    player_data["completed_research"] = []
                
                player_data["completed_research"].append(tech_id)
                
                # Store in completed dictionary
                completed[tech_id] = {
                    "name": tech["name"],
                    "category": category,
                    "effects": tech["effects"]
                }
            else:
                # Still in progress
                ongoing[tech_id] = research_data
        
        # Update current research to only include ongoing projects
        player_data["current_research"] = ongoing
        
        return completed
    
    def apply_research_effects(self, player_data, universe_id):
        """Apply the effects of completed research to a universe."""
        effects = {
            "business_income_multiplier": 1.0,
            "danger_reduction": 0,
            "quantum_income": 0,
            "universe_level_reduction": 0,
            "universe_travel_discount": 0,
            "ignore_universe_requirements": False
        }
        
        # Check if player has any completed research
        if "completed_research" not in player_data:
            return effects
        
        # Apply effects from all completed research
        for tech_id in player_data["completed_research"]:
            # Find the technology
            for category, technologies in self.technologies.items():
                if tech_id in technologies:
                    tech = technologies[tech_id]
                    
                    # Apply each effect
                    for effect_type, effect_value in tech["effects"].items():
                        if effect_type == "business_income_multiplier":
                            # Multiplicative stacking for income multipliers
                            effects[effect_type] *= effect_value
                        elif effect_type in ["danger_reduction", "quantum_income", "universe_level_reduction"]:
                            # Additive stacking for these effects
                            effects[effect_type] += effect_value
                        elif effect_type == "universe_travel_discount":
                            # Take the highest discount
                            effects[effect_type] = max(effects[effect_type], effect_value)
                        elif effect_type == "ignore_universe_requirements":
                            # Boolean OR
                            effects[effect_type] = effects[effect_type] or effect_value
        
        return effects
    
    def get_research_progress(self, player_data):
        """Get the current research progress for display."""
        if "current_research" not in player_data or not player_data["current_research"]:
            return {}
        
        progress = {}
        
        for tech_id, research_data in player_data["current_research"].items():
            progress[tech_id] = {
                "name": research_data["name"],
                "turns_remaining": research_data["turns_remaining"],
                "total_turns": research_data["total_turns"],
                "progress_percent": int((research_data["total_turns"] - research_data["turns_remaining"]) / research_data["total_turns"] * 100)
            }
        
        return progress