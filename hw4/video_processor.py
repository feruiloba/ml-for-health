import numpy as np
import cv2
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import Tuple, List, Dict

class VideoProcessor:
    """
    Video processing algorithm for HemaApp hemoglobin estimation.
    Extracts grayscale pulsatile signals from finger videos under different lighting conditions.
    """

    def __init__(self, input_video_path: str, out_video_path: str, write_new_grayscale_file=False, use_out_mean_file=False):
        """
        Initialize the video processor.

        Args:
            video_path: Path to the video file
            fps: Frames per second of the video
        """
        self.input_video_path = input_video_path
        self.out_video_path = out_video_path
        self.use_out_mean_file = use_out_mean_file
        self.write_new_grayscale_file = write_new_grayscale_file
        self.heart_rate = None

    def extract_grayscale_timeseries(self):
        cap = cv2.VideoCapture(self.input_video_path)

        if not cap.isOpened():
            print("Error: Could not open video file.")
            exit()

        # Get original video properties (width, height, frames per second)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        with open("fps.txt", "w") as f:
            f.write(f"{self.fps}\n")

        # Define the codec and create a VideoWriter object
        # 'XVID' often works well for .avi files. Other options like 'mp4v' for .mp4 might require specific codecs installed.
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.out_video_path, fourcc, self.fps, (frame_width, frame_height), isColor=False)

        print("Processing video and converting to grayscale...")
        frame_count = 0
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
                out.write(gray_frame)

            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")

        cap.release()

        with open("mean_values.txt", "w") as f:
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
        b, a = signal.butter(4, normal_cutoff, btype='high', analog=False)

        # Apply filter
        filtered = signal.filtfilt(b, a, signal_data)
        return filtered

    def estimate_heart_rate(self, filtered_signal: np.ndarray) -> float:
        """
        Estimate heart rate using FFT on filtered signal.

        Args:
            filtered_signal: High-pass filtered signal

        Returns:
            Estimated heart rate in BPM
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
        dominant_freq = xf_masked[peak_idx]

        # Convert to BPM
        heart_rate_bpm = dominant_freq * 60
        return heart_rate_bpm

    def detect_peaks_troughs(self,
                            filtered_signal: np.ndarray,
                            original_signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect peaks and troughs in the signal using heart rate estimate.

        Args:
            filtered_signal: High-pass filtered signal for peak detection
            original_signal: Original unfiltered signal for magnitude extraction

        Returns:
            Tuple of (peak_indices, trough_indices)
        """
        # Estimate heart rate
        self.heart_rate = self.estimate_heart_rate(filtered_signal)

        # Calculate minimum distance between peaks (3/4 of heart period)
        heart_period_samples = (60 / self.heart_rate) * self.fps
        min_distance = int(0.75 * heart_period_samples)

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

    def calculate_r_values(self,
                          original_signal: np.ndarray,
                          peaks: np.ndarray,
                          troughs: np.ndarray) -> List[float]:
        """
        Calculate R values (peak/trough ratio) for each pulse.

        Args:
            original_signal: Original unfiltered signal
            peaks: Indices of peaks
            troughs: Indices of troughs

        Returns:
            List of R values for each pulse
        """
        r_values = []

        # Match peaks with their preceding troughs
        min_len = min(len(peaks), len(troughs))

        for i in range(min_len):
            peak_val = original_signal[peaks[i]]
            trough_val = original_signal[troughs[i]]

            if trough_val > 0:  # Avoid division by zero
                r = peak_val / trough_val
                r_values.append(r)

        return r_values

    def process_video(self) -> Dict[str, np.ndarray]:
        """
        Complete video processing pipeline.
        """
        # Step 1: Extract grayscale time series
        if self.use_out_mean_file:
            with open("fps.txt", "r") as f:
                self.fps = float(f.read().strip())
            with open("mean_values.txt", "r") as f:
                mean_values = [float(line.strip()) for line in f.readlines()]
        else:
            mean_values = self.extract_grayscale_timeseries()

        # Step 2: Apply high-pass filter (0.5 Hz cutoff)
        values_filtered = self.highpass_filter(mean_values)

        # Step 3: Detect peaks and troughs for each channel
        peaks, troughs = self.detect_peaks_troughs(values_filtered, mean_values)

        # Step 4: Calculate R values
        r_values = self.calculate_r_values(mean_values, peaks, troughs)

        return {
            'r_values': np.array(r_values),
            'heart_rate': self.heart_rate,
            'peaks': peaks,
            'troughs': troughs,
            'mean_r': np.mean(r_values) if r_values else 0,
            'mean_values': np.array(mean_values),
            'values_filtered': values_filtered
        }

