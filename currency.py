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
            "dark_netflix": 3.0,    # 3.0 Euros = 1 Quantum Credit
            "john_wick": 1.0,       # 1.0 Gold Coin = 1 Quantum Credit (Gold Coins are very valuable)
            "monsterverse": 4.5     # 4.5 USD = 1 Quantum Credit
        }
        
        # Exchange fee (percentage)
        self.exchange_fee = 10  # 10% fee for currency conversion