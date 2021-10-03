from numpy import pi, sqrt, nan
from numpy.random import rand
from constantes import g_, ρ_acero, mm_
import pandas as pd
 
class Circular(object):
    """define una seccion Circular"""

    def __init__(self, D, Dint, color=rand(3)):
        super(Circular, self).__init__()
        self.D = D
        self.Dint = Dint
        self.color = color  #color para la seccion

    def area(self):
        return pi*(self.D**2 - self.Dint**2)/4

    def peso(self):
        return self.area()*ρ_acero*g_

    def inercia_xx(self):
        return pi*(self.D**4 - self.Dint**4)/4

    def inercia_yy(self):
        return self.inercia_xx()

    def nombre(self):
        return f"O{self.D*1e3:.0f}x{self.Dint*1e3:.0f}"

    def __str__(self):
        return f"Seccion Circular {self.nombre()}"


        
#Mas adelante, no es para P1E1

class SeccionICHA(object):
    """Lee la tabla ICHA y genera una seccion apropiada"""

    def __init__(self, denominacion, base_datos="Perfiles ICHA.xlsx", debug=False, color=rand(3)):
        super(SeccionICHA, self).__init__()
        self.denominacion = denominacion
        self.color = color  #color para la seccion
        numeros=["1","2","3","4","5","6","7","8","9"]
        self.caso=""
        self.found=False
        for i in denominacion:
            if i not in numeros:
                self.caso+=i
            else: break
        if self.caso=="H":
            df=pd.read_excel("Perfiles ICHA.xlsx",sheet_name="H")
            df=df.replace(to_replace="×", value="x")
            self.loc=0
            for i in range(len(df.index)):
                a=(str(df.iloc[i][0])+str(df.iloc[i][1])+str(df.iloc[i][2])+str(df.iloc[i][3])+str(df.iloc[i][4])+str(df.iloc[i][5]))
                if str(a)==self.denominacion:
                    self.loc=i
                    self.found=True
                    break

            self.df=df
        elif self.caso=="HR":
            df=pd.read_excel("Perfiles ICHA.xlsx",sheet_name="HR")
            df=df.replace(to_replace="×", value="x")
            self.loc=0
            for i in range(len(df.index)):
                a=(str(df.iloc[i][4])+str(df.iloc[i][5])+str(df.iloc[i][6])+str(df.iloc[i][7])+str(df.iloc[i][8])+str(df.iloc[i][9]))
                if str(a)==self.denominacion:
                    self.loc=i
                    self.found=True
                    break
         
            self.df=df
        elif self.caso=="[]":
            df=pd.read_excel("Perfiles ICHA.xlsx",sheet_name="Cajon")
            df=df.replace(to_replace="×", value="x")
            self.loc=0
            for i in range(len(df.index)):
                a=(str(df.iloc[i][0])+str(df.iloc[i][1])+str(df.iloc[i][2])+str(df.iloc[i][3])+str(df.iloc[i][4])+str(df.iloc[i][5]))
                if str(a)==self.denominacion:
                    self.loc=i
                    self.found=True
                    break
              
            self.df=df
        elif self.caso=="PH":
            df=pd.read_excel("Perfiles ICHA.xlsx",sheet_name="PH")
            df=df.replace(to_replace="×", value="x")
            self.loc=0
            for i in range(len(df.index)):
                a=(str(df.iloc[i][0])+str(df.iloc[i][1])+str(df.iloc[i][2])+str(df.iloc[i][3])+str(df.iloc[i][4])+str(df.iloc[i][5]))
                if str(a)==self.denominacion:
                    self.loc=i
                    self.found=True
                    break
                
            self.df=df        
            
        elif self.caso=="O":
            df=pd.read_excel("Perfiles ICHA.xlsx",sheet_name="Circulares Mayores")
            df=df.replace(to_replace="×", value="x")
            self.loc=0
            for i in range(len(df.index)):
                a=(str("O")+str(df.iloc[i][0])+str(",")+str(df.iloc[i][1])+str(",")+str(df.iloc[i][2]))
                if str(a)==self.denominacion:
                    self.loc=i
                    self.found=True
                    break
            #print(a,self.loc)    
            self.df=df   
        elif self.caso=="o":
            df=pd.read_excel("Perfiles ICHA.xlsx",sheet_name="Circulares Menores")
            df=df.replace(to_replace="×", value="x")
            self.loc=0
            for i in range(len(df.index)):
                a=(str("o")+str(df.iloc[i][1])+str(",")+str(df.iloc[i][2])+str(",")+str(df.iloc[i][3]))
                if str(a)==self.denominacion:
                    self.loc=i
                    self.found=True
                    break
            #print(a,self.loc)    
            self.df=df            
    def area(self):
        if self.caso=="H":
            Area=self.df.iloc[self.loc][9]
        elif self.caso=="HR":
            Area=self.df.iloc[self.loc][13]     
        elif self.caso=="PH":
            Area=self.df.iloc[self.loc][9]   
        elif self.caso=="[]":
            Area=self.df.iloc[self.loc][8] 
        elif self.caso=="O":
            Area=self.df.iloc[self.loc][4]
            #print(Area)
        elif self.caso=="o":
            Area=self.df.iloc[self.loc][5]             
        else: return("nan")
        return float(Area/10**6)
    

    def peso(self):
        if self.caso=="H":
            Peso=self.df.iloc[self.loc][5]    
        elif self.caso=="HR":
            Peso=self.df.iloc[self.loc][9]   
        elif self.caso=="PH":
            Peso=self.df.iloc[self.loc][5]     
        elif self.caso=="[]":
            Peso=self.df.iloc[self.loc][5]  
        elif self.caso=="O":
            Peso=self.df.iloc[self.loc][3]
        elif self.caso=="o":
            Peso=self.df.iloc[self.loc][4]               
        else: return("nan")
        return float(Peso)
    

    def inercia_xx(self):
        if self.caso=="H":
            inXX=self.df.iloc[self.loc][10]    
        elif self.caso=="HR":
            inXX=self.df.iloc[self.loc][14]    
        elif self.caso=="PH":
            inXX=self.df.iloc[self.loc][10]  
        elif self.caso=="[]":
            inXX=self.df.iloc[self.loc][9] 
        elif self.caso=="O":
            inXX=self.df.iloc[self.loc][5] 
        elif self.caso=="o":
            inXX=self.df.iloc[self.loc][6]              
        else: return("nan")            
        return float(inXX)


    def inercia_yy(self):
        if self.caso=="H":
            inYY=self.df.iloc[self.loc][14]      
        elif self.caso=="HR":
            inYY=self.df.iloc[self.loc][18]        
        elif self.caso=="PH":
            inYY=self.df.iloc[self.loc][14]    
        elif self.caso=="[]":
            inYY=self.df.iloc[self.loc][13] 
        elif self.caso=="O":
            inYY=self.df.iloc[self.loc][5] 
        elif self.caso=="o":
            inYY=self.df.iloc[self.loc][6]              
        else: return("nan")            
        return float(inYY)

    def nombre(self):
        return self.denominacion

    def __str__(self):
        s=""
        if self.found==True:
            s+=f"{self.denominacion}"+" encontrada. "+"A="+str(self.area())+" Ix="+str(self.inercia_xx())+" Iy="+str(self.inercia_yy())+  "\n"
        elif self.found==False:
            s+="Tipo de seccion "+f"{self.denominacion}"+ " no encontrada en base de datos"+"\n"
        s+=f"Seccion ICHA {self.denominacion}"+"\n"
        s+="Area : "+str(self.area())+"\n"
        s+="peso : "+str(self.peso())+"\n"
        s+="Ixx : "+str(self.inercia_xx())+"\n"
        s+="Iyy : "+str(self.inercia_yy())+"\n"
        return s