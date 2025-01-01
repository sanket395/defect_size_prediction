import os
import numpy as np
import pandas as pd

# Base folder path
base_folder_path = r"C:\Users\Anwender\hochschule-stralsund.de\Jan-Christian Kuhr - 1 Dr. Diestel GmbH\4 Abschlussarbeiten\Masterarbeit Talaviya\Measurement\sanket.talaviya\Measurments_Data"

# Sampling frequency
sampling_frequency = 1002.13

# Define the range of folder numbers (39 to 46)
folder_numbers = range(39, 47)

# Initialize a pandas DataFrame to store FFT results
fft_results = pd.DataFrame(columns=['Folder', 'Axis', 'Frequency', 'Magnitude'])

# Perform FFT and save results
for folder_num in folder_numbers:
    folder_path = os.path.join(base_folder_path, str(folder_num))

    # Define file paths
    x_axis_file = os.path.join(folder_path, "xAxisS1.txt")
    y_axis_file = os.path.join(folder_path, "yAxisS1.txt")
    z_axis_file = os.path.join(folder_path, "zAxisS1.txt")

    # Check if all files exist
    if not (os.path.isfile(x_axis_file) and os.path.isfile(y_axis_file) and os.path.isfile(z_axis_file)):
        print(f"Skipping folder {folder_num} due to missing files.")
        continue

    # Load Sensor 1 data
    data_x = np.loadtxt(x_axis_file) - np.mean(np.loadtxt(x_axis_file))
    data_y = np.loadtxt(y_axis_file) - np.mean(np.loadtxt(y_axis_file))
    data_z = np.loadtxt(z_axis_file) - np.mean(np.loadtxt(z_axis_file))

    # Perform FFT
    def compute_fft(data, fs):
        n = len(data)
        freqs = np.fft.fftfreq(n, d=1/fs)[:n//2]
        fft_values = np.abs(np.fft.fft(data)[:n//2])
        return freqs, fft_values

    for axis, data in zip(['X', 'Y', 'Z'], [data_x, data_y, data_z]):
        freqs, magnitudes = compute_fft(data, sampling_frequency)
        temp_df = pd.DataFrame({
            'Folder': folder_num,
            'Axis': axis,
            'Frequency': freqs,
            'Magnitude': magnitudes
        })
        fft_results = pd.concat([fft_results, temp_df], ignore_index=True)

# Save FFT results to a CSV file
output_csv_path = os.path.join(base_folder_path, "fft_results.csv")
fft_results.to_csv(output_csv_path, index=False)
print(f"FFT results saved to {output_csv_path}")
