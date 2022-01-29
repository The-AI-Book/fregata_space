import numpy as np
from PIL import Image
import io
from base64 import encodebytes
from typing import List
from os import listdir
from os.path import isfile, join

def imagToMat(image) -> np.array:
    img = Image.open(image)
    return np.array(img)

def get_response_image(image_path) -> bytes:
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

def interpolate_images(image1: np.ndarray, image2: np.ndarray, step = 10, save_first = True, average = False) -> List[any]:
    if image1.shape != image2.shape:
        raise Exception("Image must have same shape!")
    alphas = np.linspace(0, 1, step)
    alphas = alphas[::-1]
    x_range = image1.shape[0]
    y_range = image2.shape[1]
    images = list()
    
    for alpha in alphas:
        new_image = np.zeros(image1.shape)
        for i in range(x_range):
            for j in range(y_range):
                if not average:
                    new_image[i][j] = alpha * image1[i][j] + (1 - alpha) * image2[i][j]
                else: 
                    new_image[i][j] = alpha * get_average(image1, i, j) + (1 - alpha) * get_average(image2, i, j)
        if (alpha == 0 and save_first) or alpha != 0:
            images.append(Image.fromarray(new_image).convert("L"))
    return images

def get_average(image: np.array, i: int, j: int):
    pixel = 0
    counter = 0
    for n in [-1, 0, 1]:
        for m in [-1, 0, 1]:
            try:
                pixel += image[i + n][j + m]
                counter += 1
            except Exception as e: 
                #print(image[i + n][j + m])
                #print("Exception: ", str(e))
                pass
    return pixel / counter

def interpolate_set_images(data_folder = "data/piro", save_folder = "data/interpolation", step = 10, average = False):
    datapiro = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    images: List[np.array] = list()
    for file in datapiro:
        #print(file)
        image = imagToMat(data_folder + "/" + file)
        images.append(image)

    for i in range(len(images) - 2):
        image1 = images[i]
        image2 = images[i + 1]

        #Image.fromarray(image1).convert("L").save("data/interpolation/1.png")
        #Image.fromarray(image2).convert("L").save("data/interpolation/2.png")
        #sys.exit()

        save_first = False
        if i == 0: save_first = True
        #import sys
        #sys.exit()
        interpolation_images = interpolate_images(image1, image2, step = step, save_first = save_first, average = average)
        #import sys
        #sys.exit()
        j = i * step
        for interpolation_image in interpolation_images:    
            interpolation_image.save("{save_folder}/temp{j}.png".format(save_folder = save_folder, j = j))
            j += 1
        #print("-----")
        #sys.exit()


if __name__ == "__main__":
    
    """
    image1_filepath = "image1.tif"
    image2_filepath = "image2.tif"
    image1 = imagToMat(image1_filepath)
    image2 = imagToMat(image2_filepath)
    artificial_images = interpolate_images(image1, image2, average = False)
    for i in range(len(artificial_images)):
        artificial_images[i].save("./artificial_average/temp{i}.png".format(i = i))
    """
    interpolate_set_images(data_folder="data/piro", save_folder = "data/interpolation", average = False)
