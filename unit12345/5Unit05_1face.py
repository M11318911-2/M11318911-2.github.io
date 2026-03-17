#5Unit05_1face.py
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Create a FaceDetector object.
base_options = python.BaseOptions(model_asset_path='models/detector.tflite')
options = vision.FaceDetectorOptions(base_options=base_options,
                                     min_detection_confidence=0.5)
detector = vision.FaceDetector.create_from_options(options)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    
    # Convert the image to RGB
    img = cv2.resize(image, (640, 480)) # Resize for consistent performance/display
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Create MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgrgb)
    
    # Run face detection
    detection_result = detector.detect(mp_image)
    
    # Draw detections
    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = (bbox.origin_x, bbox.origin_y)
        end_point = (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 3)
        
        # Draw keypoints
        # (Right eye, Left eye, Nose tip, Mouth center, Right ear tragus, Left ear tragus)
        for keypoint in detection.keypoints:
            # keypoints are normalized [0.0, 1.0] relative to the image size
            idx = int(keypoint.x * img.shape[1])
            idy = int(keypoint.y * img.shape[0])
            cv2.circle(img, (idx, idy), 5, (0, 0, 255), -1)

    cv2.imshow('Unit05_1 | StudentID |face', img)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
detector.close()
cv2.destroyAllWindows()