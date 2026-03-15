# CERN ATLAS Warm-up: Process Resource Monitoring

## 1. Project Overview
This project involves the installation of **prmon** (Process Resource Monitor) and the application of machine learning to detect resource anomalies in time-series data. 

## 2. Methodology & Walkthrough
### Environment Setup
I built `prmon` from source within a native **Ubuntu/WSL2** environment. This was a strategic decision to ensure high-fidelity data retrieval from the Linux `/proc` filesystem and to avoid toolchain conflicts with Windows.

### Data Generation
I utilized the built-in `mem-burner` tool to generate two datasets:
- **Baseline:** 100MB allocation for 30 seconds to establish "normal" behavior.
- **Anomaly:** 800MB allocation for 20 seconds to simulate a memory-intensive resource spike.

### Detection Strategy
I implemented an **unsupervised Isolation Forest model** using `scikit-learn`. Unlike simple threshold-based detection, the Isolation Forest identifies anomalies by measuring how easy it is to "isolate" a data point, making it highly suitable for dynamic grid computing workloads where fixed thresholds are ineffective.

## 3. Visualization & Results
The model successfully flagged the inflection point of the memory spike ($T \approx 15s$) with high precision.

![Detection Results](anomaly_detection_report.png)

## 4. Discussion & Trade-offs
- **Suitability:** Isolation Forest is ideal for CERN's dynamic environment because it doesn't require pre-labeled "bad" data.
- **Trade-offs:** The `contamination` parameter is the primary lever. A setting of 0.1 was used to ensure the model distinguishes between minor noise and significant spikes.

## 5. Key Commands
- **Build:** `cmake .. && make`
- **Monitor:** `./package/prmon --interval 1 --filename normal_data.txt -- ./package/tests/mem-burner -m 100 -s 30`
- **Analyze:** `python3 analyze_prmon.py`

## 6. AI Disclosure
I utilized **Gemini 3 Flash** for:
- **Problem Discovery:** Resolving WSL2 toolchain path contamination.
- **Design Decisions:** Selecting the Isolation Forest algorithm for unsupervised detection.
- **Code Generation:** Drafting the `analyze_prmon.py` script and `README` structure.
