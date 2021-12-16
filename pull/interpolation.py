import numpy as np
from PIL import Image
import io
from base64 import encodebytes

def imagToMat(image):
    img = Image.open(image)
    return np.array(img)

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

def interpolate_images(image1: np.array, image2: np.array, average = False):
    if image1.shape != image2.shape:
        raise Exception("Image must have same shape!")
    alphas = np.linspace(0, 1, 10)
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
        print(new_image[0:10][0:10])
        images.append(Image.fromarray(new_image).convert("RGB"))
    return images

def get_average(image: np.array, i: int, j: int):
    pixel = 0
    for n in [-1, 0, 1]:
        for m in [-1, 0, 1]:
            try:
                pixel += image[i + n][j + m]
            except Exception as e: 
                #print(image[i + n][j + m])
                #print("Exception: ", str(e))
                pass
    return pixel / 9

def max_pooling(image: np.array):
    pass


if __name__ == "__main__":
    
    image1_filepath = "image1.tif"
    image2_filepath = "image2.tif"
    image1 = imagToMat(image1_filepath)
    image2 = imagToMat(image2_filepath)
    artificial_images = interpolate_images(image1, image2, average = False)
    for i in range(len(artificial_images)):
        artificial_images[i].save("./artificial_average/temp{i}.png".format(i = i))
