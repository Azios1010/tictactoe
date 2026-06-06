from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import BOARD_SIZE, EMPTY
import dl.predict_policy as predict_policy
import main


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


class ConsultantApiTest(unittest.TestCase):
    def test_consultation_endpoint_returns_fallback_when_model_missing(self) -> None:
        payload = {
            "board": empty_board(),
            "player": 1,
            "top_k": 3,
        }

        # Call the endpoint directly
        request = main.ConsultationRequest(**payload)
        missing_model = ROOT_DIR / "model" / "missing-consultant-model.pt"
        predict_policy.ConsultantPredictor._instance = None
        predict_policy.ConsultantPredictor.model = None
        with patch.dict("os.environ", {predict_policy.MODEL_PATH_ENV: str(missing_model)}):
            response = main.get_consultation(request)

        # With the model path forced to a missing file, the endpoint should
        # degrade gracefully and return model_available=False.
        self.assertFalse(response.model_available)
        self.assertEqual(len(response.moves), 0)

    def test_request_validation_for_invalid_board(self) -> None:
        # Invalid board size
        invalid_board = [[0, 0], [0, 0]]
        payload = {
            "board": invalid_board,
            "player": 1,
            "top_k": 3,
        }

        with self.assertRaises(ValueError):
            main.ConsultationRequest(**payload)

    def test_resolve_model_path_prefers_trained_model_directory(self) -> None:
        expected_path = ROOT_DIR / "model" / "consultant_model.pt"

        self.assertEqual(predict_policy.resolve_model_path(), expected_path)

    def test_load_checkpoint_uses_weights_only_when_supported(self) -> None:
        class FakeTorch:
            def __init__(self) -> None:
                self.kwargs = None

            def load(self, path: Path, **kwargs):
                self.kwargs = kwargs
                return {"model_state_dict": {}}

        fake_torch = FakeTorch()

        result = predict_policy.load_checkpoint(fake_torch, Path("model.pt"), "cpu")

        self.assertEqual(result, {"model_state_dict": {}})
        self.assertEqual(fake_torch.kwargs, {"map_location": "cpu", "weights_only": True})
