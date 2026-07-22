import numpy as np
stock_negativo=[]
class Agente:
    def __init__(self,ventas,cod_estupes,margen_precio=0.25):
        self.ventas=None
        self.cod_estupes= cod_estupes or {"N02AA01","N02AA02","N02AA03","N02AA05","N02AA59","N02AB02","N02AB03","N02AC03","N02AE01","N02AX02","N02AX06","N01AH01","N01AH02","N01AH03","N01AH06"}
        self.margen_precio=margen_precio

    def cargar(self,ruta_archivo="ventas_mes.csv"):
      self.ventas=np.genfromtxt("ventas_mes.csv",delimiter=",",dtype=None,encoding="utf-8")  

    def detectar_stock_negativo(self,ventas):
       columna_stock=self.ventas["stock actual"]
       if columna_stock<0:
          
    
       

        
