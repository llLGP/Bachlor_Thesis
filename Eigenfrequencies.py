import os  # Import os module for folder creation
import numpy as np
import matplotlib.pyplot as plt


# Read the file and parse the data
def read_eigenfrequency_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    # Skip first 4 lines (header)
    data_lines = lines[4:]

    data = []
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 3:
            try:
                dcav = float(parts[0])
                tdev = float(parts[1])
                eigenfrequency = complex(
                    parts[2].replace("i", "j")
                )  # Convert to complex number
                data.append((dcav, tdev, eigenfrequency.real, eigenfrequency.imag))
            except ValueError:
                continue  # Skip invalid lines

    return np.array(data)


# File path (modify this as needed)
filename = r"c:\Users\mario\Desktop\Parametric_sweep_tdev_1-10_dcav_100-125_Silver_solid_annealed_mat_13_epsilon_0.05_Eigenfrequencies.txt"  # Replace with the actual file path
data = read_eigenfrequency_file(filename)

# Round the dcav values to the nearest integer
data[:, 0] = np.round(data[:, 0])

# Restrict dcav values to the range 100–125 µm
dcav_values = [dcav for dcav in np.unique(data[:, 0]) if 100 <= dcav <= 125]

# Create a folder to save the plots
output_folder = r"c:\Users\mario\Desktop\Eigenfrequency_Plots"
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Loop through each dcav value and create a plot
for dcav in dcav_values:
    # Filter data for the current dcav value
    filtered_data = data[data[:, 0] == dcav]

    # Convert Hz to MHz for the x-axis
    filtered_data[:, 2] /= 1e6  # Convert real part of Eigenfrequency to MHz

    # Unique tdev values
    tdev_values = np.unique(filtered_data[:, 1])

    # Define colormap and markers
    colors = plt.cm.viridis(np.linspace(0, 1, len(tdev_values)))
    harmonic_styles = ["o", "s", "D"]  # First, second, third harmonic markers

    plt.figure(figsize=(8, 6))

    # Plot data for the current dcav value
    for i, tdev in enumerate(tdev_values):
        subset = filtered_data[filtered_data[:, 1] == tdev]
        for j, (x, y) in enumerate(zip(subset[:, 2], subset[:, 3])):
            marker = harmonic_styles[j % len(harmonic_styles)]  # Cycle through markers
            plt.scatter(
                x,
                y,
                color=colors[i],
                marker=marker,
                label=f"Harmonic {j+1}" if i == 0 else "",
            )
            # Add a red vertical line for the first harmonic point
            if i == 0:  # First harmonic point
                plt.vlines(x=x, ymin=0, ymax=y, colors="red", linestyles="dashed")

    # Create legend for tdev colors
    handles_color = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=colors[i],
            markersize=8,
            label=f"tdev {int(tdev)} µm",
        )
        for i, tdev in enumerate(tdev_values)
    ]
    handles_marker = [
        plt.Line2D(
            [0],
            [0],
            marker=m,
            color="black",
            linestyle="None",
            markersize=8,
            label=f"Harmonic {h+1}",
        )
        for h, m in enumerate(harmonic_styles)
    ]

    plt.xlabel("Real Part of Eigenfrequency (MHz)")
    plt.ylabel("Imaginary Part of Eigenfrequency (Hz)")
    plt.title(f"Eigenfrequency Plot for dcav = {int(dcav)} µm")
    plt.grid(True)

    # Place legends outside the plot
    legend1 = plt.legend(
        handles=handles_color,
        loc="upper left",
        bbox_to_anchor=(1, 1),
        title="tdev Thickness",
    )
    legend2 = plt.legend(
        handles=handles_marker,
        loc="lower left",
        bbox_to_anchor=(1, 0),
        title="Harmonics",
    )
    plt.gca().add_artist(legend1)  # Add first legend manually

    # Adjust subplot layout
    plt.subplots_adjust(right=0.8)

    # Save the plot as an .svg file
    output_file = os.path.join(
        output_folder, f"Eigenfrequency_dcav_coppermembrane_{int(dcav)}.svg"
    )
    plt.savefig(output_file, format="svg", bbox_inches="tight")
    print(f"Plot saved: {output_file}")

    plt.show()
