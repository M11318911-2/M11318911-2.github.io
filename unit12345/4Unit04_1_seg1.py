#4Unit04_1_seg1.py
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

bgb = np.zeros([300,520,3], np.uint8)                        #black background
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    img = cv2.resize(image,(520,300))                        # resize image to 520x300
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

    # In summary, this code's purpose is to create a condition or
    # boolean mask (condition) that checks whether the values in results.segmentation_mask
    # are greater than 0.1. This condition can be used for various purposes, such as filtering
    # or selecting elements that meet this specific threshold in your data.
    output_image = np.where(condition, img, bgb)
    # create an output_image that combines elements from two input arrays (img and bgb)
    # based on the condition. Where the condition is met, you get the corresponding pixel from img,
    # and where it's not met, you get the corresponding pixel from bgb.
    cv2.imshow('Unit04_1 | StudentID |original', img)
    cv2.imshow('Unit04_1 | StudentID |selfie_segmentation1', output_image)
    if cv2.waitKey(5)  & 0xFF == 27:
        break
cap.release()
segmenter.close()
cv2.destroyAllWindows()