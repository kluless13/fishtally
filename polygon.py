import numpy as np
import supervision as sv
from ultralytics import YOLO
from tqdm import tqdm
import cv2

def polygon_threshold(model_weights, source_video_path, target_video_path, polygon_points):
    # Load the YOLO model
    model = YOLO(model_weights)

    # Define the polygon zone
    polygon = np.array(polygon_points)  # polygon_points should be a list of (x, y) tuples
    video_info = sv.VideoInfo.from_video_path(source_video_path)
    zone = sv.PolygonZone(polygon=polygon, frame_resolution_wh=video_info.resolution_wh)

    # Annotators
    box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.white(), thickness=6, text_thickness=6, text_scale=4)

    # Video processing
    cap = cv2.VideoCapture(source_video_path)
    with sv.VideoSink(target_video_path, video_info) as sink:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Detect and filter detections within the polygon
            results = model(frame, imgsz=1280)[0]
            detections = sv.Detections.from_yolov8(results)
            zone.trigger(detections=detections)

            # Annotate the frame
            labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
            frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
            frame = zone_annotator.annotate(scene=frame)

            # Write the frame to the output video
            sink.write_frame(frame)

    # Release the video capture
    cap.release()

    # Output the total count
    total_count = zone.get_count()
    print(f"Total count within polygon: {total_count}")
    return total_count

# Example usage of the function
# polygon_threshold('path_to_model_weights.pt', 'path_to_source_video.mp4', 'path_to_target_video.mp4', [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
