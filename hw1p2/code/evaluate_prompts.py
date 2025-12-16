"""
Prepare test cases for manual LLM evaluation.
Generates complete prompts for all test windows across all prompt versions.
"""

import json
import os
import csv
from format_for_prompt import (
    format_raw_only,
    format_stats_only,
    format_raw_with_context,
    format_stats_with_expert_knowledge,
    compute_statistics
)

# Paths
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'accelerometer', 'processed')
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

# Prompt versions to evaluate
PROMPT_VERSIONS = [
    'v1_context_free.txt',
    'v2_context_inclusive.txt',
    'v3_expert_knowledge.txt',
    'v3_1shot.txt',
    'v3_3shot.txt',
    'v3_5shot.txt',
    'v4_stats_reasoning.txt',
    'v5_zero_shot.txt'
]


def format_stats_clean(window):
    """Clean stats format for v3 variants and v5."""
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


def detect_formatter(prompt_version, template_content):
    """Detect which formatter to use based on prompt version and content."""
    if prompt_version == 'v1_context_free.txt':
        return 'RAW_ONLY'
    elif prompt_version == 'v2_context_inclusive.txt':
        return 'RAW_WITH_CONTEXT'
    elif prompt_version.startswith('v3_'):
        return 'STATS_CLEAN'  # Clean stats for v3 variants
    elif prompt_version == 'v4_stats_reasoning.txt':
        return 'STATS_COMPACT'
    elif prompt_version == 'v5_zero_shot.txt':
        return 'STATS_CLEAN'
    else:
        # Default fallback
        return 'STATS_CLEAN'


def format_test_data(window, formatter_type):
    """Format test data according to the specified formatter type."""
    if formatter_type == 'RAW_ONLY':
        return format_raw_only(window)
    elif formatter_type == 'RAW_WITH_CONTEXT':
        # For context-inclusive, just use raw data (context is in template)
        return format_raw_only(window)
    elif formatter_type == 'STATS_CLEAN':
        return format_stats_clean(window)
    elif formatter_type == 'STATS_COMPACT':
        return format_stats_compact(window)
    else:
        return format_stats_clean(window)


def main():
    print("=" * 70)
    print("PREPARING TEST CASES FOR MANUAL EVALUATION")
    print("=" * 70)

    # Load test data
    with open(os.path.join(PROCESSED_DIR, 'test.json')) as f:
        test_data = json.load(f)

    print(f"\nLoaded {len(test_data)} test windows")

    # Load all prompt templates
    templates = {}
    for version in PROMPT_VERSIONS:
        filepath = os.path.join(PROMPTS_DIR, version)
        if os.path.exists(filepath):
            with open(filepath) as f:
                templates[version] = f.read()
            print(f"  Loaded: {version}")
        else:
            print(f"  WARNING: {version} not found!")

    # Create output directories
    test_prompts_dir = os.path.join(RESULTS_DIR, 'test_prompts')
    os.makedirs(test_prompts_dir, exist_ok=True)

    # Track all test cases for answer key
    answer_key_rows = []
    total_prompts = 0

    # Generate test prompts for each version
    print("\n" + "-" * 70)
    print("GENERATING TEST PROMPTS")
    print("-" * 70)

    for version, template in templates.items():
        version_name = version.replace('.txt', '')
        version_dir = os.path.join(test_prompts_dir, version_name)
        os.makedirs(version_dir, exist_ok=True)

        formatter_type = detect_formatter(version, template)
        prompts_generated = 0

        for window in test_data:
            window_id = window['window_id']
            true_label = window['label']

            # Format test data
            formatted_data = format_test_data(window, formatter_type)

            # Replace placeholder with test data
            complete_prompt = template.replace('[TEST_DATA_HERE]', formatted_data)

            # Save complete prompt
            prompt_path = os.path.join(version_dir, f"{window_id}.txt")
            with open(prompt_path, 'w') as f:
                f.write(complete_prompt)

            prompts_generated += 1
            total_prompts += 1

            # Add to answer key
            answer_key_rows.append({
                'prompt_version': version_name,
                'window_id': window_id,
                'true_label': true_label,
                'predicted_label': '',
                'correct': ''
            })

        print(f"  {version_name}: {prompts_generated} prompts (formatter: {formatter_type})")

    # Save answer key CSV
    answer_key_path = os.path.join(RESULTS_DIR, 'answer_key.csv')
    with open(answer_key_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['prompt_version', 'window_id', 'true_label', 'predicted_label', 'correct'])
        writer.writeheader()
        writer.writerows(answer_key_rows)

    print(f"\nSaved answer key: {answer_key_path}")
    print(f"  Total rows: {len(answer_key_rows)}")

    # Create quick_test.md with one sample from each version
    # Use first test window for consistency
    sample_window = test_data[0]
    sample_id = sample_window['window_id']
    sample_label = sample_window['label']

    quick_test_content = [
        "# Quick Test Prompts",
        "",
        f"Sample window: **{sample_id}** (true label: **{sample_label}**)",
        "",
        "Copy each prompt below into an LLM and record the classification.",
        "",
        "---",
        ""
    ]

    for version, template in templates.items():
        version_name = version.replace('.txt', '')
        formatter_type = detect_formatter(version, template)
        formatted_data = format_test_data(sample_window, formatter_type)
        complete_prompt = template.replace('[TEST_DATA_HERE]', formatted_data)

        quick_test_content.extend([
            f"## {version_name}",
            "",
            "```",
            complete_prompt,
            "```",
            "",
            f"**Prediction:** ________________",
            "",
            "---",
            ""
        ])

    quick_test_path = os.path.join(RESULTS_DIR, 'quick_test.md')
    with open(quick_test_path, 'w') as f:
        f.write('\n'.join(quick_test_content))

    print(f"Saved quick test: {quick_test_path}")
    print(f"  Sample window: {sample_id} (true label: {sample_label})")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nTotal test prompts generated: {total_prompts}")
    print(f"Test windows: {len(test_data)}")
    print(f"Prompt versions: {len(templates)}")
    print(f"Prompts per version: {len(test_data)}")

    print(f"\nOutput files:")
    print(f"  - {test_prompts_dir}/[version]/[window_id].txt")
    print(f"  - {answer_key_path}")
    print(f"  - {quick_test_path}")

    # Show test set distribution
    print("\nTest set distribution:")
    for label in ['sitting', 'walking', 'running']:
        count = sum(1 for w in test_data if w['label'] == label)
        print(f"  {label}: {count} windows")


if __name__ == "__main__":
    main()
