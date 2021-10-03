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
        self.base_datos = base_datos
        A,P,IXX,IYY,L = self.obtener_valores()
        self.L = L
        self.A = A
        self.P = P
        self.IXX = IXX
        self.IYY = IYY
        
    def cambiarx(self,s):
        l = ""
        for i in range(len(s)):
            if s[i] == "x":
                l+= "×"
            else:
                l+=s[i]
        return l
    
    def definir_seccion(self,s):
        l = ""
        for i in range(len(s)):
            if s[i].isdigit():
                break
            else:
                l+=s[i]
        if l == "[]":
            l = "Cajon"
        if l == "O":
            l = "Circulares Mayores"
        if l == "o":
            l = "Circulares Menores"
        return l
    
    def obtener_valores(self):
        df = pd.ExcelFile(self.base_datos)
        m = self.denominacion
        m = self.cambiarx(m)
        l = self.definir_seccion(m)
        if l == "Circulares Mayores" or l == "Circulares Menores":
            df1 = df.parse(l,skiprows=10)
        else:
            df1 = df.parse(l,skiprows=11)
        if l == "Cajon":
            x1 = list(df1["[]"])
            x2 = list(df1["D"])
            x4 = list(df1["B"])
            peso = list(df1["peso"])
            ixx = list(df1["Ix/10⁶"])
            iyy = list(df1["Iy/10⁶"])
            area = list(df1["A"])
        elif l == "Circulares Mayores":
            x1 = "O"
            x2 = list(df1["D"])
            x4 = list(df1["Dint"])
            peso = list(df1["peso"])
            ixx = list(df1["I/10⁶"])
            area = list(df1["A"])
        elif l == "Circulares Menores":
            x1 = "o"
            x2 = list(df1["D"])
            x4 = list(df1["Dint"])
            peso = list(df1["peso"])
            ixx = list(df1["I/10⁶"])
            area = list(df1["A"])
        else:
            x1 = list(df1[l])
            x2 = list(df1["d"])
            x4 = list(df1["bf"])
            peso = list(df1["peso"])
            ixx = list(df1["Ix/10⁶"])
            iyy = list(df1["Iy/10⁶"])
            area = list(df1["A"])
        
        for j in range(len(x2)):
            if l == "Circulares Mayores":
                try:
                    s = "O"+str(int(x2[j])) +"×" +str(int(x4[j]))
                    if s == m:
                        ixx1 = ixx[j]
                        iyy1 = 0
                        area1 = area[j]/1000000
                        peso1 = peso[j]
                        break
                except:
                    ixx1 = 0
                    iyy1 = 0
                    area1 = 0
                    peso1 = 0
                    pass
            elif l == "Circulares Menores":
                try:
                    s = "o"+str(float(x2[j])) +"×" +str(float(x4[j]))
                    if s == m:
                        ixx1 = ixx[j]
                        iyy1 = 0
                        area1 = area[j]/1000000
                        peso1 = peso[j]
                        break
                except:
                    ixx1 = 0
                    iyy1 = 0
                    area1 = 0
                    peso1 = 0
                    pass
            else:
                try:
                    s = str(x1[j])+str(int(x2[j])) +"×" +str(int(x4[j]))+"×"+str(float(peso[j]))
                    if s == m:
                        ixx1 = ixx[j]
                        iyy1 = iyy[j]
                        area1 = area[j]/1000000
                        peso1 = peso[j]
                        break
                except:
                    ixx1 = 0
                    iyy1 = 0
                    area1 = 0
                    peso1 = 0
                    pass
        L = l
        return area1,peso1,ixx1,iyy1, L
    
    def area(self):
        return self.A

    def peso(self):
        return self.P

    def inercia_xx(self):
        return self.IXX

    def inercia_yy(self):
        return self.IYY

    def nombre(self):
        return self.denominacion

    def __str__(self):
        s = ""
        if self.area() != 0:
            if self.L == "Circulares Mayores" or self.L == "Circulares Menores":
                s+= str(self.denominacion)+" encontrada. "
                s+= "A="+str(self.area())
                s+= " I="+str(self.inercia_xx())+"\n"
                s+= "Sección ICHA "+str(self.denominacion)+"\n"
                s+= "Area : "+str(self.area())+"\n"
                s+= "Peso : "+str(self.peso())+"\n"
                s+= "I  : "+str(self.inercia_xx())+"\n"
            else:
                s+= str(self.denominacion)+" encontrada. "
                s+= "A="+str(self.area())
                s+= " Ix="+str(self.inercia_xx())
                s+= " Iy="+str(self.inercia_yy())+"\n"
                s+= "Sección ICHA "+str(self.denominacion)+"\n"
                s+= "Area : "+str(self.area())+"\n"
                s+= "Peso : "+str(self.peso())+"\n"
                s+= "Ixx  : "+str(self.inercia_xx())+"\n"
                s+= "Iyy  : "+str(self.inercia_yy())+"\n"
        else:
            s += "Tipo de seccion "+str(self.denominacion)+" no encontrada en la base de datos \n"
            s+= "Sección ICHA "+str(self.denominacion)+"\n"
            s+= "Area : nan \n"
            s+= "Peso : nan \n"
            s+= "Ixx  : nan \n"
            s+= "Iyy  : nan \n"
        return s
