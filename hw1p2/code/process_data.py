"""
Process raw accelerometer data into windowed segments for LLM classification.
"""

import json
import os
import random
import pandas as pd

# Configuration
SAMPLING_RATE = 50  # Hz
WINDOW_DURATION = 5  # seconds
WINDOW_SIZE = SAMPLING_RATE * WINDOW_DURATION  # 250 samples
TEST_RATIO = 0.2
RANDOM_SEED = 42

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'accelerometer', 'raw')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'accelerometer', 'processed')

ACTIVITIES = ['sitting', 'walking', 'running']


def load_and_segment(activity):
    """Load CSV and segment into windows."""
    filepath = os.path.join(DATA_DIR, f'{activity}.csv')
    df = pd.read_csv(filepath)

    windows = []
    num_windows = len(df) // WINDOW_SIZE

    for i in range(num_windows):
        start_idx = i * WINDOW_SIZE
        end_idx = start_idx + WINDOW_SIZE
        window_df = df.iloc[start_idx:end_idx]

        # Format samples as [[x, y, z], ...]
        samples = window_df[['x', 'y', 'z']].values.tolist()

        window = {
            "window_id": f"{activity}_{i+1:03d}",
            "label": activity,
            "samples": samples
        }
        windows.append(window)

    return windows


def train_test_split(windows, test_ratio, seed):
    """Split windows into train and test sets."""
    random.seed(seed)
    shuffled = windows.copy()
    random.shuffle(shuffled)

    split_idx = int(len(shuffled) * (1 - test_ratio))
    return shuffled[:split_idx], shuffled[split_idx:]


def main():
    print("Processing accelerometer data into windows...")
    print(f"Window size: {WINDOW_DURATION}s ({WINDOW_SIZE} samples)")
    print(f"Train/Test split: {int((1-TEST_RATIO)*100)}% / {int(TEST_RATIO*100)}%")
    print()

    train_windows = []
    test_windows = []

    # Load, segment, and split each activity
    for activity in ACTIVITIES:
        windows = load_and_segment(activity)
        print(f"{activity.upper()}: {len(windows)} windows total")

        train, test = train_test_split(windows, TEST_RATIO, RANDOM_SEED)
        train_windows.extend(train)
        test_windows.extend(test)

    # Shuffle the combined sets
    random.seed(RANDOM_SEED)
    random.shuffle(train_windows)
    random.shuffle(test_windows)

    # Save to JSON
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    train_path = os.path.join(OUTPUT_DIR, 'train.json')
    with open(train_path, 'w') as f:
        json.dump(train_windows, f, indent=2)

    test_path = os.path.join(OUTPUT_DIR, 'test.json')
    with open(test_path, 'w') as f:
        json.dump(test_windows, f, indent=2)

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"\nTraining set: {len(train_windows)} windows")
    for activity in ACTIVITIES:
        count = sum(1 for w in train_windows if w['label'] == activity)
        print(f"  - {activity}: {count}")

    print(f"\nTest set: {len(test_windows)} windows")
    for activity in ACTIVITIES:
        count = sum(1 for w in test_windows if w['label'] == activity)
        print(f"  - {activity}: {count}")

    print(f"\nSaved to:")
    print(f"  - {train_path}")
    print(f"  - {test_path}")


if __name__ == "__main__":
    main()
