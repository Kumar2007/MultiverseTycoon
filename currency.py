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
            "john_wick": 1.0,       # 1.0 Gold Coin = 1 Quantum Credit (Gold Coins are very valuable)
            "monsterverse": 4.5     # 4.5 USD = 1 Quantum Credit
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