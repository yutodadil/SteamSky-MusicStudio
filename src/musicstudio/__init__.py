import os
import sys

IS_EXE = False
exe_path = None
app_path = os.path.dirname(__file__)
project_root = None
assets_path = None
scores_path = None
kv_path = None

# check if application is an '.exe' file
if getattr(sys, 'frozen', False):
	IS_EXE = True
	project_root = sys._MEIPASS    # This will be new project root
	exe_path = sys.executable
	scores_path = os.path.join(os.path.dirname(exe_path), "scores")    # store scores near exe file
else:
	project_root = os.path.dirname(app_path)
	project_root = os.path.dirname(project_root)
	scores_path = os.path.join(project_root, "scores")

assets_path = os.path.join(project_root, "assets")
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