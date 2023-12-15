import cv2
from collections import defaultdict
import supervision as sv
from ultralytics import YOLO
import numpy as np
from tqdm import tqdm

def multi_line_threshold(model_weights, source_video_path, target_video_path, line1_start, line1_end, line2_start, line2_end):
    # Load the YOLOv8 model
    model = YOLO(model_weights)

    # Set up video capture
    cap = cv2.VideoCapture(source_video_path)

    # Define line coordinates
    START = sv.Point(*line1_start)
    END = sv.Point(*line1_end)
    START2 = sv.Point(*line2_start)
    END2 = sv.Point(*line2_end)

    # Store the track history
    track_history = defaultdict(lambda: [])

    # Dictionaries to keep track of objects that have crossed each line
    crossed_objects = {}
    crossed_objects2 = {}

    # Open a video sink for the output video
    video_info = sv.VideoInfo.from_video_path(source_video_path)
    with sv.VideoSink(target_video_path, video_info) as sink:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Run YOLOv8 tracking on the frame
            results = model.track(frame, classes=[], persist=True, save=True, tracker="bytetrack.yaml")

            # Process detections and tracks
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            annotated_frame = results[0].plot()

            # Count objects crossing each line
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box.numpy()
                track = track_history[track_id]
                track.append((x, y))  # x, y center point

                if len(track) > 30:  # retain 30 tracks for 30 frames
                    track.pop(0)

                # Check if the object crosses the first line
                if START.x < x < END.x and abs(y - START.y) < 5:
                    if track_id not in crossed_objects:
                        crossed_objects[track_id] = True

                # Check if the object crosses the second line
                if START2.x < x < END2.x and abs(y - START2.y) < 5:
                    if track_id not in crossed_objects2:
                        crossed_objects2[track_id] = True

                    # Annotate the object as it crosses the line
                    cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)

            # Draw the lines and write the counts on the frame
            cv2.line(annotated_frame, (START.x, START.y), (END.x, END.y), (0, 255, 0), 2)
            cv2.line(annotated_frame, (START2.x, START2.y), (END2.x, END2.y), (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Objects crossed line 1: {len(crossed_objects)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Objects crossed line 2: {len(crossed_objects2)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Write the frame with annotations to the output video
            sink.write_frame(annotated_frame)

    # Release the video capture
    cap.release()

    # Return counts for each line
    return len(crossed_objects), len(crossed_objects2)

# Example usage of the function
# multi_line_threshold('path_to_model_weights.pt', 'path_to_source_video.mp4', 'path_to_target_video.mp4', (x1, y1), (x2, y2), (x3, y3), (x4, y4))
