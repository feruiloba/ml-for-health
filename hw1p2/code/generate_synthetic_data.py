"""
Generate synthetic accelerometer data for activity classification.

Activities:
- SITTING: low magnitude, minimal variation, gravity ~9.8 on one axis
- WALKING: periodic oscillation ~2Hz, moderate variance, rhythmic
- RUNNING: periodic oscillation ~3Hz, higher variance, pronounced peaks
"""

import numpy as np
import pandas as pd
import os

# Configuration
SAMPLING_RATE = 50  # Hz
DURATION = 120  # seconds (2 minutes)
NUM_SAMPLES = SAMPLING_RATE * DURATION  # 6000 samples
GRAVITY = 9.81  # m/s^2

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')


def generate_sitting_data(num_samples):
    """
    Sitting: Phone relatively stationary (e.g., in pocket or on table).
    - Gravity dominates on one axis (~9.8)
    - Very small random noise on all axes
    - Occasional tiny movements (fidgeting)
    """
    # Assume phone is flat, gravity on z-axis
    # Small noise to simulate sensor imperfection and micro-movements
    noise_std = 0.05

    x = np.random.normal(0, noise_std, num_samples)
    y = np.random.normal(0, noise_std, num_samples)
    z = np.random.normal(GRAVITY, noise_std, num_samples)

    # Add occasional small fidget movements (random bumps)
    num_fidgets = 10
    fidget_indices = np.random.choice(num_samples, num_fidgets, replace=False)
    for idx in fidget_indices:
        duration = np.random.randint(5, 15)
        end_idx = min(idx + duration, num_samples)
        fidget_magnitude = np.random.uniform(0.1, 0.3)
        x[idx:end_idx] += np.random.normal(0, fidget_magnitude, end_idx - idx)
        y[idx:end_idx] += np.random.normal(0, fidget_magnitude, end_idx - idx)

    return pd.DataFrame({
        'x': x,
        'y': y,
        'z': z
    })


def generate_walking_data(num_samples):
    """
    Walking: Rhythmic motion at ~2Hz step frequency.
    - Periodic oscillation on vertical axis (z)
    - Forward/backward sway on x-axis
    - Side-to-side sway on y-axis
    - Moderate amplitude variations
    """
    step_freq = 2.0  # Hz (typical walking cadence)
    t = np.arange(num_samples) / SAMPLING_RATE

    # Vertical oscillation (most prominent during walking)
    z_amplitude = 2.0
    z = GRAVITY + z_amplitude * np.sin(2 * np.pi * step_freq * t)
    # Add harmonics for more realistic gait pattern
    z += 0.5 * np.sin(2 * np.pi * 2 * step_freq * t)

    # Forward/backward acceleration (heel strike and push-off)
    x_amplitude = 1.5
    x = x_amplitude * np.sin(2 * np.pi * step_freq * t + np.pi/4)
    x += 0.3 * np.sin(2 * np.pi * 2 * step_freq * t)

    # Lateral sway (weight shift between feet)
    y_amplitude = 0.8
    y = y_amplitude * np.sin(2 * np.pi * (step_freq / 2) * t)

    # Add noise
    noise_std = 0.2
    x += np.random.normal(0, noise_std, num_samples)
    y += np.random.normal(0, noise_std, num_samples)
    z += np.random.normal(0, noise_std, num_samples)

    # Add slight amplitude variation over time (natural walking variation)
    amplitude_variation = 1 + 0.1 * np.sin(2 * np.pi * 0.1 * t)
    x *= amplitude_variation
    z = GRAVITY + (z - GRAVITY) * amplitude_variation

    return pd.DataFrame({
        'x': x,
        'y': y,
        'z': z
    })


def generate_running_data(num_samples):
    """
    Running: Higher frequency (~3Hz) and amplitude motion.
    - More pronounced vertical oscillation (flight phase)
    - Stronger impact peaks
    - Higher overall acceleration magnitudes
    """
    step_freq = 3.0  # Hz (typical running cadence)
    t = np.arange(num_samples) / SAMPLING_RATE

    # Vertical oscillation (very pronounced during running)
    z_amplitude = 4.5
    z = GRAVITY + z_amplitude * np.sin(2 * np.pi * step_freq * t)
    # Add harmonics for impact peaks
    z += 1.5 * np.sin(2 * np.pi * 2 * step_freq * t)
    z += 0.8 * np.sin(2 * np.pi * 3 * step_freq * t)

    # Forward/backward acceleration (stronger push-off)
    x_amplitude = 3.0
    x = x_amplitude * np.sin(2 * np.pi * step_freq * t + np.pi/4)
    x += 1.0 * np.sin(2 * np.pi * 2 * step_freq * t)

    # Lateral sway
    y_amplitude = 1.5
    y = y_amplitude * np.sin(2 * np.pi * (step_freq / 2) * t)
    y += 0.5 * np.sin(2 * np.pi * step_freq * t)

    # Add noise (more noise due to higher impact)
    noise_std = 0.4
    x += np.random.normal(0, noise_std, num_samples)
    y += np.random.normal(0, noise_std, num_samples)
    z += np.random.normal(0, noise_std, num_samples)

    # Add impact spikes (foot strikes)
    spike_interval = int(SAMPLING_RATE / step_freq)  # samples between spikes
    for i in range(0, num_samples, spike_interval):
        if i < num_samples:
            spike_magnitude = np.random.uniform(1.5, 2.5)
            z[i] += spike_magnitude
            # Spike affects a few samples
            for j in range(1, min(3, num_samples - i)):
                z[i + j] += spike_magnitude * (1 - j / 3)

    return pd.DataFrame({
        'x': x,
        'y': y,
        'z': z
    })


def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Set seed for reproducibility
    np.random.seed(42)

    print(f"Generating synthetic accelerometer data...")
    print(f"Sampling rate: {SAMPLING_RATE} Hz")
    print(f"Duration: {DURATION} seconds ({NUM_SAMPLES} samples)")
    print()

    # Generate and save sitting data
    print("Generating SITTING data...")
    sitting_df = generate_sitting_data(NUM_SAMPLES)
    sitting_path = os.path.join(OUTPUT_DIR, 'sitting.csv')
    sitting_df.to_csv(sitting_path, index=False)
    print(f"  Saved to: {sitting_path}")
    print(f"  X range: [{sitting_df['x'].min():.2f}, {sitting_df['x'].max():.2f}]")
    print(f"  Y range: [{sitting_df['y'].min():.2f}, {sitting_df['y'].max():.2f}]")
    print(f"  Z range: [{sitting_df['z'].min():.2f}, {sitting_df['z'].max():.2f}]")
    print()

    # Generate and save walking data
    print("Generating WALKING data...")
    walking_df = generate_walking_data(NUM_SAMPLES)
    walking_path = os.path.join(OUTPUT_DIR, 'walking.csv')
    walking_df.to_csv(walking_path, index=False)
    print(f"  Saved to: {walking_path}")
    print(f"  X range: [{walking_df['x'].min():.2f}, {walking_df['x'].max():.2f}]")
    print(f"  Y range: [{walking_df['y'].min():.2f}, {walking_df['y'].max():.2f}]")
    print(f"  Z range: [{walking_df['z'].min():.2f}, {walking_df['z'].max():.2f}]")
    print()

    # Generate and save running data
    print("Generating RUNNING data...")
    running_df = generate_running_data(NUM_SAMPLES)
    running_path = os.path.join(OUTPUT_DIR, 'running.csv')
    running_df.to_csv(running_path, index=False)
    print(f"  Saved to: {running_path}")
    print(f"  X range: [{running_df['x'].min():.2f}, {running_df['x'].max():.2f}]")
    print(f"  Y range: [{running_df['y'].min():.2f}, {running_df['y'].max():.2f}]")
    print(f"  Z range: [{running_df['z'].min():.2f}, {running_df['z'].max():.2f}]")
    print()

    print("Data generation complete!")


if __name__ == "__main__":
    main()
