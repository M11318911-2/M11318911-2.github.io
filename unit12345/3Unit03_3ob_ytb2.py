#3Unit03_3ob_ytb2.py
import cv2
import yt_dlp
import mediapipe as mp

base_options = mp.tasks.BaseOptions('models/efficientdet_lite0.tflite')
options = mp.tasks.vision.ObjectDetectorOptions(base_options, score_threshold=0.2)
detector = mp.tasks.vision.ObjectDetector.create_from_options(options)
video_url1 = "https://www.youtube.com/watch?v=OkQ0utdxwBY"
video_url = "https://www.youtube.com/watch?v=xr-vlbxXlUA"
ydl_opts = {'format': 'best',  'quiet': True }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(video_url, download=False)
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict1 = ydl.extract_info(video_url1, download=False)
stream_url = info_dict['url']
stream_url1 = info_dict1['url']

cap = cv2.VideoCapture(stream_url)
cap1 = cv2.VideoCapture(stream_url1)
while cap.isOpened():
    success, image = cap.read()
    success, image1 = cap1.read()
    image = cv2.resize(image, (600, 360))
    image1 = cv2.resize(image1, (600, 360))
    image_mp = mp.Image(mp.ImageFormat.SRGB, image)  # prepare image for mediapipe
    detection_result = detector.detect(image_mp)  # send image_mp to detector
    image_mp1 = mp.Image(mp.ImageFormat.SRGB, image1)  # prepare image for mediapipe
    detection_result1 = detector.detect(image_mp1)  # send image_mp to detector
    for detection in detection_result.detections:
      bbox = detection.bounding_box
      cv2.rectangle(image, (bbox.origin_x, bbox.origin_y),
                    (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height), (100, 200, 0), 1)
      category = detection.categories[0]
      result_text = category.category_name + ' (' + str(round(category.score, 2)) + ')'
      cv2.putText(image, result_text, (10 + bbox.origin_x, 20 + bbox.origin_y),
                  1, 1, (255, 255, 255), 1)
    cv2.imshow('Unit03_31 | StudentID |', image)

    for detection in detection_result1.detections:
      bbox = detection.bounding_box
      cv2.rectangle(image1, (bbox.origin_x, bbox.origin_y),
                    (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height), (10, 200, 0), 1)
      category = detection.categories[0]
      result_text = category.category_name + ' (' + str(round(category.score, 2)) + ')'
      cv2.putText(image1, result_text, (10 + bbox.origin_x, 20 + bbox.origin_y),
                  1, 1, (255, 255, 255), 1)
    cv2.imshow('Unit03_32 | StudentID |', image1)
    if cv2.waitKey(1) & 0xFF == 27:
       break

cap.release()
cv2.destroyAllWindows()