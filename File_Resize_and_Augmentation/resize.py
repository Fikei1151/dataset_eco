from PIL import Image
import os

def resize_images_and_masks(img_folder, mask_folder, output_img_folder, output_mask_folder, size=(224, 224)):
    # สร้างโฟลเดอร์เอาต์พุตถ้ายังไม่มี
    if not os.path.exists(output_img_folder):
        os.makedirs(output_img_folder)
    if not os.path.exists(output_mask_folder):
        os.makedirs(output_mask_folder)

    # รีไซส์ภาพ
    for filename in os.listdir(img_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(img_folder, filename)
            img = Image.open(img_path)
            img_resized = img.resize(size, Image.BILINEAR)  # ใช้ Image.BILINEAR เพื่อการปรับขนาดที่ดีขึ้น
            img_resized.save(os.path.join(output_img_folder, filename))

    # รีไซส์ mask
    for filename in os.listdir(mask_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            mask_path = os.path.join(mask_folder, filename)
            mask = Image.open(mask_path)
            mask_resized = mask.resize(size, Image.NEAREST)  # ใช้ Image.NEAREST สำหรับ mask เพื่อรักษาค่าป้าย
            mask_resized.save(os.path.join(output_mask_folder, filename))

    print('เสร็จสิ้น')

def check_matching_size_and_values(img_folder, mask_folder):
    for filename in os.listdir(img_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(img_folder, filename)

            # ตรวจสอบหลายรูปแบบไฟล์ของ mask
            mask_path = None
            for ext in ['.png', '.jpg', '.jpeg']:
                possible_mask_path = os.path.join(mask_folder, filename.split('.')[0] + ext)
                if os.path.exists(possible_mask_path):
                    mask_path = possible_mask_path
                    break

            if mask_path:
                img = Image.open(img_path)
                mask = Image.open(mask_path)

                # ตรวจสอบว่าขนาดของภาพและ mask ตรงกัน
                if img.size != mask.size:
                    print(f"ขนาดไม่ตรงกัน: {filename} (ภาพ: {img.size}, mask: {mask.size})")
                else:
                    print(f"ขนาดตรงกัน: {filename}")

                # ตรวจสอบค่าของพิกเซลที่ตำแหน่งสุ่ม
                img_pixels = img.load()
                mask_pixels = mask.load()

                mismatch_found = False
                for i in range(0, img.size[0], 10):
                    for j in range(0, img.size[1], 10):
                        if img_pixels[i, j] != mask_pixels[i, j]:
                            mismatch_found = True
                            print(f"ค่าพิกเซลไม่ตรงกันที่ตำแหน่ง {(i, j)} ในไฟล์ {filename}")
                            break
                    if mismatch_found:
                        break

                if not mismatch_found:
                    print(f"ค่าพิกเซลตรงกันสำหรับไฟล์ {filename}")
            else:
                print(f"ไม่พบ mask สำหรับไฟล์ {filename}")

# ขนาดที่ต้องการรีไซส์ (width, height)
new_size = (224, 224)

# รีไซส์ภาพและ masks
resize_images_and_masks('./data/imgs/', './data/masks/', './resize_data/imgs/', './resize_data/masks/', new_size)

# ตรวจสอบว่าภาพและ masks มีขนาดและค่าพิกเซลตรงกัน
# check_matching_size_and_values('./resize_data/imgs/', './resize_data/masks/')