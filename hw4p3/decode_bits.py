import os
import cv2
import numpy as np
import argparse
from scipy.fft import fft
import sys

class HiLightReceiver:
    def __init__(self, video_path, ground_truth_path, grid_rows=1, grid_cols=1):
        print("Video Path:", video_path)
        self.video_path = video_path
        self.ground_truth_path = ground_truth_path
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

        # HiLight Constants from the paper
        self.SAMPLING_WINDOW = 6  # 6 frames per bit
        self.FPS_REQUIREMENT = 60 # System relies on 60Hz refresh [cite: 192]

        # Scene Detection Thresholds [cite: 332]
        self.DP_CUT_THRESHOLD = 100
        self.DH_CUT_THRESHOLD = 1.0

        # Frequencies for BFSK (at 60 FPS)
        # 20Hz = Bit 0
        # 30Hz = Bit 1
        self.FREQ_0 = 20
        self.FREQ_1 = 30

    def load_ground_truth(self):
        """Loads expected bits from a text file (e.g., '10110')."""
        try:
            with open(self.ground_truth_path, 'r') as f:
                content = f.read().strip()
                # Remove spaces or newlines if present
                bits = [int(b) for b in content if b in '01']
            return np.array(bits)
        except Exception as e:
            print(f"Error loading ground truth: {e}")
            sys.exit(1)

    def calculate_dp(self, frame_prev, frame_curr):
        """
        Calculates Pixel-based metric
        d_p(F, F') = Sum(|C(p) - C(p')|) / (X * Y)
        """
        diff = cv2.absdiff(frame_prev, frame_curr)
        dp = np.sum(diff) / (frame_prev.shape[0] * frame_prev.shape[1])
        return dp

    def calculate_dh(self, frame_prev, frame_curr, bins=256):
        """
        Calculates Histogram-based metric
        """
        hist_prev = cv2.calcHist([frame_prev], [0], None, [bins], [0, 256])
        hist_curr = cv2.calcHist([frame_curr], [0], None, [bins], [0, 256])

        # Avoid division by zero by adding a small epsilon
        epsilon = 1e-10
        numerator = (hist_prev - hist_curr) ** 2
        denominator = np.maximum(hist_prev, hist_curr) + epsilon

        # Only sum where max != 0 (handled by epsilon effectively)
        dh = np.sum(numerator / denominator)
        return dh

    def decode_bfsk(self, intensity_buffer):
        """
        Decodes a bit using FFT on the intensity buffer[cite: 410].
        Bit 0: 20Hz dominant
        Bit 1: 30Hz dominant
        """
        # FFT
        N = len(intensity_buffer)
        yf = fft(intensity_buffer)
        xf = np.fft.fftfreq(N, 1 / self.FPS_REQUIREMENT)

        # Get magnitudes
        magnitudes = np.abs(yf)

        # Find indices for 20Hz and 30Hz
        # In a 6-point FFT at 60Hz:
        # Index 0: 0Hz (DC)
        # Index 1: 10Hz
        # Index 2: 20Hz
        # Index 3: 30Hz (Nyquist)

        power_20hz = magnitudes[2]
        power_30hz = magnitudes[3]

        #  Bit 0 -> 20Hz, Bit 1 -> 30Hz
        if power_30hz > power_20hz:
            return 1
        else:
            return 0

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print("Error: Could not open video.")
            sys.exit(1)

        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps < 55:
            print(f"Warning: Video FPS is {fps}. HiLight requires ~60 FPS for correct 20/30Hz BFSK.")

        decoded_bits = []
        intensity_buffer = []
        prev_frame = None

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to grayscale for intensity [cite: 41]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Scene Detection Logic
            if prev_frame is not None:
                dp = self.calculate_dp(prev_frame, gray)
                dh = self.calculate_dh(prev_frame, gray)

                # Check for Cut Scene [cite: 330]
                if dp > self.DP_CUT_THRESHOLD and dh > self.DH_CUT_THRESHOLD:
                    # [cite: 408] Receiver discards frame window if cut scene detected
                    intensity_buffer = []
                    prev_frame = gray
                    continue

            # Calculate average intensity of the screen (assuming full frame is screen for simplicity)
            # In a real scenario, we would split this into grids [cite: 344]
            avg_intensity = np.mean(gray)
            intensity_buffer.append(avg_intensity)

            # Use sliding window or fixed window?
            # The paper implies sliding window voting[cite: 413], but for simplicity
            # we will assume synchronized chunks of 6 frames.
            if len(intensity_buffer) == self.SAMPLING_WINDOW:
                bit = self.decode_bfsk(intensity_buffer)
                decoded_bits.append(bit)
                # Reset buffer (or slide) - Here we reset for fixed window decoding
                intensity_buffer = []

            prev_frame = gray
            frame_count += 1

        cap.release()
        return np.array(decoded_bits), frame_count / fps

    def save_bits_to_file(self, bits, output_path):
        """Writes the decoded bit array to a file as a string (e.g. '10110')."""
        bit_string = ''.join(map(str, bits))
        try:
            with open(output_path, 'w') as f:
                f.write(bit_string)
            print(f"Successfully saved {len(bits)} bits to {output_path}")
        except Exception as e:
            print(f"Error saving output file: {e}")

    def compute_metrics(self, decoded_bits, true_bits, duration_seconds):
        """
        Aligns streams and calculates BER and Data Rate.
        """
        if len(decoded_bits) == 0:
            return 1.0, 0.0

        print("Decoded bits" + str(decoded_bits))

        # Synchronization: Find best alignment minimizing bit errors
        # Because video might start recording before/after transmission starts
        best_accuracy = 0.0
        max_overlap = min(len(decoded_bits), len(true_bits))

        # Sweep to find best offset
        for offset in range(len(decoded_bits) - max_overlap + 1):
            sub_decoded = decoded_bits[offset : offset + max_overlap]
            sub_true = true_bits[:len(sub_decoded)]

            matches = np.sum(sub_decoded == sub_true)
            acc = matches / len(sub_true)
            if acc > best_accuracy:
                best_accuracy = acc

        # Try checking if true bits are inside decoded bits (lead-in noise)
        for offset in range(len(decoded_bits) - len(true_bits) + 1):
             sub_decoded = decoded_bits[offset : offset + len(true_bits)]
             matches = np.sum(sub_decoded == true_bits)
             acc = matches / len(true_bits)
             if acc > best_accuracy:
                best_accuracy = acc

        # Bit Error Rate = 1 - Accuracy
        ber = 1.0 - best_accuracy

        # Data Rate = Correctly received bits / Total Duration
        # Or specifically as requested: Total correct bits / second
        total_correct_bits = best_accuracy * len(true_bits) # Approx based on aligned segment

        # Note: Actual throughput in paper is roughly 1Kbps depending on grid size[cite: 65].
        # Here we calculate based on the video duration processed.
        data_rate = total_correct_bits / duration_seconds

        return ber, data_rate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate BER and Data Rate for HiLight.")
    parser.add_argument("--video", type=str, required=True, help="Path to video file")
    parser.add_argument("--bits", type=str, required=True, help="Path to ground truth bits file")

    args = parser.parse_args()

    receiver = HiLightReceiver(args.video, args.bits)

    print("Processing video...")
    decoded_bits, duration = receiver.process_video()

    base_name = os.path.splitext(args.video)[0]
    output_path = f"{base_name}_decoded.txt"
    receiver.save_bits_to_file(decoded_bits, output_path)

    print(f"Decoded {len(decoded_bits)} raw bits from video.")

    true_bits = receiver.load_ground_truth()
    print(f"Loaded {len(true_bits)} ground truth bits.")

    ber, data_rate = receiver.compute_metrics(decoded_bits, true_bits, duration)

    print("-" * 30)
    print(f"Bit Error Rate (BER): {ber:.4f}")
    print(f"Data Rate:            {data_rate:.2f} bps")
    print("-" * 30)