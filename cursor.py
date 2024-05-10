import subprocess
import time
#ps aux | grep python

while True:
    # Move the cursor to specific screen coordinates (adjust as needed)
    subprocess.run(["xdotool", "mousemove", "5", "5"])
    time.sleep(30)  # Wait for 60 seconds (1 minute)
