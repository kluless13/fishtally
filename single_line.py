import cv2
from collections import defaultdict
import supervision as sv
from ultralytics import YOLO

def single_line_threshold(model_weights, source_video_path, target_video_path, line_start, line_end, class_id):
    # Load the YOLOv8 model
    model = YOLO(model_weights)

    # Set up video capture
    cap = cv2.VideoCapture(source_video_path)

    # Define line coordinates
    START = sv.Point(*line_start)
    END = sv.Point(*line_end)

    # Store the track history
    track_history = defaultdict(lambda: [])

    # Dictionary to keep track of objects that have crossed the line
    crossed_objects = {}

    # Open a video sink for the output video
    video_info = sv.VideoInfo.from_video_path(source_video_path)
    with sv.VideoSink(target_video_path, video_info) as sink:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Run YOLOv8 tracking on the frame
            results = model.track(frame, classes=[class_id], persist=True, save=True, tracker="bytetrack.yaml")

            # Initialize annotated_frame for cases where results might be empty or not contain trackable boxes
            annotated_frame = frame.copy()

            # Ensure there are detections and they have assigned IDs before processing
            if results[0].boxes is not None and getattr(results[0].boxes, 'id', None) is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()

                annotated_frame = results[0].plot()

                # Count objects crossing the line
                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box.numpy()
                    track = track_history[track_id]
                    track.append((x, y))  # x, y center point

                    if len(track) > 30:  # Retain 30 tracks for 30 frames
                        track.pop(0)

                    # Check if the object crosses the line
                    if START.x < x < END.x and abs(y - START.y) < 5:
                        if track_id not in crossed_objects:
                            crossed_objects[track_id] = True
                            # Annotate the object as it crosses the line
                            cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
            else:
                # Optionally, log when no trackable detections are found
                print("No trackable detections in this frame.")

            # Draw the line and write the count on the frame
            cv2.line(annotated_frame, (START.x, START.y), (END.x, END.y), (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Objects crossed line: {len(crossed_objects)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Write the frame with annotations to the output video
            sink.write_frame(annotated_frame)

    # Release the video capture
    cap.release()

    # Return count for the line
    return len(crossed_objects)

# Example usage of the function
# Uncomment and adjust the paths and parameters below to test the function.
# single_line_threshold('path_to_model_weights.pt', 'path_to_source_video.mp4', 'path_to_target_video.mp4', (100, 300), (800, 300), 1)

