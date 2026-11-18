"""Leitura e gravação dos desbloqueios da campanha."""
import json
import sys

from riffrun.paths import PROJECT_DIR
from riffrun.settings import CAMPAIGN_PHASES

PROGRESS_PATH = PROJECT_DIR / "progress.json"
WEB_PROGRESS_KEY = "riff-run.progress"


def load_unlocked_phases():
    try:
        if sys.platform == "emscripten":
            from platform import window

            saved = window.localStorage.getItem(WEB_PROGRESS_KEY)
        else:
            saved = PROGRESS_PATH.read_text(encoding="utf-8")
        progress = json.loads(saved) if saved else None
        if not isinstance(progress, dict):
            return 1

        return max(
            1,
            min(CAMPAIGN_PHASES, int(progress.get("unlocked_phases", 1)))
        )

    except (OSError, ValueError, TypeError, RuntimeError):
        return 1


def save_unlocked_phases(unlocked_phases):
    try:
        saved = json.dumps({"unlocked_phases": unlocked_phases}, indent=2)
        if sys.platform == "emscripten":
            from platform import window

            window.localStorage.setItem(WEB_PROGRESS_KEY, saved)
        else:
            PROGRESS_PATH.write_text(saved, encoding="utf-8")
    except (OSError, RuntimeError):
        print("Não foi possível salvar o progresso.")
