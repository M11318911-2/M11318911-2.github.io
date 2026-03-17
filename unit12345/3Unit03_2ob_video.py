#3Unit03_2ob_video.py
import cv2
import mediapipe as mp

base_options = mp.tasks.BaseOptions('models/efficientdet_lite0.tflite')
options = mp.tasks.vision.ObjectDetectorOptions(base_options, score_threshold=0.2)
detector = mp.tasks.vision.ObjectDetector.create_from_options(options)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    image = cv2.resize(image, (800, 480))
    image_mp = mp.Image(mp.ImageFormat.SRGB, image)  # prepare image for mediapipe
    detection_result = detector.detect(image_mp)  # send image_mp to detector

    for detection in detection_result.detections:
      bbox = detection.bounding_box
      cv2.rectangle(image, (bbox.origin_x, bbox.origin_y),
                    (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height), (255, 0, 0), 2)
      category = detection.categories[0]
      result_text = category.category_name + ' (' + str(round(category.score, 2)) + ')'
      cv2.putText(image, result_text, (10 + bbox.origin_x, 20 + bbox.origin_y),
                  1, 1, (255, 0, 0), 1)
    cv2.imshow('Unit03_2 | StudentID |', image)
    if cv2.waitKey(1) & 0xFF == 27:
       break

cap.release()
cv2.destroyAllWindows()