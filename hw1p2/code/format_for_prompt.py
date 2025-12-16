"""
Format accelerometer data for LLM prompts using different strategies.
"""

import json
import os
import numpy as np

# Paths
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'accelerometer', 'processed')

# Configuration
SAMPLING_RATE = 50  # Hz
DOWNSAMPLE_FACTOR = 10  # Show every Nth sample (250 -> 25 readings)


def compute_statistics(samples):
    """Compute statistical features from samples."""
    arr = np.array(samples)
    x, y, z = arr[:, 0], arr[:, 1], arr[:, 2]
    magnitude = np.sqrt(x**2 + y**2 + z**2)

    stats = {
        'x': {'mean': np.mean(x), 'std': np.std(x), 'min': np.min(x), 'max': np.max(x)},
        'y': {'mean': np.mean(y), 'std': np.std(y), 'min': np.min(y), 'max': np.max(y)},
        'z': {'mean': np.mean(z), 'std': np.std(z), 'min': np.min(z), 'max': np.max(z)},
        'magnitude': {'mean': np.mean(magnitude), 'std': np.std(magnitude)}
    }

    # Compute dominant frequency using FFT on magnitude
    mag_centered = magnitude - np.mean(magnitude)
    fft = np.fft.fft(mag_centered)
    freqs = np.fft.fftfreq(len(magnitude), 1/SAMPLING_RATE)
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft[:len(fft)//2])
    # Ignore DC component (index 0)
    if len(positive_fft) > 1:
        dominant_idx = np.argmax(positive_fft[1:]) + 1
        stats['dominant_freq'] = positive_freqs[dominant_idx]
    else:
        stats['dominant_freq'] = 0.0

    return stats


def format_raw_only(window):
    """Format 1: RAW_ONLY - Just downsampled readings."""
    samples = window['samples']
    lines = []

    for i in range(0, len(samples), DOWNSAMPLE_FACTOR):
        x, y, z = samples[i]
        t = i / SAMPLING_RATE  # Calculate time from sample index
        lines.append(f"t={t:.2f}s: x={x:.2f}, y={y:.2f}, z={z:.2f}")

    return "\n".join(lines)


def format_stats_only(window):
    """Format 2: STATS_ONLY - Only computed statistics."""
    stats = compute_statistics(window['samples'])

    lines = [
        "Statistical Summary:",
        f"X-axis: mean={stats['x']['mean']:.2f}, std={stats['x']['std']:.2f}, min={stats['x']['min']:.2f}, max={stats['x']['max']:.2f}",
        f"Y-axis: mean={stats['y']['mean']:.2f}, std={stats['y']['std']:.2f}, min={stats['y']['min']:.2f}, max={stats['y']['max']:.2f}",
        f"Z-axis: mean={stats['z']['mean']:.2f}, std={stats['z']['std']:.2f}, min={stats['z']['min']:.2f}, max={stats['z']['max']:.2f}",
        f"Magnitude: mean={stats['magnitude']['mean']:.2f}, std={stats['magnitude']['std']:.2f}",
        f"Dominant frequency: {stats['dominant_freq']:.1f} Hz"
    ]

    return "\n".join(lines)


def format_raw_with_context(window):
    """Format 3: RAW_WITH_CONTEXT - Physical context + raw data."""
    context = """[Sensor Context]
This data is from a smartphone accelerometer measuring acceleration in m/s² along three orthogonal axes (x, y, z). When stationary, gravity contributes approximately 9.8 m/s² to one axis. Movement creates deviations from this baseline.

[Sensor Readings]"""

    raw_data = format_raw_only(window)

    return f"{context}\n{raw_data}"


def format_stats_with_expert_knowledge(window):
    """Format 4: STATS_WITH_EXPERT_KNOWLEDGE - Domain knowledge + stats."""
    expert = """[Expert Knowledge]
Activity signatures in accelerometer data:
- SITTING: Gravity-dominated (~9.8 m/s² on one axis), very low variance (std < 0.2), no periodic motion (dominant freq ~0 Hz)
- WALKING: Periodic vertical oscillation at ~1.5-2.0 Hz (step frequency), moderate variance (std 1-3), rhythmic pattern
- RUNNING: Faster periodic oscillation at ~2.5-3.5 Hz, high variance (std 3-6), pronounced impact peaks

[Statistical Summary]"""

    stats = compute_statistics(window['samples'])

    stats_lines = [
        f"X-axis: mean={stats['x']['mean']:.2f}, std={stats['x']['std']:.2f}",
        f"Y-axis: mean={stats['y']['mean']:.2f}, std={stats['y']['std']:.2f}",
        f"Z-axis: mean={stats['z']['mean']:.2f}, std={stats['z']['std']:.2f}",
        f"Magnitude: mean={stats['magnitude']['mean']:.2f}, std={stats['magnitude']['std']:.2f}",
        f"Dominant frequency: {stats['dominant_freq']:.1f} Hz"
    ]

    return f"{expert}\n" + "\n".join(stats_lines)


def format_full_context(window):
    """Format 5: FULL_CONTEXT - Everything combined."""
    sensor_context = """[Sensor Context]
This data is from a smartphone accelerometer measuring acceleration in m/s² along three orthogonal axes (x, y, z). When stationary, gravity contributes approximately 9.8 m/s² to one axis. Movement creates deviations from this baseline."""

    expert = """[Expert Knowledge]
Activity signatures in accelerometer data:
- SITTING: Gravity-dominated (~9.8 m/s² on one axis), very low variance (std < 0.2), no periodic motion (dominant freq ~0 Hz)
- WALKING: Periodic vertical oscillation at ~1.5-2.0 Hz (step frequency), moderate variance (std 1-3), rhythmic pattern
- RUNNING: Faster periodic oscillation at ~2.5-3.5 Hz, high variance (std 3-6), pronounced impact peaks"""

    stats = compute_statistics(window['samples'])
    stats_section = f"""[Statistical Summary]
X-axis: mean={stats['x']['mean']:.2f}, std={stats['x']['std']:.2f}, min={stats['x']['min']:.2f}, max={stats['x']['max']:.2f}
Y-axis: mean={stats['y']['mean']:.2f}, std={stats['y']['std']:.2f}, min={stats['y']['min']:.2f}, max={stats['y']['max']:.2f}
Z-axis: mean={stats['z']['mean']:.2f}, std={stats['z']['std']:.2f}, min={stats['z']['min']:.2f}, max={stats['z']['max']:.2f}
Magnitude: mean={stats['magnitude']['mean']:.2f}, std={stats['magnitude']['std']:.2f}
Dominant frequency: {stats['dominant_freq']:.1f} Hz"""

    raw_section = "[Sample Readings]\n" + format_raw_only(window)

    return f"{sensor_context}\n\n{expert}\n\n{stats_section}\n\n{raw_section}"


# Map format names to functions
FORMATTERS = {
    'RAW_ONLY': format_raw_only,
    'STATS_ONLY': format_stats_only,
    'RAW_WITH_CONTEXT': format_raw_with_context,
    'STATS_WITH_EXPERT_KNOWLEDGE': format_stats_with_expert_knowledge,
    'FULL_CONTEXT': format_full_context
}


def main():
    """Test each formatter on one sample from each class."""
    # Load test data
    with open(os.path.join(PROCESSED_DIR, 'test.json')) as f:
        test_data = json.load(f)

    # Get one sample per class
    samples = {}
    for window in test_data:
        label = window['label']
        if label not in samples:
            samples[label] = window

    activities = ['sitting', 'walking', 'running']

    print("=" * 80)
    print("PROMPT FORMATTING STRATEGIES - TEST OUTPUT")
    print("=" * 80)

    for format_name, formatter in FORMATTERS.items():
        print(f"\n{'='*80}")
        print(f"FORMAT: {format_name}")
        print("=" * 80)

        char_counts = []

        for activity in activities:
            window = samples[activity]
            formatted = formatter(window)
            char_count = len(formatted)
            char_counts.append(char_count)

            print(f"\n--- {activity.upper()} ({window['window_id']}) ---")
            print(formatted)
            print(f"\n[Characters: {char_count}, Est. tokens: ~{char_count//4}]")

        avg_chars = sum(char_counts) / len(char_counts)
        print(f"\n>>> Average for {format_name}: {avg_chars:.0f} chars, ~{avg_chars/4:.0f} tokens")

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY: CHARACTER COUNTS BY FORMAT")
    print("=" * 80)
    print(f"{'Format':<35} {'Sitting':>10} {'Walking':>10} {'Running':>10} {'Avg':>10}")
    print("-" * 80)

    for format_name, formatter in FORMATTERS.items():
        counts = []
        for activity in activities:
            formatted = formatter(samples[activity])
            counts.append(len(formatted))
        avg = sum(counts) / len(counts)
        print(f"{format_name:<35} {counts[0]:>10} {counts[1]:>10} {counts[2]:>10} {avg:>10.0f}")


if __name__ == "__main__":
    main()
