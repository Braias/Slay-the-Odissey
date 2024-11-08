import unittest
import sys
from pathlib import Path

game_dir = Path(__file__).parent.parent
sys.path.append("game_dir/src")

from deck import Deck