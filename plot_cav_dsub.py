import matplotlib.pyplot as plt
import pandas as pd
import os

# Define the folder path
folder_path = r"C:\Users\mario\OneDrive\Desktop\Parametric_sweep_copper\Parametric_sweep_copper"

# Load data
data_file = os.path.join(folder_path, 'Parametric_sweep_dsub_200-500_dcav_100-125_Silver_solid_annealed_mat_13_epsilon_0.05_steps_0.005MHz.txt')

# Check if the file exists
if not os.path.isfile(data_file):
    print(f"FEHLER: Datei existiert nicht, Pfad prüfen: {data_file}")
else:
    print(f"Datei gefunden: {data_file}")

# Read the data from the file
data = pd.read_csv(data_file, skiprows=5, delim_whitespace=True, header=None, names=["dcav", "dsub", "freq", "displacement"])

# Print the first few rows of the data to verify it is loaded correctly
print("Erste Zeilen der Daten:")
print(data.head())

# Handle missing data by dropping rows with any missing values
data = data.dropna()

# Alternatively, handle missing data by filling missing values with a specified value (e.g., 0)
# data = data.fillna(0)

# Round the dsub values to one decimal place
data["dsub"] = data["dsub"].round(1)

# Print the unique dcav values to verify they are being read correctly
dcav_values = data["dcav"].unique()
print("Einzigartige dcav-Werte:")
print(dcav_values)

# Create separate plots for each dcav value
for dcav in dcav_values:
    subset = data[data["dcav"] == dcav]
    
    plt.figure(figsize=(10, 6))
    max_displacement_info = []
    for dsub in subset["dsub"].unique():
        dsub_subset = subset[subset["dsub"] == dsub]
        plt.plot(dsub_subset["freq"], dsub_subset["displacement"], label=f"dsub = {dsub} µm")

        # Find the maximum displacement and its corresponding frequency
        max_displacement = dsub_subset["displacement"].max()
        max_freq = dsub_subset[dsub_subset["displacement"] == max_displacement]["freq"].values[0]
        
        # Plot the maximum point
        plt.plot(max_freq, max_displacement, 'ro', markersize=3)  # Red dot
        plt.text(max_freq, max_displacement, f'{max_displacement:.2f}', fontsize=9, ha='right')

        # Store the maximum displacement info
        max_displacement_info.append((dsub, max_displacement))
    
    # Add all maxima information to the legend
    for dsub, max_displacement in max_displacement_info:
        plt.plot([], [], ' ', label=f"Max dsub = {dsub} µm, Displacement = {max_displacement:.2f} nm")
    
    plt.xlabel("Frequenz (MHz)")
    plt.ylabel("Displacement RMS (nm)")
    plt.title(f"Displacement vs. Frequency für dcav = {dcav} µm")
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plot_file = os.path.join(folder_path, f'Displacement_vs_Frequency_für_dcav_{dcav}µm_dsub.svg')
    plt.savefig(plot_file)
    
    # Show the plot
    plt.show(block=True)