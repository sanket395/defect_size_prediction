import numpy as np
from scipy.fftpack import fft
from scipy.signal import butter, filtfilt


def bandpass_filter(signal, sampling_frequency, center_frequency, bandwidth=10):
    """
    Bandpass filter the signal around a center frequency.

    Parameters:
    - signal: Time-domain vibration signal.
    - sampling_frequency: Sampling frequency (Hz).
    - center_frequency: Center frequency for the bandpass filter (Hz).
    - bandwidth: Bandwidth around the center frequency (Hz).

    Returns:
    - Filtered signal.
    """
    nyquist = 0.5 * sampling_frequency
    low = (center_frequency - bandwidth / 2) / nyquist
    high = (center_frequency + bandwidth / 2) / nyquist
    b, a = butter(4, [low, high], btype='band')
    return filtfilt(b, a, signal)


def detect_problematic_component(signal, sampling_frequency, defect_frequencies):
    """
    Analyze the signal for defect-related frequencies and identify the problematic component.

    Parameters:
    - signal: Time-domain vibration signal.
    - sampling_frequency: Sampling frequency (Hz).
    - defect_frequencies: Dictionary with defect frequencies (BPFO, BPFI, BSF, FTF).

    Returns:
    - Defect likelihoods based on frequency amplitudes.
    """
    n = len(signal)
    freq_bins = np.fft.rfftfreq(n, d=1 / sampling_frequency)
    fft_values = np.abs(fft(signal)[:len(freq_bins)])

    defect_analysis = {}

    for defect, frequency in defect_frequencies.items():
        harmonics = [frequency * i for i in range(1, 4)]  # First three harmonics
        defect_amplitudes = []

        for harmonic in harmonics:
            # Bandpass filter the signal around each harmonic
            filtered_signal = bandpass_filter(signal, sampling_frequency, harmonic)

            # Perform FFT on the filtered signal
            filtered_fft_values = np.abs(fft(filtered_signal)[:len(freq_bins)])

            # Find the peak amplitude in the harmonic region
            idx = (np.abs(freq_bins - harmonic)).argmin()
            defect_amplitudes.append(filtered_fft_values[idx])

        # Sum amplitudes for each defect
        defect_analysis[defect] = sum(defect_amplitudes)

    return defect_analysis


# Example Usage
# Replace with actual signal and calculated defect frequencies
signal = np.sin(2 * np.pi * 25 * np.linspace(0, 1, 1002))  # Example signal
sampling_frequency = 1002.13  # Hz
defect_frequencies = {
    "BPFO": 120,  # Replace with calculated BPFO
    "BPFI": 180,  # Replace with calculated BPFI
    "BSF": 90,  # Replace with calculated BSF
    "FTF": 60  # Replace with calculated FTF
}

analysis_results = detect_problematic_component(signal, sampling_frequency, defect_frequencies)

# Determine the problematic component
print("Defect Analysis Results:")
for defect, amplitude in analysis_results.items():
    print(f"  {defect}: {amplitude:.2f}")
