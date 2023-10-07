import os
import json
import win32gui
import pyautogui
import time
import random
import sys

score_folder = "./score"

if not os.path.exists(score_folder):
    os.makedirs(score_folder)
    print("Since there is no score folder, SteamSky Music Studio have created one. Please place the Sheet file there.")
    sys.exit()

while True:
    file_name = input("Enter a File Name or \"Random\" to Select a Random Scores: ")

    if file_name.lower() == 'random':
        # ファイル名をランダムに選ぶ
        score_files = [f for f in os.listdir(score_folder) if f.endswith((".json", ".txt"))]
        if not score_files:
            print("No score files found in the score folder.")
            sys.exit()

        file_name = random.choice(score_files)

    file_path = f"{score_folder}/{file_name}"

    with open(file_path, "rb") as file:
        content = file.read().decode("utf-16-le", errors="ignore").lstrip("\ufeff")

    try:
        data = json.loads(content)
        supported = (
            isinstance(data, list)
            and all(
                isinstance(item, dict)
                and all(
                    key in item
                    for key in [
                        "name",
                        "author",
                        "transcribedBy",
                        "isComposed",
                        "bpm",
                        "bitsPerPage",
                        "pitchLevel",
                        "isEncrypted",
                        "songNotes",
                    ]
                )
                and (isinstance(item["isComposed"], bool) or isinstance(item.get("isComposed", "").lower(), str))
                and (isinstance(item["isEncrypted"], bool) or isinstance(item.get("isEncrypted", "").lower(), str))
                for item in data
            )
        )

        if supported:
            hwnd = win32gui.FindWindow(None, "Sky")
            if hwnd == 0:
                print("Process Not Found")
            else:
                win32gui.SetForegroundWindow(hwnd)

                # キーを押す
                start_time = time.time() * 1000
                for i, note in enumerate(data[0]["songNotes"]):
                    key = note["key"]
                    if key.startswith("1Key") or key.startswith("2Key"):
                        key = key.replace("2Key", "1Key")
                    if key == "1Key0":
                        pyautogui.press("Y")
                    elif key == "1Key1":
                        pyautogui.press("U")
                    elif key == "1Key2":
                        pyautogui.press("I")
                    elif key == "1Key3":
                        pyautogui.press("O")
                    elif key == "1Key4":
                        pyautogui.press("P")
                    elif key == "1Key5":
                        pyautogui.press("H")
                    elif key == "1Key6":
                        pyautogui.press("J")
                    elif key == "1Key7":
                        pyautogui.press("K")
                    elif key == "1Key8":
                        pyautogui.press("L")
                    elif key == "1Key9":
                        pyautogui.press(":")
                    elif key == "1Key10":
                        pyautogui.press("N")
                    elif key == "1Key11":
                        pyautogui.press("M")
                    elif key == "1Key12":
                        pyautogui.press(",")
                    elif key == "1Key13":
                        pyautogui.press(".")
                    elif key == "1Key14":
                        pyautogui.press("/")
                    else:
                        print(f"{key} UnknownKey")

                    if i + 1 < len(data[0]["songNotes"]):
                        next_note = data[0]["songNotes"][i + 1]
                        elapsed_time = time.time() * 1000 - start_time
                        time_to_wait = next_note["time"] - elapsed_time
                        if time_to_wait > 0:
                            time.sleep(time_to_wait / 1000)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        print("Sorry, Not Supported This File")
    except Exception as e:
        print(f"Error reading file: {str(e)}")
