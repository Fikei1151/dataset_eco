import os
import cv2
import numpy as np

def sharpen_image(image):
    # Apply sharpening using a kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image

def process_folder(image_folder, output_image_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_image_folder, exist_ok=True)

    # Iterate over all image files (supports jpg, jpeg, JPG, JPEG)
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
    
    for image_file in image_files:
        # Read the image
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)

        if image is not None:
            # Sharpen image
            sharpened_image = sharpen_image(image)

            # Save the sharpened image to the output folder
            output_image_path = os.path.join(output_image_folder, image_file)
            cv2.imwrite(output_image_path, sharpened_image)
        else:
            print(f"Failed to load image {image_file}")


image_folder = 'train_data/YOLO/images'
output_image_folder = '/Users/fikreehajiyusof/dataset_eco/enhanced_images'

process_folder(image_folder, output_image_folder)
