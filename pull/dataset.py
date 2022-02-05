from typing import List
class Dataset:
  def __init__(self, name: str, dataset_url: str, bands: List[str], visible_bands: List[str], params: map, url: str, time_frequency: str, scale: int = 1000,
               operations: List[str] = None, renames: List[str] = None):
    self.name = name
    self.dataset_url = dataset_url
    self.bands = bands
    self.visible_bands = visible_bands
    self.params = params
    self.url = url
    self.time_frequency = time_frequency
    self.scale = scale
    self.operations = operations
    self.renames = renames

  def get_conf_map(self, start_date):
    new_bands = []
    for value in self.bands:
      new_bands.append(start_date.replace("-", "_") + "_" + value)
    self.params["bands"] = new_bands
    return self.params


# Red, 
# Near Infra Red
# T4 (10.3 - 11.3 um)
# T5 (11.5 - 12.5 um)
noaa_cdr_gridsat_b1 = Dataset(name = "noaa_cdr_gridsat_b1", 
                              dataset_url = "NOAA/CDR/GRIDSAT-B1/V2",
                              bands = ['irwin_cdr'], 
                              visible_bands = ['irwin_cdr', 'vschn', 'irwvp'],
                              params = {"min": 200.0, "max": 4000.0}, 
                              url = "https://developers.google.com/earth-engine/datasets/catalog/NOAA_CDR_GRIDSAT-B1_V2?hl=en#description", 
                              time_frequency = "daily", 
                              operations=["M5", "I3-M2", "M1"],
                              renames = ["DIF1", "DIF2", "DIF3"], 
                              scale = 1000)

viirs1 = Dataset(name = "viirs1",
                 dataset_url = "NOAA/VIIRS/001/VNP09GA",
                 bands = ["M5", "M4", "M3"], 
                 visible_bands = ["M5", "M4", "M3"],
                 params = {"min": 0.0, "max": 3000.0}, 
                 url = "https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_001_VNP09GA?hl=en", 
                 time_frequency = "daily", 
                 operations=["M5", "I3-M2", "M1"],
                 renames = ["DIF1", "DIF2", "DIF3"], 
                 scale = 1000)

modis_006_mcd43a4 = Dataset(name = "modis_006_mcd43a4",
                            dataset_url="MODIS/006/MCD43A4", 
                            bands = ["Nadir_Reflectance_Band1", "Nadir_Reflectance_Band4", "Nadir_Reflectance_Band3"], 
                            visible_bands = ["Nadir_Reflectance_Band1", "Nadir_Reflectance_Band4", "Nadir_Reflectance_Band3"], 
                            params = {"min": 0.0, "max": 3000.0}, 
                            url = "https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_001_VNP09GA?hl=en", 
                            time_frequency = "daily")

modis_006_mcd43a3 = Dataset(name = "modis_006_mcd43a3",
                            dataset_url="MODIS/006/MCD43A3", 
                            bands = ["Albedo_BSA_Band1"], 
                            visible_bands = ["Albedo_BSA_Band1"], 
                            params = {"min": 0.0, "max": 400.0}, 
                            url = "https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A3", 
                            time_frequency = "daily"
                            )

copernicus_s2_sr = Dataset(
                          name = "copernicus_s2_sr",
                          dataset_url = "COPERNICUS/S2_SR", 
                          bands = ["B4", "B3", "B2"], 
                          visible_bands = ["B4", "B3", "B2"],
                          params = {"min": 0.0, "max": 0.3},
                          url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR?hl=en", 
                          time_frequency = "daily")              # 4, 8, 11 y 12 , rojo e infrared

landsat_lc08_c02_t1_l2 = Dataset(
                                name = "landsat_lc08_c02_t1_l2",
                                dataset_url = "LANDSAT/LC08/C02/T1_L2", 
                                bands = ["SR_B4", "SR_B3", "SR_B2", "ST_B10", "SR_B5", "SR_B6", "SR_B7"], 
                                visible_bands = ["SR_B4", "SR_B3", "SR_B2"],
                                params = {"min": 0.0, "max": 0.3}, 
                                url = "https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2?hl=en", 
                                time_frequency = "daily")

#############################
###    Copernicus S5P     ###
#############################

# Sentinel-5P Cloud.
copernicus_s5p_offl_l3_cloud = Dataset(name = "copernicus_s5p_offl_l3_cloud",
                                       dataset_url = "COPERNICUS/S5P/OFFL/L3_CLOUD", 
                                       bands = ["cloud_fraction"], 
                                       visible_bands = ["cloud_fraction"], 
                                       params = {"min": 0.0, "max": 0.95, "palette": ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}, 
                                       url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_CLOUD",
                                       time_frequency = "real-time", 
                                       scale = 100)

# Sentinel-5P UV Aerosol Index.
copernicus_s5p_offl_l3_aer_ai = Dataset(name = "copernicus_s5p_offl_l3_aer_ai",
                                        dataset_url = "COPERNICUS/S5P/OFFL/L3_AER_AI", 
                                        bands = ["absorbing_aerosol_index"], 
                                        visible_bands = ["absorbing_aerosol_index"], 
                                        params = {"min": -1, "max": 2.0}, 
                                        url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_AER_AI", 
                                        time_frequency = "real-time", 
                                        scale = 100)

# Sentinel-5P UV Carbon Monoxide.
copernicus_s5p_offl_l3_co = Dataset(name = "copernicus_s5p_offl_l3_co", 
                                    dataset_url="COPERNICUS/S5P/OFFL/L3_CO", 
                                    bands = ["CO_column_number_density"], 
                                    visible_bands = ["CO_column_number_density"], 
                                    params = {"min": 0, "max": 0.05}, 
                                    url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_CO", 
                                    time_frequency="real-time", 
                                    scale = 100)

# Sentinel-5P Formaldehyde.
copernicus_s5p_offl_l3_hcho = Dataset(name = "copernicus_s5p_offl_l3_hcho", 
                                    dataset_url="COPERNICUS/S5P/OFFL/L3_HCHO", 
                                    bands = ["tropospheric_HCHO_column_number_density"], 
                                    visible_bands = ["tropospheric_HCHO_column_number_density"], 
                                    params = {"min": 0.0, "max": 0.0003}, 
                                    url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_HCHO", 
                                    time_frequency="real-time", 
                                    scale = 100)

# Sentinel-5P Nitrogen.
copernicus_s5p_offl_l3_no2 = Dataset(name = "copernicus_s5p_offl_l3_no2", 
                                    dataset_url="COPERNICUS/S5P/OFFL/L3_NO2", 
                                    bands = ["NO2_column_number_density"], 
                                    visible_bands = ["NO2_column_number_density"], 
                                    params = {"min": 0, "max": 0.0002}, 
                                    url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_NO2", 
                                    time_frequency="real-time", 
                                    scale = 100)

# Sentinel-5P Ozone.
copernicus_s5p_offl_l3_o3 = Dataset(name = "copernicus_s5p_offl_l3_o3", 
                                    dataset_url="COPERNICUS/S5P/OFFL/L3_O3", 
                                    bands = ["O3_column_number_density"], 
                                    visible_bands = ["O3_column_number_density"], 
                                    params = {"min": 0.12, "max": 0.15}, 
                                    url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_O3", 
                                    time_frequency="real-time", 
                                    scale = 100)

# Sentinel-5P Sulphur Dioxide
copernicus_s5p_offl_l3_so2 = Dataset(name = "copernicus_s5p_offl_l3_so2", 
                                    dataset_url="COPERNICUS/S5P/OFFL/L3_SO2", 
                                    bands = ["SO2_column_number_density"], 
                                    visible_bands = ["SO2_column_number_density"], 
                                    params = {"min": 0.0, "max": 0.0005}, 
                                    url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_SO2", 
                                    time_frequency="real-time", 
                                    scale = 100)

# Sentinel-5P Methane.
copernicus_s5p_offl_l3_ch4 = Dataset(name = "copernicus_s5p_offl_l3_ch4", 
                                    dataset_url="COPERNICUS/S5P/OFFL/L3_CH4", 
                                    bands = ["CH4_column_volume_mixing_ratio_dry_air"], 
                                    visible_bands = ["CH4_column_volume_mixing_ratio_dry_air"], 
                                    params = {"min": 1750, "max": 1900}, 
                                    url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_CH4", 
                                    time_frequency="real-time", 
                                    scale = 100)

# 
modis_006_mod11a1 = Dataset(name = "modis_006_mod11a1", 
                            dataset_url="MODIS/006/MOD11A1", 
                            bands = ["LST_Day_1km"], 
                            visible_bands=["LST_Day_1km"], 
                            params = {
                              "min": 13000.0,
                              "max": 16500.0,
                            }, 
                            url = "https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD11A1?hl=en#description", 
                            time_frequency="daily", 
                            scale=1000)

if __name__ == "__main__":
   print("Available datasets: ")