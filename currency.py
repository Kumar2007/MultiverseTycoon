#!/usr/bin/env python3

class CurrencyExchange:
    """Handle currency conversions and interdimensional currency management."""
    
    def __init__(self, universes):
        """Initialize the currency exchange system."""
        self.universes = universes
        
        # Define the interdimensional currency
        self.inter_currency = {
            "name": "Quantum Credits",
            "symbol": "Q¢",
            "description": "A rare interdimensional currency that holds value across all universes."
        }
        
        # Define exchange rates for each universe's currency to Quantum Credits
        # These rates determine how valuable each currency is relative to Quantum Credits
        self.exchange_rates = {
            "blade_runner": 2.5,    # 2.5 Credits = 1 Quantum Credit
            "gta_v": 5.0,           # 5.0 Dollars = 1 Quantum Credit
            "mcu": 4.0,             # 4.0 USD = 1 Quantum Credit
            "doraemon": 120.0,      # 120.0 Yen = 1 Quantum Credit
            "harry_potter": 0.5,    # 0.5 Galleons = 1 Quantum Credit (Galleons are very valuable)
            "dark_netflix": 3.0     # 3.0 Euros = 1 Quantum Credit
        }
        
        # Exchange fee (percentage)
        self.exchange_fee = 10  # 10% fee for currency conversion

    def get_exchange_rate(self, universe_id):
        """Get the exchange rate for a specific universe."""
        return self.exchange_rates.get(universe_id, 1.0)
    
    def local_to_quantum(self, amount, universe_id):
        """Convert local currency to Quantum Credits."""
        if universe_id not in self.exchange_rates:
            return 0
            
        # Apply exchange rate
        quantum_amount = amount / self.exchange_rates[universe_id]
        
        # Apply exchange fee
        fee = quantum_amount * (self.exchange_fee / 100)
        quantum_amount -= fee
        
        return round(quantum_amount, 2)
    
    def quantum_to_local(self, quantum_amount, universe_id):
        """Convert Quantum Credits to local currency."""
        if universe_id not in self.exchange_rates:
            return 0
            
        # Apply exchange rate
        local_amount = quantum_amount * self.exchange_rates[universe_id]
        
        # Apply exchange fee
        fee = local_amount * (self.exchange_fee / 100)
        local_amount -= fee
        
        return round(local_amount)
    
    def display_exchange_rates(self):
        """Display current exchange rates for all universes."""
        result = "\n=== Quantum Credit Exchange Rates ===\n"
        for universe_id, rate in self.exchange_rates.items():
            universe_name = self.universes[universe_id]["name"]
            currency_name = self.universes[universe_id]["currency"]
            result += f"{universe_name}: {rate} {currency_name} = 1 {self.inter_currency['name']} ({self.inter_currency['symbol']})\n"
        
        result += f"\nExchange Fee: {self.exchange_fee}%"
        return result
    
    def calculate_total_quantum_wealth(self, player_data):
        """Calculate the player's total wealth in Quantum Credits across all universes."""
        total_quantum = player_data.get("quantum_credits", 0)
        
        # Add converted value of all local currencies
        for universe_id, universe_data in player_data["universes"].items():
            local_cash = universe_data["cash"]
            quantum_value = self.local_to_quantum(local_cash, universe_id)
            total_quantum += quantum_value
            
        return round(total_quantum, 2)


class QuantumBusinesses:
    """Special businesses that generate Quantum Credits directly."""
    
    def __init__(self):
        """Initialize quantum businesses that work across universes."""
        self.quantum_businesses = {
            "quantum_flux_harvester": {
                "name": "Quantum Flux Harvester",
                "description": "Harvests energy from interdimensional rifts to generate Quantum Credits.",
                "cost": {"quantum_credits": 50},  # Cost in Quantum Credits
                "income_per_turn": 5,  # Quantum Credits per turn
                "risk_increase": 5,
                "requirements": {"total_businesses": 3}  # Requires at least 3 total businesses
            },
            "nexus_trading_post": {
                "name": "Nexus Trading Post",
                "description": "A trading hub located at the intersection of multiple universes.",
                "cost": {"quantum_credits": 100},
                "income_per_turn": 12,
                "risk_increase": 10,
                "requirements": {"reputation": 20}  # Requires reputation of at least 20
            },
            "dimensional_bank": {
                "name": "Dimensional Bank",
                "description": "A secure institution that stores and manages Quantum Credits.",
                "cost": {"quantum_credits": 200},
                "income_per_turn": 25,
                "risk_increase": 15,
                "requirements": {"total_cash": 50000}  # Requires total wealth of at least 50,000
            }
        }
        
    def get_available_businesses(self, player_data, currency_exchange):
        """Get quantum businesses available to the player based on requirements."""
        available = {}
        
        # Calculate total number of businesses across all universes
        total_businesses = sum(
            len(universe_data["businesses"]) 
            for universe_data in player_data["universes"].values()
        )
        
        # Calculate total wealth in local currencies
        total_wealth = currency_exchange.calculate_total_quantum_wealth(player_data)
        
        # Get player's reputation from current universe
        current_universe = player_data["current_universe"]
        reputation = player_data["universes"][current_universe]["reputation"]
        
        # Check each business against requirements
        for business_id, business in self.quantum_businesses.items():
            # Skip if player already owns this quantum business
            if business_id in player_data.get("quantum_businesses", []):
                continue
                
            # Check requirements
            requirements = business["requirements"]
            meets_requirements = True
            
            if "total_businesses" in requirements and total_businesses < requirements["total_businesses"]:
                meets_requirements = False
                
            if "total_cash" in requirements and total_wealth < requirements["total_cash"]:
                meets_requirements = False
                
            if "reputation" in requirements and reputation < requirements["reputation"]:
                meets_requirements = False
                
            # Add to available businesses if requirements are met
            if meets_requirements:
                available[business_id] = business
                
        return available


class QuantumEvents:
    """Special events related to Quantum Credits and interdimensional activity."""
    
    def __init__(self):
        """Initialize quantum events that can occur across universes."""
        self.quantum_events = [
            {
                "name": "Dimensional Rift",
                "description": "A rift between universes has opened, leaking valuable quantum energy.",
                "effect": {"quantum_credits": 10, "danger": 5, "reputation": 0},
                "probability": 0.2
            },
            {
                "name": "Quantum Thief",
                "description": "A notorious interdimensional thief has stolen some of your Quantum Credits!",
                "effect": {"quantum_credits": -15, "danger": 0, "reputation": 0},
                "probability": 0.15
            },
            {
                "name": "Exchange Rate Fluctuation",
                "description": "Interdimensional market fluctuations have affected exchange rates.",
                "effect": {"exchange_rate_modifier": 0.2, "danger": 0, "reputation": 0},
                "probability": 0.25
            },
            {
                "name": "Quantum Trader",
                "description": "A mysterious trader offers to exchange local currency for Quantum Credits at a reduced fee.",
                "effect": {"exchange_fee_reduction": 50, "danger": 0, "reputation": 5},  # 50% fee reduction
                "probability": 0.1
            }
        ]
    
    def get_random_event(self):
        """Get a random quantum event based on probability."""
        import random
        
        # Roll for each event based on its probability
        for event in self.quantum_events:
            if random.random() < event["probability"]:
                return event
                
        # Return None if no event is triggered
        return None