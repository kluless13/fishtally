import argparse
from single_line import single_line_threshold
from multi_line import multi_line_threshold
from polygon import polygon_threshold

def main():
    parser = argparse.ArgumentParser(description='Fish Tallying Tool')
    parser.add_argument('--model_weights', required=True, help='Path to the model weights file')
    parser.add_argument('--source_video', required=True, help='Path to the source video file')
    parser.add_argument('--target_video', required=True, help='Path for the output video file')
    parser.add_argument('--detector_type', required=True, choices=['single_line', 'multi_line', 'polygon'], help='Type of detector to use')
    
    # For simplicity, threshold settings are added as optional arguments. You can further customize as needed.
    parser.add_argument('--line_start', nargs=2, type=int, help='Start coordinates of the line (x, y)', default=[0, 0])
    parser.add_argument('--line_end', nargs=2, type=int, help='End coordinates of the line (x, y)', default=[100, 100])
    parser.add_argument('--polygon_points', nargs='+', type=int, help='List of points (x, y) defining the polygon', default=[0, 0, 100, 0, 100, 100, 0, 100])
    
    args = parser.parse_args()

    if args.detector_type == 'single_line':
        # Call single_line_threshold function
        single_line_threshold(args.model_weights, args.source_video, args.target_video, tuple(args.line_start), tuple(args.line_end))
    elif args.detector_type == 'multi_line':
        # Call multi_line_threshold function
        # Note: You need to adjust this part to pass the correct format of line points for your multi_line_threshold function
        multi_line_threshold(args.model_weights, args.source_video, args.target_video, [tuple(args.line_start), tuple(args.line_end)])
    elif args.detector_type == 'polygon':
        # Call polygon_threshold function
        # Convert flat list of coordinates to list of tuples
        it = iter(args.polygon_points)
        polygon_points = list(zip(it, it))
        polygon_threshold(args.model_weights, args.source_video, args.target_video, polygon_points)

if __name__ == '__main__':
    main()