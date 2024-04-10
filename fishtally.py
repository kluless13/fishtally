import argparse
from single_line import single_line_threshold
from multi_line import multi_line_threshold
from polygon import CountObject
from multi_polygon import CountMultiPolygon

def main():
    parser = argparse.ArgumentParser(description='Fish Tallying Tool')
    parser.add_argument('--model_weights', required=True, help='Path to the model weights file')
    parser.add_argument('--source_video', required=True, help='Path to the source video file')
    parser.add_argument('--target_video', required=True, help='Path for the output video file')
    parser.add_argument('--detector_type', required=True, choices=['single_line', 'multi_line', 'polygon','multi_polygon'], help='Type of detector to use')
    # Updated to accept multiple class IDs
    parser.add_argument('--class_id', nargs='+', type=int, required=True, help='Class ID(s) to track') 
    parser.add_argument('--line_start', nargs=2, type=int, help='Start coordinates of the line (x, y)', default=[0, 0])
    parser.add_argument('--line_end', nargs=2, type=int, help='End coordinates of the line (x, y)', default=[100, 100])
    parser.add_argument('--line1_start', nargs=2, type=int, help='Start coordinates of the first line (x, y)')
    parser.add_argument('--line1_end', nargs=2, type=int, help='End coordinates of the first line (x, y)')
    parser.add_argument('--line2_start', nargs=2, type=int, help='Start coordinates of the second line (x, y)')
    parser.add_argument('--line2_end', nargs=2, type=int, help='End coordinates of the second line (x, y)')
    parser.add_argument('--polygon_points', nargs='+', type=int, help='List of points (x, y) defining the polygon', default=[0, 0, 100, 0, 100, 100, 0, 100])
    parser.add_argument('--polygons', nargs='+', action='append', type=int, help='Lists of points (x, y) defining each polygon. Each polygon is a flat list of x, y points.')
    args = parser.parse_args()

    if args.detector_type == 'single_line':
        single_line_threshold(args.model_weights, args.source_video, args.target_video, tuple(args.line_start), tuple(args.line_end), args.class_id)
    elif args.detector_type == 'multi_line':
        line1_start = tuple(args.line1_start)
        line1_end = tuple(args.line1_end)
        line2_start = tuple(args.line2_start)
        line2_end = tuple(args.line2_end)
        count_line1, count_line2 = multi_line_threshold(
            args.model_weights, 
            args.source_video, 
            args.target_video, 
            line1_start, 
            line1_end, 
            line2_start, 
            line2_end, 
            args.class_id
        )
        print(f"Objects crossed line 1: {count_line1}, Objects crossed line 2: {count_line2}")
    elif args.detector_type == 'polygon':
        polygon_points = list(zip(args.polygon_points[0::2], args.polygon_points[1::2]))
        obj = CountObject(args.source_video, args.target_video, args.model_weights, polygon_points, args.class_id)
        obj.process_video()
    elif args.detector_type == 'multi_polygon':
        polygons = [list(zip(polygon[0::2], polygon[1::2])) for polygon in args.polygons]
        obj = CountMultiPolygon(args.source_video, args.target_video, args.model_weights, polygons, args.class_id)
        obj.process_video()

if __name__ == '__main__':
    main()

