"""
analytics.py
------------
Traffic analytics engine. Counting, restricted-lane violation detection,
running-average speed estimation, and stalled-vehicle detection are ported
DIRECTLY from the "Clean Traffic Analytics Engine (Final)" Kaggle script --
same accumulator-based speed fix, same 30-frame position history, same
10-consecutive-frame violation rule, same stalled-ID cleanup. None of that
logic was changed.

The one addition is draw_lane(frame, visible=True): the Kaggle script kept
the lane permanently invisible on video. The Streamlit app now exposes a
"Show Restricted Lane" sidebar checkbox (default ON) that drives this flag,
so app.py controls visibility -- the analytics logic itself doesn't decide.
A live violation always overrides the toggle and shows red, since that's
safety-relevant information the user shouldn't be able to hide.
"""


from collections import defaultdict, deque
import cv2
import numpy as np

# ============================================================
# CONFIG: rough pixel-to-real-world speed conversion
# ============================================================
ASSUMED_PIXELS_PER_METER = 20.0
FPS_FOR_SPEED = 30.0


def draw_dashed_polygon(img, pts, color, thickness=2, dash_len=10, gap_len=5):
    """Draws a dashed polygon line around given points in OpenCV."""
    pts = np.array(pts, dtype=np.int32).reshape((-1, 2))
    n = len(pts)
    for i in range(n):
        p1 = pts[i]
        p2 = pts[(i + 1) % n]  # Loop back to closing point
        
        # Calculate distance and direction vector
        dist = np.linalg.norm(p2 - p1)
        if dist == 0:
            continue
            
        unit_vec = (p2 - p1) / dist
        curr_dist = 0.0
        
        while curr_dist < dist:
            start_pt = p1 + unit_vec * curr_dist
            end_dist = min(curr_dist + dash_len, dist)
            end_pt = p1 + unit_vec * end_dist
            
            cv2.line(
                img,
                (int(start_pt[0]), int(start_pt[1])),
                (int(end_pt[0]), int(end_pt[1])),
                color,
                thickness,
                lineType=cv2.LINE_AA
            )
            curr_dist += dash_len + gap_len


class TrafficAnalytics:

    LANE_LINE_COLOR = (235, 90, 40)   # Blueish-indigo border in BGR (matching image)

    def __init__(self, zone, lane_polygon, class_names, restricted_classes=None):
        self.zone = zone
        self.lane_polygon = np.array(lane_polygon, np.int32)
        self.class_names = class_names

        self.restricted_classes = set(
            [c.lower() for c in (restricted_classes or ["vehicle", "car", "bus", "truck"])]
        )
        self.motor_classes = {"vehicle", "two_wheeler", "car", "bus", "truck"}

        self.counted_ids = set()
        self.total_traffic = 0
        self.current_traffic = 0
        self.class_counts = {name: 0 for name in class_names.values()}

        self.position_history = defaultdict(lambda: deque(maxlen=30))
        self.object_speeds = {}

        self.total_speed_sum = 0.0
        self.speed_sample_count = 0
        self.average_speed_px = 0.0

        self.stalled_ids = set()
        self.stalled_count = 0

        self.lane_violations = set()
        self.current_violating_ids = set()
        self.lane_consecutive_frames = defaultdict(int)

    def point_inside_zone(self, x, y):
        x1, y1, x2, y2 = self.zone
        return x1 <= x <= x2 and y1 <= y <= y2

    def point_inside_lane(self, x, y):
        return cv2.pointPolygonTest(self.lane_polygon, (float(x), float(y)), False) >= 0

    def update(self, tracked_detections):
        self.current_traffic = len(tracked_detections)
        self.current_violating_ids.clear()

        active_frame_ids = set()

        if tracked_detections.tracker_id is None:
            return

        for i in range(len(tracked_detections)):
            tracker_id = tracked_detections.tracker_id[i]
            if tracker_id is None:
                continue

            active_frame_ids.add(tracker_id)
            class_id = tracked_detections.class_id[i]
            class_name = str(self.class_names[class_id])

            x1, y1, x2, y2 = map(int, tracked_detections.xyxy[i])
            ground_x = (x1 + x2) // 2
            ground_y = y2

            # 1. Position History
            self.position_history[tracker_id].append((ground_x, ground_y))
            history = self.position_history[tracker_id]

            # 2. Speed Estimation
            if len(history) >= 2:
                old_x, old_y = history[-2]
                new_x, new_y = history[-1]
                pixel_speed = ((new_x - old_x) ** 2 + (new_y - old_y) ** 2) ** 0.5
                self.object_speeds[tracker_id] = pixel_speed

                if pixel_speed > 1.0:
                    self.total_speed_sum += pixel_speed
                    self.speed_sample_count += 1

            # 3. Stalled Detection
            if len(history) == history.maxlen:
                start_x, start_y = history[0]
                end_x, end_y = history[-1]
                displacement = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
                if displacement < 15:
                    self.stalled_ids.add(tracker_id)
                else:
                    self.stalled_ids.discard(tracker_id)

            # 4. Lane Violation Check (10 consecutive frames required)
            if class_name.lower() in self.restricted_classes:
                if self.point_inside_lane(ground_x, ground_y):
                    self.lane_consecutive_frames[tracker_id] += 1
                    if self.lane_consecutive_frames[tracker_id] >= 10:
                        self.lane_violations.add(tracker_id)
                        self.current_violating_ids.add(tracker_id)
                else:
                    self.lane_consecutive_frames[tracker_id] = 0

            # 5. Total Traffic / Class Counting
            if self.point_inside_zone(ground_x, ground_y):
                if tracker_id not in self.counted_ids:
                    self.counted_ids.add(tracker_id)
                    self.total_traffic += 1
                    if class_name in self.class_counts:
                        self.class_counts[class_name] += 1

        self.stalled_ids = {tid for tid in self.stalled_ids if tid in active_frame_ids}
        self.stalled_count = len(self.stalled_ids)

        if self.speed_sample_count > 0:
            self.average_speed_px = self.total_speed_sum / self.speed_sample_count

    @property
    def vehicle_traffic(self):
        return sum(self.class_counts.get(c, 0) for c in self.motor_classes)

    @property
    def pedestrian_count(self):
        return self.class_counts.get("person", 0) + self.class_counts.get("pedestrian", 0)

    @property
    def average_speed_kmh(self):
        px_per_sec = self.average_speed_px * FPS_FOR_SPEED
        m_per_sec = px_per_sec / ASSUMED_PIXELS_PER_METER
        return m_per_sec * 3.6

    def draw_lane(self, frame, visible=True):
        if not visible:
            return

        # Draws clean dashed border line around polygon
        draw_dashed_polygon(
            frame, 
            self.lane_polygon, 
            color=self.LANE_LINE_COLOR, 
            thickness=2, 
            dash_len=8, 
            gap_len=5
        )

    def draw_hud(self, frame):
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

        lines = [
            (f"Current Traffic   : {self.current_traffic}", (0, 255, 0)),
            (f"Vehicle Traffic   : {self.vehicle_traffic}", (255, 255, 0)),
            (f"Lane Violations   : {len(self.lane_violations)}", (0, 0, 255)),
        ]
        y = 40
        for text, color in lines:
            cv2.putText(frame, text, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            y += 30