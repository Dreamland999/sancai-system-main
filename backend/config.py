import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

# 显式加载 .env，确保无论从哪个目录启动都能读到
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(BACKEND_DIR / ".env", override=True)

DB_PATH = str(PROJECT_ROOT / "data" / "sancai.db")

CSV_FILES = {
    "tags": str(PROJECT_ROOT / "data" / "标签字典表_最终检查版.csv"),
    "ingredients": str(PROJECT_ROOT / "data" / "饮品成分表_最终检查版.csv"),
    "recipes": str(PROJECT_ROOT / "data" / "饮品方案表_最终检查版.csv"),
}

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-pro")

LLM_MOCK_MODE = os.environ.get("LLM_MOCK_MODE", "false").lower() in ("1", "true", "yes")

WANXIANG_API_KEY = os.environ.get("WANXIANG_API_KEY", "")

IMAGE_MOCK_MODE = os.environ.get("IMAGE_MOCK_MODE", "false").lower() == "true"

TOP_K = 3
RECALL_SIZE = 30

SCORE_WEIGHTS = {
    "state_match": 0.30,
    "flavor": 0.20,
    "scene": 0.15,
    "health": 0.25,
    "visual": 0.10,
}

MODEL_DIR = str(PROJECT_ROOT / "algorithm")
TWIN_TOWER_MODEL = os.path.join(MODEL_DIR, "twin_tower_model.pt")
MLP_RANKER_MODEL = os.path.join(MODEL_DIR, "mlp_ranker_model.pt")
VOCAB_PATH = os.path.join(MODEL_DIR, "twin_tower_vocab.json")
