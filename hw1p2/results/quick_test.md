# Quick Test Prompts

Sample window: **walking_009** (true label: **walking**)

Copy each prompt below into an LLM and record the classification.

---

## v1_context_free

```
Classify the following sensor data as one of: sitting, walking, running

Example 1 (sitting):
t=60.00s: x=-0.10, y=0.04, z=9.80
t=60.20s: x=-0.00, y=0.02, z=9.79
t=60.40s: x=0.06, y=0.01, z=9.84
t=60.60s: x=-0.12, y=-0.00, z=9.76
t=60.80s: x=0.03, y=0.01, z=9.79
t=61.00s: x=-0.07, y=0.02, z=9.80
t=61.20s: x=0.02, y=-0.01, z=9.89
t=61.40s: x=-0.06, y=0.05, z=9.73
t=61.60s: x=0.06, y=-0.01, z=9.80
t=61.80s: x=-0.09, y=0.03, z=9.77
t=62.00s: x=-0.04, y=-0.02, z=9.88
t=62.20s: x=-0.06, y=0.09, z=9.90
t=62.40s: x=-0.02, y=-0.11, z=9.76
t=62.60s: x=-0.00, y=0.06, z=9.79
t=62.80s: x=0.04, y=-0.00, z=9.84
t=63.00s: x=0.04, y=0.03, z=9.84
t=63.20s: x=-0.03, y=-0.03, z=9.77
t=63.40s: x=-0.05, y=-0.05, z=9.80
t=63.60s: x=0.05, y=-0.00, z=9.79
t=63.80s: x=-0.02, y=-0.05, z=9.76
t=64.00s: x=0.01, y=0.08, z=9.86
t=64.20s: x=0.06, y=-0.07, z=9.86
t=64.40s: x=-0.05, y=0.01, z=9.82
t=64.60s: x=-0.02, y=-0.00, z=9.81
t=64.80s: x=0.00, y=0.04, z=9.83
Classification: sitting

Example 2 (walking):
t=20.00s: x=1.05, y=-0.23, z=9.74
t=20.20s: x=-0.80, y=0.76, z=10.81
t=20.40s: x=-1.00, y=0.41, z=7.41
t=20.60s: x=1.66, y=-0.32, z=12.09
t=20.80s: x=-1.21, y=-0.44, z=9.31
t=21.00s: x=0.60, y=0.06, z=9.79
t=21.20s: x=-0.74, y=0.82, z=10.32
t=21.40s: x=-0.76, y=0.48, z=8.05
t=21.60s: x=1.39, y=-0.58, z=12.45
t=21.80s: x=-1.57, y=-0.98, z=8.88
t=22.00s: x=1.11, y=0.09, z=10.42
t=22.20s: x=-0.53, y=0.80, z=10.63
t=22.40s: x=-0.82, y=0.36, z=7.09
t=22.60s: x=1.41, y=-0.38, z=12.34
t=22.80s: x=-1.84, y=-0.62, z=9.13
t=23.00s: x=0.95, y=-0.10, z=9.33
t=23.20s: x=-0.16, y=0.46, z=10.91
t=23.40s: x=-0.57, y=0.40, z=7.99
t=23.60s: x=1.46, y=-0.43, z=12.08
t=23.80s: x=-1.14, y=-0.95, z=9.35
t=24.00s: x=1.20, y=-0.23, z=9.91
t=24.20s: x=-0.57, y=0.97, z=10.36
t=24.40s: x=-0.80, y=0.70, z=7.74
t=24.60s: x=1.89, y=-0.40, z=11.55
t=24.80s: x=-0.91, y=-0.67, z=9.06
Classification: walking

Example 3 (running):
t=30.00s: x=2.01, y=-0.11, z=8.98
t=30.20s: x=-1.49, y=1.24, z=7.53
t=30.40s: x=2.73, y=-0.15, z=15.57
t=30.60s: x=-1.45, y=-1.06, z=4.96
t=30.80s: x=-1.76, y=2.36, z=11.49
t=31.00s: x=2.37, y=-0.68, z=9.72
t=31.20s: x=-1.60, y=-1.42, z=7.22
t=31.40s: x=3.30, y=1.46, z=14.54
t=31.60s: x=-2.49, y=0.00, z=4.74
t=31.80s: x=-1.74, y=-0.83, z=11.74
t=32.00s: x=1.87, y=-0.75, z=11.51
t=32.20s: x=-2.39, y=0.73, z=7.45
t=32.40s: x=3.33, y=-1.26, z=14.38
t=32.60s: x=-1.93, y=-1.34, z=4.90
t=32.80s: x=-1.20, y=1.85, z=12.34
t=33.00s: x=1.98, y=-0.14, z=10.56
t=33.20s: x=-2.09, y=-2.43, z=8.11
t=33.40s: x=3.29, y=0.81, z=14.91
t=33.60s: x=-1.68, y=0.57, z=7.56
t=33.80s: x=-2.37, y=-1.34, z=11.72
t=34.00s: x=1.77, y=0.31, z=10.30
t=34.20s: x=-1.91, y=0.71, z=7.10
t=34.40s: x=2.90, y=-0.54, z=14.16
t=34.60s: x=-1.50, y=-1.30, z=6.55
t=34.80s: x=-1.06, y=1.58, z=12.06
Classification: running

Now classify this data:
t=40.00s: x=0.96, y=-0.10, z=9.85
t=40.20s: x=-0.67, y=0.78, z=10.15
t=40.40s: x=-0.95, y=0.39, z=7.37
t=40.60s: x=1.75, y=-0.38, z=12.32
t=40.80s: x=-1.23, y=-1.07, z=8.76
t=41.00s: x=1.22, y=-0.29, z=9.75
t=41.20s: x=-0.78, y=0.65, z=10.52
t=41.40s: x=-0.90, y=0.51, z=7.28
t=41.60s: x=1.61, y=-0.13, z=12.20
t=41.80s: x=-1.26, y=-0.63, z=8.71
t=42.00s: x=1.28, y=-0.02, z=10.19
t=42.20s: x=-0.44, y=0.74, z=10.55
t=42.40s: x=-0.68, y=0.28, z=7.41
t=42.60s: x=1.76, y=-0.70, z=12.19
t=42.80s: x=-1.30, y=-0.67, z=9.22
t=43.00s: x=1.00, y=-0.05, z=9.93
t=43.20s: x=-0.42, y=0.63, z=10.64
t=43.40s: x=-1.13, y=0.28, z=7.40
t=43.60s: x=1.30, y=-0.15, z=12.00
t=43.80s: x=-1.23, y=-0.79, z=9.12
t=44.00s: x=1.34, y=-0.11, z=9.89
t=44.20s: x=-0.23, y=0.75, z=10.38
t=44.40s: x=-0.24, y=0.61, z=7.48
t=44.60s: x=1.61, y=-0.61, z=11.95
t=44.80s: x=-1.56, y=-0.90, z=9.17

Classification:
```

**Prediction:** ________________

---

## v2_context_inclusive

```
You are analyzing smartphone accelerometer data. The accelerometer measures acceleration in m/s² along three axes:
- X-axis: lateral (side-to-side) movement
- Y-axis: vertical movement (includes ~9.8 m/s² gravity when phone is upright)
- Z-axis: forward/backward movement

Your task is to classify the activity as one of: sitting, walking, running

Example 1 (sitting):
[Sensor Context]
This data is from a smartphone accelerometer measuring acceleration in m/s² along three orthogonal axes (x, y, z). When stationary, gravity contributes approximately 9.8 m/s² to one axis. Movement creates deviations from this baseline.

[Sensor Readings]
t=60.00s: x=-0.10, y=0.04, z=9.80
t=60.20s: x=-0.00, y=0.02, z=9.79
t=60.40s: x=0.06, y=0.01, z=9.84
t=60.60s: x=-0.12, y=-0.00, z=9.76
t=60.80s: x=0.03, y=0.01, z=9.79
t=61.00s: x=-0.07, y=0.02, z=9.80
t=61.20s: x=0.02, y=-0.01, z=9.89
t=61.40s: x=-0.06, y=0.05, z=9.73
t=61.60s: x=0.06, y=-0.01, z=9.80
t=61.80s: x=-0.09, y=0.03, z=9.77
t=62.00s: x=-0.04, y=-0.02, z=9.88
t=62.20s: x=-0.06, y=0.09, z=9.90
t=62.40s: x=-0.02, y=-0.11, z=9.76
t=62.60s: x=-0.00, y=0.06, z=9.79
t=62.80s: x=0.04, y=-0.00, z=9.84
t=63.00s: x=0.04, y=0.03, z=9.84
t=63.20s: x=-0.03, y=-0.03, z=9.77
t=63.40s: x=-0.05, y=-0.05, z=9.80
t=63.60s: x=0.05, y=-0.00, z=9.79
t=63.80s: x=-0.02, y=-0.05, z=9.76
t=64.00s: x=0.01, y=0.08, z=9.86
t=64.20s: x=0.06, y=-0.07, z=9.86
t=64.40s: x=-0.05, y=0.01, z=9.82
t=64.60s: x=-0.02, y=-0.00, z=9.81
t=64.80s: x=0.00, y=0.04, z=9.83
Classification: sitting

Example 2 (walking):
[Sensor Context]
This data is from a smartphone accelerometer measuring acceleration in m/s² along three orthogonal axes (x, y, z). When stationary, gravity contributes approximately 9.8 m/s² to one axis. Movement creates deviations from this baseline.

[Sensor Readings]
t=20.00s: x=1.05, y=-0.23, z=9.74
t=20.20s: x=-0.80, y=0.76, z=10.81
t=20.40s: x=-1.00, y=0.41, z=7.41
t=20.60s: x=1.66, y=-0.32, z=12.09
t=20.80s: x=-1.21, y=-0.44, z=9.31
t=21.00s: x=0.60, y=0.06, z=9.79
t=21.20s: x=-0.74, y=0.82, z=10.32
t=21.40s: x=-0.76, y=0.48, z=8.05
t=21.60s: x=1.39, y=-0.58, z=12.45
t=21.80s: x=-1.57, y=-0.98, z=8.88
t=22.00s: x=1.11, y=0.09, z=10.42
t=22.20s: x=-0.53, y=0.80, z=10.63
t=22.40s: x=-0.82, y=0.36, z=7.09
t=22.60s: x=1.41, y=-0.38, z=12.34
t=22.80s: x=-1.84, y=-0.62, z=9.13
t=23.00s: x=0.95, y=-0.10, z=9.33
t=23.20s: x=-0.16, y=0.46, z=10.91
t=23.40s: x=-0.57, y=0.40, z=7.99
t=23.60s: x=1.46, y=-0.43, z=12.08
t=23.80s: x=-1.14, y=-0.95, z=9.35
t=24.00s: x=1.20, y=-0.23, z=9.91
t=24.20s: x=-0.57, y=0.97, z=10.36
t=24.40s: x=-0.80, y=0.70, z=7.74
t=24.60s: x=1.89, y=-0.40, z=11.55
t=24.80s: x=-0.91, y=-0.67, z=9.06
Classification: walking

Example 3 (running):
[Sensor Context]
This data is from a smartphone accelerometer measuring acceleration in m/s² along three orthogonal axes (x, y, z). When stationary, gravity contributes approximately 9.8 m/s² to one axis. Movement creates deviations from this baseline.

[Sensor Readings]
t=30.00s: x=2.01, y=-0.11, z=8.98
t=30.20s: x=-1.49, y=1.24, z=7.53
t=30.40s: x=2.73, y=-0.15, z=15.57
t=30.60s: x=-1.45, y=-1.06, z=4.96
t=30.80s: x=-1.76, y=2.36, z=11.49
t=31.00s: x=2.37, y=-0.68, z=9.72
t=31.20s: x=-1.60, y=-1.42, z=7.22
t=31.40s: x=3.30, y=1.46, z=14.54
t=31.60s: x=-2.49, y=0.00, z=4.74
t=31.80s: x=-1.74, y=-0.83, z=11.74
t=32.00s: x=1.87, y=-0.75, z=11.51
t=32.20s: x=-2.39, y=0.73, z=7.45
t=32.40s: x=3.33, y=-1.26, z=14.38
t=32.60s: x=-1.93, y=-1.34, z=4.90
t=32.80s: x=-1.20, y=1.85, z=12.34
t=33.00s: x=1.98, y=-0.14, z=10.56
t=33.20s: x=-2.09, y=-2.43, z=8.11
t=33.40s: x=3.29, y=0.81, z=14.91
t=33.60s: x=-1.68, y=0.57, z=7.56
t=33.80s: x=-2.37, y=-1.34, z=11.72
t=34.00s: x=1.77, y=0.31, z=10.30
t=34.20s: x=-1.91, y=0.71, z=7.10
t=34.40s: x=2.90, y=-0.54, z=14.16
t=34.60s: x=-1.50, y=-1.30, z=6.55
t=34.80s: x=-1.06, y=1.58, z=12.06
Classification: running

Now classify this data:
t=40.00s: x=0.96, y=-0.10, z=9.85
t=40.20s: x=-0.67, y=0.78, z=10.15
t=40.40s: x=-0.95, y=0.39, z=7.37
t=40.60s: x=1.75, y=-0.38, z=12.32
t=40.80s: x=-1.23, y=-1.07, z=8.76
t=41.00s: x=1.22, y=-0.29, z=9.75
t=41.20s: x=-0.78, y=0.65, z=10.52
t=41.40s: x=-0.90, y=0.51, z=7.28
t=41.60s: x=1.61, y=-0.13, z=12.20
t=41.80s: x=-1.26, y=-0.63, z=8.71
t=42.00s: x=1.28, y=-0.02, z=10.19
t=42.20s: x=-0.44, y=0.74, z=10.55
t=42.40s: x=-0.68, y=0.28, z=7.41
t=42.60s: x=1.76, y=-0.70, z=12.19
t=42.80s: x=-1.30, y=-0.67, z=9.22
t=43.00s: x=1.00, y=-0.05, z=9.93
t=43.20s: x=-0.42, y=0.63, z=10.64
t=43.40s: x=-1.13, y=0.28, z=7.40
t=43.60s: x=1.30, y=-0.15, z=12.00
t=43.80s: x=-1.23, y=-0.79, z=9.12
t=44.00s: x=1.34, y=-0.11, z=9.89
t=44.20s: x=-0.23, y=0.75, z=10.38
t=44.40s: x=-0.24, y=0.61, z=7.48
t=44.60s: x=1.61, y=-0.61, z=11.95
t=44.80s: x=-1.56, y=-0.90, z=9.17

Classification:
```

**Prediction:** ________________

---

## v3_expert_knowledge

```
You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
The accelerometer measures acceleration in m/s² along three axes. Gravity contributes ~9.8 m/s² when stationary.

[Activity Signatures]
- SITTING: Characterized by gravity-dominated readings with very low variance (std < 0.2 m/s²). No periodic motion detected. The signal is essentially flat with minor sensor noise.

- WALKING: Shows periodic oscillation at approximately 1.5-2.0 Hz corresponding to step frequency. Moderate variance (std 1-3 m/s²) with rhythmic peaks on the vertical axis as each foot strikes the ground.

- RUNNING: Displays faster periodic oscillation at approximately 2.5-3.5 Hz. Higher variance (std 3-6 m/s²) with more pronounced impact peaks due to greater ground reaction forces.

[Examples]
Example 1 - Sitting:
[Expert Knowledge]
Activity signatures in accelerometer data:
- SITTING: Gravity-dominated (~9.8 m/s² on one axis), very low variance (std < 0.2), no periodic motion (dominant freq ~0 Hz)
- WALKING: Periodic vertical oscillation at ~1.5-2.0 Hz (step frequency), moderate variance (std 1-3), rhythmic pattern
- RUNNING: Faster periodic oscillation at ~2.5-3.5 Hz, high variance (std 3-6), pronounced impact peaks

[Statistical Summary]
X-axis: mean=-0.00, std=0.05
Y-axis: mean=-0.00, std=0.05
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 22.6 Hz
Classification: sitting

Example 2 - Walking:
[Expert Knowledge]
Activity signatures in accelerometer data:
- SITTING: Gravity-dominated (~9.8 m/s² on one axis), very low variance (std < 0.2), no periodic motion (dominant freq ~0 Hz)
- WALKING: Periodic vertical oscillation at ~1.5-2.0 Hz (step frequency), moderate variance (std 1-3), rhythmic pattern
- RUNNING: Faster periodic oscillation at ~2.5-3.5 Hz, high variance (std 3-6), pronounced impact peaks

[Statistical Summary]
X-axis: mean=0.01, std=1.18
Y-axis: mean=-0.02, std=0.59
Z-axis: mean=9.81, std=1.55
Magnitude: mean=9.90, std=1.57
Dominant frequency: 2.0 Hz
Classification: walking

Example 3 - Running:
[Expert Knowledge]
Activity signatures in accelerometer data:
- SITTING: Gravity-dominated (~9.8 m/s² on one axis), very low variance (std < 0.2), no periodic motion (dominant freq ~0 Hz)
- WALKING: Periodic vertical oscillation at ~1.5-2.0 Hz (step frequency), moderate variance (std 1-3), rhythmic pattern
- RUNNING: Faster periodic oscillation at ~2.5-3.5 Hz, high variance (std 3-6), pronounced impact peaks

[Statistical Summary]
X-axis: mean=-0.01, std=2.25
Y-axis: mean=0.01, std=1.20
Z-axis: mean=10.04, std=3.45
Magnitude: mean=10.35, std=3.47
Dominant frequency: 3.0 Hz
Classification: running

[Your Task]
Analyze the following sensor data and classify the activity:
[Statistical Summary]
X-axis: mean=-0.01, std=1.17
Y-axis: mean=-0.02, std=0.59
Z-axis: mean=9.81, std=1.57
Magnitude: mean=9.90, std=1.58
Dominant frequency: 2.0 Hz

Classification:
```

**Prediction:** ________________

---

## v3_1shot

```
You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
The accelerometer measures acceleration in m/s² along three axes. Gravity contributes ~9.8 m/s² when stationary.

[Activity Signatures]
- SITTING: Characterized by gravity-dominated readings with very low variance (std < 0.2 m/s²). No periodic motion detected. The signal is essentially flat with minor sensor noise.

- WALKING: Shows periodic oscillation at approximately 1.5-2.0 Hz corresponding to step frequency. Moderate variance (std 1-3 m/s²) with rhythmic peaks on the vertical axis as each foot strikes the ground.

- RUNNING: Displays faster periodic oscillation at approximately 2.5-3.5 Hz. Higher variance (std 3-6 m/s²) with more pronounced impact peaks due to greater ground reaction forces.

[Examples]

Example 1 - Sitting (sitting_018):
[Statistical Summary]
X-axis: mean=-0.00, std=0.05
Y-axis: mean=0.00, std=0.05
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 9.0 Hz
Classification: sitting

Example 2 - Walking (walking_024):
[Statistical Summary]
X-axis: mean=0.01, std=1.03
Y-axis: mean=0.01, std=0.58
Z-axis: mean=9.80, std=1.38
Magnitude: mean=9.87, std=1.39
Dominant frequency: 2.0 Hz
Classification: walking

Example 3 - Running (running_023):
[Statistical Summary]
X-axis: mean=0.01, std=2.24
Y-axis: mean=0.07, std=1.16
Z-axis: mean=10.02, std=3.45
Magnitude: mean=10.33, std=3.47
Dominant frequency: 3.0 Hz
Classification: running

[Your Task]
Analyze the following sensor data and classify the activity:
[Statistical Summary]
X-axis: mean=-0.01, std=1.17
Y-axis: mean=-0.02, std=0.59
Z-axis: mean=9.81, std=1.57
Magnitude: mean=9.90, std=1.58
Dominant frequency: 2.0 Hz

Classification:
```

**Prediction:** ________________

---

## v3_3shot

```
You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
The accelerometer measures acceleration in m/s² along three axes. Gravity contributes ~9.8 m/s² when stationary.

[Activity Signatures]
- SITTING: Characterized by gravity-dominated readings with very low variance (std < 0.2 m/s²). No periodic motion detected. The signal is essentially flat with minor sensor noise.

- WALKING: Shows periodic oscillation at approximately 1.5-2.0 Hz corresponding to step frequency. Moderate variance (std 1-3 m/s²) with rhythmic peaks on the vertical axis as each foot strikes the ground.

- RUNNING: Displays faster periodic oscillation at approximately 2.5-3.5 Hz. Higher variance (std 3-6 m/s²) with more pronounced impact peaks due to greater ground reaction forces.

[Examples]

Example 1 - Sitting (sitting_024):
[Statistical Summary]
X-axis: mean=-0.00, std=0.05
Y-axis: mean=-0.00, std=0.05
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 24.6 Hz
Classification: sitting

Example 2 - Sitting (sitting_010):
[Statistical Summary]
X-axis: mean=-0.01, std=0.08
Y-axis: mean=0.01, std=0.08
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 14.6 Hz
Classification: sitting

Example 3 - Sitting (sitting_022):
[Statistical Summary]
X-axis: mean=-0.01, std=0.05
Y-axis: mean=-0.00, std=0.05
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 16.0 Hz
Classification: sitting

Example 4 - Walking (walking_012):
[Statistical Summary]
X-axis: mean=-0.01, std=1.04
Y-axis: mean=0.01, std=0.61
Z-axis: mean=9.80, std=1.38
Magnitude: mean=9.87, std=1.39
Dominant frequency: 2.0 Hz
Classification: walking

Example 5 - Walking (walking_024):
[Statistical Summary]
X-axis: mean=0.01, std=1.03
Y-axis: mean=0.01, std=0.58
Z-axis: mean=9.80, std=1.38
Magnitude: mean=9.87, std=1.39
Dominant frequency: 2.0 Hz
Classification: walking

Example 6 - Walking (walking_019):
[Statistical Summary]
X-axis: mean=-0.00, std=1.18
Y-axis: mean=-0.00, std=0.61
Z-axis: mean=9.82, std=1.56
Magnitude: mean=9.90, std=1.57
Dominant frequency: 2.0 Hz
Classification: walking

Example 7 - Running (running_022):
[Statistical Summary]
X-axis: mean=-0.00, std=2.29
Y-axis: mean=-0.02, std=1.17
Z-axis: mean=10.08, std=3.40
Magnitude: mean=10.40, std=3.42
Dominant frequency: 3.0 Hz
Classification: running

Example 8 - Running (running_003):
[Statistical Summary]
X-axis: mean=0.00, std=2.31
Y-axis: mean=0.08, std=1.16
Z-axis: mean=10.07, std=3.45
Magnitude: mean=10.39, std=3.47
Dominant frequency: 3.0 Hz
Classification: running

Example 9 - Running (running_018):
[Statistical Summary]
X-axis: mean=0.01, std=2.29
Y-axis: mean=-0.09, std=1.20
Z-axis: mean=10.07, std=3.56
Magnitude: mean=10.40, std=3.55
Dominant frequency: 3.0 Hz
Classification: running

[Your Task]
Analyze the following sensor data and classify the activity:
[Statistical Summary]
X-axis: mean=-0.01, std=1.17
Y-axis: mean=-0.02, std=0.59
Z-axis: mean=9.81, std=1.57
Magnitude: mean=9.90, std=1.58
Dominant frequency: 2.0 Hz

Classification:
```

**Prediction:** ________________

---

## v3_5shot

```
You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
The accelerometer measures acceleration in m/s² along three axes. Gravity contributes ~9.8 m/s² when stationary.

[Activity Signatures]
- SITTING: Characterized by gravity-dominated readings with very low variance (std < 0.2 m/s²). No periodic motion detected. The signal is essentially flat with minor sensor noise.

- WALKING: Shows periodic oscillation at approximately 1.5-2.0 Hz corresponding to step frequency. Moderate variance (std 1-3 m/s²) with rhythmic peaks on the vertical axis as each foot strikes the ground.

- RUNNING: Displays faster periodic oscillation at approximately 2.5-3.5 Hz. Higher variance (std 3-6 m/s²) with more pronounced impact peaks due to greater ground reaction forces.

[Examples]

Example 1 - Sitting (sitting_012):
[Statistical Summary]
X-axis: mean=-0.00, std=0.06
Y-axis: mean=0.00, std=0.07
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 14.2 Hz
Classification: sitting

Example 2 - Sitting (sitting_020):
[Statistical Summary]
X-axis: mean=-0.00, std=0.05
Y-axis: mean=-0.00, std=0.05
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 23.2 Hz
Classification: sitting

Example 3 - Sitting (sitting_010):
[Statistical Summary]
X-axis: mean=-0.01, std=0.08
Y-axis: mean=0.01, std=0.08
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 14.6 Hz
Classification: sitting

Example 4 - Sitting (sitting_023):
[Statistical Summary]
X-axis: mean=-0.00, std=0.05
Y-axis: mean=0.00, std=0.05
Z-axis: mean=9.82, std=0.05
Magnitude: mean=9.82, std=0.05
Dominant frequency: 20.2 Hz
Classification: sitting

Example 5 - Sitting (sitting_011):
[Statistical Summary]
X-axis: mean=0.00, std=0.05
Y-axis: mean=0.00, std=0.05
Z-axis: mean=9.81, std=0.05
Magnitude: mean=9.81, std=0.05
Dominant frequency: 13.0 Hz
Classification: sitting

Example 6 - Walking (walking_022):
[Statistical Summary]
X-axis: mean=-0.01, std=1.03
Y-axis: mean=0.02, std=0.58
Z-axis: mean=9.82, std=1.36
Magnitude: mean=9.89, std=1.37
Dominant frequency: 2.0 Hz
Classification: walking

Example 7 - Walking (walking_010):
[Statistical Summary]
X-axis: mean=0.01, std=1.01
Y-axis: mean=0.01, std=0.57
Z-axis: mean=9.83, std=1.38
Magnitude: mean=9.90, std=1.39
Dominant frequency: 2.0 Hz
Classification: walking

Example 8 - Walking (walking_024):
[Statistical Summary]
X-axis: mean=0.01, std=1.03
Y-axis: mean=0.01, std=0.58
Z-axis: mean=9.80, std=1.38
Magnitude: mean=9.87, std=1.39
Dominant frequency: 2.0 Hz
Classification: walking

Example 9 - Walking (walking_013):
[Statistical Summary]
X-axis: mean=0.00, std=1.16
Y-axis: mean=-0.01, std=0.62
Z-axis: mean=9.82, std=1.56
Magnitude: mean=9.90, std=1.57
Dominant frequency: 2.0 Hz
Classification: walking

Example 10 - Walking (walking_015):
[Statistical Summary]
X-axis: mean=0.01, std=1.16
Y-axis: mean=-0.00, std=0.60
Z-axis: mean=9.83, std=1.57
Magnitude: mean=9.91, std=1.58
Dominant frequency: 2.0 Hz
Classification: walking

Example 11 - Running (running_006):
[Statistical Summary]
X-axis: mean=-0.01, std=2.29
Y-axis: mean=-0.07, std=1.17
Z-axis: mean=10.05, std=3.34
Magnitude: mean=10.37, std=3.35
Dominant frequency: 3.0 Hz
Classification: running

Example 12 - Running (running_012):
[Statistical Summary]
X-axis: mean=0.02, std=2.33
Y-axis: mean=-0.11, std=1.15
Z-axis: mean=10.10, std=3.41
Magnitude: mean=10.43, std=3.44
Dominant frequency: 3.0 Hz
Classification: running

Example 13 - Running (running_003):
[Statistical Summary]
X-axis: mean=0.00, std=2.31
Y-axis: mean=0.08, std=1.16
Z-axis: mean=10.07, std=3.45
Magnitude: mean=10.39, std=3.47
Dominant frequency: 3.0 Hz
Classification: running

Example 14 - Running (running_010):
[Statistical Summary]
X-axis: mean=-0.02, std=2.28
Y-axis: mean=-0.14, std=1.14
Z-axis: mean=10.12, std=3.55
Magnitude: mean=10.44, std=3.55
Dominant frequency: 3.0 Hz
Classification: running

Example 15 - Running (running_024):
[Statistical Summary]
X-axis: mean=-0.01, std=2.25
Y-axis: mean=-0.06, std=1.22
Z-axis: mean=10.02, std=3.58
Magnitude: mean=10.34, std=3.59
Dominant frequency: 3.0 Hz
Classification: running

[Your Task]
Analyze the following sensor data and classify the activity:
[Statistical Summary]
X-axis: mean=-0.01, std=1.17
Y-axis: mean=-0.02, std=0.59
Z-axis: mean=9.81, std=1.57
Magnitude: mean=9.90, std=1.58
Dominant frequency: 2.0 Hz

Classification:
```

**Prediction:** ________________

---

## v4_stats_reasoning

```
You are analyzing statistical features extracted from smartphone accelerometer data.

[Activity Patterns]
- Sitting: std < 0.2, dominant frequency ~0 Hz
- Walking: std 1-3, dominant frequency 1.5-2.0 Hz
- Running: std 3-6, dominant frequency 2.5-3.5 Hz

[Examples with Reasoning]
Example 1:
Statistics: X(mean=-0.0, std=0.05), Y(mean=-0.0, std=0.05), Z(mean=9.8, std=0.05), Magnitude(std=0.05), DominantFreq=22.6Hz
Reasoning: Very low standard deviation across all axes and near-zero dominant frequency indicate no periodic motion. This is consistent with a stationary position.
Classification: sitting

Example 2:
Statistics: X(mean=0.0, std=1.18), Y(mean=-0.0, std=0.59), Z(mean=9.8, std=1.55), Magnitude(std=1.57), DominantFreq=2.0Hz
Reasoning: Moderate variance with dominant frequency around 2 Hz matches typical walking cadence of ~120 steps/minute.
Classification: walking

Example 3:
Statistics: X(mean=-0.0, std=2.25), Y(mean=0.0, std=1.20), Z(mean=10.0, std=3.45), Magnitude(std=3.47), DominantFreq=3.0Hz
Reasoning: High variance and dominant frequency near 3 Hz indicates fast periodic motion with strong impacts, consistent with running.
Classification: running

[Your Task]
Analyze this data. First provide your reasoning, then your classification.
Statistics: X(mean=-0.0, std=1.17), Y(mean=-0.0, std=0.59), Z(mean=9.8, std=1.57), Magnitude(std=1.58), DominantFreq=2.0Hz

Reasoning:
Classification:
```

**Prediction:** ________________

---

## v5_zero_shot

```
You are an expert at analyzing smartphone accelerometer data for human activity recognition.

[Sensor Information]
Accelerometer measures acceleration in m/s² along x, y, z axes. Gravity contributes ~9.8 m/s².

[Activity Signatures]
- SITTING: Gravity-dominated, very low variance (std < 0.2), no periodic motion (freq ~0 Hz)
- WALKING: Periodic at ~1.5-2.0 Hz (step frequency), moderate variance (std 1-3)
- RUNNING: Periodic at ~2.5-3.5 Hz, high variance (std 3-6), pronounced peaks

Based on your knowledge of human motion and accelerometer physics, classify this data:
[Statistical Summary]
X-axis: mean=-0.01, std=1.17
Y-axis: mean=-0.02, std=0.59
Z-axis: mean=9.81, std=1.57
Magnitude: mean=9.90, std=1.58
Dominant frequency: 2.0 Hz

Classification (sitting/walking/running):
```

**Prediction:** ________________

---
