import os
import cv2
import numpy as np

# ฟังก์ชันหมุน bounding box ตามการหมุนของภาพ
def rotate_bbox(image_size, bbox, angle):
    h, w = image_size
    cx, cy, bw, bh = bbox

    if angle == 90:
        new_cx = cy
        new_cy = 1 - cx
    elif angle == 180:
        new_cx = 1 - cx
        new_cy = 1 - cy
    elif angle == 270:
        new_cx = 1 - cy
        new_cy = cx
    else:
        new_cx, new_cy = cx, cy

    # หากหมุน 90 หรือ 270 ต้องสลับความกว้างกับความสูงของ bounding box
    if angle in [90, 270]:
        new_bw, new_bh = bh, bw
    else:
        new_bw, new_bh = bw, bh

    return new_cx, new_cy, new_bw, new_bh

# ฟังก์ชันหมุนภาพ
def rotate_image(image, angle):
    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return image

# ฟังก์ชันแปลงและบันทึกภาพและ label
def augment_image(image_path, label_path, output_image_folder, output_label_folder):
    # สร้างโฟลเดอร์ใหม่หากไม่มี
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_label_folder, exist_ok=True)

    # อ่านภาพ
    image = cv2.imread(image_path)
    original_height, original_width = image.shape[:2]

    # อ่าน label
    with open(label_path, 'r') as f:
        labels = f.readlines()

    # สร้างมุมที่จะหมุน
    angles = [0, 90, 180, 270]

    for angle in angles:
        # หมุนภาพ
        rotated_image = rotate_image(image, angle)
        
        # บันทึกภาพที่หมุน
        image_name = os.path.basename(image_path).split('.')[0] + f'_rot{angle}.jpg'
        rotated_image_path = os.path.join(output_image_folder, image_name)
        cv2.imwrite(rotated_image_path, rotated_image)

        # ปรับ label
        rotated_label_path = os.path.join(output_label_folder, image_name.replace('.jpg', '.txt'))
        with open(rotated_label_path, 'w') as f_out:
            for label in labels:
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, label.split())

                # ตรวจสอบว่าหมุนภาพหรือไม่
                if angle != 0 and class_id in [0, 1, 2]:
                    continue  # ข้ามคลาส 0, 1, 2 ถ้าหมุนภาพ (rot90, rot180, rot270)

                # ปรับ bounding box ตามมุมที่หมุน
                new_x_center, new_y_center, new_bbox_width, new_bbox_height = rotate_bbox(
                    (original_height, original_width), 
                    (x_center, y_center, bbox_width, bbox_height), 
                    angle
                )
                # เขียน label ใหม่ลงไฟล์
                f_out.write(f"{int(class_id)} {new_x_center} {new_y_center} {new_bbox_width} {new_bbox_height}\n")

# ฟังก์ชันประมวลผลโฟลเดอร์
def process_folder(image_folder, label_folder, output_image_folder, output_label_folder):
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.jpeg')]
    label_files = [f for f in os.listdir(label_folder) if f.endswith('.txt')]

    for image_file, label_file in zip(image_files, label_files):
        image_path = os.path.join(image_folder, image_file)
        label_path = os.path.join(label_folder, label_file)
        
        # แปลงและหมุนภาพ
        augment_image(image_path, label_path, output_image_folder, output_label_folder)

# ตัวอย่างการใช้งาน
image_folder = '/Users/fikreehajiyusof/dataset_eco/Dataset_100'
label_folder = '/Users/fikreehajiyusof/dataset_eco/train_data/YOLO/obj_train_data'
output_image_folder = 'train_data/YOLO/imagesx'
output_label_folder = 'train_data/YOLO/labelsx'

process_folder(image_folder, label_folder, output_image_folder, output_label_folder)
