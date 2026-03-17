#4Unit04_2_seg2.py
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Create an ImageSegmenter object.
base_options = python.BaseOptions(model_asset_path='models/selfie_segmenter.tflite')
options = vision.ImageSegmenterOptions(base_options=base_options,
                                       output_category_mask=True)
segmenter = vision.ImageSegmenter.create_from_options(options)

bgb = np.zeros([300,520,3], np.uint8)
bgc = cv2.imread('pic/bgc.jpg')
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
    # True if background (0), False if person (1)
    condition = np.stack((mask_np,) * 3, axis=-1) < 0.5 

    output_image = np.where(condition, img, bgb)
    output_image2 = np.where(condition, img, bgc)
    cv2.imshow('Unit04_2| StudentID |original', img)
    cv2.imshow('Unit04_2| StudentID |originalblack', output_image)
    cv2.imshow('Unit04_2| StudentID |originalcolor', output_image2)
    if cv2.waitKey(5)  & 0xFF == 27:
        break
cap.release()
segmenter.close()
cv2.destroyAllWindows()