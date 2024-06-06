import argparse
import cv2
import math
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

def process_video(input_video_path, output_video_path, model_weights):
    # Initialize YOLO model with provided weights
    model = YOLO(model_weights)

    # Open the video file
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise Exception(f"Error opening video file {input_video_path}")

    # Get video properties
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))

    # Configuration for distance calculation
    center_point = (w // 2, h)  # Center point from where distances are measured
    pixel_per_meter = 1000  # Adjust this value based on your actual scaling factor

    # Define colors for text and bounding boxes
    txt_color, txt_background, bbox_clr = ((0, 0, 0), (255, 255, 255), (255, 0, 255))

    while True:
        ret, im0 = cap.read()
        if not ret:
            print("End of video stream or cannot fetch the frame.")
            break

        annotator = Annotator(im0, line_width=2)
        results = model.track(im0, persist=True)  # Ensure the YOLO model has a track method that supports this usage

        if results and results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.int().cpu().tolist()

            for box, track_id in zip(results[0].boxes.xyxy.cpu(), track_ids):
                annotator.box_label(box, label=str(track_id), color=bbox_clr)

                x1, y1 = int((box[0] + box[2]) // 2), int((box[1] + box[3]) // 2)
                distance = math.sqrt((x1 - center_point[0]) ** 2 + (y1 - center_point[1]) ** 2) / pixel_per_meter

                text_size, _ = cv2.getTextSize(f"Distance: {distance:.2f} m", cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                cv2.rectangle(im0, (x1, y1 - text_size[1] - 10), (x1 + text_size[0] + 10, y1), txt_background, -1)
                cv2.putText(im0, f"Distance: {distance:.2f} m", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, txt_color, 3)

        out.write(im0)
        cv2.imshow("FishTally Distance Calculation", im0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video for object detection and distance calculation using YOLO.")
    parser.add_argument("model_weights", help="Path to YOLO model weights file.")
    parser.add_argument("input_video_path", help="Path to the input video file.")
    parser.add_argument("output_video_path", help="Path for the output video file.")

    args = parser.parse_args()

    process_video(args.input_video_path, args.output_video_path, args.model_weights)