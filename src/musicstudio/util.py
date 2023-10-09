class Utils():
	'''
	Class that provides various useful functions

	NOTE: It *must not* know anything about GUI. All GUI operations
		  should be done in :class:`MDApp` class (aka `musicstudio.current_app`)
	'''

	@staticmethod
	def format_time(milliseconds):
		seconds, milliseconds = divmod(milliseconds, 1000)
		minutes, seconds = divmod(seconds, 60)
		hours, minutes = divmod(minutes, 60)
		
		if hours == 0:
			return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
		else:
			return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"