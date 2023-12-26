import cv2
import argparse
import numpy as np

def show_first_frame_with_graph(video_path, save_path):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    if success:
        height, width, _ = frame.shape
        graph = np.zeros((height, width, 3), dtype=np.uint8)

        # Draw the axes
        cv2.line(graph, (0, 0), (width, 0), (255, 255, 255), 1)
        cv2.line(graph, (0, 0), (0, height), (255, 255, 255), 1)

        # Draw labels on the axes
        for i in range(0, width, 100):
            cv2.line(graph, (i, 0), (i, 10), (255, 255, 255), 1)
            cv2.putText(graph, str(i), (i - 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        for j in range(0, height, 100):
            cv2.line(graph, (0, j), (10, j), (255, 255, 255), 1)
            cv2.putText(graph, str(j), (20, j + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Overlay the graph on the frame
        combined = cv2.addWeighted(frame, 1, graph, 1, 0)

        cv2.imshow("First Frame with Graph", combined)
        print("Press 's' to save the image, or 'q' to quit without saving.")
        key = cv2.waitKey(0)
        if key == ord('q'):  # Quit if 'q' is pressed
            cv2.destroyAllWindows()
        elif key == ord('s'):  # Save if 's' is pressed
            cv2.imwrite(save_path, combined)
            print(f"Frame saved as {save_path}")
        cv2.destroyAllWindows()
    else:
        print("Failed to load the video.")
    cap.release()

def main():
    parser = argparse.ArgumentParser(description="Show First Frame of Video with Graph")
    parser.add_argument("--source_video", required=True, help="Path to the source video file")
    parser.add_argument("--save_path", required=True, help="Path to save the image file")
    args = parser.parse_args()

    show_first_frame_with_graph(args.source_video, args.save_path)

if __name__ == "__main__":
    main()