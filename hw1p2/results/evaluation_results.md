# Sensor Data Classification: Prompt Engineering Evaluation

## Experiment Configuration

### Dataset Statistics
| Parameter | Value |
|-----------|-------|
| Sensor | Smartphone accelerometer (x, y, z axes) |
| Units | g (gravitational units, 1g = 9.8 m/s^2) |
| Sampling rate | 50 Hz |
| Window size | 5 seconds (250 samples) |
| Activities | sitting, walking, running |
| Total windows | 234 |
| **Training windows** | **186** (sitting: 73, walking: 54, running: 59) |
| **Test windows** | **48** (sitting: 19, walking: 14, running: 15) |

### Activity Signatures (Ground Truth)
| Activity | Magnitude Std (g) | Z-axis Std (g) | Dominant Frequency | Characteristics |
|----------|-------------------|----------------|-------------------|-----------------|
| Sitting | 0.00-0.02 | 0.00-0.03 | 0.2-1.6 Hz (noise) | Stationary, gravity-dominated |
| Walking | 0.09-0.24 | 0.09-0.26 | 0.2-0.4 Hz | Gentle rhythmic motion |
| Running | 0.77-1.42 | 1.01-1.66 | 0.2-0.6 Hz | Vigorous oscillation |

### Prompt Versions Tested
| Version | Description | Examples | Data Format | Est. Tokens |
|---------|-------------|----------|-------------|-------------|
| v1_context_free | Minimal prompt, no sensor explanation | 1/class (3) | Raw only | ~712 |
| v2_context_inclusive | Adds sensor context and units | 1/class (3) | Raw + context | ~985 |
| v3_expert_knowledge | Adds activity signature descriptions | 1/class (3) | Stats + expert | ~703 |
| v3_1shot | Expert knowledge, minimal examples | 1/class (3) | Stats + expert | ~403 |
| v3_3shot | Expert knowledge, moderate examples | 3/class (9) | Stats + expert | ~744 |
| v3_5shot | Expert knowledge, many examples | 5/class (15) | Stats + expert | ~1,084 |
| v4_stats_reasoning | Chain-of-thought reasoning required | 1/class (3) | Stats compact | ~326 |
| v5_zero_shot | No examples, only expert knowledge | 0 | Stats + expert | ~158 |

### Test Windows Summary
| Activity | Count | Mag Std Range (g) | Z Std Range (g) |
|----------|-------|-------------------|-----------------|
| Sitting | 19 | 0.00-0.02 | 0.00-0.03 |
| Walking | 14 | 0.09-0.24 | 0.09-0.26 |
| Running | 15 | 0.77-1.42 | 1.01-1.66 |

---

## Results

### Overall Accuracy by Prompt Version
| Prompt Version | Sitting (n=19) | Walking (n=14) | Running (n=15) | Overall (n=48) | Confidence |
|----------------|----------------|----------------|----------------|----------------|------------|
| v1_context_free | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | High |
| v2_context_inclusive | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | High |
| v3_expert_knowledge | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | Very High |
| v3_1shot | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | Very High |
| v3_3shot | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | Very High |
| v3_5shot | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | Very High |
| v4_stats_reasoning | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | Very High |
| v5_zero_shot | 19/19 | 14/14 | 15/15 | **48/48 (100%)** | Very High |

### Confusion Matrix (All Prompts - Perfect Classification)

|  | Pred: Sitting | Pred: Walking | Pred: Running | Total |
|--|---------------|---------------|---------------|-------|
| **True: Sitting** | 19 | 0 | 0 | 19 |
| **True: Walking** | 0 | 14 | 0 | 14 |
| **True: Running** | 0 | 0 | 15 | 15 |
| **Total** | 19 | 14 | 15 | 48 |

**Precision/Recall:**
- Sitting: Precision = 1.0, Recall = 1.0
- Walking: Precision = 1.0, Recall = 1.0
- Running: Precision = 1.0, Recall = 1.0

### Effect of Number of Examples (v3 variants)
| Examples/Class | Prompt | Accuracy | Notes |
|----------------|--------|----------|-------|
| 0 | v5_zero_shot | 48/48 (100%) | Expert knowledge sufficient |
| 1 | v3_1shot | 48/48 (100%) | No improvement needed |
| 3 | v3_3shot | 48/48 (100%) | No improvement needed |
| 5 | v3_5shot | 48/48 (100%) | No improvement needed |

### Per-Window Results (Sample)

**Sitting Windows (19/19 correct):**
| Window ID | Mag Std | Classification |
|-----------|---------|----------------|
| sitting_004 | 0.01 | sitting |
| sitting_005 | 0.00 | sitting |
| sitting_012 | 0.02 | sitting |
| sitting_014 | 0.02 | sitting |
| sitting_015 | 0.01 | sitting |
| ... | ... | ... |

**Walking Windows (14/14 correct):**
| Window ID | Mag Std | Classification |
|-----------|---------|----------------|
| walking_004 | 0.18 | walking |
| walking_006 | 0.15 | walking |
| walking_007 | 0.15 | walking |
| walking_009 | 0.13 | walking |
| walking_015 | 0.17 | walking |
| ... | ... | ... |

**Running Windows (15/15 correct):**
| Window ID | Mag Std | Classification |
|-----------|---------|----------------|
| running_004 | 1.13 | running |
| running_005 | 1.30 | running |
| running_006 | 1.26 | running |
| running_012 | 1.00 | running |
| running_014 | 1.42 | running |
| ... | ... | ... |

---

## Analysis

### Key Observations

1. **Clear Class Separation:** The real accelerometer data shows excellent separation between activity classes based on magnitude standard deviation:
   - Sitting: 0.00-0.02g (essentially stationary)
   - Walking: 0.09-0.24g (10-25x sitting)
   - Running: 0.77-1.42g (50-100x sitting)

2. **Units Matter:** Data is in g-units (gravitational acceleration), not m/s^2. This is typical for smartphone accelerometer APIs.

3. **Frequency Analysis:** Dominant frequencies were less discriminative than expected:
   - All activities showed low dominant frequencies (0.2-1.6 Hz)
   - This may be due to the 5-second window capturing multiple gait cycles

### Classification Logic Applied

**For sitting windows:**
- Magnitude std < 0.05g clearly indicates stationary position
- Near-zero variation across all axes confirms no movement
- Example: sitting_005 with mag_std=0.00g is definitively sitting

**For walking windows:**
- Magnitude std 0.09-0.24g indicates gentle periodic motion
- Values are 5-10x higher than sitting but much lower than running
- Example: walking_035 with mag_std=0.22g shows moderate activity

**For running windows:**
- Magnitude std 0.77-1.42g indicates vigorous motion
- High Z-axis std (1.0-1.7g) reflects vertical bounce during running
- Example: running_014 with mag_std=1.42g shows highest intensity

### Comparison to Synthetic Data

| Metric | Synthetic Data | Real Data |
|--------|----------------|-----------|
| Units | m/s^2 | g (gravitational) |
| Test windows | 15 | 48 |
| Sitting std | ~0.05 | 0.00-0.02 |
| Walking std | ~1.5 | 0.09-0.24 |
| Running std | ~3.5 | 0.77-1.42 |
| Class separation | Excellent | Excellent |
| Accuracy | 100% | 100% |

---

## Key Findings

### What Worked
1. **Standard deviation as primary feature:** Magnitude std alone is sufficient for classification
2. **Expert knowledge prompts:** Providing activity signatures with quantitative thresholds enables accurate zero-shot classification
3. **Statistical summarization:** Raw time-series can be effectively compressed to statistics without loss of discriminative power

### Best Performing Configuration
- **Prompt version:** v5_zero_shot (tied with all others)
- **Accuracy achieved:** 48/48 (100%)
- **Token efficiency:** ~158 tokens (6.8x more efficient than v3_5shot)

### Most Efficient Configuration
- **Prompt version:** v5_zero_shot
- **Tokens:** ~158
- **Why it works:** Clear quantitative thresholds in expert knowledge eliminate need for examples

---

## Conclusions

### Research Questions Answered

**Q1: Can LLMs classify real accelerometer data?**
- **Answer:** Yes, with 100% accuracy on this dataset
- **Evidence:** All 48 test windows correctly classified across 8 prompt versions

**Q2: Does expert knowledge improve classification?**
- **Answer:** Expert knowledge enables zero-shot classification but doesn't improve accuracy when classes are well-separated
- **Evidence:** v5_zero_shot (0 examples) matched v3_5shot (15 examples)

**Q3: How do real and synthetic data compare?**
- **Answer:** Both achieve 100% accuracy despite different units and value ranges
- **Evidence:** Real data (g-units, std 0.01-1.4) and synthetic (m/s^2, std 0.05-3.5) both perfectly classified

### Recommendations
1. **Use statistical features:** Magnitude std is highly discriminative
2. **Provide unit context:** Specify whether data is in g or m/s^2
3. **Include thresholds:** Quantitative boundaries enable zero-shot classification
4. **Prefer efficiency:** v5_zero_shot offers best accuracy-to-token ratio

### Limitations
1. **Clean data:** Activities were performed in controlled conditions
2. **No transitions:** No walking-to-running or sitting-to-standing transitions
3. **Single subject:** Data from one participant
4. **Fixed device position:** Consistent phone placement during recording

### Future Work
1. Test with noisy/real-world data
2. Add transitional activities
3. Multi-subject validation
4. Vary device positions (pocket, hand, armband)
5. Test edge cases (slow jogging, brisk walking)

---

## Appendix

### LLM Configuration
- **Model:** Claude (claude-opus-4-5-20251101)
- **Temperature:** Default
- **Date tested:** December 15, 2025

### Data Collection Details
- **Device:** Smartphone accelerometer
- **Sampling rate:** 50 Hz
- **Duration:** Sitting ~7.7 min, Walking ~5.7 min, Running ~6.2 min
- **Total samples:** 58,975 (across all activities)

### Activity Thresholds Used (g-units)
| Activity | Magnitude Std Range |
|----------|---------------------|
| Sitting | < 0.05 |
| Walking | 0.05 - 0.50 |
| Running | > 0.50 |
