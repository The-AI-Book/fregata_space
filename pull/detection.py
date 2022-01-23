import numpy as np
import matplotlib.pyplot as plt
from interpolation import imagToMat
from PIL import Image
from os import listdir
from os.path import isfile, join

def hsi(R,G,B):

  I = (R/3)+(G/3)+(B/3)

  r_6 = np.sqrt(6) #Para no reclcularlo cada ves

  V_1 = ((R/-6)-(G/6)+(B/3))*r_6
  V_2 = ((R)-(G*2))/r_6

  H = np.zeros((len(R),len(R[0])))

  for i in range(len(R)):
    for j in range(len(R[0])):
      if V_1[i][j] != 1:
        H[i][j] = (np.arctan(V_1[i][j]/V_2[i][j]) + np.pi)*(255/(2*np.pi))
      else:
        H[i][j] = -1 #Este valor simbolisa que la entrada no esta definida

  return [H,I] #En la codificacion HSI existe un valor S = np.sqrt(V_1**2 + V_2**2) que no necesitaremos

def wr(H,I,epsilon=0.1):

  W = (H + epsilon)/(I + epsilon)

  return np.round(W*255)

def otsu_optimal(W): #Aplicare el metodo de otsu https://en.wikipedia.org/wiki/Otsu%27s_method#:~:text=In%20computer%20vision%20and%20image,two%20classes%2C%20foreground%20and%20background.
                    #Pero con la seleccion optima propuesta en el articulo guia
  total= len(W[0])*len(W)
  top = 256
  sumB = 0
  wB = 0
  maximum = 0
  level = 0
  
  counts =np.zeros(255)
  sum1=0
  for i in range(255):
    counts[i] =  (W == i).sum()
    sum1 = sum1 + i*counts[i]

  for j in range(255):
    wF = total - wB
    if (wB > 0) and (wF > 0):
        mF = (sum1 - sumB) / wF
        val = wB * wF * ((sumB / wB) - mF) * ((sumB / wB) - mF)
        if ( val >= maximum ):
            level = j
            maximum = val
    wB = wB + counts[j]
    sumB = sumB + (j-1) * counts[j]
  
  if level < 100:
    T = 100
  elif level < 150:
    T = level
  else:
    T = 150

  return T

def clouds_filter(BV,BF,U,C=500,Visual=True,Color="hot"):
  """
  BV Banda visible sobre la que se aplica el filtro
  BF Banda con la informacion de interes
  U  Umbral de separación
  C  Valor que se le da a los pixeles filtrados
  Visual (True) Muestra la imagen segun el filtro
         (False) Retorna mascara binaria 
  """

  if Visual:
      for i in range(len(BV)):
        for j in range(len(BV[0])):
          if BF[i][j] >= U:
            BV[i][j] = C

      plt.figure(figsize=(10,10))
      plt.title('Filtro',fontsize=15)
      plt.imshow(BV,cmap=Color)

  else:
      for i in range(len(BV)):
        for j in range(len(BV[0])):
          if BF[i][j] >= U:
            BV[i][j] = 0
          else:
            BV[i][j] = 1

      return BV

def get_cloud_image(filename: str):
    blue = imagToMat("./data/bands_data/" + filename + "M3.tif")
    green = imagToMat("./data/bands_data/" + filename + "M4.tif")
    red =  imagToMat("./data/bands_data/" + filename + "M5.tif")
    hi = hsi(red, green, blue)
    w = wr(hi[0],hi[1])
    t = otsu_optimal(w)
    clouds = clouds_filter(w,w,t,400,Color='hot', Visual=False)
    clouds = Image.fromarray(clouds * 255).convert("RGB")
    print(clouds)
    #res.save("juan.png")
    return clouds

def get_clouds_image(data_folder = "data/bands_data", results_folder = "data/results/"):
    onlyfiles = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    unique_names = list()
    for file in onlyfiles: 
      index0 = file.find("viirs1")
      index1 = file.find("M")
      filename = file[index0: index1]
      if filename not in unique_names and filename != "":
        unique_names.append(filename)
    print(unique_names)
    counter = 0
    for file in unique_names:
      clouds = get_cloud_image(file)  
      clouds.save(results_folder + "clouds_day_" + str(counter) + ".png")
      counter += 1

def get_infrared_filter_by_clouds(threshold = 230, data_folder = "data/bands_data", clouds_folder = "data/results/", results_folder = "data/results/"):
    infraredfiles = [f for f in listdir(data_folder) if isfile(join(data_folder, f)) and f.find("noaa") != -1]
    cloudsfiles = [f for f in listdir(clouds_folder) if isfile(join(clouds_folder, f))]

    for i in range(0, len(infraredfiles)):
      infrared_data = imagToMat(data_folder + "/" + infraredfiles[i])
      clouds_data = imagToMat(clouds_folder + "/" + cloudsfiles[i])
      clouds_data = clouds_data.reshape(3, clouds_data.shape[0], clouds_data.shape[1])[0]
      #print(infrared_data.shape)
      #print(clouds_data.shape)
      for x in range(infrared_data.shape[0]):
        for y in range(infrared_data.shape[1]):
          if clouds_data[x][y] == 0:# and infrared_data[x][y] < threshold:
            for z in range(3):
              infrared_data[x][y][z] = 0
          else:
            for z in range(3):
              infrared_data[x][y][z] = 255
      result = Image.fromarray(infrared_data).convert("RGB")
      result.save(results_folder + "piro_day_" + str(i) + ".png")
      print("Image saved.")


if __name__ == "__main__":
    #get_clouds_image(data_folder = "data/bands_data", results_folder = "data/results/")
    get_infrared_filter_by_clouds()