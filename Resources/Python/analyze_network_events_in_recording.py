import sys
import os.path
from tkinter import filedialog
import tkinter as tk
import numpy as np

if __name__ == "__main__":

    # Create the main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # select TTL folder of recording containing full_words.npy, sample_numbers.npy, states.npy, timestamps.npy
    dirname = filedialog.askdirectory()

    if not dirname:
        sys.exit(0)

    if not os.path.exists(dirname):
        print(f"Directory {dirname} does not exist.")
        sys.exit(1)

    print(f"Selected directory: {dirname}")

    full_words = np.load(os.path.join(dirname, "full_words.npy"))
    sample_numbers = np.load(os.path.join(dirname, "sample_numbers.npy"))
    states = np.load(os.path.join(dirname, "states.npy"))
    timestamps = np.load(os.path.join(dirname, "timestamps.npy"))
    print(f"Full words shape: {full_words.shape}")
    print(f"Sample numbers shape: {sample_numbers.shape}")
    print(f"States shape: {states.shape}")
    print(f"Timestamps shape: {timestamps.shape}")

    print(full_words[:128:2])

    print(full_words[128:])
