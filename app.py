import os
import tempfile

import cv2
import streamlit as st

from utils import save_uploaded_video, extract_first_frame
from roi import ROISelector
from detector import TrafficDetector

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="AI Traffic Analytics",
    page_icon="🚗",
    layout="wide"
)

# ---------------------------------------
# Enterprise Dark Theme CSS (Fixed High Contrast Labels)
# ---------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg-primary: #0F172A;
            --bg-secondary: #1E293B;
            --bg-card: #1E293B;
            --accent-cyan: #38BDF8;
            --accent-blue: #3B82F6;
            --text-primary: #F8FAFC;
            --text-secondary: #E2E8F0;
            --border-color: #334155;
        }

        .stApp {
            background-color: var(--bg-primary) !important;
            font-family: 'Inter', sans-serif !important;
            color: var(--text-primary);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #090D16 !important;
            border-right: 1px solid var(--border-color) !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stMarkdown p {
            color: #E2E8F0 !important;
            font-weight: 600 !important;
        }

        /* Headers */
        h1 {
            background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-size: 2.3rem !important;
            letter-spacing: -0.5px;
            padding-bottom: 0px;
        }
        h3, h4 {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: -0.3px;
        }
        .stCaption { color: #94A3B8 !important; font-size: 0.95rem !important; }

        /* Step badges */
        .step-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 999px;
            padding: 6px 16px;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-secondary);
            margin-bottom: 14px;
        }
        .step-badge.active {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
            box-shadow: 0 0 0 1px rgba(56,189,248,0.25);
        }
        .step-badge.done {
            border-color: #22C55E;
            color: #22C55E;
        }
        .step-num {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 20px; height: 20px;
            border-radius: 50%;
            background: currentColor;
            font-size: 0.7rem;
        }
        .step-num span { color: var(--bg-primary); font-weight: 800; }

        /* Metric Cards Styling */
        div[data-testid="stMetric"] {
            background: #1E293B !important;
            border: 1px solid #334155 !important;
            padding: 18px 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
            transition: all 0.2s ease-in-out !important;
        }
        div[data-testid="stMetric"]:hover {
            border-color: #38BDF8 !important;
            transform: translateY(-2px);
        }

        /* METRIC LABELS ("Traffic", "Vehicles", etc.) HIGH CONTRAST FIX */
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] *,
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] label,
        [data-testid="stMetricLabel"] div,
        [data-testid="stMetricLabel"] span {
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
            font-size: 0.95rem !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.8px !important;
            opacity: 1 !important;
            filter: none !important;
        }

        /* METRIC VALUES ("0", "33.0 km/h", etc.) */
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] *,
        [data-testid="stMetricValue"] div {
            color: #38BDF8 !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }

        /* Form controls */
        div[data-testid="stRadioButton"] label { color: #E2E8F0 !important; }
        div[data-baseweb="slider"] div { color: var(--accent-cyan) !important; }
        div[data-testid="stSlider"] label { color: #E2E8F0 !important; }

        section[data-testid="stFileUploader"] {
            background-color: #131C2E !important;
            border: 1px dashed var(--border-color) !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        section[data-testid="stFileUploader"] label { color: #E2E8F0 !important; }

        div.stButton > button {
            background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.25rem !important;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4) !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6) !important;
            transform: translateY(-1px);
        }

        /* Toggle switch */
        div[data-testid="stToggle"] label p {
            color: #E2E8F0 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        hr { border-color: var(--border-color) !important; margin: 1.5rem 0 !important; }
    </style>
""", unsafe_allow_html=True)


def step_badge(label, state):
    icon = "✓" if state == "done" else ""
    cls = f"step-badge {state}" if state != "pending" else "step-badge"
    st.markdown(
        f'<div class="{cls}"><span class="step-num"><span>{icon}</span></span>{label}</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------
# Header
# ---------------------------------------
st.title("🚗 AI Traffic Analytics Dashboard")
st.caption("Real-Time Vehicle Detection, Tracking & Restricted-Lane Analytics")
st.divider()

# ---------------------------------------
# Session state defaults
# ---------------------------------------
st.session_state.setdefault("last_video_name", None)
st.session_state.setdefault("processing", False)
st.session_state.setdefault("processing_done", False)
st.session_state.setdefault("output_path_shown", None)
st.session_state.setdefault("output_path_hidden", None)
st.session_state.setdefault("cap", None)
st.session_state.setdefault("detector", None)
st.session_state.setdefault("writer_shown", None)
st.session_state.setdefault("writer_hidden", None)
st.session_state.setdefault("frame_idx", 0)
st.session_state.setdefault("total_frames", 1)

for key, default in [("traffic", 0), ("vehicles", 0), ("pedestrians", 0),
                      ("violations", 0), ("avg_speed", "0 km/h")]:
    st.session_state.setdefault(key, default)

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:
    st.header("⚙️ Controls")
    st.subheader("Input Source")

    source = st.radio("Choose Input", ["Upload Video", "Live Stream URL"])

    uploaded_video = None
    stream_url = None

    if source == "Upload Video":
        uploaded_video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    else:
        stream_url = st.text_input("Live Stream URL")
        st.info("Live stream ingestion isn't wired up yet — upload a file for now.")

    st.divider()
    confidence = st.slider("Confidence", 0.10, 1.00, 0.45)
    iou = st.slider("IoU Threshold", 0.10, 1.00, 0.50)
    st.divider()

    st.subheader("Display")
    show_lane = st.toggle(
        "Show Restricted Lane",
        value=True,
        key="show_lane",
        help="Toggles the restricted polygon overlay on the video feed in real-time."
    )
    st.divider()

    roi_ready = st.session_state.get("roi_saved", False)
    processing_active = st.session_state.processing

    process = st.button(
        "▶ Process Video",
        use_container_width=True,
        disabled=not roi_ready or processing_active,
        type="primary",
    )
    stop = st.button(
        "⏹ Stop Processing",
        use_container_width=True,
        disabled=not processing_active,
    )
    if not roi_ready:
        st.caption("Select and save a restricted lane to enable this.")

# ---------------------------------------
# Reset state on new file upload
# ---------------------------------------
if uploaded_video is not None and st.session_state.last_video_name != uploaded_video.name:
    ROISelector.reset()
    st.session_state.processing = False
    st.session_state.processing_done = False
    st.session_state.output_path_shown = None
    st.session_state.output_path_hidden = None
    st.session_state.cap = None
    st.session_state.detector = None
    st.session_state.writer_shown = None
    st.session_state.writer_hidden = None
    st.session_state.frame_idx = 0
    st.session_state.last_video_name = uploaded_video.name

# ---------------------------------------
# Layout
# ---------------------------------------
left, right = st.columns([2, 1], gap="large")

with right:
    st.subheader("📊 Live Analytics")

    m1_col, m2_col = st.columns(2)
    m1 = m1_col.empty()
    m2 = m2_col.empty()
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    m3_col, m4_col = st.columns(2)
    m3 = m3_col.empty()
    m4 = m4_col.empty()
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    m5 = st.empty()
    progress_bar = st.empty()

    st.divider()
    status_placeholder = st.empty()

# Metric cards display
m1.metric("Traffic", st.session_state["traffic"])
m2.metric("Vehicles", st.session_state["vehicles"])
m3.metric("Pedestrians", st.session_state["pedestrians"])
m4.metric("Violations", st.session_state["violations"])
m5.metric("Average Speed", st.session_state["avg_speed"])

# ---------------------------------------
# LEFT PANEL (Video Feed & Loop)
# ---------------------------------------
with left:
    if source != "Upload Video" or uploaded_video is None:
        step_badge("1. Upload a video", "active")
        st.info("📤 Upload a video from the sidebar to begin.")
    else:
        video_path = save_uploaded_video(uploaded_video)
        frame = extract_first_frame(video_path)

        if frame is None:
            st.error("Unable to read the uploaded video frame. Try a different file.")
        else:
            roi_locked = st.session_state.get("roi_saved", False)

            # Step badges
            b1, b2, b3 = st.columns(3)
            with b1: step_badge("1. Video uploaded", "done")
            with b2: step_badge("2. Select lane", "done" if roi_locked else "active")
            with b3: step_badge("3. Process", "active" if roi_locked else "pending")

            # ROI Selector view (only when not processing/done)
            if not st.session_state.processing and not st.session_state.processing_done:
                selector = ROISelector()
                roi_polygon = selector.show(frame)
                if roi_polygon is not None:
                    st.session_state["roi"] = roi_polygon

            st.subheader("🎥 Video Feed")
            
            # Persistent video feed placeholder
            video_frame_placeholder = st.empty()

            # Trigger video processing initialization
            if process:
                if "roi" not in st.session_state:
                    st.warning("⚠️ Please select and save a restricted lane first.")
                elif not os.path.exists("best.pt"):
                    st.error("Model file 'best.pt' was not found. Place weights next to app.py.")
                else:
                    detector = TrafficDetector(
                        model_path="best.pt",
                        roi_polygon=st.session_state["roi"],
                        confidence=confidence,
                        iou=iou,
                    )
                    cap = cv2.VideoCapture(video_path)
                    fps = cap.get(cv2.CAP_PROP_FPS) or 25
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

                    output_path_shown = os.path.join(tempfile.gettempdir(), "traffic_output_lane.mp4")
                    output_path_hidden = os.path.join(tempfile.gettempdir(), "traffic_output_clean.mp4")
                    
                    fourcc = cv2.VideoWriter_fourcc(*"avc1")
                    writer_shown = cv2.VideoWriter(output_path_shown, fourcc, fps, (width, height))
                    writer_hidden = cv2.VideoWriter(output_path_hidden, fourcc, fps, (width, height))

                    if not writer_shown.isOpened():
                        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                        writer_shown = cv2.VideoWriter(output_path_shown, fourcc, fps, (width, height))
                        writer_hidden = cv2.VideoWriter(output_path_hidden, fourcc, fps, (width, height))

                    # Save streaming objects to session state
                    st.session_state.cap = cap
                    st.session_state.detector = detector
                    st.session_state.writer_shown = writer_shown
                    st.session_state.writer_hidden = writer_hidden
                    st.session_state.output_path_shown = output_path_shown
                    st.session_state.output_path_hidden = output_path_hidden
                    st.session_state.total_frames = total_frames
                    st.session_state.frame_idx = 0
                    st.session_state.processing = True
                    st.session_state.processing_done = False
                    st.rerun()

            # Handle Stop button
            if stop and st.session_state.processing:
                st.session_state.processing = False
                if st.session_state.cap:
                    st.session_state.cap.release()
                if st.session_state.writer_shown:
                    st.session_state.writer_shown.release()
                if st.session_state.writer_hidden:
                    st.session_state.writer_hidden.release()
                st.rerun()

            # Continuous execution loop
            if st.session_state.processing and st.session_state.cap is not None:
                cap = st.session_state.cap
                detector = st.session_state.detector
                writer_shown = st.session_state.writer_shown
                writer_hidden = st.session_state.writer_hidden
                total_frames = st.session_state.total_frames

                while cap.isOpened() and st.session_state.processing:
                    ret, current_frame = cap.read()
                    if not ret:
                        cap.release()
                        writer_shown.release()
                        writer_hidden.release()
                        st.session_state.processing = False
                        st.session_state.processing_done = True
                        st.session_state.cap = None
                        progress_bar.empty()
                        st.rerun()
                        break

                    # Dual-pass detection & frame annotation
                    frame_shown, frame_hidden = detector.process_frame_dual(current_frame)
                    writer_shown.write(frame_shown)
                    writer_hidden.write(frame_hidden)

                    # Dynamic Overlay Selection
                    active_display_frame = frame_shown if st.session_state.get("show_lane", True) else frame_hidden
                    active_display_rgb = cv2.cvtColor(active_display_frame, cv2.COLOR_BGR2RGB)

                    # Update live stream container
                    video_frame_placeholder.image(active_display_rgb, use_container_width=True)

                    # Update analytics metrics
                    stats = detector.get_analytics()
                    st.session_state["traffic"] = stats.get("traffic", 0)
                    st.session_state["vehicles"] = stats.get("vehicles", 0)
                    st.session_state["pedestrians"] = stats.get("pedestrians", 0)
                    st.session_state["violations"] = stats.get("violations", 0)
                    st.session_state["avg_speed"] = f"{round(stats.get('avg_speed', 0), 1)} km/h"

                    m1.metric("Traffic", st.session_state["traffic"])
                    m2.metric("Vehicles", st.session_state["vehicles"])
                    m3.metric("Pedestrians", st.session_state["pedestrians"])
                    m4.metric("Violations", st.session_state["violations"])
                    m5.metric("Average Speed", st.session_state["avg_speed"])

                    # Update frame progress
                    st.session_state.frame_idx += 1
                    fraction = min(st.session_state.frame_idx / total_frames, 1.0)
                    progress_bar.progress(fraction, text=f"Processing video… {int(fraction * 100)}%")

            # -------------------------------------------------------------
            # Final Video Preview & Dual Export Buttons (Enterprise Pattern)
            # -------------------------------------------------------------
            if st.session_state.processing_done:
                is_lane_on = st.session_state.get("show_lane", True)
                active_path = (
                    st.session_state.output_path_shown
                    if is_lane_on
                    else st.session_state.output_path_hidden
                )

                if active_path and os.path.exists(active_path):
                    st.video(active_path)
                    st.caption("💡 *Use the sidebar toggle above to switch live video views.*")
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

                    st.markdown("#### 📥 Export Video Options")
                    
                    dl_col1, dl_col2 = st.columns(2)

                    with dl_col1:
                        if st.session_state.output_path_shown and os.path.exists(st.session_state.output_path_shown):
                            with open(st.session_state.output_path_shown, "rb") as f:
                                st.download_button(
                                    label="⬇️ Download Annotated Video (With Lane)",
                                    data=f,
                                    file_name="traffic_analytics_annotated.mp4",
                                    mime="video/mp4",
                                    use_container_width=True,
                                    type="primary"
                                )

                    with dl_col2:
                        if st.session_state.output_path_hidden and os.path.exists(st.session_state.output_path_hidden):
                            with open(st.session_state.output_path_hidden, "rb") as f:
                                st.download_button(
                                    label="⬇️ Download Clean Video (No Lane)",
                                    data=f,
                                    file_name="traffic_analytics_clean.mp4",
                                    mime="video/mp4",
                                    use_container_width=True,
                                )

# Status box updates
if source == "Upload Video" and uploaded_video is not None:
    if st.session_state.get("roi_saved"):
        status_placeholder.success("✅ Restricted lane saved — ready to process.")
    elif "roi" in st.session_state:
        status_placeholder.info("Lane points selected. Save to lock them in.")
    else:
        status_placeholder.info("Select a restricted lane on the video frame to continue.")