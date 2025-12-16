# Sensor Data Classification: Prompt Engineering Evaluation

## Experiment Configuration

### Dataset Statistics
| Parameter | Value |
|-----------|-------|
| Sensor | Smartphone accelerometer (x, y, z axes) |
| Units | m/s² |
| Sampling rate | 50 Hz |
| Window size | 5 seconds (250 samples) |
| Activities | sitting, walking, running |
| Total duration per activity | 2 minutes (120 seconds) |
| Windows per activity | 24 |
| **Training windows per class** | **19** |
| **Test windows per class** | **5** |
| **Total training windows** | **57** |
| **Total test windows** | **15** |

### Activity Signatures (Ground Truth)
| Activity | Magnitude Std | Dominant Frequency | Characteristics |
|----------|--------------|-------------------|-----------------|
| Sitting | 0.05 | N/A (noise) | Gravity-dominated, minimal motion |
| Walking | 1.37-1.60 (mean 1.47) | 2.0 Hz | Rhythmic step pattern |
| Running | 3.34-3.61 (mean 3.48) | 3.0 Hz | High-impact, fast cadence |

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

### Test Windows Used
| Window ID | True Label | Mag Std | Dom Freq |
|-----------|------------|---------|----------|
| sitting_001 | sitting | 0.05 | 18.2 Hz (noise) |
| sitting_004 | sitting | 0.05 | 22.6 Hz (noise) |
| sitting_008 | sitting | 0.05 | 10.6 Hz (noise) |
| sitting_009 | sitting | 0.05 | 5.8 Hz (noise) |
| sitting_021 | sitting | 0.05 | 19.8 Hz (noise) |
| walking_001 | walking | 1.59 | 2.0 Hz |
| walking_004 | walking | 1.39 | 2.0 Hz |
| walking_008 | walking | 1.39 | 2.0 Hz |
| walking_009 | walking | 1.58 | 2.0 Hz |
| walking_021 | walking | 1.58 | 2.0 Hz |
| running_001 | running | 3.35 | 3.0 Hz |
| running_004 | running | 3.43 | 3.0 Hz |
| running_008 | running | 3.62 | 3.0 Hz |
| running_009 | running | 3.35 | 3.0 Hz |
| running_021 | running | 3.63 | 3.0 Hz |

---

## Results

### Overall Accuracy by Prompt Version
| Prompt Version | Sitting (n=5) | Walking (n=5) | Running (n=5) | Overall (n=15) | Confidence |
|----------------|---------------|---------------|---------------|----------------|------------|
| v1_context_free | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | High |
| v2_context_inclusive | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | High |
| v3_expert_knowledge | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | Very High |
| v3_1shot | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | Very High |
| v3_3shot | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | Very High |
| v3_5shot | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | Very High |
| v4_stats_reasoning | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | Very High |
| v5_zero_shot | 5/5 | 5/5 | 5/5 | **15/15 (100%)** | Very High |

### Confusion Matrix (All Prompts - Perfect Classification)

|  | Pred: Sitting | Pred: Walking | Pred: Running | Total |
|--|---------------|---------------|---------------|-------|
| **True: Sitting** | 5 | 0 | 0 | 5 |
| **True: Walking** | 0 | 5 | 0 | 5 |
| **True: Running** | 0 | 0 | 5 | 5 |
| **Total** | 5 | 5 | 5 | 15 |

**Precision/Recall:**
- Sitting: Precision = 1.0, Recall = 1.0
- Walking: Precision = 1.0, Recall = 1.0
- Running: Precision = 1.0, Recall = 1.0

### Effect of Number of Examples (v3 variants)
| Examples/Class | Prompt | Accuracy | Δ from Zero-shot | Notes |
|----------------|--------|----------|------------------|-------|
| 0 | v5_zero_shot | 15/15 (100%) | baseline | Expert knowledge sufficient |
| 1 | v3_1shot | 15/15 (100%) | +0% | No improvement needed |
| 3 | v3_3shot | 15/15 (100%) | +0% | No improvement needed |
| 5 | v3_5shot | 15/15 (100%) | +0% | No improvement needed |

### Effect of Context (v1 → v2 → v3 comparison)
| Context Level | Prompt | Accuracy | Δ from Previous |
|---------------|--------|----------|-----------------|
| None | v1_context_free | 15/15 (100%) | baseline |
| Sensor context | v2_context_inclusive | 15/15 (100%) | +0% |
| Expert knowledge | v3_expert_knowledge | 15/15 (100%) | +0% |

### Per-Window Results (Detailed)
| Window ID | True | v1 | v2 | v3 | v3_1 | v3_3 | v3_5 | v4 | v5 |
|-----------|------|----|----|----|----|-----|-----|----|----|
| sitting_001 | S | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| sitting_004 | S | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| sitting_008 | S | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| sitting_009 | S | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| sitting_021 | S | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| walking_001 | W | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| walking_004 | W | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| walking_008 | W | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| walking_009 | W | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| walking_021 | W | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| running_001 | R | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| running_004 | R | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| running_008 | R | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| running_009 | R | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| running_021 | R | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

*(S=sitting, W=walking, R=running, ✓=correct)*

---

## Analysis

### Common Misclassification Patterns
1. **None observed** - All 120 classifications (15 windows × 8 prompts) were correct
2. The synthetic data has exceptionally clear class separation
3. No edge cases challenged the classifier

### Qualitative Observations

**Response Quality:**
- v4_stats_reasoning produced the most explicit reasoning, directly mapping features to activity signatures
- v5_zero_shot was most efficient (~158 tokens) while maintaining perfect accuracy
- v1_context_free required pattern matching from raw data but was still effective

**Chain-of-Thought (v4) Analysis:**
- Reasoning correctly identified:
  - Low std (< 0.2) → sitting
  - Moderate std (1-3) + 2.0 Hz → walking
  - High std (3-6) + 3.0 Hz → running
- The explicit activity pattern thresholds made classification straightforward
- No reasoning errors observed

**Key Classification Logic Applied:**

For **sitting** windows:
- std=0.05 clearly matches "std < 0.2" threshold
- High dominant frequency (5-22 Hz) correctly interpreted as sensor noise, not periodic motion
- Gravity-dominated z-axis (~9.8) confirmed stationary state

For **walking** windows:
- std=1.39-1.59 falls within "std 1-3" range
- Dominant frequency=2.0 Hz exactly matches expected step frequency
- Moderate z-axis oscillation (~7-12) visible in raw data

For **running** windows:
- std=3.35-3.63 falls within "std 3-6" range
- Dominant frequency=3.0 Hz matches expected running cadence
- Large z-axis oscillation (~5-15) with pronounced peaks

---

## Key Findings

### What Improved Accuracy
| Change | Improvement | Explanation |
|--------|-------------|-------------|
| Adding sensor context (v1 → v2) | +0% | Data too clean to show improvement |
| Adding expert knowledge (v2 → v3) | +0% | Baseline already at ceiling |
| Increasing examples 1→3 (v3_1shot → v3_3shot) | +0% | No additional benefit |
| Increasing examples 3→5 (v3_3shot → v3_5shot) | +0% | Diminishing returns plateau |
| Chain-of-thought reasoning (v3 → v4) | +0% | Already at perfect accuracy |

### What Didn't Help (or Hurt)
1. **Additional examples** - Zero-shot performed as well as 5-shot
2. **More tokens** - v5 (158 tokens) matched v2 (985 tokens)
3. **Raw data format** - Statistical summary equally effective and more compact

### Best Performing Configuration
- **Prompt version:** v5_zero_shot (tied with all others)
- **Accuracy achieved:** 15/15 (100%)
- **Why it worked:**
  - Expert knowledge provided clear, quantitative decision boundaries
  - Statistical features (std, frequency) are highly discriminative
  - Synthetic data has ideal class separation with no overlap

### Most Efficient Configuration
- **Prompt version:** v5_zero_shot
- **Tokens:** ~158 (vs ~1,084 for v3_5shot)
- **Token efficiency:** 6.8x more efficient than v3_5shot with same accuracy

### Worst Performing Configuration
- **Prompt version:** None - all achieved 100%
- **Accuracy achieved:** N/A
- **Why:** Synthetic data is too clean to challenge any prompt design

---

## Conclusions

### Research Questions Answered

**Q1: Can LLMs classify accelerometer data?**
- **Answer:** Yes, with 100% accuracy on this synthetic dataset
- **Evidence:** All 8 prompt versions achieved perfect classification across 15 test windows

**Q2: Does expert knowledge improve classification?**
- **Answer:** Not demonstrably on clean data, but likely beneficial for ambiguous cases
- **Evidence:** v1 (no context) performed equally to v3 (expert knowledge), but expert knowledge provides more interpretable decision-making

**Q3: How many examples are needed?**
- **Answer:** Zero examples sufficient when expert knowledge provides clear thresholds
- **Evidence:** v5_zero_shot (0 examples) matched v3_5shot (15 examples)

**Q4: Is chain-of-thought reasoning helpful?**
- **Answer:** Not for accuracy on this task, but improves interpretability
- **Evidence:** v4 produced explicit reasoning that correctly identified key features

### Recommendations
1. **For production use:** v5_zero_shot or v4_stats_reasoning
   - v5 for efficiency (158 tokens)
   - v4 for interpretability (explicit reasoning)
2. **Minimum examples needed:** 0 (with good expert knowledge)
3. **Key features to always include:**
   - Standard deviation thresholds
   - Dominant frequency ranges
   - Clear activity descriptions

### Limitations
1. **Synthetic data** - Perfectly separated classes don't reflect real-world noise, sensor drift, or transitional activities
2. **Only 15 test samples** - Limited statistical power to detect small differences
3. **Single LLM tested** - Results may vary across models (GPT-4, Gemini, etc.)
4. **No ambiguous cases** - Walking-running boundary not tested with intermediate intensities
5. **Fixed phone orientation** - Real data would have gravity distributed across axes

### Future Work
1. **Test with real smartphone sensor data** - UCI HAR dataset or custom collection
2. **Add more activity classes** - stairs, cycling, standing, lying down
3. **Compare multiple LLM models** - GPT-4, Gemini, Llama, etc.
4. **Test boundary cases** - slow jogging, fast walking, transitions
5. **Vary phone orientation** - pocket, hand, armband positions
6. **Add noise and drift** - Test robustness to real-world sensor artifacts

---

## Appendix

### LLM Configuration
- **Model:** Claude (claude-opus-4-5-20251101)
- **Temperature:** Default
- **Date tested:** 2025-12-15

### Sample Correct Classification (v5_zero_shot)

**Input:**