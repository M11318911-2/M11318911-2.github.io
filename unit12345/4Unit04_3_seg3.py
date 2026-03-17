#4Unit04_3_seg3.py
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

blur=0
prev_time = 0
bg_image = None
BG_COLOR = (255, 255, 0)

# Create an ImageSegmenter object.
base_options = python.BaseOptions(model_asset_path='models/selfie_segmenter.tflite')
options = vision.ImageSegmenterOptions(base_options=base_options,
                                       output_category_mask=True)
segmenter = vision.ImageSegmenter.create_from_options(options)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    img = cv2.resize(image,(520,300))
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Create MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgrgb)
    
    # Run segmentation
    segmentation_result = segmenter.segment(mp_image)
    category_mask = segmentation_result.category_mask
    
    # Convert mask for visualization
    # category_mask is uint8 (0=background, 1=person)
    mask_np = category_mask.numpy_view()
    
    # Ensure mask is 2D (H, W) not (H, W, 1)
    if mask_np.ndim == 3:
        mask_np = mask_np.squeeze(-1)
        
    # Invert condition to swap foreground/background
    # Now: True if background (0), False if person (1)
    condition = np.stack((mask_np,) * 3, axis=-1) < 0.5 

    if bg_image is None:
        bg_image = np.zeros([300,520,3], np.uint8)
        bg_image[:] = BG_COLOR
    else:
        bg_image = cv2.resize(bg_image, (520,300))
        if blur > 0:
            bg_image = cv2.GaussianBlur(bg_image, (55, 55), 0)
            blur = 0
    output_image = np.where(condition, img, bg_image)
    cv2.putText(output_image, f'FPS: {int(1 / (time.time() - prev_time))}'
                ,(3, 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
    prev_time = time.time()
    cv2.imshow("Unit04_3 | StudentID |", output_image)
    keyb = cv2.waitKey(1) & 0xFF
    if  keyb == 27:
        break
    elif keyb == ord('0'):
        bg_image = None
    elif keyb == ord('1'):
        bg_image = cv2.imread('pic/bgc.jpg')
    elif keyb == ord('2'):
        bg_image = cv2.imread('pic/2.png')
    elif keyb == ord('3'):
        bg_image = cv2.imread('pic/3.png')
    elif keyb == ord('b'):
        blur +=1

cap.release()
segmenter.close()
cv2.destroyAllWindows()