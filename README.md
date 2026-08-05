# 🚦 AI Traffic & Pedestrian Analytics System

**A real-time computer vision pipeline for vehicle/pedestrian detection, multi-object tracking, and automated traffic analytics — with an interactive Streamlit dashboard for restricted-lane violation monitoring.**

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)
![ByteTrack](https://img.shields.io/badge/Tracking-ByteTrack-orange)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

<div align="center">

### 🎯 Detect &nbsp;→&nbsp; 🔗 Track &nbsp;→&nbsp; 📊 Analyze &nbsp;→&nbsp; 🖥️ Visualize

**One live pipeline, from raw video to actionable traffic insight.**

</div>

---

## 📸 Demo

<div align="center">

![demo gif](d<img width="600" height="315" alt="AITrafficAnalyticsand1morepage-Profile1-MicrosoftEdge2026-08-0518-21-41-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/16941519-b5b7-47bc-b1f0-13f13563883f" />
ocs/demo.gif)

*A custom-trained YOLOv8 detector, ByteTrack multi-object tracking, and a purpose-built analytics engine processing live footage inside the Streamlit dashboard.*

</div>

---

## 🧠 Overview

A custom-trained **YOLOv8** detector, **ByteTrack** multi-object tracking, and a purpose-built analytics engine come together in one live traffic monitoring pipeline — wrapped in an interactive Streamlit dashboard where anyone can upload footage, calibrate a restricted lane, and watch the numbers update in real time.

> Built end-to-end — dataset curation → model training → tracking pipeline → deployable web app.

---

## ✨ Features

<table>
<tr><td width="33%" valign="top">

### 🔍 Detection & Tracking
- Custom YOLOv8 fine-tuned on BDD100K
- 3 practical classes: `vehicle`, `two_wheeler`, `person`
- ByteTrack persistent ID tracking, tuned to resist fragmentation
- Motion trace overlays + class-color-coded boxes

</td><td width="33%" valign="top">

### 📊 Analytics Engine
- Per-class traffic volume counting (zone-based, no double-counting)
- Restricted-lane violations — 10-consecutive-frame rule, ground-anchor accuracy
- Speed estimation (labeled, uncalibrated km/h)
- Stalled-vehicle detection with active-ID cleanup

</td><td width="33%" valign="top">

### 🖥️ Interactive Dashboard
- Upload video, click-to-draw restricted lane (no hardcoded zones)
- Live metric cards: traffic, vehicles, pedestrians, violations, speed
- Show/Hide Lane toggle — live, mid-playback
- Dual export: annotated or clean video
- Custom dark enterprise UI

</td></tr>
</table>

---

## 🖼️ Screenshots

### 1️⃣ Interactive Lane Calibration
Click 4 points directly on the first frame to define a custom restricted lane — no hardcoded coordinates, works for any uploaded video.

![roi selector](docs/roi_selector_demo.png)

### 2️⃣ Live Detection & Tracking
Each object gets a persistent ID and color-coded box by class (vehicle / two-wheeler / person), with motion trails showing recent movement.

![tracking](docs/tracking_demo.png)

### 3️⃣ Restricted Lane Violation Alert
A vehicle is highlighted in red only after spending 10 consecutive frames inside the restricted zone — the zone itself stays invisible so the feed remains clean.

![violation](docs/violation_demo.png)

### 4️⃣ Show / Hide Lane — Live Toggle
Switch between the annotated view (dashed lane outline visible) and a completely clean feed, at any point during processing — without interrupting the run.

| Lane Visible | Lane Hidden |
|---|---|
| ![lane on](docs/lane_on_demo.png) | ![lane off](docs/lane_off_demo.png) |

### 5️⃣ Live Analytics Dashboard
Traffic volume, vehicle/pedestrian counts, average speed, and violation totals update in real time as the video processes.

![analytics](docs/dashboard_metrics_demo.png)

---

## 🎥 Full Demo Video

<div align="center">

[![Watch the full demo](docs/video_thumbnail.png)](https://youtu.be/your-video-id)

**▶️ [Watch the full walkthrough (2:15)](https://youtu.be/your-video-id)**
*Upload → polygon selection → processing → live results*

</div>

---

## 🏗️ Architecture

```
Video Upload
     │
     ▼
┌─────────────────────┐
│  User draws ROI      │  (roi.py — click-to-select 4-point polygon)
│  (restricted lane)   │
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  YOLOv8 Detection    │  vehicle / two_wheeler / person
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  ByteTrack           │  persistent tracker IDs
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  TrafficAnalytics    │  (analytics.py)
│  • Volume counting   │
│  • Lane violations   │
│  • Speed estimation  │
│  • Stalled detection │
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  Streamlit Dashboard │  live video + metrics, side-by-side
└─────────────────────┘
```

**Module breakdown:**
| File | Responsibility |
|---|---|
| `app.py` | Streamlit UI, page layout, session state, processing loop |
| `detector.py` | Wraps YOLO + ByteTrack, per-class annotation styling, dual-frame (lane visible/hidden) rendering |
| `analytics.py` | `TrafficAnalytics` — all counting/speed/violation/stall logic |
| `roi.py` | Interactive polygon selector for the restricted lane |
| `utils.py` | Video I/O helpers (save upload to disk, extract first frame) |

---

## 📊 Model Training & Performance

**Dataset:** [BDD100K (Kaggle)](https://www.kaggle.com/datasets/aayusmaanjain/bdd100k-for-self-driving-cars) — 22,000 images, YOLO-format annotations across day/night driving scenes.

**Class simplification:** the original 10 BDD100K classes were merged into 3 categories relevant to this project's scope:

| New Class | Merged From |
|---|---|
| `vehicle` | car, bus, truck, train |
| `two_wheeler` | bike, motor |
| `person` | person, rider |

*(traffic light / traffic sign were dropped — out of scope for this project)*

**Training:** YOLOv8n, 50 epochs, Tesla T4 GPU.

| Class | Precision | Recall | mAP50 |
|---|---|---|---|
| vehicle | 0.77 | 0.68 | 0.74 |
| person | 0.69 | 0.45 | 0.52 |
| two_wheeler | 0.60 | 0.36 | 0.40 |

📉 **Known limitation:** vehicle detection significantly outperforms person/two-wheeler detection — a direct, measured consequence of BDD100K's class imbalance (vehicles outnumber two-wheelers ~71:1 in the raw dataset). This was diagnosed via exploratory data analysis, confirmed against real test footage, and is documented here rather than hidden.

---

<details>
<summary><h2 style="display:inline">⚠️ Limitations & Known Trade-offs</h2></summary>

Being upfront about what this system does *not* do well is part of treating it as a real engineering project, not a polished demo:

| Limitation | Detail |
|---|---|
| **Small/distant & low-light objects** | Weaker detection, confirmed via direct testing — a consequence of dataset composition and the nano model variant (chosen for speed) |
| **Tracking ID fragmentation** | A single real object can briefly split into multiple IDs during occlusion/low confidence, modestly inflating counts. Mitigated (not eliminated) via a minimum-consecutive-frame rule |
| **Speed is uncalibrated** | Estimated from pixel displacement with an assumed pixels-per-meter constant — not a true measurement |
| **Static 2D ROI** | The lane polygon is fixed to one reference frame; significant camera movement/panning can cause drift over the video |
| **Stalled ≠ illegally parked** | Legitimately parked vehicles and vehicles stuck in traffic both register identically as "stalled" |

</details>

<details>
<summary><h2 style="display:inline">🗺️ Future Scope (v2.0)</h2></summary>

- **Perspective transformation** (bird's-eye / homography) for real-world speed calibration and ROI stability across camera motion
- **Multi-frame preview slider** — scrub the video before placing the ROI, instead of relying on frame 0
- **Live stream ingestion** — wire up RTSP/HLS support (URL field already scaffolded)
- **Per-class lane rules** — configurable restrictions beyond standard vehicles (e.g. two-wheeler-only lanes)
- **Model improvements** — oversampling/augmentation for under-represented classes to close the recall gap

</details>

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Object Detection | YOLOv8 (Ultralytics) |
| Object Tracking | ByteTrack (via `supervision`) |
| Computer Vision | OpenCV |
| Analytics Engine | Custom Python (`TrafficAnalytics`) |
| Dashboard | Streamlit |
| Training Environment | Kaggle Notebooks (Tesla T4 GPU) |

---

## 🚀 Getting Started

### Prerequisites
```bash
python 3.10+
```

### Installation
```bash
git clone https://github.com/<your-username>/traffic-analytics-system.git
cd traffic-analytics-system
pip install -r requirements.txt
```

`requirements.txt` should include:
```
ultralytics
supervision
opencv-python
streamlit
streamlit-image-coordinates
numpy
```

### Place your trained weights
Put your trained `best.pt` in the project root, next to `app.py`.

### Run the dashboard
```bash
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

### Usage
1. Upload a traffic video (MP4/AVI/MOV)
2. Click 4 points on the preview frame to draw your restricted lane, then **Save Lane**
3. Click **Process Video** — watch live analytics update as the video processes
4. Toggle **Show Restricted Lane** on/off at any time, even mid-processing
5. Once done, preview and download either the annotated or clean version of the output

---

## 📁 Project Structure

```
traffic-analytics-system/
├── app.py              # Streamlit dashboard & UI
├── detector.py          # YOLO + ByteTrack wrapper, annotation logic
├── analytics.py          # TrafficAnalytics engine (counting/speed/violations/stalls)
├── roi.py                # Interactive lane-polygon selector
├── utils.py               # Video I/O helpers
├── best.pt                 # Trained YOLOv8 weights (not committed - see Releases)
├── requirements.txt
└── README.md
```

---

## 🙏 Acknowledgements

- [BDD100K](https://www.kaggle.com/datasets/aayusmaanjain/bdd100k-for-self-driving-cars) dataset
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Roboflow Supervision](https://github.com/roboflow/supervision) for ByteTrack integration and annotation utilities

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
