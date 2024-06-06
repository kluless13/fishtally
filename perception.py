import argparse
from ultralytics import YOLO
from distance_calculator import DistanceCalculation
import cv2

def process_video(input_video_path, output_video_path, model_weights, target_class=None):
    model = YOLO(model_weights)
    names = model.model.names

    cap = cv2.VideoCapture(input_video_path)
    assert cap.isOpened(), f"Error opening video file {input_video_path}"
    w, h, fps = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                 int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                 int(cap.get(cv2.CAP_PROP_FPS)))

    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    dist_obj = DistanceCalculation()
    dist_obj.set_args(names=names, view_img=True)

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, size=640)  # Adjust size as needed
        if target_class is not None:
            # Filtering results by target_class
            results = results.xyxy[0]  # Results of predictions (tensor)
            results = results[results[:, 5] == target_class]  # Filter by class

        # Example of how to handle results if you need to iterate
        for *box, conf, cls_id in results:
            if int(cls_id) == target_class:
                # Do something with the results, e.g., draw boxes
                pass

        frame = dist_obj.start_process(frame, results)
        video_writer.write(frame)

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    print("Processing complete. Output saved to:", output_video_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video for object detection and distance calculation using YOLO.")
    parser.add_argument("model_weights", help="Path to YOLO model weights file.")
    parser.add_argument("input_video_path", help="Path to the input video file.")
    parser.add_argument("output_video_path", help="Path for the output video file.")
    parser.add_argument("--class", dest="target_class", type=int, help="Optional class ID to focus on.")

    args = parser.parse_args()
    
    process_video(args.input_video_path, args.output_video_path, args.model_weights, args.target_class)
