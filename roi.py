"""
roi.py
------
Lets the user click 4 points on the first video frame to draw a
"restricted lane" polygon.

UX design (deliberate):
  - While selecting: interactive canvas is shown, points/lines drawn
    live, Reset/Save buttons available.
  - Once saved: the canvas is REPLACED by a compact one-line summary
    card + "Edit Lane" button. We don't need the click UI anymore,
    and the polygon itself keeps showing on the live video later
    (drawn by TrafficAnalytics.draw_lane in analytics.py), so nothing
    is actually lost -- just the editing controls are tucked away.
"""

import cv2
import numpy as np
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates


class ROISelector:

    MAX_POINTS = 4
    POINT_COLOR = (56, 189, 248)       # cyan (BGR)
    LINE_COLOR_CLOSED = (34, 197, 94)  # green
    LINE_COLOR_OPEN = (250, 204, 21)   # amber, while still drawing

    def __init__(self):
        st.session_state.setdefault("roi_points", [])
        st.session_state.setdefault("roi_saved", False)

    # -----------------------------------------------------------
    def _draw_overlay(self, image: np.ndarray) -> np.ndarray:
        display = image.copy()
        points = st.session_state.roi_points

        for i, point in enumerate(points):
            cv2.circle(display, tuple(point), 7, self.POINT_COLOR, -1)
            cv2.circle(display, tuple(point), 7, (255, 255, 255), 2)
            cv2.putText(
                display, str(i + 1), (point[0] + 10, point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2
            )

        if len(points) >= 2:
            closed = len(points) == self.MAX_POINTS
            color = self.LINE_COLOR_CLOSED if closed else self.LINE_COLOR_OPEN
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(display, [pts], isClosed=closed, color=color, thickness=2)

            if closed:
                tint = display.copy()
                cv2.fillPoly(tint, [pts], self.LINE_COLOR_CLOSED)
                display = cv2.addWeighted(tint, 0.15, display, 0.85, 0)

        return display

    # -----------------------------------------------------------
    def show(self, image: np.ndarray):
        """Returns the saved polygon once locked, otherwise None."""
        if st.session_state.roi_saved:
            return self._show_locked_summary()
        return self._show_selector(image)

    # -----------------------------------------------------------
    def _show_locked_summary(self):
        st.markdown("#### 🛣️ Restricted Lane")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"Lane locked in with {len(st.session_state.roi_points)} points.")
        with col2:
            if st.button("✏️ Edit Lane", use_container_width=True):
                st.session_state.roi_saved = False
                st.rerun()
        return st.session_state.roi_points

    # -----------------------------------------------------------
    def _show_selector(self, image: np.ndarray):
        st.markdown("#### 🛣️ Select Restricted Lane")

        remaining = self.MAX_POINTS - len(st.session_state.roi_points)
        if remaining > 0:
            st.caption(f"Click {remaining} more point(s) on the road to outline the lane.")
        else:
            st.caption("4 points selected — save to lock the lane in.")

        display = self._draw_overlay(image)
        clicked = streamlit_image_coordinates(display, key="roi_selector")

        if clicked is not None:
            point = [int(clicked["x"]), int(clicked["y"])]
            if point not in st.session_state.roi_points and len(st.session_state.roi_points) < self.MAX_POINTS:
                st.session_state.roi_points.append(point)
                st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True, disabled=not st.session_state.roi_points):
                st.session_state.roi_points = []
                st.session_state.roi_saved = False
                st.rerun()
        with col2:
            can_save = len(st.session_state.roi_points) == self.MAX_POINTS
            if st.button("💾 Save Lane", use_container_width=True, disabled=not can_save, type="primary"):
                st.session_state.roi_saved = True
                st.rerun()

        if st.session_state.roi_points:
            with st.expander("Raw coordinates"):
                st.write(st.session_state.roi_points)

        return None

    # -----------------------------------------------------------
    @staticmethod
    def reset():
        """Call when a new video is uploaded so the old lane doesn't carry over."""
        st.session_state.roi_points = []
        st.session_state.roi_saved = False