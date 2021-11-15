import ee
import geemap
from typing import List
from dataset import Dataset, viirs1, modis_006_mcd43a4
from dates import generate_dates

# Initialize google earth engine.
ee.Authenticate()
ee.Initialize()

def load_satetile_images(m, dataset: Dataset, start_date = "2021-04-09", end_date = "2021-04-30"):

    data = ee.ImageCollection(dataset.dataset_url) \
              .filterDate(start_date, end_date)
    image = data.toBands()
    #m.addLayer(image, {}, "Time series {name}".format(name = dataset.dataset_url), False)
    labels = data.aggregate_array("system:index").getInfo()
    vis_parms = dataset.get_conf_map(start_date)
    m.addLayer(image, vis_parms, dataset.dataset_url)
    #m.add_time_slider(data, rgbVis, labels=labels, time_interval=1)
    return m

def generate_timeseries(num_days: int, datasets: List[Dataset], point: List[float], zoom: int):
    days = generate_dates(num_days = num_days)
    for i in range(len(days) - 1):
        start_date = days[i]
        end_date = days[i + 1]

        # Create a new map.
        m = geemap.Map()
        m.setCenter(point[0], point[1], zoom)

        for dataset in datasets: 
            m = load_satetile_images(m, dataset, start_date = start_date, end_date = end_date)
        m.to_html("./data/{name}.html".format(name = start_date))

def downloadImageCollection(dataset: Dataset, start_date = "2021-04-09", end_date = "2021-04-30"):
    loc = ee.Geometry.Point(-99.2222, 46.7816)
    polygon = ee.Geometry.BBox(-121.55, 39.01, -120.57, 39.38)
    data = ee.ImageCollection(dataset.dataset_url) \
              .select(dataset.bands) \
              .filterDate(start_date, end_date) \
              
    geemap.ee_export_image_collection(data, out_dir="./images")

if __name__ == '__main__':
    datasets = [viirs1, modis_006_mcd43a4]
    point = [61.2006, 13.3027]
    zoom = 2
    num_days = 30
    generate_timeseries(num_days, datasets, point, zoom)
    #downloadImageCollection(viirs1)