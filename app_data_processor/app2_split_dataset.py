import os
import shutil
import random


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

crop_dir = os.path.join(ROOT_DIR, '22_crop')
# Check crop dir
if not os.path.exists(crop_dir):
    print('No crop dir')
    exit()

output_dir              = os.path.join(ROOT_DIR, '31_splitted')
dataset_name            = 'cloth6k'
train_dir               = os.path.join(output_dir, 'train_source')
val_source_dir          = os.path.join(output_dir, 'val_source')
visual_test_source_dir  = os.path.join(output_dir, 'visual_test_source')
eval_source_dir         = os.path.join(output_dir, 'eval_source')

# Create directories
dirs = [train_dir, val_source_dir, visual_test_source_dir, eval_source_dir]
for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)


# Read image list in crop/
img_list = os.listdir(crop_dir)
if len(img_list) == 0:
    print('No image in crop dir')
    # Get splitted image list
    val_img_list    = os.listdir(val_source_dir)
    test_img_list   = os.listdir(visual_test_source_dir)
    train_img_list  = os.listdir(train_dir)

    # Move images back to crop dir
    for img_name in val_img_list:
        shutil.move(os.path.join(val_source_dir, img_name), os.path.join(crop_dir, img_name))
        os.remove(os.path.join(eval_source_dir, img_name))
    for img_name in test_img_list:
        shutil.move(os.path.join(visual_test_source_dir, img_name), os.path.join(crop_dir, img_name))
    for img_name in train_img_list:
        shutil.move(os.path.join(train_dir, img_name), os.path.join(crop_dir, img_name))

    print('Move back done')

else:
    # Split the image list: val_num for val and eval, test_num for visual_test, the rest for train
    val_num = 1200
    test_num = 0
    if len(img_list) < val_num + test_num:
        print('Not enough images')
        exit()
    # fix random seed
    random.seed(0)
    random.shuffle(img_list)
    val_img_list    = img_list[:val_num]
    test_img_list   = img_list[val_num:val_num+test_num]
    train_img_list  = img_list[val_num+test_num:]

    # Move images to correspoining directories
    for img_name in val_img_list:
        shutil.move(os.path.join(crop_dir, img_name), os.path.join(val_source_dir, img_name))
        shutil.copy(os.path.join(val_source_dir, img_name), os.path.join(eval_source_dir, img_name))
    for img_name in test_img_list:
        shutil.move(os.path.join(crop_dir, img_name), os.path.join(visual_test_source_dir, img_name))
    for img_name in train_img_list:
        shutil.move(os.path.join(crop_dir, img_name), os.path.join(train_dir, img_name))

    print('Split done')