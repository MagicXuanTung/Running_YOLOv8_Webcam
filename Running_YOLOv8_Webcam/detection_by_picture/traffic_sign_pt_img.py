from ultralytics import YOLO
import cv2
import os

# Directory containing the images for detection
image_directory = "./Running_YOLOv8_Webcam/detection_by_picture/input_images_traffic_sign"

# Set desired frame size
frame_width = 800
frame_height = 600

# Create a window and set its size
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", frame_width, frame_height)

# Initialize the YOLO model
model = YOLO("../YOLO-Weights/traffic_signs.pt")

class_dict = {
    0: 'bus_stop', 1: 'do_not_enter', 2: 'do_not_stop', 3: 'do_not_turn_l', 4: 'do_not_turn_r', 5: 'do_not_u_turn',
    6: 'enter_left_lane', 7: 'green_light', 8: 'left_right_lane', 9: 'no_parking', 10: 'parking', 11: 'ped_crossing',
    12: 'ped_zebra_cross', 13: 'railway_crossing', 14: 'red_light', 15: 'stop', 16: 't_intersection_l',
    17: 'traffic_light', 18: 'u_turn', 19: 'warning', 20: 'yellow_light'
}

# Loop through all images in the directory
for image_filename in os.listdir(image_directory):
    image_path = os.path.join(image_directory, image_filename)
    img = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if img is None:
        print(f"Error: Unable to read the image from the path '{image_path}'.")
        continue

    # Run YOLO on the image
    results = model(img)

    # Draw bounding boxes and display confidence for each detection
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = round(float(box.conf[0]), 2)
            cls = int(box.cls[0])
            class_name = class_dict[cls]
            label = f'{class_name} {conf}'

            # Draw bounding box
            color = (255, 0, 255)  # Magenta color
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

            # Draw text with confidence using the same color
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    # Display the image with bounding boxes and confidence
    cv2.imshow("Image", img)
    cv2.waitKey(0)

cv2.destroyAllWindows()