"""
Create few-shot prompt variants with different numbers of examples.
Selection based on statistical diversity within each class.
"""

import json
import os
import numpy as np
from format_for_prompt import compute_statistics

# Paths
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')

ACTIVITIES = ['sitting', 'walking', 'running']


def format_stats_clean(window):
    """Clean stats format without repeated expert knowledge."""
    stats = compute_statistics(window['samples'])
    return f"""[Statistical Summary]
X-axis: mean={stats['x']['mean']:.2f}, std={stats['x']['std']:.2f}
Y-axis: mean={stats['y']['mean']:.2f}, std={stats['y']['std']:.2f}
Z-axis: mean={stats['z']['mean']:.2f}, std={stats['z']['std']:.2f}
Magnitude: mean={stats['magnitude']['mean']:.2f}, std={stats['magnitude']['std']:.2f}
Dominant frequency: {stats['dominant_freq']:.1f} Hz"""


def get_window_intensity(window):
    """Calculate intensity metric (magnitude std) for a window."""
    stats = compute_statistics(window['samples'])
    return stats['magnitude']['std']


def get_window_frequency(window):
    """Get dominant frequency for a window."""
    stats = compute_statistics(window['samples'])
    return stats['dominant_freq']


def select_typical_examples(windows_by_activity):
    """Select 1 example per class closest to class mean intensity."""
    selected = {}

    for activity in ACTIVITIES:
        windows = windows_by_activity[activity]
        intensities = [get_window_intensity(w) for w in windows]
        mean_intensity = np.mean(intensities)

        # Find window closest to mean
        distances = [abs(i - mean_intensity) for i in intensities]
        best_idx = np.argmin(distances)
        selected[activity] = [windows[best_idx]]

    return selected


def select_diverse_3shot(windows_by_activity):
    """Select 3 examples per class: low, typical, high intensity."""
    selected = {}

    for activity in ACTIVITIES:
        windows = windows_by_activity[activity]
        # Sort by intensity
        sorted_windows = sorted(windows, key=get_window_intensity)

        n = len(sorted_windows)
        # Select low (25th percentile), median, high (75th percentile)
        low_idx = n // 4
        mid_idx = n // 2
        high_idx = 3 * n // 4

        # Ensure we don't pick sequential windows
        selected[activity] = [
            sorted_windows[low_idx],
            sorted_windows[mid_idx],
            sorted_windows[high_idx]
        ]

    return selected


def select_diverse_5shot(windows_by_activity):
    """Select 5 examples per class spanning the full range."""
    selected = {}

    for activity in ACTIVITIES:
        windows = windows_by_activity[activity]
        # Sort by intensity
        sorted_windows = sorted(windows, key=get_window_intensity)

        n = len(sorted_windows)
        # Select at 10%, 30%, 50%, 70%, 90% percentiles
        indices = [
            int(n * 0.1),
            int(n * 0.3),
            int(n * 0.5),
            int(n * 0.7),
            int(n * 0.9)
        ]
        # Ensure unique indices
        indices = list(dict.fromkeys(indices))

        selected[activity] = [sorted_windows[i] for i in indices[:5]]

        # Pad if we don't have 5 unique
        while len(selected[activity]) < 5:
            for i in range(n):
                if sorted_windows[i] not in selected[activity]:
                    selected[activity].append(sorted_windows[i])
                    break

    return selected


def create_prompt_header():
    """Create the common header for all v3 variants."""
    return """You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
The accelerometer measures acceleration in m/s² along three axes. Gravity contributes ~9.8 m/s² when stationary.

[Activity Signatures]
- SITTING: Characterized by gravity-dominated readings with very low variance (std < 0.2 m/s²). No periodic motion detected. The signal is essentially flat with minor sensor noise.

- WALKING: Shows periodic oscillation at approximately 1.5-2.0 Hz corresponding to step frequency. Moderate variance (std 1-3 m/s²) with rhythmic peaks on the vertical axis as each foot strikes the ground.

- RUNNING: Displays faster periodic oscillation at approximately 2.5-3.5 Hz. Higher variance (std 3-6 m/s²) with more pronounced impact peaks due to greater ground reaction forces.

[Examples]"""


def create_prompt_footer():
    """Create the common footer for all prompts."""
    return """
[Your Task]
Analyze the following sensor data and classify the activity:
[TEST_DATA_HERE]

Classification:"""


def create_fewshot_prompt(selected_examples, shot_name):
    """Create a few-shot prompt with selected examples."""
    lines = [create_prompt_header()]

    example_num = 1
    for activity in ACTIVITIES:
        for window in selected_examples[activity]:
            lines.append(f"\nExample {example_num} - {activity.capitalize()} ({window['window_id']}):")
            lines.append(format_stats_clean(window))
            lines.append(f"Classification: {activity}")
            example_num += 1

    lines.append(create_prompt_footer())

    return "\n".join(lines)


def create_zero_shot_prompt():
    """Create zero-shot prompt (no examples)."""
    return """You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
Accelerometer measures acceleration in m/s² along x, y, z axes. Gravity contributes ~9.8 m/s².

[Activity Signatures]
- SITTING: Gravity-dominated, very low variance (std < 0.2), no periodic motion (freq ~0 Hz)
- WALKING: Periodic at ~1.5-2.0 Hz (step frequency), moderate variance (std 1-3)
- RUNNING: Periodic at ~2.5-3.5 Hz, high variance (std 3-6), pronounced peaks

Based on your knowledge of human motion and accelerometer physics, classify this data:
[TEST_DATA_HERE]

Classification (sitting/walking/running):"""


def main():
    # Load training data
    with open(os.path.join(PROCESSED_DIR, 'train.json')) as f:
        train_data = json.load(f)

    # Group windows by activity
    windows_by_activity = {activity: [] for activity in ACTIVITIES}
    for window in train_data:
        windows_by_activity[window['label']].append(window)

    print("=" * 70)
    print("FEW-SHOT PROMPT CREATION")
    print("=" * 70)

    print(f"\nTraining windows available per class:")
    for activity in ACTIVITIES:
        print(f"  {activity}: {len(windows_by_activity[activity])} windows")

    # Select examples for each variant
    selections = {
        '1shot': select_typical_examples(windows_by_activity),
        '3shot': select_diverse_3shot(windows_by_activity),
        '5shot': select_diverse_5shot(windows_by_activity)
    }

    # Create and save prompts
    os.makedirs(PROMPTS_DIR, exist_ok=True)

    results = []

    for shot_name, selected in selections.items():
        prompt = create_fewshot_prompt(selected, shot_name)
        filename = f"v3_{shot_name}.txt"
        filepath = os.path.join(PROMPTS_DIR, filename)

        with open(filepath, 'w') as f:
            f.write(prompt)

        char_count = len(prompt)
        token_est = char_count // 4
        total_examples = sum(len(v) for v in selected.values())

        results.append({
            'name': filename,
            'chars': char_count,
            'tokens': token_est,
            'examples': total_examples,
            'selected': selected
        })

    # Create/confirm zero-shot
    zero_shot = create_zero_shot_prompt()
    zero_shot_path = os.path.join(PROMPTS_DIR, 'v5_zero_shot.txt')
    with open(zero_shot_path, 'w') as f:
        f.write(zero_shot)

    results.append({
        'name': 'v5_zero_shot.txt',
        'chars': len(zero_shot),
        'tokens': len(zero_shot) // 4,
        'examples': 0,
        'selected': {}
    })

    # Report results
    print("\n" + "=" * 70)
    print("TOKEN COUNTS")
    print("=" * 70)
    print(f"{'Prompt':<20} {'Examples':>10} {'Chars':>10} {'Est. Tokens':>12}")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<20} {r['examples']:>10} {r['chars']:>10} {r['tokens']:>12}")

    # Report selected windows
    print("\n" + "=" * 70)
    print("SELECTED WINDOWS")
    print("=" * 70)

    for r in results:
        if r['examples'] == 0:
            print(f"\n{r['name']}: No examples (zero-shot)")
            continue

        print(f"\n{r['name']}:")
        for activity in ACTIVITIES:
            windows = r['selected'].get(activity, [])
            print(f"  {activity.upper()}:")
            for w in windows:
                stats = compute_statistics(w['samples'])
                print(f"    - {w['window_id']}: std={stats['magnitude']['std']:.2f}, freq={stats['dominant_freq']:.1f}Hz")

    # Show intensity distribution for context
    print("\n" + "=" * 70)
    print("INTENSITY DISTRIBUTION (magnitude std)")
    print("=" * 70)
    for activity in ACTIVITIES:
        intensities = [get_window_intensity(w) for w in windows_by_activity[activity]]
        print(f"{activity.upper()}: min={min(intensities):.2f}, mean={np.mean(intensities):.2f}, max={max(intensities):.2f}")


if __name__ == "__main__":
    main()
