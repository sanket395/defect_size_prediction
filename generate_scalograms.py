import os
import numpy as np
import pywt
import matplotlib.pyplot as plt

# Define the root folder containing your measurement data
root_folder = r"C:\Users\Anwender\hochschule-stralsund.de\Jan-Christian Kuhr - 1 Dr. Diestel GmbH\4 Abschlussarbeiten\Masterarbeit Talaviya\Measurement"

# Define the measurement folders (adjust if more folders exist)
measurement_folders = ["31", "32", "34"]

# Sampling rate of the ADXL335 data
sampling_rate = 1002.13  # Hz
sampling_period = 1 / sampling_rate  # Sampling period in seconds

# Iterate through each measurement folder
for folder in measurement_folders:
    folder_path = os.path.join(root_folder, folder)

    # Files for x, y, and z axes
    files = {
        "x": os.path.join(folder_path, "xAxisS1.txt"),
        "y": os.path.join(folder_path, "yAxisS1.txt"),
        "z": os.path.join(folder_path, "zAxisS1.txt")
    }

    # Process each file (x, y, z axes)
    for axis, file_path in files.items():
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        # Load the data from the file
        try:
            data = np.loadtxt(file_path)
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            continue

        # Define scales for the CWT
        scales = np.arange(1, 128)  # Adjust the range if needed

        # Perform CWT using the Morlet wavelet
        coefficients, frequencies = pywt.cwt(data, scales, 'cmor', sampling_period=sampling_period)

        # Generate a scalogram
        plt.figure(figsize=(10, 6))
        plt.imshow(
            np.abs(coefficients),
            extent=[0, len(data) * sampling_period, frequencies[-1], frequencies[0]],
            cmap='jet',
            aspect='auto'
        )
        plt.colorbar(label='Magnitude')
        plt.title(f'Scalogram: Measurement {folder}, Axis {axis.upper()}')
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')

        # Save the scalogram as an image
        output_file = os.path.join(folder_path, f"scalogram_{axis}.png")
        plt.savefig(output_file)
        plt.close()

        print(f"Scalogram saved: {output_file}")
