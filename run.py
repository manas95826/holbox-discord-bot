import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.bot.bot import CommunityBot

def main():
    bot = CommunityBot()
    bot.run()

if __name__ == "__main__":
    main() 