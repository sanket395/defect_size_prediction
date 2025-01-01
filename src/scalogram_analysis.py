import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pywt

# Path to FFT results CSV file
base_folder_path = r"C:\Users\Anwender\hochschule-stralsund.de\Jan-Christian Kuhr - 1 Dr. Diestel GmbH\4 Abschlussarbeiten\Masterarbeit Talaviya\Measurement\sanket.talaviya\Measurments_Data"
fft_results_csv_path = os.path.join(base_folder_path, "fft_results.csv")

# Load FFT results
fft_results = pd.read_csv(fft_results_csv_path)
# Sampling frequency (define the same value as in fft_analysis.py)
sampling_frequency = 1002.13


# Define a function to generate a scalogram
def generate_scalogram(folder, axis, sampling_frequency):
    # Filter FFT results for the selected folder and axis
    filtered_data = fft_results[(fft_results['Folder'] == folder) & (fft_results['Axis'] == axis)]
    signal = filtered_data['Magnitude'].values  # Use magnitude as the signal

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
        cmap='gray'  # Use grayscale colormap
    )
    plt.colorbar(label='Magnitude')
    plt.title(f"Grayscale Scalogram - Folder {folder} - {axis} Axis")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.show()


# Example usage: Generate scalogram for folder 39, X-Axis
generate_scalogram(folder=39, axis='X', sampling_frequency=sampling_frequency)
