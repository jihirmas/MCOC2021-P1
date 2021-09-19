from numpy import pi, sqrt, nan
from numpy.random import rand
from constantes import g_, ρ_acero, mm_
 
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
        return l
    
    def obtener_valores(self):
        df = pd.ExcelFile(self.base_datos)
        m = self.denominacion
        m = self.cambiarx(m)
        l = self.definir_seccion(m)
        df1 = df.parse(l,skiprows=11)
        if l == "Cajon":
            x1 = list(df1["[]"])
            x2 = list(df1["D"])
            x4 = list(df1["B"])
            peso = list(df1["peso"])
            ixx = list(df1["Ix/10⁶"])
            iyy = list(df1["Iy/10⁶"])
            area = list(df1["A"])
        else:
            x1 = list(df1[l])
            x2 = list(df1["d"])
            x4 = list(df1["bf"])
            peso = list(df1["peso"])
            ixx = list(df1["Ix/10⁶"])
            iyy = list(df1["Iy/10⁶"])
            area = list(df1["A"])
        if l == "HR":
            peso = list(df1["peso.1"])
        
        for j in range(len(x1)):
            try:
                s = str(x1[j])+str(int(x2[j])) +"×" +str(int(x4[j]))+"×"+str(peso[j])
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
        return area1,peso1,ixx1,iyy1
    
    def area(self):
        A,P,IXX,IYY = self.obtener_valores()
        return A

    def peso(self):
        A,P,IXX,IYY = self.obtener_valores()
        return P

    def inercia_xx(self):
        A,P,IXX,IYY = self.obtener_valores()
        return IXX

    def inercia_yy(self):
        A,P,IXX,IYY = self.obtener_valores()
        return IYY

    def __str__(self):
        s = ""
        if self.area() != 0:
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
            s+= "Sección ICHA"+str(self.denominacion)+"\n"
            s+= "Area : nan \n"
            s+= "Peso : nan \n"
            s+= "Ixx  : nan \n"
            s+= "Iyy  : nan \n"
        return s
