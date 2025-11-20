from matplotlib import pyplot as plt
from video_processor import VideoProcessor



input_video_file = "finger_pulse.MOV"
output_grayscale_video_file = "grayscale_finger_pulse.avi"
processor = VideoProcessor(input_video_file, output_grayscale_video_file, write_new_grayscale_file=False, use_out_mean_file=True)
output = processor.process_video()

plt.plot(output['values_filtered'], label='Mean Grayscale Values', color='blue')
plt.title("Extracted Grayscale Pulsatile Signal")
plt.xlabel("Frame Number")
plt.ylabel("Mean Grayscale Value")
plt.show()