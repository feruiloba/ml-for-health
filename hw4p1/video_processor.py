import numpy as np
import cv2
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import Tuple, List, Dict
from matplotlib import pyplot as plt
from pathlib import Path
import math
import json

class VideoProcessor:
    """
    Video processing algorithm for HemaApp hemoglobin estimation.
    Extracts grayscale pulsatile signals from finger videos under different lighting conditions.
    """

    def __init__(self, input_video_path: str, out_video_path: str, write_new_grayscale_file=False, use_out_mean_file=False):
        """
        Initialize the video processor.
        """
        self.input_video_path = input_video_path
        self.out_video_path = out_video_path
        self.use_out_mean_file = use_out_mean_file
        base_path = Path(input_video_path).stem
        self.mean_out_file_path = f"{base_path}_mean_values.txt"
        self.fps_file_path = f"{base_path}_fps.json"
        self.write_new_grayscale_file = write_new_grayscale_file
        self.heart_rate = None

    def extract_grayscale_timeseries(self):
        cap = cv2.VideoCapture(self.input_video_path)

        if not cap.isOpened():
            print("Error: Could not open video file.")
            exit()

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        print("Processing video and converting to grayscale...")
        self.frame_count = 0
        mean_values = []
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Stream ending (probably end of file, but might be error). Exiting...")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_val = gray_frame.mean()
            mean_values.append(mean_val)

            if self.write_new_grayscale_file:
                # Define the codec and create a VideoWriter object
                # 'XVID' often works well for .avi files. Other options like 'mp4v' for .mp4 might require specific codecs installed.
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(self.out_video_path, fourcc, self.fps, (frame_width, frame_height), isColor=False)
                out.write(gray_frame)

            self.frame_count += 1
            if self.frame_count % 100 == 0:
                print(f"Processed {self.frame_count} frames...")

        cap.release()


        # Get original video properties (width, height, frames per second)
        self.num_seconds = self.frame_count / self.fps
        with open(self.fps_file_path, "w") as f:
            json.dump({"fps": self.fps, "frame_count": self.frame_count, "num_seconds": self.num_seconds}, f)

        with open(self.mean_out_file_path, "w") as f:
            for val in mean_values:
                f.write(f"{val}\n")

        return mean_values


    def highpass_filter(self, signal_data: np.ndarray, cutoff: float = 0.5) -> np.ndarray:
        """
        Apply high-pass filter to remove breathing fluctuations.

        Args:
            signal_data: Input signal
            cutoff: Cutoff frequency in Hz (default 0.5 Hz)

        Returns:
            Filtered signal
        """
        # Design Butterworth high-pass filter
        nyquist = self.fps / 2
        normal_cutoff = cutoff / nyquist
        order = min(4, len(signal_data) // 9)
        b, a = signal.butter(order, normal_cutoff, btype='high')

        # Apply filter
        filtered = signal.filtfilt(b, a, signal_data)
        return filtered

    def get_fft_signal(self, filtered_signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute FFT of the filtered signal.

        Args:
            filtered_signal: High-pass filtered signal

        Returns:
            Tuple of (frequencies, FFT magnitudes)
        """
        # Compute FFT
        n = len(filtered_signal)
        yf = fft(filtered_signal)
        xf = fftfreq(n, 1/self.fps)

        # Only consider positive frequencies in typical heart rate range (0.5-3 Hz = 30-180 BPM)
        mask = (xf > 0.5) & (xf < 3.0)
        xf_masked = xf[mask]
        yf_masked = np.abs(yf[mask])

        # Find dominant frequency
        peak_idx = np.argmax(yf_masked)
        self.dominant_freq = xf_masked[peak_idx]

        return xf_masked, yf_masked

    def detect_peaks_troughs(self, filtered_signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect peaks and troughs in the signal using heart rate estimate.

        Args:
            xf: Frequencies from FFT
            yf: FFT magnitudes

        Returns:
            Tuple of (peak_indices, trough_indices)
        """

        if not hasattr(self, 'dominant_freq'):
            raise ValueError("Dominant frequency not computed. Run get_fft_signal() first.")

        # Calculate minimum distance between peaks (3/4 of heart period)
        heart_period_samples = self.dominant_freq * self.fps
        min_distance = 0.75 * heart_period_samples

        # Find peaks
        peaks, _ = signal.find_peaks(filtered_signal, distance=min_distance)

        # Find troughs between consecutive peaks
        troughs = []
        for i in range(len(peaks) - 1):
            segment = filtered_signal[peaks[i]:peaks[i+1]]
            if len(segment) > 0:
                trough_idx = peaks[i] + np.argmin(segment)
                troughs.append(trough_idx)

        return peaks, np.array(troughs)

    def process_video(self) -> Dict[str, np.ndarray]:
        """
        Complete video processing pipeline.
        """
        # Step 1: Extract grayscale time series
        if self.use_out_mean_file:
            with open(self.fps_file_path, "r") as f:
                data = json.load(f)
                self.fps = data["fps"]
                self.num_seconds = data["num_seconds"]
                self.frame_count = data["frame_count"]
            with open(self.mean_out_file_path, "r") as f:
                mean_values = [float(line.strip()) for line in f.readlines()]
        else:
            mean_values = self.extract_grayscale_timeseries()

        # Step 2: Apply high-pass filter (0.5 Hz cutoff)
        values_filtered = self.highpass_filter(mean_values)

        # Step 3: Get FFT of filtered signal
        x_freq, y_freq_mag = self.get_fft_signal(values_filtered)

        # Step 3: Detect peaks and troughs for each channel
        peaks, troughs = self.detect_peaks_troughs(values_filtered)

        return {
            'bpm': len(peaks) / self.num_seconds * 60,
            'peaks': peaks,
            'troughs': troughs,
            'mean_values': np.array(mean_values),
            'values_filtered': values_filtered,
            'x_fft': x_freq,
            'y_fft': y_freq_mag,
            'dominant_freq': self.dominant_freq,
        }

    def plot_fft(self, results, title="Video"):
        """Plot FFT results."""
        plt.figure(figsize=(10, 4))
        plt.plot(results['x_fft'], results['y_fft'], 'b-')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.title(f'{title}: Dominant Frequency: {results["dominant_freq"]:.2f} Hz')
        plt.grid(alpha=0.3)
        plt.tight_layout()

    def plot_peaks(self, results, title="Video"):
        """Simple plot of results."""

        time = np.arange(len(results['values_filtered'])) / self.fps
        plt.figure(figsize=(12, 4))
        plt.plot(time, results['values_filtered'], 'r-', label='Signal')

        plt.plot(time[results['peaks']], results['values_filtered'][results['peaks']],
                'go', markersize=8, label='Peaks', markerfacecolor="None")
        plt.plot(time[results['troughs']], results['values_filtered'][results['troughs']],
                'bo', markersize=8, label='Troughs', markerfacecolor="None")

        plt.xlabel('Time (s)')
        plt.ylabel('Filtered Signal Amplitude')
        plt.title(f'{title}: {results["bpm"]:.1f} BPM')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
