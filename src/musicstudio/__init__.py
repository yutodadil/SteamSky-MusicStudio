import os

app_path = os.path.dirname(__file__)
project_root = os.path.dirname(app_path)
project_root = os.path.dirname(project_root)

assets_path = os.path.join(project_root, "assets")
scores_path = os.path.join(project_root, "scores")
kv_path = os.path.join(project_root, "kv")

current_app = None

from .localization.Localization import Localization
from .objects.player import ScorePlayer
from .util import Utils
from .consts import MusicStudioConsts

player = ScorePlayer()
utils = Utils
consts = MusicStudioConsts

__all__ = (
	"current_app", "project_root",
	"assets_path", "scores_path", "kv_path",
	"player", "utils", "consts",

	"Localization"
)


# put this in the end, because app can use everything above
from . import app