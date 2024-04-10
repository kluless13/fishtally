import argparse
from ultralytics import YOLO
from ultralytics.solutions import distance_calculation
import cv2

def process_video(input_video_path, output_video_path, model_weights):
    # Load the YOLO model with specified weights
    model = YOLO(model_weights)
    names = model.model.names

    # Setup video capture and writer
    cap = cv2.VideoCapture(input_video_path)
    assert cap.isOpened(), f"Error opening video file {input_video_path}"
    w, h, fps = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                 int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                 int(cap.get(cv2.CAP_PROP_FPS)))

    video_writer = cv2.VideoWriter(output_video_path,
                                   cv2.VideoWriter_fourcc(*'mp4v'),  # or use 'XVID' if 'mp4v' doesn't work
                                   fps,
                                   (w, h))

    # Initialize distance calculation object
    dist_obj = distance_calculation.DistanceCalculation()
    dist_obj.set_args(names=names, view_img=True)

    # Process video frames
    while True:
        success, frame = cap.read()
        if not success:
            break  # Exit loop if no more frames to read

        # Process frame for object tracking and distance calculation
        tracks = model.track(frame, persist=True, show=False)
        frame = dist_obj.start_process(frame, tracks)
        video_writer.write(frame)

    # Cleanup
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    print("Processing complete. Output saved to:", output_video_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video for object detection and distance calculation using YOLO.")
    parser.add_argument("model_weights", help="Path to YOLO model weights file.")
    parser.add_argument("input_video_path", help="Path to the input video file.")
    parser.add_argument("output_video_path", help="Path for the output video file.")
    
    args = parser.parse_args()
    
    process_video(args.input_video_path, args.output_video_path, args.model_weights)

