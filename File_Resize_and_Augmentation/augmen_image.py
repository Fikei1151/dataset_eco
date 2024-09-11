import os
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import random

# กำหนดเส้นทางที่เก็บรูปภาพเดิมและที่เก็บรูปภาพใหม่
imgs_source_folder = './imgs/'  # โฟลเดอร์ที่เก็บไฟล์ imgs
imgs_destination_folder = './augm_imgs/'  # โฟลเดอร์ที่ต้องการเซฟไฟล์ imgs ใหม่

masks_source_folder = './masks/'  # โฟลเดอร์ที่เก็บไฟล์ masks
masks_destination_folder = './augm_masks/'  # โฟลเดอร์ที่ต้องการเซฟไฟล์ masks ใหม่

# ตรวจสอบให้แน่ใจว่าโฟลเดอร์ปลายทางมีอยู่แล้ว
if not os.path.exists(imgs_destination_folder):
    os.makedirs(imgs_destination_folder)
if not os.path.exists(masks_destination_folder):
    os.makedirs(masks_destination_folder)

# ฟังก์ชันเพิ่มจุดสีขาว
def add_white_spots(img):
    np_img = np.array(img)
    num_spots = int(np_img.size * 0.01)  # จำนวนจุดที่ต้องการเพิ่ม (1% ของพิกเซลทั้งหมด)
    
    for _ in range(num_spots):
        x = random.randint(0, np_img.shape[1] - 1)
        y = random.randint(0, np_img.shape[0] - 1)
        np_img[y, x] = [255, 255, 255]  # เพิ่มจุดสีขาว
    
    return Image.fromarray(np_img)

# ฟังก์ชันเพิ่มจุดสีดำ
def add_black_spots(img):
    np_img = np.array(img)
    num_spots = int(np_img.size * 0.01)  # จำนวนจุดที่ต้องการเพิ่ม (1% ของพิกเซลทั้งหมด)
    
    for _ in range(num_spots):
        x = random.randint(0, np_img.shape[1] - 1)
        y = random.randint(0, np_img.shape[0] - 1)
        np_img[y, x] = [0, 0, 0]  # เพิ่มจุดสีดำ
    
    return Image.fromarray(np_img)

# ฟังก์ชันเพิ่มทั้งจุดสีขาวและดำ
def add_white_and_black_spots(img):
    np_img = np.array(img)
    num_spots = int(np_img.size * 0.01)  # จำนวนจุดที่ต้องการเพิ่ม (1% ของพิกเซลทั้งหมด)
    
    for _ in range(num_spots):
        x = random.randint(0, np_img.shape[1] - 1)
        y = random.randint(0, np_img.shape[0] - 1)
        if random.choice([True, False]):
            np_img[y, x] = [255, 255, 255]  # เพิ่มจุดสีขาว
        else:
            np_img[y, x] = [0, 0, 0]  # เพิ่มจุดสีดำ
    
    return Image.fromarray(np_img)

# ฟังก์ชันทำ augmentation สำหรับโฟลเดอร์ใดโฟลเดอร์หนึ่ง
def augment_images(source_folder, destination_folder, do_noise_and_blur=True):
    files = [f for f in sorted(os.listdir(source_folder)) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # วนลูปไฟล์ทั้งหมดที่พบ
    for idx, file_name in enumerate(files, start=1):
        file_path = os.path.join(source_folder, file_name)
        img = Image.open(file_path)

        # แยกชื่อไฟล์และนามสกุล
        name, ext = os.path.splitext(file_name)

        # 1. กลับหัวรูปภาพ (flip vertically)
        flipped_img = ImageOps.flip(img)
        flipped_img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 1).zfill(3)}{ext}"))

        # 2. เอียงขวา (rotate right)
        rotated_right_img = img.rotate(-90, expand=True)
        rotated_right_img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 2).zfill(3)}{ext}"))

        # 3. เอียงซ้าย (rotate left)
        rotated_left_img = img.rotate(90, expand=True)
        rotated_left_img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 3).zfill(3)}{ext}"))

        # ถ้าอนุญาตให้ทำ noise และ blur
        if do_noise_and_blur:
            # 4. เพิ่มจุดสีขาว (add white spots)
            white_spots_img = add_white_spots(img)
            white_spots_img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 4).zfill(3)}{ext}"))

            # 5. เพิ่มจุดสีดำ (add black spots)
            black_spots_img = add_black_spots(img)
            black_spots_img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 5).zfill(3)}{ext}"))

            # 6. เพิ่มทั้งจุดสีขาวและสีดำ (add white and black spots)
            white_black_spots_img = add_white_and_black_spots(img)
            white_black_spots_img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 6).zfill(3)}{ext}"))

            # 7. ทำการเบลอ (blur)
            blurred_img = img.filter(ImageFilter.GaussianBlur(radius=2))
            blurred_img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 7).zfill(3)}{ext}"))
        else:
            # 4. บันทึกภาพปกติแทนการทำ noise
            img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 4).zfill(3)}{ext}"))
            
            # 5. บันทึกภาพปกติแทนการเพิ่ม noise สีดำ
            img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 5).zfill(3)}{ext}"))

            # 6. บันทึกภาพปกติแทนการเพิ่ม noise ทั้งสีขาวและสีดำ
            img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 6).zfill(3)}{ext}"))

            # 7. บันทึกภาพปกติแทนการเบลอ
            img.save(os.path.join(destination_folder, f"{str(100 + (idx-1) * 7 + 7).zfill(3)}{ext}"))

# เรียกใช้ฟังก์ชันสำหรับ imgs (ทำ noise และ blur)
augment_images(imgs_source_folder, imgs_destination_folder, do_noise_and_blur=True)

# เรียกใช้ฟังก์ชันสำหรับ masks (ไม่ทำ noise และ blur)
augment_images(masks_source_folder, masks_destination_folder, do_noise_and_blur=False)

print("การทำ augmentation และบันทึกไฟล์เสร็จสมบูรณ์!")
