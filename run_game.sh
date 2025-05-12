#!/bin/bash
echo "Starting Multiverse Tycoon..."

# Check if the executable exists
if [ -f "dist/MultiVerseTycoon" ]; then
    # Make sure it's executable
    chmod +x dist/MultiVerseTycoon
    
    # Run the game
    ./dist/MultiVerseTycoon
else
    echo "MultiVerseTycoon executable not found in dist directory."
    echo "Please build the game first by running: python3 build.py"
fi

echo "Press Enter to exit..."
read