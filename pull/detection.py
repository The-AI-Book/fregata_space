import numpy as np
import matplotlib.pyplot as plt
from interpolation import imagToMat
def HSI(R,G,B):

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


def WR (H,I,epsilon=0.1):

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


def Filtro(BV,BF,U,C=500,Visual=True,Color="hot"):
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

if __name__ == "__main__":
    #RGB = WaveToRGB(Rojo,Verde,Azul)

    blue = imagToMat("experimento/viirs1_day_0_2019-11-07_M3.tif")
    green = imagToMat("experimento/viirs1_day_0_2019-11-07_M4.tif")
    red =  imagToMat("experimento/viirs1_day_0_2019-11-07_M5.tif")
    
    HI = HSI(red, green, blue)
    W = WR (HI[0],HI[1])
    T = otsu_optimal(W)
    res = Filtro(W,W,T,400,Color='hot', Visual=False)
    from PIL import Image
    res = Image.fromarray(res * 255).convert("RGB")
    res.save("juan.png")