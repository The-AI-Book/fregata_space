from typing import List
class Dataset:
  def __init__(self, dataset_url: str, bands: List[str], params: map, url: str, time_frequency: str):
    self.dataset_url = dataset_url
    self.bands = bands
    self.params = params
    self.url = url
    self.time_frequency = time_frequency

  def get_conf_map(self, start_date):
    new_bands = []
    for value in self.bands:
      new_bands.append(start_date.replace("-", "_") + "_" + value)
    self.params["bands"] = new_bands
    return self.params

viirs1 = Dataset(dataset_url = "NOAA/VIIRS/001/VNP09GA",
                 bands = ["M5", "M4", "M3"], 
                 params = {"min": 0.0, "max": 3000.0}, 
                 url = "https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_001_VNP09GA?hl=en", 
                 time_frequency = "daily")

modis_006_mcd43a4 = Dataset(dataset_url="MODIS/006/MCD43A4", 
                            bands = ["Nadir_Reflectance_Band1", "Nadir_Reflectance_Band4", "Nadir_Reflectance_Band3"], 
                            params = {"min": 0.0, "max": 3000.0}, 
                            url = "https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_001_VNP09GA?hl=en", 
                            time_frequency = "daily")

modis_006_mcd43a3 = Dataset(dataset_url="MODIS/006/MCD43A3", 
                            bands = ["Albedo_BSA_Band1"], 
                            params = {"min": 0.0, "max": 400.0}, 
                            url = "https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A3", 
                            time_frequency = "daily"
                            )

copernicus_s5p_offl_l3_cloud = Dataset(dataset_url = "COPERNICUS/S5P/OFFL/L3_CLOUD", 
                                       bands = ["cloud_fraction"], 
                                       params = {"min": 0.0, "max": 0.95, "palette": ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}, 
                                       url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_CLOUD",
                                       time_frequency = "real-time")