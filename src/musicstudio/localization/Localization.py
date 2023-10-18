import os
import toml
import musicstudio
import musicstudio.exceptions

class _LocalizationBase:
	EN = {
		"HOME": "Home",
		"INSTRUMENT": "Instrument",
		"INSTRUMENTS": "Instruments",
		"SETTINGS": "Settings",
		"PLAY": "Play %s",
		"PAUSE": "Pause %s",
		"STOP": "Stop %s",
		"ADD": "Add",
		"REMOVE": "Remove",
		"ADD_FILE": "Add File",
		"ADD_SCORE": "Add Score",
		"RANDOM": "Random",
		"SELECT": "Select",
		"PLAY_RANDOM_SCORE": "Play Random Score",
		"NO_SCORE_SELECTED": "[No Score Selected]",
		"OK": "Ok",
		"CANCEL": "Cancel",
		"CLOSE": "Close"
	}

class Localization:
	def __init__(self, language="EN"):
		self.set_localization(language)

	def set_localization(self, language):
		if not hasattr(_LocalizationBase, language):
			raise musicstudio.exceptions.LocalizationError(language)

		self.language = language

		config_dir = os.path.join(musicstudio.assets_path, "config")
		config_file = os.path.join(config_dir, "config.toml")
		hotkeys = self.load_hotkeys(config_file)

		lang = getattr(_LocalizationBase, language)

		for key, value in lang.items():
			if "%s" in value:
				hotkey = hotkeys.get(key.lower(), "")
				setattr(self, key, value % hotkey)
			else:
				setattr(self, key, value)

	def load_hotkeys(self, config_file):
		hotkeys = {}
		if os.path.exists(config_file):
			config = toml.load(config_file)
			key_section = config.get("key", {})
			for action, hotkey in key_section.items():
				hotkeys[action.lower()] = hotkey
		return hotkeys
