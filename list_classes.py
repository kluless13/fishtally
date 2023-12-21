from ultralytics import YOLO

def list_model_classes(model_weights_path):
    model = YOLO(model_weights_path)
    class_names = model.model.names
    print("Available Classes:", class_names)    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='List Classes in YOLO Model')
    parser.add_argument('--model_weights', required=True, help='Path to the model weights file')
    args = parser.parse_args()

    list_model_classes(args.model_weights)
