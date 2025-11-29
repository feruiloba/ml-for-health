import csv
import matplotlib.pyplot as plt
import sys

# Data structure to hold points: { alpha_value: [(cm, ber, dr), ...] }
data_by_alpha = {}

try:
    with open('results.csv', 'r') as f:
        reader = csv.reader(f)

        # Skip the header row (alpha,cm,BER,DR)
        next(reader, None)

        for row in reader:
            if not row: continue # Skip empty rows

            # Parse values
            try:
                alpha = float(row[0])
                cm = float(row[1])
                ber = float(row[2])
                dr = float(row[3])

                if alpha not in data_by_alpha:
                    data_by_alpha[alpha] = []

                # Store as a tuple
                data_by_alpha[alpha].append((cm, ber, dr))

            except ValueError:
                print(f"Skipping invalid row: {row}")

except FileNotFoundError:
    print("Error: 'results.csv' not found.")
    sys.exit()

# Sort the data by distance (cm) for each alpha to ensure lines connect correctly
for alpha in data_by_alpha:
    # Sort by the first element of the tuple (cm)
    data_by_alpha[alpha].sort(key=lambda x: x[0])

# Get sorted unique alphas for consistent legend order
sorted_alphas = sorted(data_by_alpha.keys())

# Create the plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Plot 1: BER vs Distance ---
for alpha in sorted_alphas:
    points = data_by_alpha[alpha]
    x_cm = [p[0] for p in points]
    y_ber = [p[1] for p in points]

    ax1.plot(x_cm, y_ber, marker='o', label=f'Alpha={alpha}')

ax1.set_xlabel('Distance (cm)')
ax1.set_ylabel('Bit Error Rate (BER)')
ax1.set_title('Bit Error Rate vs Distance')
ax1.legend()
ax1.grid(True)

# --- Plot 2: Data Rate vs Distance ---
for alpha in sorted_alphas:
    points = data_by_alpha[alpha]
    x_cm = [p[0] for p in points]
    y_dr = [p[2] for p in points]

    ax2.plot(x_cm, y_dr, marker='s', label=f'Alpha={alpha}')

ax2.set_xlabel('Distance (cm)')
ax2.set_ylabel('Data Rate (bps)')
ax2.set_title('Data Rate vs Distance')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()