import os
import cv2
import numpy as np


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class MaskExtractor:
    def __init__(self):
        pass

    def binarize_img(self, masked_img):
        # ----------- binarize the image -----------
        # equalized_img = cv2.equalizeHist(masked_img)
        blurred = cv2.GaussianBlur(masked_img, (9, 9), 0)

        im_bn = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

        # Apply morphological operations to remove small noise
        kernel = np.ones((5, 5), np.uint8)
        im_bn = cv2.morphologyEx(im_bn, cv2.MORPH_OPEN, kernel)
        im_bn = cv2.morphologyEx(im_bn, cv2.MORPH_CLOSE, kernel)

        # denoise the outlier
        im_bn = cv2.medianBlur(im_bn, 9)

        return im_bn
    

    def process_images(self, data_dir, mask_dir):
        # Create the mask directory if it doesn't exist
        os.makedirs(mask_dir, exist_ok=True)

        import tqdm
        # Create a progress bar
        progress = tqdm.tqdm(total=len(os.listdir(data_dir)))

        # Iterate over all images in the data directory
        for filename in os.listdir(data_dir):
            progress.update(1)

            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(data_dir, filename)

                img_src = cv2.imread(image_path)
                
                # Read the image in grayscale
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                
                # Extract the mask
                mask = self.binarize_img(img)

                # # calculate a center of mass
                # M = cv2.moments(mask)
                # cX = int(M["m10"] / M["m00"])
                # cY = int(M["m01"] / M["m00"])
                # width = 1024
                # height = 1024
                
                # img_crop = img_src[cY - height // 2:cY + height // 2, cX - width // 2:cX + width // 2]
                
                # Save the mask with the same filename in the mask directory
                mask_path = os.path.join(mask_dir, filename)
                cv2.imwrite(mask_path, mask)
                # if img_crop is not None:
                #     cv2.imwrite(mask_path, img_crop)
                # else:
                #     print(f"Error: {filename}")


    def crop_images(self, data_dir, mask_dir, crop_dir, width=1024, height=1024):
        # Create the crop directory if it doesn't exist
        os.makedirs(crop_dir, exist_ok=True)

        # Create a progress bar
        import tqdm
        progress = tqdm.tqdm(total=len(img_list := os.listdir(data_dir)))

        # Iterate over all images in the data directory
        for filename in img_list:
            progress.update(1)
            # skip file if it exist in the crop directory
            if os.path.exists(os.path.join(crop_dir, filename)):
                continue

            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(data_dir, filename)
                mask_path = os.path.join(mask_dir, filename)

                img_src = cv2.imread(image_path)
                mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
                
                # calculate a center of mass
                M = cv2.moments(mask)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Check if the region of crop is within the image
                if cX < width // 2:
                    cX = width // 2
                if cY < height // 2:
                    cY = height // 2
                if cX > img_src.shape[1] - width // 2:
                    cX = img_src.shape[1] - width // 2
                if cY > img_src.shape[0] - height // 2:
                    cY = img_src.shape[0] - height // 2
                
                img_crop = img_src[cY - height // 2:cY + height // 2, cX - width // 2:cX + width // 2]
                
                # Save the mask with the same filename in the mask directory
                crop_path = os.path.join(crop_dir, filename)
                if img_crop is not None:
                    cv2.imwrite(crop_path, img_crop)
                else:
                    print(f"Error: {filename}")
                    exit()

    
import os
extractor = MaskExtractor()

''' image processing for training set '''
data_directory = crop_dir = os.path.join(ROOT_DIR, '11_rgb')
mask_directory = crop_dir = os.path.join(ROOT_DIR, '21_edge')
crop_directory = crop_dir = os.path.join(ROOT_DIR, '22_crop')

''' use the same image processing for testing set '''
# data_directory = "./31_trainingset/visual_test_source/"
# mask_directory = "./31_trainingset/21_edge/"
# crop_directory = "./31_trainingset/22_crop/"


# # Step 1
# extractor.process_images(data_directory, mask_directory)

# Step 2
width = 1024
height = 1024
extractor.crop_images(data_directory, mask_directory, crop_directory, width, height)
