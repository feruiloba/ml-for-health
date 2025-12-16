"""
Create prompt templates and populate them with real training examples.
"""

import json
import os
from format_for_prompt import (
    format_raw_only,
    format_raw_with_context,
    format_stats_with_expert_knowledge,
    format_stats_only,
    compute_statistics
)

# Paths
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')


def get_examples_by_activity(data):
    """Get one example per activity from training data."""
    examples = {}
    for window in data:
        label = window['label']
        if label not in examples:
            examples[label] = window
        if len(examples) == 3:
            break
    return examples


def create_v1_context_free(examples):
    """V1: Context-free with RAW_ONLY format."""
    template = """Classify the following sensor data as one of: sitting, walking, running

Example 1 (sitting):
{sitting_example}
Classification: sitting

Example 2 (walking):
{walking_example}
Classification: walking

Example 3 (running):
{running_example}
Classification: running

Now classify this data:
[TEST_DATA_HERE]

Classification:"""

    return template.format(
        sitting_example=format_raw_only(examples['sitting']),
        walking_example=format_raw_only(examples['walking']),
        running_example=format_raw_only(examples['running'])
    )


def create_v2_context_inclusive(examples):
    """V2: Context-inclusive with RAW_WITH_CONTEXT format."""
    template = """You are analyzing smartphone accelerometer data. The accelerometer measures acceleration in m/s² along three axes:
- X-axis: lateral (side-to-side) movement
- Y-axis: vertical movement (includes ~9.8 m/s² gravity when phone is upright)
- Z-axis: forward/backward movement

Your task is to classify the activity as one of: sitting, walking, running

Example 1 (sitting):
{sitting_example}
Classification: sitting

Example 2 (walking):
{walking_example}
Classification: walking

Example 3 (running):
{running_example}
Classification: running

Now classify this data:
[TEST_DATA_HERE]

Classification:"""

    return template.format(
        sitting_example=format_raw_with_context(examples['sitting']),
        walking_example=format_raw_with_context(examples['walking']),
        running_example=format_raw_with_context(examples['running'])
    )


def create_v3_expert_knowledge(examples):
    """V3: Expert knowledge with STATS_WITH_EXPERT_KNOWLEDGE format."""
    template = """You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
The accelerometer measures acceleration in m/s² along three axes. Gravity contributes ~9.8 m/s² when stationary.

[Activity Signatures]
- SITTING: Characterized by gravity-dominated readings with very low variance (std < 0.2 m/s²). No periodic motion detected. The signal is essentially flat with minor sensor noise.

- WALKING: Shows periodic oscillation at approximately 1.5-2.0 Hz corresponding to step frequency. Moderate variance (std 1-3 m/s²) with rhythmic peaks on the vertical axis as each foot strikes the ground.

- RUNNING: Displays faster periodic oscillation at approximately 2.5-3.5 Hz. Higher variance (std 3-6 m/s²) with more pronounced impact peaks due to greater ground reaction forces.

[Examples]
Example 1 - Sitting:
{sitting_example}
Classification: sitting

Example 2 - Walking:
{walking_example}
Classification: walking

Example 3 - Running:
{running_example}
Classification: running

[Your Task]
Analyze the following sensor data and classify the activity:
[TEST_DATA_HERE]

Classification:"""

    return template.format(
        sitting_example=format_stats_with_expert_knowledge(examples['sitting']),
        walking_example=format_stats_with_expert_knowledge(examples['walking']),
        running_example=format_stats_with_expert_knowledge(examples['running'])
    )


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


def create_v4_stats_reasoning(examples):
    """V4: Stats with reasoning examples."""
    # Get stats for each example
    sitting_stats = format_stats_compact(examples['sitting'])
    walking_stats = format_stats_compact(examples['walking'])
    running_stats = format_stats_compact(examples['running'])

    template = """You are analyzing statistical features extracted from smartphone accelerometer data.

[Activity Patterns]
- Sitting: std < 0.2, dominant frequency ~0 Hz
- Walking: std 1-3, dominant frequency 1.5-2.0 Hz
- Running: std 3-6, dominant frequency 2.5-3.5 Hz

[Examples with Reasoning]
Example 1:
{sitting_stats}
Reasoning: Very low standard deviation across all axes and near-zero dominant frequency indicate no periodic motion. This is consistent with a stationary position.
Classification: sitting

Example 2:
{walking_stats}
Reasoning: Moderate variance with dominant frequency around 2 Hz matches typical walking cadence of ~120 steps/minute.
Classification: walking

Example 3:
{running_stats}
Reasoning: High variance and dominant frequency near 3 Hz indicates fast periodic motion with strong impacts, consistent with running.
Classification: running

[Your Task]
Analyze this data. First provide your reasoning, then your classification.
[TEST_DATA_HERE]

Reasoning:
Classification:"""

    return template.format(
        sitting_stats=sitting_stats,
        walking_stats=walking_stats,
        running_stats=running_stats
    )


def create_v5_zero_shot():
    """V5: Zero-shot (no examples)."""
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

    # Get one example per activity
    examples = get_examples_by_activity(train_data)

    print("Creating prompt templates...")
    print(f"Using examples: {[w['window_id'] for w in examples.values()]}")

    os.makedirs(PROMPTS_DIR, exist_ok=True)

    # Create and save each prompt
    prompts = {
        'v1_context_free.txt': create_v1_context_free(examples),
        'v2_context_inclusive.txt': create_v2_context_inclusive(examples),
        'v3_expert_knowledge.txt': create_v3_expert_knowledge(examples),
        'v4_stats_reasoning.txt': create_v4_stats_reasoning(examples),
        'v5_zero_shot.txt': create_v5_zero_shot()
    }

    for filename, content in prompts.items():
        filepath = os.path.join(PROMPTS_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        char_count = len(content)
        print(f"  Saved {filename} ({char_count} chars, ~{char_count//4} tokens)")

    # Show v3 as requested
    print("\n" + "=" * 80)
    print("COMPLETE PROMPT: v3_expert_knowledge.txt")
    print("=" * 80)
    print(prompts['v3_expert_knowledge.txt'])


if __name__ == "__main__":
    main()
