import os
import sys
from ultralytics import YOLO
from supervision.draw.color import ColorPalette
from supervision.geometry.dataclasses import Point
from supervision.video.dataclasses import VideoInfo
from supervision.video.source import get_video_frames_generator
from supervision.video.sink import VideoSink
from supervision.tools.detections import Detections, BoxAnnotator
from supervision.tools.line_counter import LineCounter, LineCounterAnnotator
from yolox.tracker.byte_tracker import BYTETracker, STrack
from onemetric.cv.utils.iou import box_iou_batch
from dataclasses import dataclass
from typing import List
import numpy as np
from tqdm import tqdm

# Define the BYTETracker arguments
@dataclass(frozen=True)
class BYTETrackerArgs:
    track_thresh: float = 0.25
    track_buffer: int = 30
    match_thresh: float = 0.8
    aspect_ratio_thresh: float = 3.0
    min_box_area: float = 1.0
    mot20: bool = False

# Function for single line threshold counting
def single_line_threshold(model_weights, source_video_path, target_video_path, line_start, line_end, class_id):
    # Load the model
    model = YOLO(model_weights)
    model.fuse()

    # Create BYTETracker instance
    byte_tracker = BYTETracker(BYTETrackerArgs())

    # Setup video capture and other initializations
    video_info = VideoInfo.from_video_path(source_video_path)
    generator = get_video_frames_generator(source_video_path)
    line_counter = LineCounter(start=line_start, end=line_end)
    box_annotator = BoxAnnotator(color=ColorPalette.default(), thickness=4, text_thickness=4, text_scale=2)
    line_annotator = LineCounterAnnotator(thickness=4, text_thickness=2, text_scale=1)

    # Open target video file
    with VideoSink(target_video_path, video_info) as sink:
        # Loop over video frames
        for frame in tqdm(generator, total=video_info.total_frames):
            # Model prediction and conversion to supervision Detections
            results = model(frame)
            detections = Detections(
                xyxy=results[0].boxes.xyxy.cpu().numpy(),
                confidence=results[0].boxes.conf.cpu().numpy(),
                class_id=results[0].boxes.cls.cpu().numpy().astype(int)
            )

            # Filtering out detections with unwanted classes
            mask = np.isin(detections.class_id, class_id)
            detections.filter(mask=mask, inplace=True)

            # Converts detections to the format for ByteTrack
            def detections2boxes(detections):
                return np.hstack((detections.xyxy, detections.confidence[:, np.newaxis]))

            # Converts tracks to the format for ByteTrack
            def tracks2boxes(tracks):
                return np.array([track.tlbr for track in tracks], dtype=float)

            # Tracking detections
            tracks = byte_tracker.update(
                output_results=detections2boxes(detections),
                img_info=frame.shape,
                img_size=frame.shape
            )

            # Matches detections with tracks
            def match_detections_with_tracks(detections, tracks):
                if not np.any(detections.xyxy) or len(tracks) == 0:
                    return np.empty((0,))
                
                tracks_boxes = tracks2boxes(tracks)
                iou = box_iou_batch(tracks_boxes, detections.xyxy)
                track2detection = np.argmax(iou, axis=1)

                tracker_ids = [None] * len(detections)
                for tracker_index, detection_index in enumerate(track2detection):
                    if iou[tracker_index, detection_index] != 0:
                        tracker_ids[detection_index] = tracks[tracker_index].track_id

                return tracker_ids

            # Updating tracker IDs in detections
            tracker_ids = match_detections_with_tracks(detections, tracks)
            detections.tracker_id = np.array(tracker_ids)

            # Filtering out detections without trackers
            mask = np.array([tracker_id is not None for tracker_id in detections.tracker_id], dtype=bool)
            detections.filter(mask=mask, inplace=True)

            # Updating line counter
            line_counter.update(detections=detections)

            # Formatting custom labels for detections
            labels = [
                f"#{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, tracker_id in detections
            ]

            # Annotate and display frame
            frame = box_annotator.annotate(frame=frame, detections=detections, labels=labels)
            line_annotator.annotate(frame=frame, line_counter=line_counter)

            # Write frame to the output video
            sink.write_frame(frame)

    # Output the final count
    final_count = line_counter.get_count()
    print(f"Total fish count: {final_count}")
    return final_count

# Example usage of the function
# single_line_threshold("path_to_model_weights.pt", "path_to_source_video.mp4", "path_to_target_video.mp4", Point(10,100), Point(1200, 700), [3])