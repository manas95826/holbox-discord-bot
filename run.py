import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from bot.bot import CommunityBot

def main():
    bot = CommunityBot()
    bot.run()

if __name__ == "__main__":
    main() 