import os
import numpy as np
import matplotlib.pyplot as plt
import pywt
from src.load_data import load_data  # Import the load_data function
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend



# Define constants
root_folder = r"C:\Users\Anwender\hochschule-stralsund.de\Jan-Christian Kuhr - 1 Dr. Diestel GmbH\2 Wissenschaftliche Literatur\Abschlussarbeiten\Talaviya (Masterarbeit)\Measurement"
measurement_folders = ["31", "32", "34"]
sampling_frequency = 1002.13  # Sampling frequency

# Load measurement data into a pandas DataFrame
data = load_data(root_folder, measurement_folders)

def generate_and_save_scalogram(df, folder, axis, sampling_frequency):
    """
    Generate and save a scalogram for a given folder and axis.
    If a scalogram image already exists, replace it with the new one.
    """
    # Filter data for the specified folder and axis
    filtered_data = df[df['folder'] == folder]
    if axis not in filtered_data:
        print(f"No data found for axis {axis} in folder {folder}")
        return

    signal = filtered_data[axis].values  # Extract signal for the given axis

    # Perform Continuous Wavelet Transform (CWT)
    scales = np.arange(1, 128)  # Define scales
    wavelet = 'cmor'  # Complex Morlet wavelet
    coefficients, frequencies = pywt.cwt(signal, scales, wavelet, 1 / sampling_frequency)

    # Plot Scalogram
    plt.figure(figsize=(10, 6))
    plt.imshow(
        np.abs(coefficients),
        extent=[0, len(signal) / sampling_frequency, frequencies[-1], frequencies[0]],
        aspect='auto',
        cmap='gray'  # Grayscale colormap
    )
    plt.colorbar(label='Magnitude')
    plt.title(f"Grayscale Scalogram - Folder {folder} - {axis.upper()} Axis")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

    # Save scalogram image in the same folder
    output_folder = os.path.join(root_folder, folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f"scalogram_{axis.lower()}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Scalogram saved: {output_file}")

# Iterate through measurement folders and axes to generate scalograms
axes = ['x', 'y', 'z']
for folder in measurement_folders:
    for axis in axes:
        generate_and_save_scalogram(data, folder, axis, sampling_frequency)
