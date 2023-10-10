import json
import chardet
import logging

from musicstudio.exceptions import ScoreParseError, ScoreDataError

logger = logging.getLogger(__file__)

class Score:
	'''
	This is a model/class of score

	It stores:
	- ``title`` Score Title -> string
	- ``author`` Music author name -> string
	- ``transcribed_by`` Score transcriber name -> string
	- ``is_composed`` -> bool
	- ``bpm`` BPM -> int
	- ``bits_per_page`` Bits per Page -> int
	- ``pitch_level`` Pitch Level -> int
	- ``is_encrypted`` -> bool
	- ``song_notes`` -> array of dicts
	'''

	def __init__(self, score_path):
		self.score_path = score_path

	@property
	def score_path(self):
		return self._score_path

	@score_path.setter
	def score_path(self, value):
		self._score_path = value
		self.reload()

	def raise_for_structure(self, json_data):
		'''
		Raise exception if important fields don't exist
		'''

		while True:
			if not "bpm" in json_data:
				break

			if not "bitsPerPage" in json_data:
				break

			if not "songNotes" in json_data:
				break

			return

		raise ScoreDataError(self.score_path)

	def reload(self):
		json_data = None
		data = None

		with open(self.score_path, "rb") as file:
			data = file.read()

		try:
			json_data = json.loads(data.decode("cp1251"))
		except json.JSONDecodeError as e:
			logger.debug("Score: Trying to detect encoding of: {}".format(self.score_path))

			res = chardet.detect(data)
			encoding = res.get("encoding", None)
			logger.debug("Score: Got encoding: {}".format(encoding))

			if not encoding:
				raise ScoreParseError(e)

			encoding = encoding.lower().replace(" ", "-")

			try:
				json_data = json.loads(data.decode(encoding))

			except json.JSONDecodeError as e2:
				raise ScoreParseError(e2)

		if type(json_data) is list:
			if len(json_data) > 0:
				json_data = json_data[0]
			else:
				raise ScoreDataError(self.score_path)

		self.raise_for_structure(json_data)

		self.title = json_data.get("name", "Unknown")
		self.author = json_data.get("author", "Unknown")
		self.transcribed_by = json_data.get("transcribedBy", "Unknown")
		self.is_composed = json_data.get("isComposed", True)
		self.bpm = json_data["bpm"]
		self.bits_per_page = json_data["bitsPerPage"]
		self.pitch_level = json_data.get("pitchLevel", 0)
		self.is_encrypted = json_data.get("isEncrypted", False)
		self.song_notes = json_data["songNotes"]