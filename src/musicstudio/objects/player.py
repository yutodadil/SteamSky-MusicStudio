import threading
import time
import logging
from enum import Enum

import musicstudio
from musicstudio.exceptions import ScorePlayerActiveError, WindowNotFoundError

import win32gui
import pydirectinput

logger = logging.getLogger(__file__)

class ScorePlayerState(Enum):
	PLAYER_STOPPED    = 0
	PLAYER_PLAYING    = 1
	PLAYER_PAUSED     = 2    # TODO: need to implement pause feature

class ScorePlayer:
	'''
	This class is responsible for playing scores
	Must automatically handle windows
	'''
	_default_interrupt_function = None

	def __init__(self):
		self.state = ScorePlayerState.PLAYER_STOPPED
		self.score = None
		self.player_break = threading.Event()
		pydirectinput.PAUSE = 0    # Please don't put this to :None:, instead use 0

	def set_state(self, state):
		self.state = state

	def get_state(self):
		return self.state

	def set_score(self, score):
		if self.state == ScorePlayerState.PLAYER_PLAYING:
			raise ScorePlayerActiveError("Cannot select score when player is playing")

		if self.state == ScorePlayerState.PLAYER_PAUSED:
			self.stop()

		self.score = score

	def _press_key(self, key):
		if key in musicstudio.consts.NOTE_KEY_MAPPINGS:
			logger.debug("KeyPress: {}".format(musicstudio.consts.NOTE_KEY_MAPPINGS[key]))
			pydirectinput.press(musicstudio.consts.NOTE_KEY_MAPPINGS[key])
		else:
			logger.warning("f{key} Unknown Key")

	def _interrupt(self):
		if self.state == self._interrupt_type:
			return

		self.set_state(self._interrupt_type)
		self.player_break.set()

	def _paused(self):
		self.player_break.clear()
		self.player_break.wait()

	def _play(self, stop_callback):
		'''
		The actual function that plays the score

		NOTE: Don't remove this function and keep it seperate from `play()` function
		      because we need to change this to non-ui-blocking function
		'''

		self.set_state(ScorePlayerState.PLAYER_PLAYING)

		start_time = time.monotonic() * 1000    # Don't ask why `time.monotonic()`

		total_notes = len(self.score.song_notes)
		for i, note in enumerate(self.score.song_notes):
			key = note["key"]
			if key.startswith("2Key"):
				key = key.replace("2Key", "1Key")

			elapsed_time = time.monotonic() * 1000 - start_time
			time_to_wait = note["time"] - elapsed_time
			progress = (i + 1) / total_notes * 100

			if time_to_wait > 0:
				self.player_break.wait(time_to_wait / 1000)

				if self.player_break.is_set():
					if self.state == ScorePlayerState.PLAYER_PAUSED:
						self._paused()

					if self.state == ScorePlayerState.PLAYER_STOPPED:
						break

					self.player_break.clear()

				if self.current_hwnd != win32gui.GetForegroundWindow():
					# Here we could implement something like pausing the player when window changes
					# but this is an idea for the next time :)
					logger.warning("Window changed before the score is completed")
					break

			end_time = self.score.song_notes[-1]["time"]

			logger.debug(f"Player: [{progress:.2f}%] Press Key {key} at {musicstudio.utils.format_time(int(elapsed_time))}/{musicstudio.utils.format_time(int(end_time))}")
			self._press_key(key)

		if self.player_break.is_set():
			self.player_break.clear()
		else:
			self.set_state(ScorePlayerState.PLAYER_STOPPED)

		if callable(stop_callback):
			stop_callback()

	def play(self, stop_callback = None):
		window_name = "Sky"

		hwnd = win32gui.FindWindow(None, window_name)
		if hwnd == 0:
			logger.warning("HWND of \"{}\" wasn't found, trying another method...".format(window_name))
			hwnd = win32gui.FindWindowEx(None, None, None, window_name)

			if hwnd == 0:
				raise WindowNotFoundError(window_name)

		logger.debug("Player: HWND: \"{}\" -> {}".format(window_name, hwnd))

		win32gui.SetForegroundWindow(hwnd)
		self.current_hwnd = hwnd

		if self.state == ScorePlayerState.PLAYER_PAUSED:
			self.state = ScorePlayerState.PLAYER_PLAYING
			self.player_break.set()
			return

		threading.Thread(target = self._play, args = (stop_callback,)).start()

	def stop(self):
		if (self.state != ScorePlayerState.PLAYER_STOPPED):
			self._interrupt_type = ScorePlayerState.PLAYER_STOPPED
			self._interrupt()

	def pause(self):
		if (self.state != ScorePlayerState.PLAYER_PAUSED):
			self._interrupt_type = ScorePlayerState.PLAYER_PAUSED
			self._interrupt()
