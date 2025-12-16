# Sensor Data Classification with LLMs

This project explores using Large Language Models (LLMs) to classify smartphone accelerometer sensor data into human activity states.

## Objective

Classify accelerometer readings into three activity categories:
- **Sitting** - stationary, minimal movement
- **Walking** - moderate, rhythmic motion patterns
- **Running** - high-intensity, rapid movement patterns

## Project Structure

```
hw1p2/
├── data/
│   ├── raw/          # Original sensor data files
│   └── processed/    # Cleaned and formatted data for LLM input
├── prompts/          # Prompt templates and versions
├── results/          # LLM classification outputs
└── README.md
```

## Data

The accelerometer data consists of x, y, z axis readings captured from smartphone sensors during different physical activities.

## Approach

1. Collect raw accelerometer sensor data
2. Process and format data for LLM consumption
3. Design and iterate on classification prompts
4. Evaluate LLM performance on activity classification
