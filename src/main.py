import musicstudio
from musicstudio.objects import player

def main():
	musicstudio.current_app.run()

	# Stop player if it was running, or else window will hang without closing
	if musicstudio.player.get_state() != player.ScorePlayerState.PLAYER_STOPPED:
		musicstudio.player.stop()

if __name__ == '__main__':
	main()