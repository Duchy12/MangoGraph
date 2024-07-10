import numpy as np
import tkinter as tk
from tkinter import filedialog
import re
import threading
import matplotlib.pyplot as plt

def calculate_one_percent_lows(fps_sorted):
    index = int(len(fps_sorted) * 0.01)
    one_percent_low_fps = fps_sorted[index]
    return one_percent_low_fps
    
def calculate_point_one_percent_lows(fps_sorted):
    index = int(len(fps_sorted) * 0.001)
    zero_point_one_percent_low_fps = fps_sorted[index]
    return zero_point_one_percent_low_fps

def calculate_ninety_seven_percentile(fps_sorted):
    index = int(len(fps_sorted) * 0.97)
    ninety_seven_percentile_fps = fps_sorted[index]
    return ninety_seven_percentile_fps

def show_tkinter_window(duration, one_percent_low_fps, zero_point_one_percent_low_fps, ninety_seven_percentile_fps):
    root = tk.Tk()
    root.title("FPS Data")
    root.geometry("300x100")

    label1 = tk.Label(root, text="Duration: " + str(duration) + "s")
    label1.pack()
    label2 = tk.Label(root, text="1% Low FPS: " + str(one_percent_low_fps))
    label2.pack()
    label3 = tk.Label(root, text="0.1% Low FPS: " + str(zero_point_one_percent_low_fps))
    label3.pack()
    label4 = tk.Label(root, text="97% FPS: " + str(ninety_seven_percentile_fps))
    label4.pack()

    root.mainloop()

# Open file prompt (opens file dialog)
file_path = filedialog.askopenfilename()
print(file_path)

# Remove first 3 lines from file if it doesn't match the specified data
with open(file_path, 'r') as fin:
    data = fin.read().splitlines(True)
    if not re.match(r'^\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+,\d+,\d+,\d+,\d+,\d+\.\d+,\d+,\d+\.\d+,\d+,\d+,\d+$', data[0]):
        data = data[3:]
with open(file_path, 'w') as fout:
    fout.writelines(data)

# Load data from file
data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
fps = data[:, 0]
fps_sorted = np.sort(fps)

# Calculate metrics
one_percent_low_fps = calculate_one_percent_lows(fps_sorted)
zero_point_one_percent_low_fps = calculate_point_one_percent_lows(fps_sorted)
ninety_seven_percentile_fps = calculate_ninety_seven_percentile(fps_sorted)
duration = len(fps) * 0.5

# Print metrics
print("1% Low FPS:", one_percent_low_fps)
print("0.1% Low FPS:", zero_point_one_percent_low_fps)
print("97% FPS:", ninety_seven_percentile_fps)
print("Duration:", duration, "s")

# Show tkinter window in a new thread
thread = threading.Thread(target=show_tkinter_window, args=(duration, one_percent_low_fps, zero_point_one_percent_low_fps, ninety_seven_percentile_fps))
thread.start()

# Plot the fps data
time = np.arange(len(fps)) * 0.5
plt.plot(time, fps)
plt.xlabel('Time (s)')
plt.ylabel('FPS')
plt.title('FPS Data')
plt.show()
