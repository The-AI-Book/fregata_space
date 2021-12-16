
import ee
import geemap
from typing import List
from dataset import viirs1, copernicus_s5p_offl_l3_cloud, copernicus_s5p_offl_l3_aer_ai, copernicus_s5p_offl_l3_co, copernicus_s2_sr, landsat_lc08_c02_t1_l2
from dataset import modis_006_mod11a1
from data import generate_daily_timeseries, download_collections_to_drive

# Initialize google earth engine.
ee.Authenticate()
ee.Initialize()

if __name__ == '__main__':
    #datasets = [viirs1, modis_006_mcd43a4]
    #datasets = [copernicus_s2_sr, landsat_lc08_c02_t1_l2]
    point = [61.2006, 13.3027]
    zoom = 2
    num_days = 3
    datasets = [copernicus_s5p_offl_l3_cloud]
    geom = ee.Geometry.Polygon([[
            [-18.10375181457037,28.415547083183785],
            [-17.50499693175787,28.415547083183785],
            [-17.50499693175787,28.907193367603675],
            [-18.10375181457037,28.907193367603675],
            [-18.10375181457037,28.415547083183785]
        ]])
    feature = ee.Feature(geom, {})
    #ataset: Dataset, feature: ee.Feature, start_date = "2021-04-01", end_date = "2021-04-30", file: str = "data"
    #download_image_collection_2(viirs1, feature, file = "./data/data7")
    
    # download_collections(datasets, feature, file = "./data/data8")
    #generate_timeseries(num_days, datasets, feature, point, zoom, file = "data")
    #downloadImageCollection(viirs1)
    #downloadImage()
    #test_images()
    datasets = [viirs1]

    square = ee.Geometry.Polygon(
        [[[-63.846874469110226, 14.789676135536729],
          [-63.846874469110226, 11.301164527965645],
          [-58.683300250360226, 11.301164527965645],
          [-58.683300250360226, 14.789676135536729]]], None, False)
    #download_collections_to_drive(viirs1, square, drive_folder = "data5_juan")
    #download_collections_to_drive(copernicus_s5p_offl_l3_cloud, square, drive_folder="data_clouds", start_date="2021-04-1", end_date = "2021-04-30")
    #datasets=[copernicus_s5p_offl_l3_cloud, copernicus_s5p_offl_l3_aer_ai, copernicus_s5p_offl_l3_co]
    #datasets=[landsat_lc08_c02_t1_l2]
    datasets = [viirs1, copernicus_s5p_offl_l3_cloud]
    datasets = [modis_006_mod11a1]
    generate_daily_timeseries(20, datasets=datasets, point = [0, 0], zoom = 2, file = "data/data9")
    
    #download_collections_to_drive(datasets = datasets, polygon=square, start_date="2021-04-01", end_date="2021-04-03", drive_folder="prueba_datasets")