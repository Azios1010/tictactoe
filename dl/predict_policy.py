from __future__ import annotations

import os
from pathlib import Path
from typing import Any

# Check if PyTorch is available, if not, we degrade gracefully
try:
    import numpy as np
    import torch
    from dl.model import PolicyValueNet

    TORCH_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    TORCH_AVAILABLE = False

BOARD_SIZE = 15
PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_PATHS = (
    PROJECT_DIR / "model" / "consultant_model.pt",
    PROJECT_DIR / "backend" / "consultant_model.pt",
)
MODEL_PATH_ENV = "GOMOKU_CONSULTANT_MODEL_PATH"


def resolve_model_path() -> Path:
    configured_path = os.getenv(MODEL_PATH_ENV)
    if configured_path:
        return Path(configured_path).expanduser().resolve()

    for model_path in DEFAULT_MODEL_PATHS:
        if model_path.exists():
            return model_path

    return DEFAULT_MODEL_PATHS[0]


def load_checkpoint(torch_module: Any, model_path: Path, device: Any) -> Any:
    try:
        return torch_module.load(model_path, map_location=device, weights_only=True)
    except TypeError:
        return torch_module.load(model_path, map_location=device)


def encode_board(board_arr: np.ndarray) -> np.ndarray:
    # Channel 0: Active player's stones (1)
    # Channel 1: Opponent's stones (-1)
    # Channel 2: Empty squares (0)
    x = np.zeros((3, BOARD_SIZE, BOARD_SIZE), dtype=np.float32)
    x[0] = board_arr == 1
    x[1] = board_arr == -1
    x[2] = board_arr == 0
    return x


def mask_illegal_logits(logits: torch.Tensor, occupied: torch.Tensor) -> torch.Tensor:
    return logits.masked_fill(occupied.to(dtype=torch.bool, device=logits.device), -1e9)


class ConsultantPredictor:
    _instance: ConsultantPredictor | None = None
    model: Any = None
    device: Any = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not TORCH_AVAILABLE or self.model is not None:
            return

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = resolve_model_path()
        if not model_path.exists():
            return

        try:
            checkpoint = load_checkpoint(torch, model_path, self.device)
            # Support loading both checkpoints containing state_dict and raw state dicts
            state_dict = (
                checkpoint.get("model_state_dict", checkpoint)
                if isinstance(checkpoint, dict)
                else checkpoint
            )

            model = PolicyValueNet(board_size=BOARD_SIZE)
            model.load_state_dict(state_dict)
            model.to(self.device)
            model.eval()
            self.model = model
        except Exception as e:
            print(f"Warning: Failed to load consultant model: {e}")
            self.model = None

    def predict(self, board: list[list[int]], player: int, top_k: int = 3) -> dict[str, Any]:
        if not TORCH_AVAILABLE or self.model is None:
            return {"moves": [], "value": 0.0, "model_available": False}

        try:
            # 1. Perspective normalization: active player is always 1, opponent is -1
            board_arr = np.array(board, dtype=np.int8)
            normalized_board = board_arr * player

            # 2. Masking occupied positions (any position that is not EMPTY (0) in the original board)
            occupied_flat = board_arr.reshape(-1) != 0
            occupied_tensor = torch.from_numpy(occupied_flat).unsqueeze(0).to(self.device)

            # 3. Encode input map (3, 15, 15)
            x = encode_board(normalized_board)
            x_tensor = torch.from_numpy(x).unsqueeze(0).to(self.device)

            with torch.no_grad():
                logits, value_tensor = self.model(x_tensor)
                # Apply logit masking on occupied squares
                masked_logits = mask_illegal_logits(logits, occupied_tensor)
                probs = masked_logits.softmax(dim=1)[0]
                value = float(value_tensor.item())

            # 4. Extract top K legal moves
            actual_k = min(top_k, int((~occupied_flat).sum()))
            if actual_k <= 0:
                return {"moves": [], "value": value, "model_available": True}

            top_indices = probs.topk(actual_k).indices.cpu().numpy().tolist()
            top_probs = probs.topk(actual_k).values.cpu().numpy().tolist()

            recommended_moves = []
            for rank, (idx, prob) in enumerate(zip(top_indices, top_probs), 1):
                row, col = divmod(idx, BOARD_SIZE)
                recommended_moves.append(
                    {
                        "row": row,
                        "col": col,
                        "probability": float(prob),
                        "rank": rank,
                    }
                )

            return {
                "moves": recommended_moves,
                "value": value,
                "model_available": True,
            }
        except Exception as e:
            print(f"Error during consultant model inference: {e}")
            return {"moves": [], "value": 0.0, "model_available": True}


def predict_top_moves(board: list[list[int]], player: int, top_k: int = 3) -> dict[str, Any]:
    predictor = ConsultantPredictor()
    return predictor.predict(board, player, top_k)
