import os
import json
import win32gui
import pyautogui
import time
import random
import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

pyautogui.PAUSE = 0

class SteamSkyMusicStudioGUI(App):
    def build(self):
        self.title = "SteamSky Music Studio"
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        resource_add_path('./fonts')
        LabelBase.register(DEFAULT_FONT, fn_regular="NotoSansCJK-Regular.ttc")

        self.file_chooser = FileChooserListView(
            path="./score",
            filters=["*.json", "*.txt"],
        )
        self.layout.add_widget(self.file_chooser)

        self.run_button = Button(text="Run", size_hint=(None, None), size=(100, 30))
        self.run_button.bind(on_release=self.run_music)
        self.random_button = Button(text="Random", size_hint=(None, None), size=(100, 30))
        self.random_button.bind(on_release=self.select_random_score)
        
        self.layout.add_widget(self.run_button)
        self.layout.add_widget(self.random_button)

        return self.layout

    def show_error_popup(self, message):
        popup = Popup(
            title="Error",
            content=BoxLayout(orientation="vertical"),
            size_hint=(None, None),
            size=(300, 150)
        )

        label = Label(text=message)
        ok_button = Button(text="OK")
        ok_button.bind(on_release=popup.dismiss)

        popup.content.add_widget(label)
        popup.content.add_widget(ok_button)

        popup.open()

    def press_key(self, key):
        key_mappings = {
            "1Key0": "Y", "1Key1": "U", "1Key2": "I", "1Key3": "O",
            "1Key4": "P", "1Key5": "H", "1Key6": "J", "1Key7": "K",
            "1Key8": "L", "1Key9": ":", "1Key10": "N", "1Key11": "M",
            "1Key12": ",", "1Key13": ".", "1Key14": "/"
        }
        if key in key_mappings:
            pyautogui.press(key_mappings[key])
        else:
            print(f"{key} UnknownKey")

    def play_score(self, file_path):
        score_data = self.load_score_file(file_path)

        if score_data and isinstance(score_data, list):
            hwnd = win32gui.FindWindow(None, "Sky")
            if hwnd == 0:
                self.show_error_popup("Process Not Found")
                return

            win32gui.SetForegroundWindow(hwnd)
            start_time = time.time() * 1000

            for i, note in enumerate(score_data[0]["songNotes"]):
                key = note["key"]
                if key.startswith("2Key"):
                    key = key.replace("2Key", "1Key")

                self.press_key(key)

                if i + 1 < len(score_data[0]["songNotes"]):
                    next_note = score_data[0]["songNotes"][i + 1]
                    elapsed_time = time.time() * 1000 - start_time
                    time_to_wait = next_note["time"] - elapsed_time
                    if time_to_wait > 0:
                        time.sleep(time_to_wait / 1000)
        else:
            self.show_error_popup("Sorry, Not Supported This File")

    def load_score_file(self, file_path):
        try:
            with open(file_path, "rb") as file:
                content = file.read().decode("utf-16-le", errors="ignore").lstrip("\ufeff")
            return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.show_error_popup(f"Error reading file: {str(e)}")
            return None

    def run_music(self, instance):
        selected_file = self.file_chooser.selection and self.file_chooser.selection[0]
        if selected_file:
            self.play_score(selected_file)

    def select_random_score(self, instance):
        score_files = self.file_chooser.get_files("./score", filters=["*.json", "*.txt"])
        if score_files:
            random_file = random.choice(score_files)
            self.play_score(random_file)

if __name__ == "__main__":
    SteamSkyMusicStudioGUI().run()
