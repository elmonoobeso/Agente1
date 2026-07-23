import numpy as np
lista_abuso=[]

class Agente:
    def __init__(self,ventas,cod_estupes):
        self.ventas=None
        self.cod_estupes= cod_estupes or {"N02AA01","N02AA02","N02AA03","N02AA05","N02AA59","N02AB02","N02AB03","N02AC03","N02AE01","N02AX02","N02AX06","N01AH01","N01AH02","N01AH03","N01AH06"}
        self.margen_precio=margen_precio

    def cargar(self,ruta_archivo="ventas_mes.csv"):
      self.ventas=np.genfromtxt("ventas_mes.csv",delimiter=",",dtype=None,encoding="utf-8")  

    def detectar_stock_negativo(self):
       columna_stock=self.ventas["stock actual"]
       negativo=columna_stock<0
       return dict(ventas[nombre_medicamento],ventas[negativo],ventas[codigo_nacional])#lo pongo como dict y el codigo nacional como key?no quiero negativo quiero nombres y cn

    def abuso_estupes(self,limite_estupes=10):
       
       estupes=np.isin(self.ventas["cod_estupes"],self.cod_estupes)
       sub=self.ventas[estupes]
       clientes=np.unique(sub["id_paciente"])
       for cliente in clientes:
          ventas_cliente = sub[sub["id_paciente"] == cliente]
          suma = np.sum(ventas_cliente["cantidad"])
          
          if suma>limite_estupes:
             meds_unicos = ", ".join(ventas_cliente["nombre_medicamento"].unique())
             codigo_med=(ventas_cliente["codigo_nacional"].astype(str)
             cod_med=",".join(codigo_med).unique())  
             lista_abuso.append({"id_paciente":cliente,"nombre medicamento":meds_unicos,"cantidad":suma,"codigo_nacional":cod_med})
       return lista_abuso

    def anomalias_precio(self, margen_precio_para=0.25,margen_precio=0.05):
       if self.ventas["codigo_nacional"].startswith(6,7) and np.std(self.ventas["puc"])>0.25
          

       
        
    
          
    
       

        
