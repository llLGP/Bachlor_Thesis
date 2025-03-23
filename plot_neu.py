import matplotlib.pyplot as plt
import pandas as pd
import os

# Define the folder path
folder_path = r"C:\Users\mario\OneDrive\Desktop\Parametric_sweep_copper\Parametric_sweep_copper"

# Load data
data_file = os.path.join(folder_path, 'Parametric_sweep_dcav_100-130_Silver_solid_annealed_mat_13_epsilon_0.05_steps_0.005MHz.txt')

# Check if the file exists
if not os.path.isfile(data_file):
    print(f"FEHLER: Datei existiert nicht, Pfad prüfen: {data_file}")
else:
    print(f"Datei gefunden: {data_file}")

# Read the data from the file
data = pd.read_csv(data_file, skiprows=5, delim_whitespace=True, header=None, names=["dcav", "freq", "displacement"])

# Print the first few rows of the data to verify it is loaded correctly
print("Erste Zeilen der Daten:")
print(data.head())

# Handle missing data by dropping rows with any missing values
data = data.dropna()

# Alternatively, handle missing data by filling missing values with a specified value (e.g., 0)
# data = data.fillna(0)

# Print the unique dcav values to verify they are being read correctly
dcav_values = data["dcav"].unique()
print("Einzigartige dcav-Werte:")
print(dcav_values)

# Exclude the last dcav value
dcav_values = dcav_values[:-1]
print("Einzigartige dcav-Werte ohne den letzten:")
print(dcav_values)

# Create the plot
plt.figure(figsize=(10, 6))
for dcav in dcav_values:
    subset = data[data["dcav"] == dcav]
    plt.plot(subset["freq"], subset["displacement"], label=f"dcav = {dcav} µm")
    
    # Find the maximum displacement and its corresponding frequency
    max_displacement = subset["displacement"].max()
    max_freq = subset[subset["displacement"] == max_displacement]["freq"].values[0]
    
    # Plot the maximum point
    plt.plot(max_freq, max_displacement, 'ro')  # Red dot
    plt.text(max_freq, max_displacement, f'{max_displacement:.2f}', fontsize=9, ha='right')

plt.xlabel("Frequenz (MHz)")
plt.ylabel("Displacement RMS (nm)")
plt.title("Displacement vs. Frequency für verschiedene Cavity-Durchmesser")
plt.legend()
plt.grid(True)

# Save the plot
plot_file = os.path.join(folder_path, 'Displacement vs. Frequency für verschiedene Cavity-Durchmesser.svg')
plt.savefig(plot_file)

# Show the plot and block execution until the plot window is closed
plt.show(block=True)