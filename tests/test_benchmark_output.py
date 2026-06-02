from __future__ import annotations

import unittest

from benchmark_ai import summarize_accuracy


class BenchmarkOutputTest(unittest.TestCase):
    def test_summarize_accuracy_by_agent_ignores_cases_without_expected_moves(self) -> None:
        rows = [
            {"agent": "project_easy", "expected_moves": [[7, 7]], "is_correct": True},
            {"agent": "project_easy", "expected_moves": [[6, 4]], "is_correct": False},
            {"agent": "project_easy", "expected_moves": [], "is_correct": None},
            {"agent": "project_hard", "expected_moves": [[7, 7]], "is_correct": True},
        ]

        self.assertEqual(
            summarize_accuracy(rows),
            {
                "project_easy": {"correct": 1, "total": 2, "accuracy": 0.5},
                "project_hard": {"correct": 1, "total": 1, "accuracy": 1.0},
            },
        )
