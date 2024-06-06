import cv2
from collections import defaultdict
import supervision as sv
from ultralytics import YOLOWorld
import argparse

def single_line_threshold(model_weights, source_video_path, target_video_path, line_start, line_end, classes):
    # Load the YOLOWorld model
    model = YOLOWorld(model_weights)
    model.set_classes(classes)  # Set custom classes provided by CLI

    # Set up video capture
    cap = cv2.VideoCapture(source_video_path)

    # Define line coordinates
    START = sv.Point(*line_start)
    END = sv.Point(*line_end)

    # Store the track history and crossed objects
    track_history = defaultdict(lambda: [])
    crossed_objects = {}

    # Open a video sink for the output video
    video_info = sv.VideoInfo.from_video_path(source_video_path)
    with sv.VideoSink(target_video_path, video_info) as sink:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Run YOLOWorld tracking on the frame
            results = model.track(frame, persist=True, save=True, tracker="bytetrack.yaml")

            if results and results[0].boxes and results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
                annotated_frame = results[0].plot()

                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box.numpy()
                    track = track_history[track_id]
                    track.append((x, y))

                    if len(track) > 30:
                        track.pop(0)

                    if START.x < x < END.x and abs(y - START.y) < 5:
                        if track_id not in crossed_objects:
                            crossed_objects[track_id] = True
                            cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)

                cv2.line(annotated_frame, (START.x, START.y), (END.x, END.y), (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"Objects crossed line: {len(crossed_objects)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                sink.write_frame(annotated_frame)
            else:
                print("No detections or tracking results.")

    cap.release()
    return len(crossed_objects)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track objects across a line using YOLOWorld.")
    parser.add_argument('--model_weights', type=str, required=True, help='Path to model weights file.')
    parser.add_argument('--source_video', type=str, required=True, help='Path to the source video file.')
    parser.add_argument('--target_video', type=str, required=True, help='Path to the output video file.')
    parser.add_argument('--line_start', nargs=2, type=int, required=True, help='Start coordinates of the line (x, y).')
    parser.add_argument('--line_end', nargs=2, type=int, required=True, help='End coordinates of the line (x, y).')
    parser.add_argument('--classes', nargs='+', required=True, help='List of classes to track.')

    args = parser.parse_args()

    count = single_line_threshold(
        args.model_weights,
        args.source_video,
        args.target_video,
        tuple(args.line_start),
        tuple(args.line_end),
        args.classes
    )

    print(f"Total objects crossed the line: {count}")