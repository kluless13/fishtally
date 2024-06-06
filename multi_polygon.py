import argparse
import numpy as np
import supervision as sv
from ultralytics import YOLO
import cv2

class CountMultiPolygon:
    def __init__(self, input_video_path, output_video_path, model_weights, polygons, class_ids):
        self.model = YOLO(model_weights)
        self.class_ids = class_ids
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.video_info = sv.VideoInfo.from_video_path(input_video_path)

        # Initialize multiple polygon zones
        self.zones = [sv.PolygonZone(polygon=np.array(polygon), frame_resolution_wh=self.video_info.resolution_wh) for polygon in polygons]

        # Initialize annotators for each zone
        self.zone_annotators = [sv.PolygonZoneAnnotator(zone=zone, color=sv.ColorPalette.default().by_idx(i), thickness=4, text_thickness=4, text_scale=2) for i, zone in enumerate(self.zones)]

    def process_frame(self, frame: np.ndarray, _) -> np.ndarray:
        results = self.model(frame, imgsz=1280)[0]
        detections = sv.Detections.from_ultralytics(results)
        # Filter detections for the specified class_ids
        mask = np.isin(detections.class_id, self.class_ids)
        filtered_detections = detections[mask]

        for zone, zone_annotator in zip(self.zones, self.zone_annotators):
            zone.trigger(detections=filtered_detections)
            frame = zone_annotator.annotate(scene=frame)

        return frame

    def process_video(self):
        sv.process_video(source_path=self.input_video_path, target_path=self.output_video_path, callback=self.process_frame)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Multi-Polygon Video Processing Tool')
    parser.add_argument('--source_video', required=True, help='Path to the source video file')
    parser.add_argument('--target_video', required=True, help='Path for the output video file')
    parser.add_argument('--model_weights', required=True, help='Path to the model weights file')
    parser.add_argument('--class_ids', nargs='+', type=int, required=True, help='List of Class IDs to detect')
    parser.add_argument('--polygons', nargs='+', action='append', type=int, required=True, help='List of points defining each polygon. Each polygon is a flat list of x, y points.')

    args = parser.parse_args()
    # Convert flat list of points to list of polygons
    polygons = [list(zip(polygon[0::2], polygon[1::2])) for polygon in args.polygons]

    obj = CountMultiPolygon(args.source_video, args.target_video, args.model_weights, polygons, args.class_ids)
    obj.process_video()