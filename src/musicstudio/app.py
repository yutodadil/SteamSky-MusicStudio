import os
import logging
import importlib

import musicstudio
from musicstudio.exceptions import *

if True:
    from kivy.core.window import Window
    Window.size = (1024, 600)

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.uix.screenmanager import FadeTransition

from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

from .objects.score import Score

from .widgets.ScoreItem import ScoreItem

logger = logging.getLogger(__file__)


class MainScreenManager(MDScreenManager):
    '''
    Screen managers are responsible for changing screens, so they are "must be"
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MainScreen(MDScreen):
    '''
    This is main screen :P
    '''
    nav_drawer = ObjectProperty(None)

    def _initialize(self, delta = None):
        self.nav_drawer.set_state("open")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self._initialize)


class InnerMainScreenManager(MDScreenManager):
    '''
    This screen manager will be used more than `MainScreenManager`
    because we need to change screens but remain `MDNavigationLayout` untouched
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def change_screen(self, screen_name):
        self.current = screen_name


class InnerMainScreen(MDScreen):
    '''
    This screen will be inside :class:`MDNavigationLayout`
    '''

    scores_list = ObjectProperty(None)
    current_score_title = ObjectProperty(None)
    stop_button = ObjectProperty(None)
    play_button = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self):
        '''
        This function is called everytime we enter this screen
        '''

        # idk if we should enable this here...
        # self.reload_scores()

        return

    def reload_scores(self):
        score_item_index = 0
        score_items_count = len(self.scores_list.children)

        for root, dirs, files in os.walk(musicstudio.scores_path):
            for filename in files:
                if filename.endswith((".json", ".txt")):    # scores must be in json format
                    score_path = os.path.join(root, filename)

                    try:
                        if score_item_index < score_items_count:
                            self.scores_list.children[score_item_index].score.score_path = score_path
                            score_item_index += 1
                            continue

                        score = Score(score_path)
                        score_item = ScoreItem(score, on_release = lambda instance : self.on_score_select(instance))
                        self.scores_list.add_widget(score_item)

                    except ScoreParseError as e:
                        logger.error(e)

                    except ScoreDataError as e:
                        logger.error(e)

            break    # Folders inside `musicstudio.scores_path` path are not allowed X

        if score_item_index < score_items_count:
            # Remove unused widgets
            while score_items_count > score_item_index:
                score_items_count -= 1
                self.scores_list.remove_widget(self.scores_list.children[score_items_count])

    def on_score_select(self, score_item):
        if musicstudio.current_app.set_current_score_item(score_item):
            self.current_score_title.text = score_item.score.title
            self.play_button.disabled = False

    def _stop_callback(self):
        self.stop_button.disabled = True
        self.play_button.disabled = False

    def play(self):
        self.stop_button.disabled = False
        self.play_button.disabled = True

        try:
            musicstudio.player.play(self._stop_callback)
        except WindowNotFoundError:
            self.stop()
            musicstudio.current_app.show_alert_dialog("Process not found")

    def stop(self):
        self.stop_button.disabled = True
        self.play_button.disabled = False
        musicstudio.player.stop()

class SteamSkyMusicStudioGUI(MDApp):
    dialog = None
    inner_main_screen_manager = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set title here
        self.title = "Sky Music Studio"
        self.localization = musicstudio.Localization("EN")

        self._current_score_item = None

        resource_add_path(os.path.join(musicstudio.assets_path, "fonts"))
        LabelBase.register(DEFAULT_FONT, fn_regular="NotoSansCJK-Regular.ttc")

    def _load_kvs(self):
        '''
        Here we load all '.kv' files from 'kv' folder

        .kv is a kivy designing language extension which allows creating
        widgets, screens and other design related things much faster and easier
        '''

        for root, dirs, files in os.walk(musicstudio.kv_path):
            for filename in files:
                if filename.endswith(".kv"):
                    # if you want to print something, consider use `logger.debug(...)`
                    logger.debug("KV: {}".format(filename))
                    Builder.load_file(os.path.join(root, filename))

    def _load_widgets_and_screens(self):
        for root, dirs, files in os.walk(os.path.join(musicstudio.app_path, "widgets")):
            for filename in files:
                if filename.endswith(".py"):
                    logger.debug("Loading Widget: {}".format(filename))
                    widget_name = filename[:-3]
                    importlib.import_module(".widgets.%s" % widget_name, musicstudio.__name__)

        for root, dirs, files in os.walk(os.path.join(musicstudio.app_path, "screens")):
            for filename in files:
                if filename.endswith("Screen.py"):
                    logger.debug("Loading Screen: {}".format(filename))
                    widget_name = filename[:-3]
                    importlib.import_module(".screens.%s" % widget_name, musicstudio.__name__)

    def set_current_score_item(self, score_item):
        '''
        Return False if `score_item` is already `self._current_score_item`, otherwise True
        '''
        if score_item is self._current_score_item:
            return False

        try:
            musicstudio.player.set_score(score_item.score)
        except ScorePlayerActiveError:
            return False

        if self._current_score_item:
            self._current_score_item.text_color = self.theme_cls.text_color

        self._current_score_item = score_item
        self._current_score_item.text_color = self.theme_cls.primary_color
        logger.debug("Current score item \"{}\"".format(self._current_score_item.score.title))

        return True

    def get_current_score_item(self):
        return self._current_score_item

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self._load_widgets_and_screens()
        self._load_kvs()

        self.main_screen_manager = MainScreenManager()
        self.inner_main_screen_manager = self.main_screen_manager.get_screen("main_screen").ids.inner_main_screen_manager

        self.inner_main_screen_manager.get_screen("inner_main_screen").reload_scores()

        return self.main_screen_manager

    def change_screen(self, screen_name):
        self.main_screen_manager.current = screen_name

    def change_inner_screen(self, screen_name):
        self.inner_main_screen_manager.change_screen(screen_name)

    def show_alert_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text = message,
                buttons = [
                    MDFlatButton(
                        text = self.localization.OK,
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = (lambda x : self.dialog.dismiss())
                    )
                ]
            )

        else:
            self.dialog.text = message

        self.dialog.open()

if __name__ == "__main__":
    raise RuntimeError("This file must not be ran directly")

musicstudio.current_app = SteamSkyMusicStudioGUI()