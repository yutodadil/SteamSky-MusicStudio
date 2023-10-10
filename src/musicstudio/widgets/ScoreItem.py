from kivymd.uix.list import TwoLineIconListItem

class ScoreItem(TwoLineIconListItem):
	'''
	This is widget of score
	Holds one score object
	'''

	def __init__(self, score, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.score = score

	@property
	def score(self):
		return self._score

	@score.setter
	def score(self, value):
		self._score = value

		self.reload()

	def reload(self):
		score = self.score

		self.text = score.title
		self.secondary_text = score.author