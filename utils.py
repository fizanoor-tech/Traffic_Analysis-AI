"""
utils.py
--------
Small I/O helpers used by app.py.

save_uploaded_video(uploaded_video)
    Streamlit gives us an in-memory UploadedFile. OpenCV needs a real
    path on disk, so we write it to a temp file and hand back the path.

extract_first_frame(video_path)
    Opens the video, reads frame 0, converts BGR -> RGB (Streamlit/PIL
    expect RGB), and returns it as a numpy array. Returns None if the
    file couldn't be read (corrupt upload, unsupported codec, etc.)
"""

import tempfile
import cv2
import numpy as np
from typing import Optional


def save_uploaded_video(uploaded_video) -> str:
    """Persist a Streamlit UploadedFile to a temp .mp4 and return its path."""
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_video.read())
    temp_video.close()
    return temp_video.name


def extract_first_frame(video_path: str) -> Optional[np.ndarray]:
    """Return the first frame of a video as an RGB numpy array, or None on failure."""
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()

    if not success or frame is None:
        return None

    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)