from matplotlib import pyplot as plt
from video_processor import VideoProcessor
import numpy as np

class HeartRateExtractor():

    def __init__(self):
        pass

    def analyze_video(self, video_file_path1: str, video_file_path2: str, label1="FFT", label2="HR"):
        """Process and compare two videos."""

        processor1 = VideoProcessor(
            video_file_path1,
            f"{video_file_path1}_out",
            write_new_grayscale_file=False,
            use_out_mean_file=True)
        output1 = processor1.process_video()

        # Plot both
        processor1.plot_fft(output1, label1)
        processor1.plot_peaks(output1, label2)

        plt.show()

video_file_path1 = "finger_pulse.MOV"
video_file_path2 = "pulse_attempt_2.mov"
hr_ext = HeartRateExtractor()
hr_ext.analyze_video(video_file_path1, video_file_path2)