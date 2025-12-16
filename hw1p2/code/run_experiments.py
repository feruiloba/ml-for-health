"""
Run experiments: Generate all test prompts with their data for LLM evaluation.
Outputs prompts in a format ready for batch evaluation.
"""

import json
import os
from format_for_prompt import compute_statistics, format_raw_only

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

PROMPT_VERSIONS = [
    'v1_context_free',
    'v2_context_inclusive',
    'v3_expert_knowledge',
    'v3_1shot',
    'v3_3shot',
    'v3_5shot',
    'v4_stats_reasoning',
    'v5_zero_shot'
]


def format_stats_clean(window):
    """Clean stats format."""
    stats = compute_statistics(window['samples'])
    return f"""[Statistical Summary]
X-axis: mean={stats['x']['mean']:.2f}, std={stats['x']['std']:.2f}
Y-axis: mean={stats['y']['mean']:.2f}, std={stats['y']['std']:.2f}
Z-axis: mean={stats['z']['mean']:.2f}, std={stats['z']['std']:.2f}
Magnitude: mean={stats['magnitude']['mean']:.2f}, std={stats['magnitude']['std']:.2f}
Dominant frequency: {stats['dominant_freq']:.1f} Hz"""


def format_stats_compact(window):
    """Compact stats format for v4."""
    stats = compute_statistics(window['samples'])
    return (
        f"Statistics: X(mean={stats['x']['mean']:.1f}, std={stats['x']['std']:.2f}), "
        f"Y(mean={stats['y']['mean']:.1f}, std={stats['y']['std']:.2f}), "
        f"Z(mean={stats['z']['mean']:.1f}, std={stats['z']['std']:.2f}), "
        f"Magnitude(std={stats['magnitude']['std']:.2f}), "
        f"DominantFreq={stats['dominant_freq']:.1f}Hz"
    )


def get_formatter(version):
    """Get the appropriate formatter for each prompt version."""
    if version in ['v1_context_free', 'v2_context_inclusive']:
        return format_raw_only
    elif version == 'v4_stats_reasoning':
        return format_stats_compact
    else:
        return format_stats_clean


def main():
    # Load test data
    with open(os.path.join(PROCESSED_DIR, 'test.json')) as f:
        test_data = json.load(f)

    # Sort by label for organized output
    test_data.sort(key=lambda x: (x['label'], x['window_id']))

    print("=" * 80)
    print("TEST DATA SUMMARY FOR LLM EVALUATION")
    print("=" * 80)
    print("\nTest windows to classify:")
    print("-" * 40)

    for w in test_data:
        stats = compute_statistics(w['samples'])
        print(f"  {w['window_id']}: label={w['label']}, z_std={stats['z']['std']:.2f}, freq={stats['dominant_freq']:.1f}Hz")

    # Generate compact view of all test cases
    print("\n" + "=" * 80)
    print("COMPACT TEST DATA FOR QUICK CLASSIFICATION")
    print("=" * 80)
    print("\nFor each window, classify as: sitting, walking, or running")
    print("Key features: sitting(std<0.2), walking(std~1.5, 2Hz), running(std~3.5, 3Hz)\n")

    for w in test_data:
        stats = compute_statistics(w['samples'])
        print(f"{w['window_id']}: X(std={stats['x']['std']:.2f}) Y(std={stats['y']['std']:.2f}) Z(std={stats['z']['std']:.2f}) Mag(std={stats['magnitude']['std']:.2f}) Freq={stats['dominant_freq']:.1f}Hz")

    # Save batch evaluation file
    batch_file = os.path.join(RESULTS_DIR, 'batch_evaluation.txt')
    with open(batch_file, 'w') as f:
        f.write("BATCH EVALUATION: Classify each window\n")
        f.write("=" * 60 + "\n\n")
        f.write("Activity signatures:\n")
        f.write("- SITTING: std < 0.2, no periodic motion\n")
        f.write("- WALKING: std 1-3, frequency ~2.0 Hz\n")
        f.write("- RUNNING: std 3-6, frequency ~3.0 Hz\n\n")
        f.write("Window Data:\n")
        f.write("-" * 60 + "\n")

        for w in test_data:
            stats = compute_statistics(w['samples'])
            f.write(f"\n{w['window_id']}:\n")
            f.write(f"  X: mean={stats['x']['mean']:.2f}, std={stats['x']['std']:.2f}\n")
            f.write(f"  Y: mean={stats['y']['mean']:.2f}, std={stats['y']['std']:.2f}\n")
            f.write(f"  Z: mean={stats['z']['mean']:.2f}, std={stats['z']['std']:.2f}\n")
            f.write(f"  Magnitude: mean={stats['magnitude']['mean']:.2f}, std={stats['magnitude']['std']:.2f}\n")
            f.write(f"  Dominant frequency: {stats['dominant_freq']:.1f} Hz\n")

    print(f"\n\nSaved batch evaluation file: {batch_file}")


if __name__ == "__main__":
    main()
