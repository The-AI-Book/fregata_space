from interpolation import interpolate_set_images
from detection import get_clouds_image, get_infrared_filter_by_clouds
from resize import resize_images

if __name__ == "__main__":
    """
    get_clouds_image(
        data_folder = "./data/", 
        results_folder="./clouds/"
    )
    get_infrared_filter_by_clouds(
        threshold=232, 
        padding = 0, 
        data_folder="./data/", 
        clouds_folder="./clouds/", 
        results_folder="./pyrocumulus/"
    )
    resize_images(
        dimension = 512, 
        data_folder = "./pyrocumulus/", 
        save_folder = "./resize/"
    )
    """
    interpolate_set_images(
        data_folder = "./resize/", 
        save_folder = "./interpolation/"
    )