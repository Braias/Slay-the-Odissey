import unittest
import sys
from pathlib import Path

game_dir = Path(__file__).parent.parent
sys.path.append(f"{game_dir}/src")

from world_level import CombatLevel
