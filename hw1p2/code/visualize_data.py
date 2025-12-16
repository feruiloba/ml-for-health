"""
Visualize accelerometer data for activity classification.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'accelerometer', 'raw')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

ACTIVITIES = ['sitting', 'walking', 'running']
SAMPLING_RATE = 50  # Hz
PLOT_DURATION = 10  # seconds to plot


def load_data():
    """Load all activity CSV files."""
    data = {}
    for activity in ACTIVITIES:
        filepath = os.path.join(DATA_DIR, f'{activity}.csv')
        data[activity] = pd.read_csv(filepath)
        # Calculate magnitude
        df = data[activity]
        df['magnitude'] = np.sqrt(df['x']**2 + df['y']**2 + df['z']**2)
    return data


def print_statistics(data):
    """Print summary statistics for each activity."""
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    for activity in ACTIVITIES:
        df = data[activity]
        print(f"\n{activity.upper()}")
        print("-" * 40)

        stats = []
        for axis in ['x', 'y', 'z', 'magnitude']:
            stats.append({
                'Axis': axis.upper(),
                'Mean': df[axis].mean(),
                'Std': df[axis].std(),
                'Min': df[axis].min(),
                'Max': df[axis].max()
            })

        stats_df = pd.DataFrame(stats)
        stats_df = stats_df.set_index('Axis')
        print(stats_df.to_string(float_format=lambda x: f'{x:8.3f}'))

    print("\n" + "=" * 80)


def create_visualization(data):
    """Create visualization plots."""
    samples_to_plot = PLOT_DURATION * SAMPLING_RATE

    fig, axes = plt.subplots(len(ACTIVITIES), 4, figsize=(16, 10))
    fig.suptitle(f'Accelerometer Data: {samples_to_plot} Samples per Activity', fontsize=14, fontweight='bold')

    colors = {'x': '#e74c3c', 'y': '#27ae60', 'z': '#3498db', 'magnitude': '#9b59b6'}

    for row, activity in enumerate(ACTIVITIES):
        df = data[activity].head(samples_to_plot)
        samples = np.arange(len(df))

        for col, axis in enumerate(['x', 'y', 'z', 'magnitude']):
            ax = axes[row, col]
            ax.plot(samples, df[axis], color=colors[axis], linewidth=0.8)
            ax.set_xlim(0, samples_to_plot)

            # Set y-axis limits based on axis type (data in g-units)
            if axis == 'magnitude':
                ax.set_ylim(0, 3)
            elif axis == 'z':
                ax.set_ylim(-1, 3)
            else:
                ax.set_ylim(-2, 2)

            # Labels
            if row == 0:
                ax.set_title(axis.upper(), fontweight='bold')
            if col == 0:
                ax.set_ylabel(f'{activity.upper()}\n(g)')
            if row == len(ACTIVITIES) - 1:
                ax.set_xlabel('Samples')

            ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save plot
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, 'data_visualization.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: {output_path}")

    plt.close()


def main():
    print("Loading data...")
    data = load_data()

    print_statistics(data)

    print("\nCreating visualization...")
    create_visualization(data)

    print("\nDone!")


if __name__ == "__main__":
    main()
