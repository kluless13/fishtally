import argparse
from ultralytics import YOLO
import numpy as np
import supervision as sv
import cv2

class CountObject:

    def __init__(self, input_video_path, output_video_path, model_weights, polygon_points, class_ids):
        self.model_weights = model_weights
        self.model = YOLO(model_weights)
        self.class_ids = class_ids
        
        # Initialize polygon zone
        self.polygon = np.array(polygon_points)
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path

        self.video_info = sv.VideoInfo.from_video_path(input_video_path)
        self.zone = sv.PolygonZone(polygon=self.polygon, frame_resolution_wh=self.video_info.resolution_wh)

        # Initialize annotators
        self.box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
        self.zone_annotator = sv.PolygonZoneAnnotator(zone=self.zone, color=sv.Color.white(), thickness=6, text_thickness=6, text_scale=4)

    def process_frame(self, frame: np.ndarray, _) -> np.ndarray:
        # Detect objects and filter based on class_ids
        results = self.model(frame, imgsz=1280)[0]
        detections = sv.Detections.from_ultralytics(results)
        # Filter detections for the specified class_ids
        mask = np.isin(detections.class_id, self.class_ids)
        filtered_detections = detections[mask]
        self.zone.trigger(detections=filtered_detections)

        # Annotate the frame
        labels = [f"Class ID: {class_id}" for class_id in filtered_detections.class_id]
        frame = self.box_annotator.annotate(scene=frame, detections=filtered_detections, labels=labels)
        frame = self.zone_annotator.annotate(scene=frame)

        return frame
    
    def process_video(self):
        sv.process_video(source_path=self.input_video_path, target_path=self.output_video_path, callback=self.process_frame)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Polygon-based Video Processing Tool')
    parser.add_argument('--source_video', required=True, help='Path to the source video file')
    parser.add_argument('--target_video', required=True, help='Path for the output video file')
    parser.add_argument('--model_weights', required=True, help='Path to the model weights file')
    parser.add_argument('--class_ids', nargs='+', type=int, required=True, help='List of Class IDs to detect')
    parser.add_argument('--polygon_points', nargs='+', type=int, required=True, help='List of points (x, y) defining the polygon')

    args = parser.parse_args()
    polygon_points = list(zip(args.polygon_points[0::2], args.polygon_points[1::2]))  # Convert flat list to list of tuples

    obj = CountObject(args.source_video, args.target_video, args.model_weights, polygon_points, args.class_ids)
    obj.process_video()