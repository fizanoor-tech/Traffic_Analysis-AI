# 🚦 AI Traffic & Pedestrian Analytics System

**A real-time computer vision pipeline for vehicle/pedestrian detection, multi-object tracking, and automated traffic analytics — with an interactive Streamlit dashboard for restricted-lane violation monitoring.**

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)
![ByteTrack](https://img.shields.io/badge/Tracking-ByteTrack-orange)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

# 🎬 Live Demo

<div align="center">

<img src="https://github.com/user-attachments/assets/3baa528f-cfea-4be9-8c7d-956e49ef6f5e" width="72%" alt="AI Traffic Analytics Live Demo" />

<br><br>
<i>
Real-time traffic analytics powered by a custom-trained <b>YOLOv8</b> detector,
<b>ByteTrack</b> multi-object tracking, and an interactive <b>Streamlit</b> dashboard.
</i>
<br><br>

<img src="https://img.shields.io/badge/-Vehicle_Detection-1fd7b5?style=flat-square"/>
<img src="https://img.shields.io/badge/-Object_Tracking-7f77dd?style=flat-square"/>
<img src="https://img.shields.io/badge/-Lane_Violation_Detection-e24b4a?style=flat-square"/>
<img src="https://img.shields.io/badge/-Speed_Estimation-f0997b?style=flat-square"/>
<img src="https://img.shields.io/badge/-Analytics_Dashboard-378ADD?style=flat-square"/>

</div>

## 🧠 Overview

<div align="center">

### 🎯 Detect &nbsp;→&nbsp; 🔗 Track &nbsp;→&nbsp; 📊 Analyze &nbsp;→&nbsp; 🖥️ Visualize

**One live pipeline, from raw video to actionable traffic insight.**

</div>

<br>

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

<p align="center">
  <img src="https://github.com/user-attachments/assets/ebccb012-e3f7-429f-99be-955ace5ba88d" alt="Interactive Lane Calibration" width="85%" />
  <br/>
  <em>4-point polygon calibration — no hardcoded lane coordinates required</em>
</p>

### 2️⃣ Live Detection & Tracking

Each object gets a persistent ID and color-coded box by class (vehicle / two-wheeler / person), with motion trails showing recent movement.

<p align="center">
  <img src="https://github.com/user-attachments/assets/d9d2d5fe-d28c-4e7f-81cc-7b8adf4dadf7" alt="Live Detection & Tracking" width="85%" />
  <br/>
  <em>Persistent object IDs with class-based color coding and motion trails</em>
</p>

### 3️⃣ Restricted Lane Violation Alert

A vehicle is highlighted in red only after spending 10 consecutive frames inside the restricted zone — the zone itself stays invisible so the feed remains clean.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5f8bcd67-55f3-418c-84fc-27fdc58c4366" alt="Restricted Lane Violation Alert" width="85%" />
  <br/>
  <em>Vehicle #207 flagged after sustained presence in the restricted zone</em>
</p>



### 4️⃣ Live Analytics Dashboard

Traffic volume, vehicle/pedestrian counts, average speed, and violation totals update in real time as the video processes.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c338945a-d963-45e7-88aa-02617f652958" alt="Live Analytics Dashboard" width="40%" />
  <br/>
  <em>Metrics update live as each frame is processed</em>
</p>


## 🎬 Full Demo Video

<div align="center">

*Watch the full walkthrough — upload, calibration, live detection & analytics in action*

<br/>

<a href="https://youtu.be/0Q7lv8L1VGc" target="_blank">
  <img src="https://img.youtube.com/vi/0Q7lv8L1VGc/maxresdefault.jpg" 
       alt="AI Traffic & Pedestrian Analytics — Full Walkthrough" 
       width="720" 
       style="border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 12px 32px rgba(0,0,0,0.55);">
</a>

<br/><br/>

<a href="https://youtu.be/0Q7lv8L1VGc" target="_blank">
  <img src="https://img.shields.io/badge/▶_WATCH_FULL_WALKTHROUGH-1:40-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube"/>
</a>

<br/><br/>

<img src="https://img.shields.io/badge/1_Upload_Video-0d1117?style=flat-square&labelColor=161b22&color=1fd7b5"/>
<img src="https://img.shields.io/badge/→-0d1117?style=flat-square&labelColor=0d1117&color=0d1117"/>
<img src="https://img.shields.io/badge/2_Polygon_ROI-0d1117?style=flat-square&labelColor=161b22&color=7f77dd"/>
<img src="https://img.shields.io/badge/→-0d1117?style=flat-square&labelColor=0d1117&color=0d1117"/>
<img src="https://img.shields.io/badge/3_YOLOv8_Processing-0d1117?style=flat-square&labelColor=161b22&color=f0997b"/>
<img src="https://img.shields.io/badge/→-0d1117?style=flat-square&labelColor=0d1117&color=0d1117"/>
<img src="https://img.shields.io/badge/4_Live_Analytics-0d1117?style=flat-square&labelColor=161b22&color=378ADD"/>

</div>

<br/>

---

<br/>

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
