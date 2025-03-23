"""
This module provides a MATLAB-like plotting framework.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Install pandas package
# Run the following command in the terminal: pip install pandas

# Define the file_path variable
folder_path = r"C:\Users\mario\OneDrive\Desktop\Parametric_sweep_copper\Parametric_sweep_copper"

# Load data
data_file = os.path.join(folder_path, 'Parametric_sweep_dcav_100-130_Silver_solid_annealed_mat_13_epsilon_0.05_steps_0.005MHz.txt')

# Read the data from the file
data = pd.read_csv(data_file, skiprows=4, delim_whitespace=True, header=None, names=["dcav", "freq", "displacement"])

# Handle missing data by dropping rows with any missing values
data = data.dropna()

# Alternatively, handle missing data by filling missing values with a specified value (e.g., 0)
# data = data.fillna(0)

# Create the plot
dcav_values = data["dcav"].unique()
plt.figure(figsize=(10, 6))
for dcav in dcav_values:
    subset = data[data["dcav"] == dcav]
    plt.plot(subset["freq"], subset["displacement"], label=f"dcav = {dcav} µm")
plt.xlabel("Frequenz (MHz)")
plt.ylabel("Displacement RMS (nm)")
plt.title("Displacement vs. Frequency für verschiedene Cavity-Durchmesser")
plt.legend()
plt.grid(True)
plt.show()