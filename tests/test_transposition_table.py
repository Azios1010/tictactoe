from __future__ import annotations

import pickle
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import GomokuAI


class TranspositionTableTest(unittest.TestCase):
    def test_load_memory_accepts_entries_with_cached_best_move(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "gomoku_tt.pkl"
            payload = {
                "version": GomokuAI.MEMORY_VERSION,
                "entries": {
                    123: (2, 42.5, GomokuAI.EXACT, (6, 7)),
                },
            }
            with cache_path.open("wb") as handle:
                pickle.dump(payload, handle)

            ai = GomokuAI(memory_filename=cache_path)

            self.assertEqual(ai.transposition_table[123], (2, 42.5, GomokuAI.EXACT, (6, 7)))
