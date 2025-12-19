k
#!/usr/bin/env python3
"""
ducky_fake_cmd.py — Safe simulation of a USB Rubber Ducky payload.
Instead of real commands, it just types harmless "echo" commands.
Educational only!
"""

import time
from pynput.keyboard._base import Key, Controller

def ducky_fake_cmd():
    kb = Controller()
    

    print("Click into a terminal/command prompt window. Starts in 5 seconds...")
    time.sleep(5)
    #ray = kb.press('r''control panel')
    # Fake payload (safe)
    payload = ["control panel",]
        #'echo "Imagine if these were real malicious commands..."',
        #'echo "This is 100% safe and just text."',
        #'echo "Simulation complete!"'
    #]
    # press CTRL key to simulate admin privileges
    admin = True
    if admin:
     #kb.press(Key.cmd)
     kb.press(Key.enter)
     kb.press('r')
     kb.release('r')
     kb.release(Key.cmd)
     time.sleep(2) # wait for terminal to open
    else:
       raise NotImplementedError() 


    for line in payload:
        # Type each characterecho "=== USB Rubber Ducky Simulation ==="
#
        
        for ch in line:
            kb.press(Key.enter)
            kb.type(ch)
            time.sleep(0.03)
        # Press Enter at the end
        kb.press(Key.enter)
        kb.release(Key.enter)
        time.sleep(1)

#mouse = Controller()
#Controller._Key()
#Controller._Key(Button.left)
#mouse.press(Button.left)
#mouse.release(Button.left)



if __name__ == "__main__":
    ducky_fake_cmd()
