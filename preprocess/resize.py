from PIL import Image
from os import listdir
from os.path import isfile, join

def resize_image(image: Image.Image, dimension: int = 512) -> Image.Image:
    width = image.size[0]
    height = image.size[1]

    start_x = int((width - 512) / 2) 
    start_y = int((height - 512) / 2) 
    end_x = start_x + 512
    end_y = start_y + 512

    box = (start_x, start_y, end_x, end_y)
    cropped_image = image.crop(box)
    return cropped_image
    #cropped_image.save('cropped_image.jpg')

def resize_images(dimension = 512, data_folder = "./data/pyrocumulus", save_folder = "./data/resize"):
    pyrocumulus = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    for i in range(0, len(pyrocumulus)):
        image = Image.open(data_folder + "/" + pyrocumulus[i])
        image = resize_image(image, dimension = dimension)
        image.save(save_folder + "/" + pyrocumulus[i])

if __name__ == "__main__":
    #url = "./data/viirs1_day_2_2019-11-08_M5.tif"
    url = "./data/noaa_cdr_gridsat_b1_day_45_2019-12-21_irwin_cdr.tif"
    image = Image.open(url)
    resize_image(image)  
