#5Unit05_2face2.py
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
    
    w, h = (img.shape[1], img.shape[0])
    
    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = (bbox.origin_x, bbox.origin_y)
        end_point = (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 3)

        # Eye logic
        # keypoints[0] is right eye (from observer perspective, or left on face?), 
        # actually docs say: 0: left eye, 1: right eye, 2: nose tip, 3: mouth center, 4: right ear tragus, 5: left ear tragus.
        # But in mirror mode/selfie, let's just stick to 0 and 1.
        
        # Legacy code: relative_keypoints[0] -> a, relative_keypoints[1] -> b
        # New API: detection.keypoints[0] -> left eye, detection.keypoints[1] -> right eye
        
        kp0 = detection.keypoints[0]
        kp1 = detection.keypoints[1]
        
        # Calculate eye size based on bounding box width (similar to logic: s.width * w * 0.1)
        # bbox.width is in pixels now!
        eye = int(bbox.width * 0.1)

        ax, ay = int(kp0.x * w), int(kp0.y * h)
        bx, by = int(kp1.x * w), int(kp1.y * h)
        
        # Draw cartoon eyes
        cv2.circle(img, (ax, ay), (eye + 10), (255, 255, 255), -1)  # draw left eye (white)
        cv2.circle(img, (bx, by), (eye + 10), (255, 255, 0), -1)    # draw right eye (white)
        cv2.circle(img, (ax, ay), eye, (0, 0, 0), -1)               # draw left eye (black)
        cv2.circle(img, (bx, by), eye, (0, 0, 0), -1)               # draw right eye (black)
        
        # Draw other keypoints
        for keypoint in detection.keypoints[2:]: # nose, mouth, ears
             idx = int(keypoint.x * w)
             idy = int(keypoint.y * h)
             cv2.circle(img, (idx, idy), 5, (0, 0, 255), -1)

    cv2.imshow('Unit05_2 | StudentID |face2', img)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
detector.close()
cv2.destroyAllWindows()