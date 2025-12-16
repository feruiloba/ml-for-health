# Sensor Data Classification with LLMs

## Project Overview
This project explores using Large Language Models to classify smartphone accelerometer data into human activity states (sitting, walking, running).

## Directory Structure
```
hw1p2/
├── code/                    # Python scripts
│   ├── generate_synthetic_data.py   # Creates synthetic accelerometer data
│   ├── visualize_data.py            # Plots and statistics
│   ├── process_data.py              # Windows data into 5s segments
│   ├── format_for_prompt.py         # Formatting strategies for LLM prompts
│   ├── create_prompts.py            # Generates prompt templates
│   ├── create_fewshot_prompts.py    # Few-shot variants (1/3/5 examples)
│   └── evaluate_prompts.py          # Prepares test cases for evaluation
├── data/
│   ├── raw/                 # Original CSV files (sitting.csv, walking.csv, running.csv)
│   └── processed/           # Windowed JSON files (train.json, test.json)
├── prompts/                 # Prompt template versions (v1-v5)
├── results/                 # Evaluation outputs and test prompts
└── .venv/                   # Python virtual environment
```

## Key Commands
```bash
# Activate virtual environment
source .venv/bin/activate

# Generate synthetic data (2 min per activity, 50Hz)
python code/generate_synthetic_data.py

# Visualize data and statistics
python code/visualize_data.py

# Process into 5-second windows (80/20 train/test split)
python code/process_data.py

# Create prompt templates with examples
python code/create_prompts.py
python code/create_fewshot_prompts.py

# Prepare test cases for evaluation
python code/evaluate_prompts.py
```

## Data Format
- **Raw**: CSV with columns `timestamp, x, y, z` (50Hz sampling)
- **Processed**: JSON windows with `window_id`, `label`, `samples[]`
- **Window size**: 5 seconds (250 samples)

## Prompt Strategies
| Version | Description | Est. Tokens |
|---------|-------------|-------------|
| v1_context_free | Raw data only | ~712 |
| v2_context_inclusive | Sensor context + raw | ~985 |
| v3_expert_knowledge | Expert signatures + stats | ~703 |
| v3_1shot/3shot/5shot | Few-shot variants | 403-1084 |
| v4_stats_reasoning | Stats + reasoning chain | ~326 |
| v5_zero_shot | No examples | ~158 |

## Activity Signatures
- **Sitting**: std < 0.2, freq ~0 Hz, gravity-dominated
- **Walking**: std 1-3, freq 1.5-2.0 Hz
- **Running**: std 3-6, freq 2.5-3.5 Hz

## Dependencies
- numpy
- pandas
- matplotlib
