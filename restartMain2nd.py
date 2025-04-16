import time
import subprocess
import os
import signal
import multiprocessing
import signal
import tempfile

if __name__ == "__main__":
    while True:
        process = subprocess.Popen(["python3","main.py"])
        print("is running")
        process.wait()
        print("is terminated, will be restarting soon")
        time.sleep(10)