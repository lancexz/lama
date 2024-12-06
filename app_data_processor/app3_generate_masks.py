import os
import cv2
import numpy as np
import random
import tqdm
import shutil


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def process_images(data_dir, output_dir, ext='png', crop_size=512, num_mask=1, circle_radius=20):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    ext = f".{ext}"

    # Create a progress bar
    progress = tqdm.tqdm(total=len(filenames:=os.listdir(data_dir)))

    # Iterate over all images in the data directory
    for filename in filenames:
        progress.update(1)

        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(data_dir, filename)
            
            # Read the image
            img = cv2.imread(image_path)
            
            # Get the image dimensions
            height, width, _ = img.shape
            crop_num_w = width // crop_size
            crop_num_h = height // crop_size

            # Calculate the center coordinates and crop size
            step_w = width // (2 * crop_num_w)
            step_h = height // (2 * crop_num_h)
            
            cnt_crop = 0
            # Crop the image
            for i in range(crop_num_w):
                base_name, ext_ = os.path.splitext(filename)

                for j in range(crop_num_h):
                    center_x = step_w + 2 * i * step_w
                    center_y = step_h + 2 * j * step_h
                    half_crop_size = crop_size // 2
                    crop_img = img[center_y - half_crop_size:center_y + half_crop_size, center_x - half_crop_size:center_x + half_crop_size]
                    
                    crop_filename = f"{base_name}_crop00{cnt_crop}{ext}"
                    crop_path = os.path.join(output_dir, crop_filename)
                    cv2.imwrite(crop_path, crop_img)

                    cnt_mask = 0
                    for k in range(num_mask):
                        nx = random.uniform(0.2, 0.8)
                        ny = random.uniform(0.2, 0.8)
                        x = int(nx * crop_size)
                        y = int(ny * crop_size)

                        # Create a circular mask
                        mask = np.zeros((crop_size, crop_size), dtype=np.uint8)
                        cv2.circle(mask, (x, y), circle_radius, 1, -1)
                        
                        # Generate the output filenames
                        mask_filename = f"{base_name}_crop00{cnt_crop}_mask00{cnt_mask}.png"
                        cnt_mask += 1
                
                        # Save the cropped image and mask
                        mask_path = os.path.join(output_dir, mask_filename)
                        cv2.imwrite(mask_path, mask * 255)
                    cnt_crop += 1
            

# Set paths
datapath = os.path.join(ROOT_DIR, "31_splitted")
folder_names = ["val", "eval", "train", "visual_test"] 
data_path = '/home/user/ws/data'
dataset_name = "cloth6k"

for folder_name in folder_names:
    input_directory = os.path.join(datapath, folder_name+"_source")
    output_directory = os.path.join(data_path, "lama", "trainingset", dataset_name, folder_name)
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    if folder_name != "train":
        process_images(input_directory, output_directory)
    else:
        process_images(input_directory, output_directory, ext="jpg", num_mask=0)    # training does not need masks