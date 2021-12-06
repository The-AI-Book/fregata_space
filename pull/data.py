from dataset import Dataset
import ee
import geemap
from dates import generate_last_dates, generate_days_between
from typing import List 

##############################
## Generate HTML timeseries ##
##############################
def load_satetile_images(m: geemap.Map, dataset: Dataset, start_date = "2021-04-09", end_date = "2021-04-30"):
    """
    This functions loads the image collection of an specific dataset according to the start_date and end_date.
    Additionaly, it extracts the bands specified in the dataset object.
    Finally it adds a new layers to the map that is beign generated.
    """
    collections_data = ee.ImageCollection(dataset.dataset_url) \
              .filterDate(start_date, end_date)
    count = collections_data.size().getInfo()
    img_list = collections_data.toList(count)
    #print("Image list count: ", count)
    combined_img =  ee.ImageCollection(img_list).mosaic()
    #print("Combined image: ")
    #print(combined_img.getInfo())
    vis_parms = dataset.params
    vis_parms["bands"] = dataset.visible_bands
    m.addLayer(combined_img, vis_parms, dataset.dataset_url)
    return m

def generate_timeseries(num_days: int, datasets: List[Dataset], point: List[float], zoom: int, file = "data"):
    """
    Generates a timeseries of images. 
    This images are save locally as html files.
    Input: 
    - num_days: Number of last days you want to consider for the timeseries.
    - datasets: List of Datasets objects that are going to be use to build the timeseries.
    - feature: You can indicate a specific region to generate the timeseries.
    - point: Center of the map
    - zoom: Zoom level
    - file: Name of the file where you want to save the data.
    """
    days = generate_last_dates(num_days = num_days)
    for i in range(len(days) - 1):
        start_date = days[i]
        end_date = days[i + 1]

        # Create a new map.
        m = geemap.Map()
        m.setCenter(point[0], point[1], zoom)

        for dataset in datasets: 
            m = load_satetile_images(m, dataset, start_date = start_date, end_date = end_date)
        #m.to_image(*)
        m.to_html("./{file}/{name}.html".format(file = file, name = start_date))

##############################
##  Get image collections   ##
##############################
def get_image_collection(dataset: Dataset, start_date = '2021-04-1', end_date = '2021-04-30'):
    data = ee.ImageCollection(dataset.dataset_url) \
            .select(dataset.bands) \
            .filterDate(start_date, end_date)
    return data

def get_collection_data(dataset: Dataset, bands: List[str], operations: List[str], renames: List[str], start_date = '2021-04-1', end_date = '2021-04-30'):
    data = get_image_collection(dataset, start_date, end_date)
    return data
    s_data = None
    for i in range(len(operations)):
        band_name = bands[i]
        rename_name = renames[i]
        band_data = data.map(lambda img: img.expression(operations[i], {band_name: img.select(band_name)}).rename(rename_name))
        if s_data == None:
            s_data = band_data
        else: 
            s_data = s_data.combine(band_data)
    return s_data

def get_collections_data(datasets: List[Dataset], start_date = '2021-04-1', end_date = '2021-04-30'):
    collections_data = None
    for dataset in datasets: 
        bands = dataset.bands
        operations = dataset.operations
        renames = dataset.renames
        data = get_collection_data(dataset = dataset, bands = bands, operations = operations, renames = renames, start_date = start_date, end_date = end_date)
        data = data.select(dataset.bands)
        if collections_data == None:
            collections_data = data
        else: 
            collections_data.merge(data)
    return collections_data

################################
##   Download data locally   ###
################################
def download_image_collection(dataset: Dataset, feature: ee.Feature, start_date = "2021-04-29", end_date = "2021-04-30", file: str = "data", with_changes: bool = False):
    """
    This functions returns the image collection of the specified dataset according to the start and end dates entered.
    You can specify where you want to save the data using the parameters 'file'.
    """
    collection = get_image_collection(dataset, start_date=start_date, end_date=end_date)
    roi = feature.geometry()
    if with_changes:
        s_1 = collection.map(lambda img:img.expression('bnd1',{'bnd1':img.select('M5')}).rename('DIF1'))
        s_2 = collection.map(lambda img:img.expression('bnd1-bnd2*0.2',{'bnd1':img.select('I3'),'bnd2':img.select('M2')}).rename('DIF2'))
        s_3 = collection.map(lambda img:img.expression('bnd1',{'bnd1':img.select('M1')}).rename('DIF3'))
        collection=s_1.combine(s_2)
        collection=s_3.combine(collection)
    geemap.ee_export_image_collection(collection, out_dir="{file}".format(file = file), scale = 90, region = roi, file_per_band=True)

#################################
##   Download data to Drive   ###
#################################
def download_collections_to_drive(datasets: List[Dataset], polygon: ee.Geometry.Polygon, start_date = '2021-04-1', end_date = '2021-04-30', drive_folder: str = "data"):
    
    days = generate_days_between(start_date, end_date)
    
    for day_num in range(len(days) - 1):
        start_date = days[day_num]
        end_date = days[day_num + 1]

        for dataset in datasets: 
            print("Dataset scale: ", dataset.scale)
            task_config = {
                "scale": dataset.scale,
                "region": polygon, 
                "folder": drive_folder, 
            }
            collections_data = get_image_collection(dataset, start_date, end_date)
            count = collections_data.size().getInfo()
            img_list = collections_data.toList(count)
            combined_img =  ee.ImageCollection(img_list).mosaic() # Imagen combinada.

            for band in dataset.bands:
                task = ee.batch.Export.image.toDrive(
                    image = combined_img.visualize(
                        min = dataset.params["min"], 
                        max = dataset.params["max"], 
                        bands=[band]
                    ),
                    fileNamePrefix='{dataset}_day_{day_num}_{start_date}_{band}'.format(dataset = dataset.name, day_num = day_num, start_date = start_date, band = band),
                    **task_config)
                task.start()
                print(task.status())