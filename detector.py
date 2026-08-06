
from collections import defaultdict
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

from analytics import TrafficAnalytics


# ============================================================
# Professional Color Palette (RGB for Supervision)
# ============================================================

CLASS_COLOR_PALETTE = {

    # 🌸 Magenta (Cyclists & Two Wheelers)
    "cyclist": (235, 0, 140),
    "two_wheeler": (235, 0, 140),

    # 🔷 Royal Blue (Cars & Vehicles)
    "car": (35, 75, 220),
    "vehicle": (35, 75, 220),

    # 🟦 Deep Sky Blue (Bus & Truck)
    "bus": (0, 170, 255),
    "truck": (0, 170, 255),

    # 🟢 Teal (Person & Pedestrian)
    "person": (0, 190, 170),
    "pedestrian": (0, 190, 170),
}

FALLBACK_COLORS = [
    (235, 0, 140),   # Magenta
    (35, 75, 220),   # Royal Blue
    (0, 170, 255),   # Sky Blue
    (0, 190, 170),   # Teal
]



class TrafficDetector:

    def __init__(self, model_path, roi_polygon, confidence=0.45, iou=0.50):
        self.model = YOLO(model_path)
        self.class_names = self.model.names

        self.confidence = confidence
        self.iou = iou
        self.roi_polygon = np.array(roi_polygon, dtype=np.int32)

        self.tracker = sv.ByteTrack(lost_track_buffer=60, track_activation_threshold=0.35)

        self._class_annotators = {}

        # Violation Annotator (Vibrant Red)
        self.red_box = sv.BoxAnnotator(
            thickness=2, color=sv.Color(r=255, g=0, b=0)
        )
        self.red_label = sv.LabelAnnotator(
            text_scale=0.4, text_thickness=1,
            color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.WHITE,
        )

        self.trace = sv.TraceAnnotator(thickness=2, trace_length=15)
        self.analytics = None

    def initialize(self, frame):
        h, w = frame.shape[:2]
        zone = (0, 0, w, h)

        self.analytics = TrafficAnalytics(
            zone=zone,
            lane_polygon=self.roi_polygon,
            class_names=self.class_names,
            restricted_classes=["vehicle", "car", "truck", "bus"],
        )

    def _run_detection(self, frame):
        if self.analytics is None:
            self.initialize(frame)

        results = self.model.predict(frame, conf=self.confidence, iou=self.iou, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        tracked = self.tracker.update_with_detections(detections)
        self.analytics.update(tracked)
        return tracked

    def _get_class_annotators(self, class_name):
        """Returns (box_annotator, label_annotator) matching modern UI styling."""
        key = class_name.lower()
        if key not in self._class_annotators:
            if key in CLASS_COLOR_PALETTE:
                color_bgr = CLASS_COLOR_PALETTE[key]
            else:
                idx = len(self._class_annotators) % len(FALLBACK_COLORS)
                color_bgr = FALLBACK_COLORS[idx]

            # Convert BGR tuple to Supervision Color (RGB format expected by Supervision Color)
            sv_color = sv.Color(r=color_bgr[2], g=color_bgr[1], b=color_bgr[0])

            box = sv.BoxAnnotator(thickness=5, color=sv_color)
            label = sv.LabelAnnotator(
                text_scale=0.45,
                text_thickness=1,
                color=sv_color,
                text_color=sv.Color.WHITE,
            )
            self._class_annotators[key] = (box, label)

        return self._class_annotators[key]

    def _draw_detections(self, canvas, tracked):
        if len(tracked) > 0 and tracked.tracker_id is not None:
            canvas = self.trace.annotate(scene=canvas, detections=tracked)

            violating_idx = []
            normal_by_class = defaultdict(list)

            for idx, tracker_id in enumerate(tracked.tracker_id):
                if tracker_id in self.analytics.current_violating_ids:
                    violating_idx.append(idx)
                else:
                    class_id = tracked.class_id[idx]
                    class_name = str(self.class_names[class_id])
                    normal_by_class[class_name].append(idx)

            # Class-based Annotations
            for class_name, idxs in normal_by_class.items():
                dets = tracked[np.array(idxs)]
                labels = [f"{class_name} #{t}" for t in dets.tracker_id]
                box_ann, label_ann = self._get_class_annotators(class_name)
                canvas = box_ann.annotate(scene=canvas, detections=dets)
                canvas = label_ann.annotate(scene=canvas, detections=dets, labels=labels)

            # Violation Annotations
            if violating_idx:
                dets = tracked[np.array(violating_idx)]
                labels = [f"{self.class_names[c]} #{t} | VIOLATION" for c, t in zip(dets.class_id, dets.tracker_id)]
                canvas = self.red_box.annotate(scene=canvas, detections=dets)
                canvas = self.red_label.annotate(scene=canvas, detections=dets, labels=labels)

        return canvas

    def process_frame_dual(self, frame):
        """Generates two frame versions: with lane overlay and clean/no lane overlay."""
        tracked = self._run_detection(frame)

        # Version A: With Lane
        canvas_shown = frame.copy()
        self.analytics.draw_lane(canvas_shown, visible=True)
        canvas_shown = self._draw_detections(canvas_shown, tracked)
        self.analytics.draw_hud(canvas_shown)

        # Version B: Without Lane
        canvas_hidden = frame.copy()
        self.analytics.draw_lane(canvas_hidden, visible=False)
        canvas_hidden = self._draw_detections(canvas_hidden, tracked)
        self.analytics.draw_hud(canvas_hidden)

        return canvas_shown, canvas_hidden

    def get_analytics(self):
        if self.analytics is None:
            return {}
        return {
            "traffic": self.analytics.current_traffic,
            "vehicles": self.analytics.vehicle_traffic,
            "pedestrians": self.analytics.pedestrian_count,
            "violations": len(self.analytics.lane_violations),
            "avg_speed": round(self.analytics.average_speed_kmh, 1),
            "stalled": self.analytics.stalled_count,
        }