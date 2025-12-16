import tkinter as tk
import subprocess
import os
import json

INPUT_STREAM = "http://192.168.100.3:8080/video"
POINTS_FILE = "zone_points.json"

def run_pick_points():
    """
    Run pick_points.py to mark 4 points on floor.
    """
    print("📌 Launching point selector...")
    subprocess.Popen([
        "python3", "pick_points.py",
        "--i", INPUT_STREAM,
        "-m", "-s"
    ])


def run_fastmot():
    """
    Run FastMOT danger zone detection.
    """
    if not os.path.exists(POINTS_FILE):
        print("❌ ERROR: You must select 4 points first!")
        return

    print("🚀 Launching FastMOT Detection...")
    subprocess.Popen([
        "python3", "app.py",
        "-i", INPUT_STREAM,
        "-m", "-s"
    ])


def main():
    window = tk.Tk()
    window.title("Danger Zone Human Detection System")
    window.geometry("380x220")
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=15)

    btn_select = tk.Button(
        window,
        text="1. Mark Floor Region (Pick 4 Points)",
        font=("Arial", 12),
        width=30,
        command=run_pick_points
    )
    btn_select.pack(pady=10)

    btn_run = tk.Button(
        window,
        text="2. Start Danger Zone Detection",
        font=("Arial", 12),
        width=30,
        command=run_fastmot
    )
    btn_run.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    main()

