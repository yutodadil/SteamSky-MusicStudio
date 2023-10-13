import musicstudio.exceptions

class _LocalizationBase:
	EN = {
		"HOME" : "Home",
		"INSTRUMENT" : "Instrument",
		"INSTRUMENTS" : "Instruments",
		"SETTINGS" : "Settings",
		"PLAY" : "Play",
		"PAUSE" : "Pause",
		"STOP" : "Stop",
		"ADD" : "Add",
		"REMOVE" : "Remove",
		"ADD_FILE" : "Add File",
		"ADD_SCORE" : "Add Score",
		"RANDOM" : "Random",
		"SELECT" : "Select",
		"PLAY_RANDOM_SCORE" : "Play Random Score",
		"NO_SCORE_SELECTED" : "[No Score Selected]",

		"OK" : "Ok",
		"CANCEL" : "Cancel",
		"CLOSE" : "Close"
	}

class Localization:
	def __init__(self, language = "EN"):
		self.set_localization(language)

	def set_localization(self, language):
		if not hasattr(_LocalizationBase, language):
			raise musicstudio.exceptions.LocalizationError(language)

		self.language = language

		lang = getattr(_LocalizationBase, language)

		for key, value in lang.items():
			setattr(self, key, value)