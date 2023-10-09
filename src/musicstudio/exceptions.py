class LocalizationError(Exception):
	'''
	Raised when given language localization doesn't exist
	'''

	def __init__(self, language = None):
		if not language:
			super().__init__("Unknown localization")
			return

		super().__init__("Localization '{}' doesn't exist".format(language))


class ScoreParseError(Exception):
	'''
	Raised when parsing score files wasn't successful (aka :class:`json.JSONDecodeError`)
	'''

	def __init__(self, score_path, json_error = None):
		if json_error is None:
			super().__init__("Couldn't parse score file: {}".format(score_path))
			return

		super().__init__("Couldn't parse score file: {}\n{}".format(score_path, json_error))


class ScoreDataError(Exception):
	'''
	Raised if score has wrong structure
	'''

	def __init__(self, score_path, pos = None, reason = None):
		if reason is None:
			if pos is None:
				super().__init__("{} has wrong structure".format(score_path))
				return

			super().__init__("{} has wrong structure at position {}".format(score_path, pos))

		super().__init__("Score file structure error\nScore: {}\nPos: {}\nReason: {}".format(score_path, pos, reason))


class ScorePlayerActiveError(Exception):
	'''
	Raised when trying to change :class:`ScorePlayer`'s properties when it was active
	'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class WindowNotFoundError(Exception):
	'''
	Raised when `win32gui` couldn't find `window_name` window
	'''

	def __init__(self, window_name):
		super().__init__("Window with name \"{}\" wasn't found".format(window_name))