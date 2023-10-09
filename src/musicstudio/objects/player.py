import threading    # no reason to remove this line, next plan is to make score playing seperate from main thread
import time
import logging
from enum import Enum

import musicstudio
from musicstudio.exceptions import ScorePlayerActiveError, WindowNotFoundError

import win32gui
import pyautogui

logger = logging.getLogger(__file__)

class ScorePlayerState(Enum):
	PLAYER_IDLE    = 0
	PLAYER_PLAYING = 1
	PLAYER_PAUSE   = 2    # TODO: need to implement pause feature

class ScorePlayer:
	'''
	This class is responsible for playing scores
	Must automatically handle windows
	'''
	def __init__(self):
		self.state = ScorePlayerState.PLAYER_IDLE
		self.score = None

	def set_state(self, state):
		self.state = state

	def get_state(self):
		return self.state

	def set_score(self, score):
		if self.state != ScorePlayerState.PLAYER_IDLE:
			raise ScorePlayerActiveError("Cannot set `score` when `ScorePlayer.state != ScorePlayerState.PLAYER_IDLE`")

		self.score = score

	def _press_key(self, key):
		if key in musicstudio.consts.NOTE_KEY_MAPPINGS:
			pyautogui.press(musicstudio.consts.NOTE_KEY_MAPPINGS[key])
		else:
			logger.warning("f{key} Unknown Key")

	def _play(self, stop_callback):
		'''
		The actual function that plays the score

		NOTE: Don't remove this function and keep it seperate from `play()` function
		      because we need to change this to non-ui-blocking event driven function
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
				time.sleep(time_to_wait / 1000)
				if hwnd != win32gui.GetForegroundWindow():
					# Here we could implement something like pausing the player when window changes
					# but this is an idea for the next time :)
					logger.warning("Window changed before the score is completed")
					break

			end_time = self.score.song_notes[-1]["time"]
			logger.debug(f"[{progress:.2f}%] Press Key {key} at {musicstudio.utils.format_time(int(elapsed_time))}/{musicstudio.utils.format_time(int(end_time))}")
			self._press_key(key)

		if callable(stop_callback):
			stop_callback()

		self.stop()

	def play(self, stop_callback = None):
		window_name = "Sky"
		hwnd = win32gui.FindWindow(None, window_name)
		if hwnd == 0:
			logger.warning("HWND of \"{}\" wasn't found, trying another method...".format(window_name))
			hwnd = win32gui.FindWindowEx(None, None, None, window_name)

			if hwnd == 0:
				raise WindowNotFoundError(window_name)

		logger.debug("HWDN: \"{}\" -> {}".format(window_name, hwnd))

		win32gui.SetForegroundWindow(hwnd)

		self._play(stop_callback)

	def stop(self):
		self.set_state(ScorePlayerState.PLAYER_IDLE)

	def pause(self):
		raise NotImplementedError()